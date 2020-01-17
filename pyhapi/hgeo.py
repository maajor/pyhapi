"""Summary
"""
import numpy as np

from . import hdata as HDATA
from . import hapi as HAPI

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
        self.part_info = HDATA.HAPI_PartInfo()
        self.point_count = 0
        self.vertex_count = 0
        self.face_count = 0
        self.detail_count = 1
        self.attribs = {}

        self.type_to_add_attrib = {
            HDATA.AttributeType.VERTEX: self.add_vertex_attrib,
            HDATA.AttributeType.POINT: self.add_point_attrib,
            HDATA.AttributeType.PRIM: self.add_prim_attrib,
            HDATA.AttributeType.DETAIL: self.add_detail_attrib}

    def add_attrib(self, attrib_type, name, data):
        """[summary]

        Args:
            attrib_type ([type]): [description]
            name ([type]): [description]
            data ([type]): [description]
        """
        self.type_to_add_attrib[attrib_type](name, data)

    def add_point_attrib(self, name, data):
        """Summary

        Args:
            name (TYPE): Description
            data (TYPE): Description

        Returns:
            TYPE: Description
        """
        count, tuple_size = data.shape
        if count != self.point_count:
            print("AddPointAttrib Error, Data length {0} not compatible with point count {1}".\
                format(count, self.point_count))
            return
        attrib_info = HDATA.HAPI_AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_POINT
        self.part_info.pointAttribCount += 1

        #self.Attribs.append((attribInfo, name, data))
        self.attribs[(HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_POINT, name)] = (
            attrib_info, name, data)

    def add_vertex_attrib(self, name, data):
        """Summary

        Args:
            name (TYPE): Description
            data (TYPE): Description

        Returns:
            TYPE: Description
        """
        count, tuple_size = data.shape
        if count != self.vertex_count:
            print("AddVertexAttrib Error, Data length {0} not compatible with vertex count {1}".\
                format(count, self.vertex_count))
            return
        attrib_info = HDATA.HAPI_AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_VERTEX
        self.part_info.vertexAttribCount += 1

        #self.Attribs.append((attribInfo, name, data))
        self.attribs[(HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_VERTEX, name)] = (
            attrib_info, name, data)

    def add_prim_attrib(self, name, data):
        """Summary

        Args:
            name (TYPE): Description
            data (TYPE): Description

        Returns:
            TYPE: Description
        """
        count, tuple_size = data.shape
        if count != self.face_count:
            print("AddPrimAttrib Error, Data length {0} not compatible with prim count {1}".\
                format(count, self.face_count))
            return
        attrib_info = HDATA.HAPI_AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_PRIM
        self.part_info.primAttribCount += 1

        #self.Attribs.append((attribInfo, name, data))
        self.attribs[(HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_PRIM, name)] = (
            attrib_info, name, data)

    def add_detail_attrib(self, name, data):
        """Summary

        Args:
            name (TYPE): Description
            data (TYPE): Description
        """
        count, tuple_size = data.shape
        if count != self.detail_count:
            print("add_detail_attrib Error, Data length {0} not compatible with detail count {1}".\
                format(count, self.detail_count))
            return
        attrib_info = HDATA.HAPI_AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_DETAIL
        self.part_info.detailAttribCount += 1

        #self.Attribs.append((attribInfo, name, data))
        self.attribs[(HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_DETAIL, name)] = (
            attrib_info, name, data)

    def get_attrib_data(self, attrib_type, name):
        """[summary]

        Args:
            attrib_type ([type]): [description]
            name ([type]): [description]

        Returns:
            [type]: [description]
        """
        _, _, data = self.attribs[(attrib_type, name)]
        return data

    def get_attrib_names(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        attrib_names = []
        for k, _ in self.attribs.items():
            attrib_type, name = k
            attrib_names.append([name, HDATA.AttributeType(attrib_type)])
        return attrib_names

    def commit_to_node(self, session, node_id):
        """Summary

        Args:
            session (TYPE): Description
            node_id (TYPE): Description
        """

        HAPI.SetPartInfo(session.hapi_session, node_id, self.part_info)

        for attrib_info, name, data in self.attribs.values():
            HAPI.AddAttribute(session.hapi_session, node_id, name, attrib_info)
            HAPI.StorageTypeToSetAttrib[attrib_info.storage](
                session.hapi_session, node_id, name, attrib_info, data)


class HGeoMesh(HGeo):

    """Summary

    Attributes:
        FaceCount (TYPE): Description
        Faces (TYPE): Description
        PointCount (TYPE): Description
        VertexCount (TYPE): Description
    """

    def __init__(self, vertices=None, faces=None):
        """Summary

        Args:
            vertices (TYPE): Description
            faces (TYPE): Description
        """
        super(HGeoMesh, self).__init__()
        if isinstance(vertices, np.ndarray) and isinstance(faces, np.ndarray):
            self.point_count = vertices.shape[0]
            self.vertex_count = faces.flatten().shape[0]
            self.face_count = faces.shape[0]
            self.faces = faces

            self.part_info.type = HDATA.HAPI_PartType.HAPI_PARTTYPE_MESH
            self.part_info.faceCount = self.face_count
            self.part_info.vertexCount = self.vertex_count
            self.part_info.pointCount = self.point_count

            self.add_attrib(HDATA.AttributeType.POINT, "P", vertices)

    def extract_from_sop(self, session, node_id, part_id):
        """[summary]

        Args:
            session ([type]): [description]
            node_id ([type]): [description]
            part_id ([type]): [description]
        """
        self.part_info = HAPI.GetPartInfo(session.hapi_session, node_id, part_id)
        for attrib_type in range(0, HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_MAX):
            attrib_names = HAPI.GetAttributeNames(
                session.hapi_session,
                node_id,
                self.part_info,
                attrib_type)
            for attrib_name in attrib_names:
                # do not extract private data
                if not attrib_name.startswith("__"):
                    attrib_info = HAPI.GetAttributeInfo(
                        session.hapi_session, node_id, part_id, attrib_name, attrib_type)
                    data = HAPI.StorageTypeToGetAttrib[attrib_info.storage](
                        session.hapi_session, node_id, part_id, attrib_name, attrib_info)
                    self.attribs[(attrib_type, attrib_name)] = (
                        attrib_info, attrib_name, data)

    def commit_to_node(self, session, node_id):
        """Summary

        Args:
            session (TYPE): Description
            node_id (TYPE): Description
        """
        super().commit_to_node(session, node_id)

        HAPI.SetVertexList(session.hapi_session, node_id, self.faces)
        # Todo: what if each face's vertex count not same
        HAPI.SetFaceCounts(session.hapi_session, node_id, np.repeat(
            self.faces.shape[1], self.faces.shape[0]))
        HAPI.CommitGeo(session.hapi_session, node_id)


class HGeoCurve(HGeo):
    """[summary]

    Args:
        HGeo ([type]): [description]
    """

    def __init__(self, vertices, curve_knots=None,\
        is_periodic=False, order=4, curve_type=HDATA.HAPI_CurveType.HAPI_CURVETYPE_LINEAR):
        """Summary

        Args:
            vertices (TYPE): Description
            faces (TYPE): Description
        """
        super(HGeoCurve, self).__init__()
        self.point_count = vertices.shape[0]
        self.vertex_count = vertices.shape[0]
        self.face_count = 1
        self.curve_knots = curve_knots
        self.curve_count = np.repeat(vertices.shape[0], 1)

        self.part_info.type = HDATA.HAPI_PartType.HAPI_PARTTYPE_CURVE
        self.part_info.faceCount = self.face_count
        self.part_info.vertexCount = self.vertex_count
        self.part_info.pointCount = self.point_count

        self.curve_info = HDATA.HAPI_CurveInfo()
        self.curve_info.curveType = curve_type
        self.curve_info.curveCount = 1
        self.curve_info.vertexCount = vertices.shape[0]
        self.curve_info.knotCount = (
            curve_knots.shape[0] if isinstance(curve_knots, np.ndarray) else 0)
        self.curve_info.isPeriodic = is_periodic
        self.curve_info.order = order
        self.curve_info.hasKnots = isinstance(curve_knots, np.ndarray)

        #self.AddPointAttrib("P", vertices)
        self.add_attrib(HDATA.AttributeType.POINT, "P", vertices)

    def commit_to_node(self, session, node_id):
        """Summary

        Args:
            session (TYPE): Description
            node_id (TYPE): Description
        """
        super().commit_to_node(session, node_id)

        HAPI.SetCurveInfo(session.hapi_session, node_id, self.curve_info)
        HAPI.SetCurveCounts(session.hapi_session, node_id,
                            self.part_info.id, self.curve_count)
        HAPI.SetCurveKnots(session.hapi_session, node_id,
                           self.part_info.id, self.curve_knots)

        HAPI.CommitGeo(session.hapi_session, node_id)
