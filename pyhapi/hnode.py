"""Summary
"""
from . import *

class HNode():

    """Summary
    
    Attributes:
        HAPISession (TYPE): Description
        Instantiated (bool): Description
        NodeId (TYPE): Description
        NodeInfo (TYPE): Description
        ParamIdDict (dict): Description
        ParamInfo (TYPE): Description
        Session (TYPE): Description
    """
    
    def __init__(self, session, operator_name, node_name, parent_node = None, cook_on_creation = False):
        """Summary
        
        Args:
            session (TYPE): Description
            operator_name (TYPE): Description
            node_name (TYPE): Description
        """
        self.Session      = session
        self.HAPISession  = session.HAPISession
        self.Instantiated = False
        self.NodeId       = HAPI.CreateNode(self.HAPISession,
            operator_name, 
            node_name, 
            parent_node_id = parent_node.NodeId if parent_node != None else -1, 
            cook_on_creation = cook_on_creation)
        self.Instantiated = True
        self.Session.Nodes[self.NodeId] = self
        self.Name = node_name

    def IsInited(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        if not self.Instantiated:
            print("Asset Not Instantiated")
        return self.Instantiated

    def GetParams(self):
        """Summary
        """
        self.NodeInfo    = HAPI.GetNodeInfo(self.HAPISession, self.NodeId);
        self.ParamInfo   = HAPI.GetParameters(self.HAPISession, self.NodeId, self.NodeInfo)
        self.ParamIdDict = {}
        for i in range(0, self.NodeInfo.parmCount):
            namesh = self.ParamInfo[i].labelSH
            namestr = HAPI.GetString(self.HAPISession, namesh).decode()
            self.ParamIdDict[namestr] = i

    def GetParamValue(self, param_name):
        """Summary
        
        Args:
            param_name (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        if not self.IsInited():
            return
        paramid = self.ParamIdDict[param_name]
        paraminfo = self.ParamInfo[paramid]
        if paraminfo.IsInt():
            return HAPI.GetParmIntValue(self.HAPISession, self.NodeId, param_name)
        elif paraminfo.isFloat():
            return HAPI.GetParmFloatValue(self.HAPISession, self.NodeId, param_name)
        elif paraminfo.isString():
            return HAPI.GetParamStringValue(self.HAPISession, self.NodeId, param_name)

    def SetParamValue(self, param_name, value):
        """Summary
        
        Args:
            param_name (TYPE): Description
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        if not self.IsInited():
            return
        paramid   = self.ParamIdDict[param_name]
        paraminfo = self.ParamInfo[paramid]
        if paraminfo.IsInt():
            return HAPI.SetParmIntValue(self.HAPISession, self.NodeId, param_name, value)
        elif paraminfo.isFloat():
            return HAPI.SetParmFloatValue(self.HAPISession, self.NodeId, param_name, value)
        elif paraminfo.isString():
            return HAPI.SetParamStringValue(self.HAPISession, self.NodeId, paramid, value)

    def GetDisplayGeos(self):
        all_geos = []
        asset_info = HAPI.GetAssetInfo(self.HAPISession, self.NodeId)
        child_sop_count = HAPI.ComposeObjectList(self.HAPISession, self.NodeId)
        child_object_infos = HAPI.GetComposedObjectList(self.HAPISession, self.NodeId, child_sop_count)
        for objectinfo in child_object_infos:
            geo_info = HAPI.GetDisplayGeoInfo(self.HAPISession, objectinfo.nodeId)
            for part_id in range(0, geo_info.partCount):
                extract_mesh = HGeoMesh()
                extract_mesh.ExtractFromSop(self.Session, geo_info.nodeId, part_id)
                all_geos.append(extract_mesh)
        return all_geos

    def Cook(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        if not self.IsInited():
            return
        HAPI.CookNode(self.HAPISession, self.Session.CookOption, self.NodeId)
        return self

    async def CookAsync(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        if not self.IsInited():
            return
        await HAPI.CookNodeAsync(self.HAPISession, self.Session.CookOption, self.NodeId)

    def PressButton(self, param_name):
        """Summary
        
        Args:
            param_name (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        if not self.IsInited():
            return
        paramid   = self.ParamIdDict[param_name]
        paraminfo = self.ParamInfo[paramid]
        HAPI.SetParmIntValue(self.HAPISession, self.NodeId, param_name, 1)
        HAPI.WaitCook(self.HAPISession, 5.0)
        HAPI.SetParmIntValue(self.HAPISession, self.NodeId, param_name, 0)

    async def PressButtonAsync(self, param_name):
        """Summary
        
        Args:
            param_name (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        if not self.IsInited():
            return
        paramid   = self.ParamIdDict[param_name]
        paraminfo = self.ParamInfo[paramid]
        HAPI.SetParmIntValue(self.HAPISession, self.NodeId, param_name, 1)
        await HAPI.WaitCookAsync(self.HAPISession, 5.0)
        HAPI.SetParmIntValue(self.HAPISession, self.NodeId, param_name, 0)

    def ConnectNodeInput(self, node_to_connect, input_index = 0, output_index = 0):
        """Summary
        
        Args:
            node_to_connect (HNode): Description
            input_index (int, optional): Description
            output_index (int, optional): Description
        """
        HAPI.ConnectNodeInput(self.HAPISession, self.NodeId, node_to_connect.NodeId, input_index, output_index)
        return self

    def DisconnectNodeInput(self, node_to_connect, input_index = 0):
        """Summary
        
        Args:
            node_to_connect (HNode): Description
            input_index (int, optional): Description
            output_index (int, optional): Description
        """
        HAPI.DisconnectNodeInput(self.HAPISession, self.NodeId, input_index)
        return self

    def GetNodeInput(self, input_index = 0):
        input_node_id = HAPI.QueryNodeInput(self.HAPISession, self.NodeId, input_index)
        return self.Session.GetNode(input_node_id)

    def GetChildNodes(self):
        child_count = HAPI.ComposeChildNodeList(self.HAPISession, self.NodeId)
        child_nodes = HAPI.GetComposedChildNodeList(self.HAPISession, self.NodeId, child_count)
        '''child_hnodes = []
        for node_id in child_nodes:
            try_get_node = self.Session.Nodes.get(node_id)
            if try_get_node != None:
                child_hnodes.append(try_get_node)
            else:
                existing_node = HExistingNode(self.Session, node_id)
                child_hnodes.append(existing_node)'''

        return [self.Session.GetNode(node_id) for node_id in child_nodes]

    def SetGeometry(self, geo):
        """Summary
        
        Args:
            geo (TYPE): Description
        """
        geo.CommitToNode(self.Session, self.NodeId)

    def Delete(self):
        """Summary
        """
        try:
            HAPI.DeleteNode(self.HAPISession, self.NodeId)
            self.Instantiated = False
        except Exception as e:
            print(e)



class HInputNode(HNode):

    """Summary
    
    Attributes:
        HAPISession (TYPE): Description
        Instantiated (bool): Description
        NodeId (TYPE): Description
        Session (TYPE): Description
    """
    
    def __init__(self, session, node_name):
        """Summary
        
        Args:
            session (TYPE): Description
            node_name (TYPE): Description
        """
        self.Session                    = session
        self.HAPISession                = session.HAPISession
        self.Instantiated               = False
        self.NodeId                     = HAPI.CreateInputNode(self.HAPISession, node_name)
        self.Instantiated               = True
        self.Name                       = node_name
        self.Session.Nodes[self.NodeId] = self

class HExistingNode(HNode):

    def __init__(self, session, node_id):
        self.Session                    = session
        self.HAPISession                = session.HAPISession
        self.NodeId                     = node_id

        try:
            self.NodeInfo                   = HAPI.GetNodeInfo(self.HAPISession, self.NodeId);
            self.Name                       = HAPI.GetString(self.HAPISession, self.NodeInfo.nameSH)
            self.Instantiated               = True
        except Exception as e:
            self.Instantiated               = False

        return

