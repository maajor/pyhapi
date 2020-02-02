# -*- coding: utf-8 -*-
"""wrapper for houdini engine's session.
Author  : Maajor
Email   : hello_myd@126.com

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
from . import hdata as HDATA
from . import hapi as HAPI
from .hnode import HExistingNode


__all__ = [
    # Classes
    'HSession', 'HSessionManager'
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

    def create_thrift_pipe_session(self, rootpath, auto_close=True, timeout=10000.0):
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
        return self.__internal_create_thrift_pipe_session(rootpath, True, auto_close, timeout)

    def __internal_create_thrift_pipe_session(\
        self, rootpath, create_session=True, auto_close=True, timeout=10000.0):

        try:
            self.check_and_close_existing_session()

            self.hapi_session = HDATA.Session(HDATA.SessionType.THRIFT, 0)
            self.connected_state = HDATA.SessionConnectionState.FAILED_TO_CONNECT

            if create_session:
                server_options = HDATA.ThriftServerOptions(auto_close, timeout)
                self.process_id = HAPI.start_thrift_named_pipe_server(server_options)

            HAPI.create_thrift_named_pipe_session(self.hapi_session)
            self.__initialize_session(rootpath)
            return True
        except AssertionError as error:
            print("HAPI excecution failed")
            print(error)
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
            print("Close Session")
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
        print("Session saved to {0}".format(filename))

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
    _rootpath = ""

    @staticmethod
    def get_or_create_default_session(rootpath=""):
        """Get or create an session

        Args:
            rootpath (str, optional): file path to hsession project's root path, \
                it could contain /hda folder

        Returns:
            HSession: session created
        """
        HSessionManager._rootpath = rootpath
        if HSessionManager._defaultSession is not None and\
            HSessionManager._defaultSession.is_session_valid():
            return HSessionManager._defaultSession
        if HSessionManager._defaultSession is None or\
            HSessionManager._defaultSession.ConnectedState ==\
                HDATA.SessionConnectionState.NOT_CONNECTED:
            if HSessionManager.__create_thrift_pipe_session(rootpath):
                return HSessionManager._defaultSession
        HSessionManager._defaultSession = None
        return None

    @staticmethod
    def __check_and_close_existing_session():
        if HSessionManager._defaultSession is not None:
            HSessionManager._defaultSession.CloseSession()
            HSessionManager._defaultSession = None

    @staticmethod
    def __create_thrift_pipe_session(rootpath, auto_close=True, timeout=10000.0):
        HSessionManager.__check_and_close_existing_session()
        HSessionManager._defaultSession = HSession()
        return HSessionManager._defaultSession.\
            create_thrift_pipe_session(rootpath, auto_close, timeout)

    @staticmethod
    def restart_session():
        """Restart default session

        Returns:
            HSession: session created
        """
        if HSessionManager._defaultSession is not None:
            return HSessionManager._defaultSession.restart_session()
        session = HSession()
        if session.create_thrift_pipe_session(HSessionManager._rootpath, True):
            HSessionManager._defaultSession = session
        return None
