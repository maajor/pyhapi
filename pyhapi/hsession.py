"""Summary
"""
from . import *

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
        self.HAPISession = HAPI_Session(HAPI_SessionType.HAPI_SESSION_THRIFT, 0)
        self.ConnectedState = SessionConnectionState.NOT_CONNECTED
        self.Nodes = {}

    def CreateThriftPipeSession(self, rootpath, pipeName = "hapi", autoClose = True, timeout = 10000.0):
        """Summary
        
        Args:
            rootpath (TYPE): Description
            pipeName (str, optional): Description
            autoClose (bool, optional): Description
            timeout (float, optional): Description
        
        Returns:
            TYPE: Description
        """
        return self.InternalCreateThriftPipeSession(rootpath, True)

    def InternalCreateThriftPipeSession(self, rootpath, bCreateSession = True, pipeName = "hapi", autoClose = True, timeout = 10000.0):
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
        self.CheckAndCloseExistingSession()

        self.HAPISession = HAPI_Session(HAPI_SessionType.HAPI_SESSION_THRIFT, 0)
        self.ConnectedState = SessionConnectionState.FAILED_TO_CONNECT

        if bCreateSession:
            serverOptions = HAPI_ThriftServerOptions(autoClose, timeout)
            self.ProcessId = HAPI.StartThriftNamedPipeServer(serverOptions)

        HAPI.CreateThriftNamedPipeSession(self.HAPISession)

        return self.InitializeSession(rootpath)

    def InitializeSession(self, rootpath):
        """Summary
        
        Args:
            rootpath (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        self.CookOption = HAPI.GetCookOptions()
        HAPI.Initialize(self.HAPISession, self.CookOption,\
            otl_search_path="{0}\\hda\\".format(rootpath))
        self.ConnectedState = SessionConnectionState.CONNECTED
        return True

    def Cleanup(self):
        """Summary
        """
        if self.IsSessionValid():
            HAPI.Cleanup(self.HAPISession)

    def CloseSession(self):
        """Summary
        """
        if self.IsSessionValid():
            print("Close Session")
            HAPI.Cleanup(self.HAPISession)
            HAPI.CloseSession(self.HAPISession)

    def CheckAndCloseExistingSession(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        if self.HAPISession != None and self.IsSessionValid():
            return self.CloseSession()
        return True

    def IsSessionValid(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        if self.ConnectedState != SessionConnectionState.FAILED_TO_CONNECT:
            return HAPI.IsSessionValid(self.HAPISession)
        return False

    def SaveHIP(self, filename = "debug.hip"):
        """Summary
        
        Args:
            filename (str, optional): Description
        """
        HAPI.SaveHIPFile(self.HAPISession, filename)
        print("Session saved to {0}".format(filename))

class HSessionManager():

    """Summary
    """
    
    _defaultSession = None

    @staticmethod
    def GetOrCreateDefaultSession(rootpath = ""):
        """Summary
        
        Args:
            rootpath (str, optional): Description
        
        Returns:
            TYPE: Description
        """
        if HSessionManager._defaultSession != None and HSessionManager._defaultSession.IsSessionValid():
            return HSessionManager._defaultSession
        elif HSessionManager._defaultSession == None or HSessionManager._defaultSession.ConnectedState == SessionConnectionState.NOT_CONNECTED:
            HSessionManager.CreateThriftPipeSession(rootpath)
        return HSessionManager._defaultSession

    @staticmethod
    def CheckAndCloseExistingSession():
        """Summary
        """
        if HSessionManager._defaultSession != None:
            HSessionManager._defaultSession.CloseSession()
            HSessionManager._defaultSession = None

    @staticmethod
    def CreateThriftPipeSession(rootpath, pipeName = "hapi", autoClose = True, timeout = 10000.0):
        """Summary
        
        Args:
            rootpath (TYPE): Description
            pipeName (str, optional): Description
            autoClose (bool, optional): Description
            timeout (float, optional): Description
        
        Returns:
            TYPE: Description
        """
        HSessionManager.CheckAndCloseExistingSession()
        HSessionManager._defaultSession = HSession()
        return HSessionManager._defaultSession.CreateThriftPipeSession(rootpath, pipeName, autoClose, timeout)

    @staticmethod
    def CloseDefaultSession():
        """Summary
        """
        HSessionManager.CheckAndCloseExistingSession()

    @staticmethod
    def RestartSession():
        """Summary
        
        Returns:
            TYPE: Description
        """
        if HSessionManager._defaultSession != None:
            return HSessionManager._defaultSession.RestartSession()
        else:
            session = HSession()
            if session.CreateThriftPipeSession(true):
                HSessionManager._defaultSession = session
