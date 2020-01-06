from . import *

class HSession():

    def __init__(self):
        self.HAPISession = HAPI_Session(HAPI_SessionType.HAPI_SESSION_THRIFT, 0)
        self.ConnectedState = SessionConnectionState.NOT_CONNECTED

    def CreateThriftPipeSession(self, rootpath, pipeName = "hapi", autoClose = True, timeout = 10000.0):
        return self.InternalCreateThriftPipeSession(rootpath, True)

    def InternalCreateThriftPipeSession(self, rootpath, bCreateSession = True, pipeName = "hapi", autoClose = True, timeout = 10000.0):
        self.CheckAndCloseExistingSession()

        self.HAPISession = HAPI_Session(HAPI_SessionType.HAPI_SESSION_THRIFT, 0)
        self.ConnectedState = SessionConnectionState.FAILED_TO_CONNECT

        if bCreateSession:
            serverOptions = HAPI_ThriftServerOptions(autoClose, timeout)
            self.ProcessId = HAPI.StartThriftNamedPipeServer(serverOptions)

        HAPI.CreateThriftNamedPipeSession(self.HAPISession)

        return self.InitializeSession(rootpath)

    def InitializeSession(self, rootpath):
        self.CookOption = HAPI.GetCookOptions()
        HAPI.Initialize(self.HAPISession, self.CookOption,\
            otl_search_path="{0}\\hda\\".format(rootpath))
        self.ConnectedState = SessionConnectionState.CONNECTED
        return True

    def Cleanup(self):
        if self.IsSessionValid():
            HAPI.Cleanup(self.HAPISession)

    def CloseSession(self):
        if self.IsSessionValid():
            print("Close Session")
            HAPI.Cleanup(self.HAPISession)
            HAPI.CloseSession(self.HAPISession)

    def CheckAndCloseExistingSession(self):
        if self.HAPISession != None and self.IsSessionValid():
            return self.CloseSession()
        return True

    def IsSessionValid(self):
        if self.ConnectedState != SessionConnectionState.FAILED_TO_CONNECT:
            return HAPI.IsSessionValid(self.HAPISession)
        return False

    def SaveHIP(self, filename = "debug.hip"):
        HAPI.SaveHIPFile(self.HAPISession, filename)
        print("Session saved to {0}".format(filename))

class HSessionManager():

    _defaultSession = None

    @staticmethod
    def GetOrCreateDefaultSession(rootpath = ""):
        if HSessionManager._defaultSession != None and HSessionManager._defaultSession.IsSessionValid():
            return HSessionManager._defaultSession
        elif HSessionManager._defaultSession == None or HSessionManager._defaultSession.ConnectedState == SessionConnectionState.NOT_CONNECTED:
            HSessionManager.CreateThriftPipeSession(rootpath)
        return HSessionManager._defaultSession

    @staticmethod
    def CheckAndCloseExistingSession():
        if HSessionManager._defaultSession != None:
            HSessionManager._defaultSession.CloseSession()
            HSessionManager._defaultSession = None

    @staticmethod
    def CreateThriftPipeSession(rootpath, pipeName = "hapi", autoClose = True, timeout = 10000.0):
        HSessionManager.CheckAndCloseExistingSession()
        HSessionManager._defaultSession = HSession()
        return HSessionManager._defaultSession.CreateThriftPipeSession(rootpath, pipeName, autoClose, timeout)

    @staticmethod
    def CloseDefaultSession():
        HSessionManager.CheckAndCloseExistingSession()

    @staticmethod
    def RestartSession():
        if HSessionManager._defaultSession != None:
            return HSessionManager._defaultSession.RestartSession()
        else:
            session = HSession()
            if session.CreateThriftPipeSession(true):
                HSessionManager._defaultSession = session
