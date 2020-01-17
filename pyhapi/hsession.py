"""Summary
"""
from . import hdata as HDATA
from . import hapi as HAPI
from .hnode import HExistingNode

class HSession():

    """Summary

    Attributes:
        ConnectedState (TYPE): Description
        CookOption (TYPE): Description
        HAPISession (TYPE): Description
        ProcessId (TYPE): Description
    """

    def __init__(self):
        """Summary
        """
        self.hapi_session = HDATA.HAPI_Session(HDATA.HAPI_SessionType.HAPI_SESSION_THRIFT, 0)
        self.connected_state = HDATA.SessionConnectionState.NOT_CONNECTED
        self.nodes = {}
        self.process_id = -1
        self.cook_option = HAPI.GetCookOptions()

    def get_node(self, node_id):
        """[summary]

        Args:
            node_id ([type]): [description]

        Returns:
            [type]: [description]
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
        """Summary

        Args:
            rootpath (TYPE): Description
            pipeName (str, optional): Description
            autoClose (bool, optional): Description
            timeout (float, optional): Description

        Returns:
            TYPE: Description
        """
        return self.internal_create_thrift_pipe_session(rootpath, True, auto_close, timeout)

    def internal_create_thrift_pipe_session(\
        self, rootpath, create_session=True, auto_close=True, timeout=10000.0):
        """Summary

        Args:
            rootpath (TYPE): Description
            bCreateSession (bool, optional): Description
            pipeName (str, optional): Description
            autoClose (bool, optional): Description
            timeout (float, optional): Description

        Returns:
            TYPE: Description
        """
        self.check_and_close_existing_session()

        self.hapi_session = HDATA.HAPI_Session(HDATA.HAPI_SessionType.HAPI_SESSION_THRIFT, 0)
        self.connected_state = HDATA.SessionConnectionState.FAILED_TO_CONNECT

        if create_session:
            server_options = HDATA.HAPI_ThriftServerOptions(auto_close, timeout)
            self.process_id = HAPI.StartThriftNamedPipeServer(server_options)

        HAPI.CreateThriftNamedPipeSession(self.hapi_session)

        return self.initialize_session(rootpath)

    def initialize_session(self, rootpath):
        """Summary

        Args:
            rootpath (TYPE): Description

        Returns:
            TYPE: Description
        """
        HAPI.Initialize(self.hapi_session, self.cook_option,\
            otl_search_path="{0}\\hda\\".format(rootpath))
        self.connected_state = HDATA.SessionConnectionState.CONNECTED
        return True

    def cleanup(self):
        """Summary
        """
        if self.is_session_valid():
            HAPI.Cleanup(self.hapi_session)

    def close_session(self):
        """Summary
        """
        if self.is_session_valid():
            print("Close Session")
            HAPI.Cleanup(self.hapi_session)
            HAPI.CloseSession(self.hapi_session)

    def check_and_close_existing_session(self):
        """Summary

        Returns:
            TYPE: Description
        """
        if self.hapi_session is not None and self.is_session_valid():
            return self.close_session()
        return True

    def is_session_valid(self):
        """Summary

        Returns:
            TYPE: Description
        """
        if self.connected_state != HDATA.SessionConnectionState.FAILED_TO_CONNECT:
            return HAPI.IsSessionValid(self.hapi_session)
        return False

    def save_hip(self, filename="debug.hip"):
        """Summary

        Args:
            filename (str, optional): Description
        """
        HAPI.SaveHIPFile(self.hapi_session, filename)
        print("Session saved to {0}".format(filename))

    def __del__(self):
        self.check_and_close_existing_session()

class HSessionManager():

    """Summary
    """

    _defaultSession = None

    @staticmethod
    def get_or_create_default_session(rootpath=""):
        """Summary

        Args:
            rootpath (str, optional): Description

        Returns:
            TYPE: Description
        """
        if HSessionManager._defaultSession is not None and\
            HSessionManager._defaultSession.IsSessionValid():
            return HSessionManager._defaultSession
        if HSessionManager._defaultSession is None or\
            HSessionManager._defaultSession.ConnectedState ==\
                HDATA.SessionConnectionState.NOT_CONNECTED:
            HSessionManager.create_thrift_pipe_session(rootpath)
        return HSessionManager._defaultSession

    @staticmethod
    def check_and_close_existing_session():
        """Summary
        """
        if HSessionManager._defaultSession is not None:
            HSessionManager._defaultSession.CloseSession()
            HSessionManager._defaultSession = None

    @staticmethod
    def create_thrift_pipe_session(rootpath, auto_close=True, timeout=10000.0):
        """Summary

        Args:
            rootpath (TYPE): Description
            pipeName (str, optional): Description
            autoClose (bool, optional): Description
            timeout (float, optional): Description

        Returns:
            TYPE: Description
        """
        HSessionManager.check_and_close_existing_session()
        HSessionManager._defaultSession = HSession()
        return HSessionManager._defaultSession.\
            create_thrift_pipe_session(rootpath, auto_close, timeout)

    @staticmethod
    def close_default_session():
        """Summary
        """
        HSessionManager.check_and_close_existing_session()

    @staticmethod
    def restart_session():
        """Summary

        Returns:
            TYPE: Description
        """
        if HSessionManager._defaultSession is not None:
            return HSessionManager._defaultSession.RestartSession()
        session = HSession()
        if session.create_thrift_pipe_session(True):
            HSessionManager._defaultSession = session
        return None
