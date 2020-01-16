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
        self.DetailCount = 1
        self.Attribs     = {}

        self.TypeToAddAttrib = {
            AttributeType.VERTEX:self.AddVertexAttrib,
            AttributeType.POINT:self.AddPointAttrib,
            AttributeType.PRIM:self.AddPrimAttrib,
            AttributeType.DETAIL:self.AddDetailAttrib}

    def AddAttrib(self, attrib_type, name, data):
        self.TypeToAddAttrib[attrib_type](name, data)

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

        #self.Attribs.append((attribInfo, name, data))
        self.Attribs[(HAPI_AttributeOwner.HAPI_ATTROWNER_POINT, name)] = (attribInfo, name, data)


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

        #self.Attribs.append((attribInfo, name, data))
        self.Attribs[(HAPI_AttributeOwner.HAPI_ATTROWNER_VERTEX, name)] = (attribInfo, name, data)

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

        #self.Attribs.append((attribInfo, name, data))
        self.Attribs[(HAPI_AttributeOwner.HAPI_ATTROWNER_PRIM, name)] = (attribInfo, name, data)

    def AddDetailAttrib(self, name, data):
        """Summary
        
        Args:
            name (TYPE): Description
            data (TYPE): Description
        """
        pass

    def GetAttribData(self, attrib_type, name):
        _, _, data = self.Attribs[(attrib_type, name)]
        return data

    def GetAttribNames(self):
        attrib_names = []
        for attrib_type, name in self.Attribs.keys():
            attrib_names.append([name, AttributeType(attrib_type)])
        return attrib_names

    def CommitToNode(self, session, node_id):
        """Summary
        
        Args:
            session (TYPE): Description
            node_id (TYPE): Description
        """
        
        HAPI.SetPartInfo(session.HAPISession, node_id, self.PartInfo)

        for attribInfo, name, data in self.Attribs.values():
            HAPI.AddAttribute(session.HAPISession, node_id, name, attribInfo)
            HAPI.StorageTypeToSetAttrib[attribInfo.storage](session.HAPISession, node_id, name, attribInfo, data)

class HGeoMesh(HGeo):

    """Summary
    
    Attributes:
        FaceCount (TYPE): Description
        Faces (TYPE): Description
        PointCount (TYPE): Description
        VertexCount (TYPE): Description
    """
    
    def __init__(self, vertices = None, faces = None):
        """Summary
        
        Args:
            vertices (TYPE): Description
            faces (TYPE): Description
        """
        super(HGeoMesh, self).__init__()
        if type(vertices) != type(None) and type(faces) != type(None):
            self.PointCount           = vertices.shape[0]
            self.VertexCount          = faces.flatten().shape[0]
            self.FaceCount            = faces.shape[0]
            self.Faces                = faces

            self.PartInfo.type        = HAPI_PartType.HAPI_PARTTYPE_MESH
            self.PartInfo.faceCount   = self.FaceCount
            self.PartInfo.vertexCount = self.VertexCount
            self.PartInfo.pointCount  = self.PointCount

            self.AddAttrib(AttributeType.POINT, "P", vertices)

    def ExtractFromSop(self, session, node_id, part_id):
        self.PartInfo = HAPI.GetPartInfo(session.HAPISession, node_id, part_id)
        for attrib_type in range(0, HAPI_AttributeOwner.HAPI_ATTROWNER_MAX):
            attrib_names = HAPI.GetAttributeNames(
                session.HAPISession, 
                node_id, 
                self.PartInfo,
                attrib_type)
            for attrib_name in attrib_names:
                #do not extract private data
                if not attrib_name.startswith("__"):
                    attrib_info = HAPI.GetAttributeInfo(session.HAPISession, node_id, part_id,attrib_name,attrib_type)
                    data = HAPI.StorageTypeToGetAttrib[attrib_info.storage](session.HAPISession, node_id, part_id, attrib_name, attrib_info)
                    self.Attribs[(attrib_type, attrib_name)] = (attrib_info, attrib_name, data)


    def CommitToNode(self, session, node_id):
        """Summary
        
        Args:
            session (TYPE): Description
            node_id (TYPE): Description
        """
        super().CommitToNode(session, node_id)

        HAPI.SetVertexList(session.HAPISession, node_id, self.Faces)
        #Todo: what if each face's vertex count not same
        HAPI.SetFaceCounts(session.HAPISession, node_id, np.repeat(self.Faces.shape[1], self.Faces.shape[0]))
        HAPI.CommitGeo(session.HAPISession, node_id)

class HGeoCurve(HGeo):

    def __init__(self, vertices, curve_knots = None, has_knot = False, is_periodic = False, order = 4, curve_type = HAPI_CurveType.HAPI_CURVETYPE_LINEAR):
        """Summary
        
        Args:
            vertices (TYPE): Description
            faces (TYPE): Description
        """
        super(HGeoCurve, self).__init__()
        self.PointCount           = vertices.shape[0]
        self.VertexCount          = vertices.shape[0]
        self.FaceCount            = 1
        self.CurveKnots           = curve_knots
        self.CurveCount           = np.repeat(vertices.shape[0], 1)

        self.PartInfo.type        = HAPI_PartType.HAPI_PARTTYPE_CURVE
        self.PartInfo.faceCount   = self.FaceCount
        self.PartInfo.vertexCount = self.VertexCount
        self.PartInfo.pointCount  = self.PointCount

        self.CurveInfo = HAPI_CurveInfo()
        self.CurveInfo.curveType = curve_type
        self.CurveInfo.curveCount = 1
        self.CurveInfo.vertexCount = vertices.shape[0]
        self.CurveInfo.knotCount = (0 if type(curve_knots) == type(None) else curve_knots.shape[0])
        self.CurveInfo.isPeriodic = is_periodic
        self.CurveInfo.order = order
        self.CurveInfo.hasKnots = has_knot

        #self.AddPointAttrib("P", vertices)
        self.AddAttrib(AttributeType.POINT, "P", vertices)

    def CommitToNode(self, session, node_id):
        """Summary
        
        Args:
            session (TYPE): Description
            node_id (TYPE): Description
        """
        super().CommitToNode(session, node_id)

        HAPI.SetCurveInfo(session.HAPISession, node_id, self.CurveInfo)
        HAPI.SetCurveCounts(session.HAPISession, node_id, self.PartInfo.id, self.CurveCount)
        HAPI.SetCurveKnots(session.HAPISession, node_id, self.PartInfo.id, self.CurveKnots)

        HAPI.CommitGeo(session.HAPISession, node_id)