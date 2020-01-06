from . import *

class HAsset():

    def __init__(self, session, hdapath):
        self.Instantiated = False
        self.HDAPath = hdapath
        self.Session = session
        assetLibId = HAPI.LoadAssetLibraryFromFile(session.HAPISession, self.HDAPath)
        self.AssetNames = HAPI.GetAvailableAssets(session.HAPISession, assetLibId)

    def Instantiate(self, node_name = "Node", operator_id = 0):
        node = HNode(self.Session, self.AssetNames[operator_id], node_name)
        return node