"""Summary
"""
from . import *

class HAsset():

    """Summary
    
    Attributes:
        AssetNames (TYPE): Description
        HDAPath (TYPE): Description
        Instantiated (bool): Description
        Session (TYPE): Description
    """
    
    def __init__(self, session, hdapath):
        """Summary
        
        Args:
            session (TYPE): Description
            hdapath (TYPE): Description
        """
        self.Instantiated = False
        self.HDAPath = hdapath
        self.Session = session
        assetLibId = HAPI.LoadAssetLibraryFromFile(session.HAPISession, self.HDAPath)
        self.AssetNames = HAPI.GetAvailableAssets(session.HAPISession, assetLibId)

    def Instantiate(self, node_name = "Node", operator_id = 0):
        """Summary
        
        Args:
            node_name (str, optional): Description
            operator_id (int, optional): Description
        
        Returns:
            TYPE: Description
        """
        node = HNode(self.Session, self.AssetNames[operator_id], node_name)
        return node