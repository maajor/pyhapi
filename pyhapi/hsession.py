# -*- coding: utf-8 -*-
"""wrapper for houdini engine's session.
Author  : Maajor
Email   : info@ma-yidong.com

HSession:
    A wrapper fou houdini engine's session, it contains the session itself\
         and other informations such as nodes, process id etc.
    Use this object to get nodes, save hips. Creating nodes and\
         lots of hengine operation need HSession object as parameter.

HSessionManager:
    Use this object to get HSession object

Example usage:

import pyhapi as ph

#create a houdini engine session
session = ph.HSessionManager.get_or_create_default_session()

#create a geo objnode
box = ph.HNode(session, "geo", "ProgrammaticBox")

#save the session to a hip file
session.save_hip("test.hip")

"""
import os
import logging
import asyncio
import threading
import enum
import time
import pyhapi
from . import hdata as HDATA
from . import hapi as HAPI
from .hnode import HExistingNode


__all__ = [
    # Classes
    'HSession', 'HSessionManager', 'HSessionPool', 'HSessionTask'
]


class HSession():

    """A wrapper fou houdini engine's session, it contains the session itself\
        and other informations such as nodes, process id etc.

    Attributes:
        hapi_session (HAPI_SessionId:int64): hapi session id
        connected_state (hdata.SessionConnectionState): state of current session
        nodes (list(hnode.HNodeBase)): all nodes in this session
        process_id (int): process id used by this session
        cook_option (hdata.CookOptions): cook option of this session
        root_path (str): file path to hsession project's root path, \
                it could contain /hda folder
    """

    def __init__(self):
        """Initialize the session
        """
        self.hapi_session = HDATA.Session(HDATA.SessionType.THRIFT, 0)
        self.connected_state = HDATA.SessionConnectionState.NOT_CONNECTED
        self.nodes = {}
        self.process_id = -1
        self.cook_option = HAPI.get_cook_options()
        self.root_path = ""
        self.pipe_name = "hapi"

        self.asset_libs = {}

    def get_node(self, node_id):
        """Get node in this session by HAPI_NodeId

        Args:
            node_id (hdata.HAPI_NodeId ): node's id store by the session

        Returns:
            hnode.HNodeBase: an object represent that node in session. It will\
                return None if cannot find any node matching the node id
        """
        try_get_node = self.nodes.get(node_id)
        if try_get_node is not None:
            return try_get_node

        existing_node = HExistingNode(self, node_id)
        if existing_node is not None:
            self.nodes[node_id] = existing_node
            return existing_node
        return None

    def reload_asset_library(self, asset):
        asset.session = self
        asset_lib_id = HAPI.load_asset_library_from_file(
            self.hapi_session, asset.hda_path)

        asset.library_id = asset_lib_id
        self.asset_libs[asset.library_id.value] = asset

        # asset.asset_names = HAPI.get_available_assets(
        #    self.hapi_session, asset_lib_id)


    def create_thrift_pipe_session(self, rootpath, pipe_name, auto_close=True, timeout=10000.0):
        """Create the session in thrift-pipe manner

        Args:
            rootpath (string): file path to hsession project's root path, \
                it could contain /hda folder
            auto_close (bool, optional): Close the server automatically when\
                 all clients disconnect from it. Defaults to True.
            timeout (float, optional): Timeout in milliseconds for waiting on \
                the server to signal that it's ready to serve. If the server \
                    fails to signal within this time interval, the start server \
                        call fails and the server process is terminated. \
                            Defaults to 10000.0.

        Returns:
            bool: true if the session created successfully, false not.
        """
        self.root_path = rootpath
        self.pipe_name = pipe_name
        return self.__internal_create_thrift_pipe_session(rootpath, pipe_name, True, auto_close, timeout)

    def __internal_create_thrift_pipe_session(\
        self, rootpath, pipe_name, create_session=True, auto_close=True, timeout=10000.0):

        try:
            self.check_and_close_existing_session()

            self.hapi_session = HDATA.Session(HDATA.SessionType.THRIFT, 0)
            self.connected_state = HDATA.SessionConnectionState.FAILED_TO_CONNECT

            if create_session:
                server_options = HDATA.ThriftServerOptions(auto_close, timeout)
                self.process_id = HAPI.start_thrift_named_pipe_server(server_options, pipe_name)

            HAPI.create_thrift_named_pipe_session(self.hapi_session, pipe_name)
            self.__initialize_session(rootpath)
            return True
        except AssertionError as error:
            logging.error("HAPI excecution failed")
            logging.error(error)
            return False

    def __initialize_session(self, rootpath):
        HAPI.initialize(self.hapi_session, self.cook_option,\
            otl_search_path="{0}\\hda\\".format(rootpath))
        self.root_path = rootpath
        self.connected_state = HDATA.SessionConnectionState.CONNECTED

    def cleanup(self):
        """Clean up current session
        """
        if self.is_session_valid():
            HAPI.cleanup(self.hapi_session)

    def check_and_close_existing_session(self):
        """Close current session

        Returns:
            bool: if the close success
        """
        if self.hapi_session is not None and self.is_session_valid():
            logging.info("Close Session")
            HAPI.cleanup(self.hapi_session)
            HAPI.close_session(self.hapi_session)
        return True

    def is_session_valid(self):
        """Check if current session is valid

        Returns:
            bool: if current session is valid
        """
        if self.connected_state != HDATA.SessionConnectionState.FAILED_TO_CONNECT:
            return HAPI.is_session_valid(self.hapi_session)
        return False

    def save_hip(self, filename="debug.hip", lock_nodes=True):
        """Save current session to a hip file

        Args:
            filename (str, optional): name of saved hip file
            lock_nodes (bool, optional): Specify whether to lock all SOP nodes \
            before saving the scene file.
        """
        HAPI.save_hip_file(self.hapi_session, filename, lock_nodes)
        logging.info("Session saved to {0}".format(filename))

    def restart_session(self):
        """Restart current session

        Returns:
            HSession: session itself
        """
        HAPI.cleanup(self.hapi_session)
        self.__initialize_session(self.root_path)
        return self

    def load_hip(self, filename, cook_on_load=False):
        """Loads a .hip file into the main Houdini scene

        Args:
            filename ([type]): HIP file absolute path to load
            cook_on_load (bool, optional): \
                Set to true if you wish the nodes to cook as soon as they are created.\
                    Defaults to False.

        Returns:
            HSession: session itself
        """
        HAPI.load_hip_file(self.hapi_session, filename, cook_on_load)
        return self

    def __del__(self):
        self.check_and_close_existing_session()

