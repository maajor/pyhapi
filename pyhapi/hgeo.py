import numpy as np
from . import *

class HGeo():

    def __init__(self, session):
        self.Session = session
        self.HAPISession = session.HAPISession
        self.PointCount = 0
        self.VertexCount = 0
        self.FaceCount = 0

    def AddPointAttrib(self, name, data):
        pass


    def AddVertexAttrib(self, name, data):
        pass


    def AddPrimAttrib(self, name, data):
        pass

    def AddDetailAttrib(self, name, data):
        pass


    def CommitToNode(self, node_id):
        pass

class HGeoMesh(HGeo):

    def __init__(self, session, vertices, faces):
        #super(HGeoMesh, self).__init__(session)
        self.PointCount = vertices.shape[0]
        self.VertexCount = faces.flatten().shape[0]
        self.FaceCount = faces.shape[0]

        self.PartInfo = HAPI_PartInfo()
        self.PartInfo.type = HAPI_PartType.HAPI_PARTTYPE_MESH
        self.PartInfo.faceCount =  self.FaceCount
        self.PartInfo.vertexCount = self.VertexCount 
        self.PartInfo.pointCount = self.PointCount
        self.PartInfo.pointAttribCount = 1

        self.PAttribInfo = HAPI_AttributeInfo()
        self.PAttribInfo.count = self.PartInfo.pointCount
        self.PAttribInfo.tupleSize = 3
        self.PAttribInfo.exists = True
        self.PAttribInfo.storage = HAPI_StorageType.HAPI_STORAGETYPE_FLOAT
        self.PAttribInfo.owner = HAPI_AttributeOwner.HAPI_ATTROWNER_POINT
