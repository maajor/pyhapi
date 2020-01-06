from . import *

class HNode():

    def __init__(self, session, operator_name, node_name):
        self.Session = session
        self.HAPISession = session.HAPISession
        self.Instantiated = False
        self.NodeId = HAPI.CreateNode(self.HAPISession, operator_name, node_name)
        self.Instantiated = True

    def IsInited(self):
        if not self.Instantiated:
            print("Asset Not Instantiated")
        return self.Instantiated

    def GetParams(self):
        self.NodeInfo = HAPI.GetNodeInfo(self.HAPISession, self.NodeId.value);
        self.ParamInfo = HAPI.GetParameters(self.HAPISession, self.NodeId.value, self.NodeInfo)

        self.ParamIdDict = {}
        for i in range(0, self.NodeInfo.parmCount):
            namesh = self.ParamInfo[i].labelSH
            namestr = HAPI.GetString(self.HAPISession, namesh).decode()
            self.ParamIdDict[namestr] = i

    def GetParamValue(self, param_name):
        if not self.IsInited():
            return
        paramid = self.ParamIdDict[param_name]
        paraminfo = self.ParamInfo[paramid]
        if paraminfo.IsInt():
            return HAPI.GetParmIntValue(self.HAPISession, self.NodeId.value, param_name)
        elif paraminfo.isFloat():
            return HAPI.GetParmFloatValue(self.HAPISession, self.NodeId.value, param_name)
        elif paraminfo.isString():
            return HAPI.GetParamStringValue(self.HAPISession, self.NodeId.value, param_name)

    def SetParamValue(self, param_name, value):
        if not self.IsInited():
            return
        paramid = self.ParamIdDict[param_name]
        paraminfo = self.ParamInfo[paramid]
        if paraminfo.IsInt():
            return HAPI.SetParmIntValue(self.HAPISession, self.NodeId.value, param_name, value)
        elif paraminfo.isFloat():
            return HAPI.SetParmFloatValue(self.HAPISession, self.NodeId.value, param_name, value)
        elif paraminfo.isString():
            return HAPI.SetParamStringValue(self.HAPISession, self.NodeId.value, paramid, value)

    def Cook(self):
        if not self.IsInited():
            return
        HAPI.CookNode(self.HAPISession, self.Session.CookOption, self.NodeId)

    async def CookAsync(self):
        if not self.IsInited():
            return
        await HAPI.CookNodeAsync(self.HAPISession, self.Session.CookOption, self.NodeId)

    def PressButton(self, param_name):
        if not self.IsInited():
            return
        paramid = self.ParamIdDict[param_name]
        paraminfo = self.ParamInfo[paramid]
        HAPI.SetParmIntValue(self.HAPISession, self.NodeId.value, param_name, 1)
        HAPI.WaitCook(self.HAPISession, 5.0)
        HAPI.SetParmIntValue(self.HAPISession, self.NodeId.value, param_name, 0)

    async def PressButtonAsync(self, param_name):
        if not self.IsInited():
            return
        paramid = self.ParamIdDict[param_name]
        paraminfo = self.ParamInfo[paramid]
        HAPI.SetParmIntValue(self.HAPISession, self.NodeId.value, param_name, 1)
        await HAPI.WaitCookAsync(self.HAPISession, 5.0)
        HAPI.SetParmIntValue(self.HAPISession, self.NodeId.value, param_name, 0)

    def __del__(self):
        HAPI.DeleteNode(self.HAPISession, self.NodeId)