class HSessionManager():

    """Use this object to get HSession object
    """

    _defaultSession = None
    _defaultSessionPool = None
    _rootpath = os.getcwd()
    _pipe_name = "hapi"

    @staticmethod
    def get_or_create_default_session(rootpath=os.getcwd(), pipe_name = "hapi"):
        """Get or create an session

        Args:
            rootpath (str, optional): file path to hsession project's root path, \
                it could contain /hda folder

        Returns:
            HSession: session created
        """
        # check if can find libHAPIL otherwise return
        assert pyhapi.__library_initialized__,  "libHAPIL not found, Please refer to https://pyhapi.readthedocs.io/en/latest/install.html to setup Houdini Engine's PATH"
        if rootpath:
            HSessionManager._rootpath = rootpath
        if pipe_name:
            HSessionManager._pipe_name = pipe_name
        if HSessionManager._defaultSession is not None and\
            HSessionManager._defaultSession.is_session_valid():
            return HSessionManager._defaultSession
        if HSessionManager._defaultSession is None or\
            HSessionManager._defaultSession.ConnectedState ==\
                HDATA.SessionConnectionState.NOT_CONNECTED:
            if HSessionManager.__create_thrift_pipe_session( \
                HSessionManager._rootpath, pipe_name=HSessionManager._pipe_name):
                return HSessionManager._defaultSession
        HSessionManager._defaultSession = None
        return None

    @staticmethod
    def __check_and_close_existing_session():
        if HSessionManager._defaultSession is not None:
            HSessionManager._defaultSession.CloseSession()
            HSessionManager._defaultSession = None

    @staticmethod
    def __create_thrift_pipe_session(rootpath, pipe_name, auto_close=True, timeout=10000.0):
        HSessionManager.__check_and_close_existing_session()
        HSessionManager._defaultSession = HSession()
        return HSessionManager._defaultSession.\
            create_thrift_pipe_session(rootpath, pipe_name, auto_close, timeout)

    @staticmethod
    def restart_session():
        """Restart default session

        Returns:
            HSession: session created
        """
        if HSessionManager._defaultSession is not None:
            return HSessionManager._defaultSession.restart_session()
        session = HSession()
        if session.create_thrift_pipe_session(HSessionManager._rootpath, HSessionManager._pipe_name, True):
            HSessionManager._defaultSession = session
        return None

    @staticmethod
    def get_or_create_session_pool(session_count=10, rootpath=os.getcwd(), pipe_name = "hapi"):
        """Restart default session

        Returns:
            HSession: session created
        """
        if HSessionManager._defaultSessionPool is not None:
            if session_count == HSessionManager._defaultSessionPool._session_count:
                return HSessionManager._defaultSessionPool.restart_session_pool()
            else:
                return HSessionManager._defaultSessionPool.resize(session_count)
        if rootpath:
            HSessionManager._rootpath = rootpath
        if pipe_name:
            HSessionManager._pipe_name = pipe_name
        session_pool = HSessionPool(session_count)
        if session_pool.create_thrift_pipe_session(HSessionManager._rootpath, HSessionManager._pipe_name, True):
            HSessionManager._defaultSessionPool = session_pool
            return HSessionManager._defaultSessionPool
        return None


