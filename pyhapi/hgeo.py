"""Summary
"""
from . import *

class HGeo():

    """Summary
    
    Attributes:
        Attribs (list): Description
        FaceCount (int): Description
        PartInfo (TYPE): Description
        PointCount (int): Description
        VertexCount (int): Description
    """
    
    def __init__(self):
        """Summary
        """
        self.PartInfo    = HAPI_PartInfo()
        self.PointCount  = 0
        self.VertexCount = 0
        self.FaceCount   = 0
        self.Attribs     = []

    def AddPointAttrib(self, name, data):
        """Summary
        
        Args:
            name (TYPE): Description
            data (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        count, tupleSize = data.shape
        if count != self.PointCount:
            print("AddPointAttrib Error, Data length {0} not compatible with point count {1}".format(count, self.PointCount))
            return
        attribInfo                       = HAPI_AttributeInfo()
        attribInfo.count                 = count
        attribInfo.tupleSize             = tupleSize
        attribInfo.exists                = True
        attribInfo.storage               = NpTypeToHStorageType[data.dtype]
        attribInfo.owner                 = HAPI_AttributeOwner.HAPI_ATTROWNER_POINT
        self.PartInfo.pointAttribCount  += 1

        self.Attribs.append((attribInfo, name, data))


    def AddVertexAttrib(self, name, data):
        """Summary
        
        Args:
            name (TYPE): Description
            data (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        count, tupleSize = data.shape
        if count != self.VertexCount:
            print("AddVertexAttrib Error, Data length {0} not compatible with vertex count {1}".format(count, self.VertexCount))
            return
        attribInfo                        = HAPI_AttributeInfo()
        attribInfo.count                  = count
        attribInfo.tupleSize              = tupleSize
        attribInfo.exists                 = True
        attribInfo.storage                = NpTypeToHStorageType[data.dtype]
        attribInfo.owner                  = HAPI_AttributeOwner.HAPI_ATTROWNER_VERTEX
        self.PartInfo.vertexAttribCount  += 1

        self.Attribs.append((attribInfo, name, data))

    def AddPrimAttrib(self, name, data):
        """Summary
        
        Args:
            name (TYPE): Description
            data (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        count, tupleSize = data.shape
        if count != self.FaceCount:
            print("AddPrimAttrib Error, Data length {0} not compatible with prim count {1}".format(count, self.FaceCount))
            return
        attribInfo                      = HAPI_AttributeInfo()
        attribInfo.count                = count
        attribInfo.tupleSize            = tupleSize
        attribInfo.exists               = True
        attribInfo.storage              = NpTypeToHStorageType[data.dtype]
        attribInfo.owner                = HAPI_AttributeOwner.HAPI_ATTROWNER_PRIM
        self.PartInfo.primAttribCount  += 1

        self.Attribs.append((attribInfo, name, data))

    def AddDetailAttrib(self, name, data):
        """Summary
        
        Args:
            name (TYPE): Description
            data (TYPE): Description
        """
        pass

    def CommitToNode(self, session, node_id):
        """Summary
        
        Args:
            session (TYPE): Description
            node_id (TYPE): Description
        """
        pass

class HGeoMesh(HGeo):

    """Summary
    
    Attributes:
        FaceCount (TYPE): Description
        Faces (TYPE): Description
        PointCount (TYPE): Description
        VertexCount (TYPE): Description
    """
    
    def __init__(self, vertices, faces):
        """Summary
        
        Args:
            vertices (TYPE): Description
            faces (TYPE): Description
        """
        super(HGeoMesh, self).__init__()
        self.PointCount           = vertices.shape[0]
        self.VertexCount          = faces.flatten().shape[0]
        self.FaceCount            = faces.shape[0]
        self.Faces                = faces

        self.PartInfo.type        = HAPI_PartType.HAPI_PARTTYPE_MESH
        self.PartInfo.faceCount   = self.FaceCount
        self.PartInfo.vertexCount = self.VertexCount
        self.PartInfo.pointCount  = self.PointCount

        self.AddPointAttrib("P", vertices)

    def CommitToNode(self, session, node_id):
        """Summary
        
        Args:
            session (TYPE): Description
            node_id (TYPE): Description
        """
        HAPI.SetPartInfo(session.HAPISession, node_id, self.PartInfo)

        for attribInfo, name, data in self.Attribs:
            HAPI.AddAttribute(session.HAPISession, node_id, name, attribInfo)
            HAPI.StorageTypeToSetAttrib[attribInfo.storage](session.HAPISession, node_id, name, attribInfo, data)

        HAPI.SetVertexList(session.HAPISession, node_id, self.Faces)
        HAPI.SetFaceCounts(session.HAPISession, node_id, np.repeat(self.Faces.shape[1], self.Faces.shape[0]))
        HAPI.CommitGeo(session.HAPISession, node_id)

        