class HSessionPool():

    def __init__(self, session_count, max_task_time: int = 10000):
        """Initialize the session pool
        """
        self.sessions = []
        self._session_count = session_count
        self.current_id = 0
        self.task_queue = asyncio.Queue()
        self._loop = asyncio.get_event_loop()
        self._max_task_time = max_task_time
        self._workers = None
        self._pipe_name_prefix = "hapi"
        self._root_path = os.getcwd()
        self._timeout = 10000
        self._auto_close = True

    def __iter__(self):
        return iter(self.sessions)

    def __next__(self):
        if self.current_id <= self._session_count:
            x = self.sessions[self.current_id]
            self.current_id += 1
            return x
        else:
            raise StopIteration

    def __getitem__(self, key):
        return self.sessions[key]

    # for producer to add task
    def enqueue_task(self, task, *args):
        logging.debug("enqueue task {0} with param {1}".format(task, args))
        self.task_queue.put_nowait((task, *args))

    # for producer to add task
    async def enqueue_task_async(self, task, *args):
        logging.debug("enqueue task {0} with param {1}".format(task, args))
        await self.task_queue.put((task, *args))

    def run_on_task_producer(self, producer):
        self._loop.run_until_complete(self.run_on_task_producer_async(producer))
        self._loop.close() 

    async def run_on_task_producer_async(self, producer):
        task_producer = asyncio.create_task(producer(self))
        self._workers = [asyncio.create_task(self.__worker_loop(i)) for i in range(self._session_count)]
        await asyncio.gather(*self._workers, task_producer, return_exceptions=True)

    # run all enqueued tasks by now
    def run_all_tasks(self):
        self._loop.run_until_complete(self.__run_tasks_available())
        self._loop.close() 

    def create_thrift_pipe_session(self, rootpath, pipe_name_prefix, auto_close=True, timeout=10000.0):
        valid_session = 0
        self._root_path = rootpath
        self._timeout = timeout
        self._auto_close = auto_close
        self._pipe_name_prefix = pipe_name_prefix
        for i in range(self._session_count):
            session = HSession()
            if session.create_thrift_pipe_session(rootpath, pipe_name_prefix+str(i), auto_close, timeout):
                valid_session += 1
                self.sessions.append(session)
        self._session_count = valid_session
        if valid_session>1:
            return True
        return False

    def restart_session_pool(self):
        for session in self.sessions:
            session.restart_session()

    def resize(self, session_count):
        if session_count < self._session_count:
            for i in range(session_count, self._session_count):
                self.sessions[i].check_and_close_existing_session()
            for i in range(session_count, self._session_count):
                self.sessions.remove(session_count)
            self._session_count = session_count
        elif session_count > self._session_count:
            valid_session = 0
            for i in range(self._session_count, session_count):
                session = HSession()
                if session.create_thrift_pipe_session(self._root_path, self._pipe_name_prefix+str(i), self._auto_close, self._timeout):
                    valid_session += 1
                    self.sessions.append(session)
            self._session_count += valid_session

    async def __run_tasks_available(self):
        self._workers = [asyncio.create_task(self.__worker_loop(i)) for i in range(self._session_count)]
        await self.task_queue.join()
        for worker in self._workers:
            worker.cancel()

    # https://github.com/CaliDog/asyncpool
    # one consumer worker per houdini engine session
    async def __worker_loop(self, i):
        while True:
            got_obj = False

            try:
                avail_session = self.sessions[i]
                task_to_proceed, *args = await self.task_queue.get()
                got_obj = True

                running_coro = asyncio.wait_for(task_to_proceed(avail_session, *args), self._max_task_time, loop=self._loop)
                await running_coro
            except asyncio.CancelledError:
                logging.info("Worker {0} is Cancelled".format(i))
                break
            except KeyboardInterrupt as e:
                logging.info("Worker {0} is Interrupt".format(i))
                break
            except (MemoryError, SystemExit) as e:
                logging.exception(e)
                raise
            except BaseException as e:
                logging.exception(e)
                logging.exception("Worker Call Failed")
            finally:
                if got_obj:
                    self.task_queue.task_done()

def HSessionTask(task):
    async def wrapper(*args, **kwargs):
        assert isinstance(args[0], HSession), "{0}'s first parameter should be HSession".format(task)
        await task(*args, **kwargs)
        args[0].restart_session()
    return wrapper