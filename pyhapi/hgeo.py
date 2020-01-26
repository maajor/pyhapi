# -*- coding: utf-8 -*-
"""Wrapper for houdini engine's geometry.
Author  : Maajor
Email   : hello_myd@126.com

HGeo:
    An base class for houdini engine's geometry, including shared operation\
        for setting and getting attributes. It could derived HGeoMesh\
        for handling mesh, HGeoCurve for handling curve, HGeoVolume for \
            handling volume data.

HGeoMesh:
    An object containing mesh data

HGeoCurve:
    An object containing curve data

Example usage:

import pyhapi as ph

#create houdini engine session
session = ph.HSessionManager.get_or_create_default_session()

#create an inputnode where you can set geometry
geo_inputnode = ph.HInputNode(session, "Cube")

#create a geomesh
cube_geo = ph.HGeoMesh(
    vertices=np.array(
        [[0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0],
            [1.0, 1.0, 1.0]], dtype=np.float32),
    faces=np.array(
        [[0, 2, 6, 4],
            [2, 3, 7, 6],
            [2, 0, 1, 3],
            [1, 5, 7, 3],
            [5, 4, 6, 7],
            [0, 4, 5, 1]], dtype=np.int32))

#set this geomesh as geometry of inputnode
geo_inputnode.set_geometry(cube_geo)

"""
import numpy as np

from . import hdata as HDATA
from . import hapi as HAPI

class HGeo():

    """An base class for houdini engine's geometry, including shared operation\
        for setting and getting attributes. It could derived HGeoMesh\
            for handling mesh, HGeoCurve for handling curve, HGeoVolume for \
                handling volume data.

    Attributes:
        part_info (PartInfo): geom info of this part
        point_count (int): number of points in this geo
        vertex_count (int): number of vertices in this geo
        face_count (int): number of faces in this geo
        detail_count (int): number of details in this geo, should be 1
        attribs (dict((int,str),(AttributeInfo,str,np.ndarray)): attribute's name\
            to attribute's actual data
        type_to_add_attrib (dict(int,func)): attribute's type to the function to \
            set the attribute data into hengine
    """

    def __init__(self):
        self.part_info = HDATA.PartInfo()
        self.point_count = 0
        self.vertex_count = 0
        self.face_count = 0
        self.detail_count = 1
        self.attribs = {}

        self.type_to_add_attrib = {
            HDATA.AttributeOwner.VERTEX: self.add_vertex_attrib,
            HDATA.AttributeOwner.POINT: self.add_point_attrib,
            HDATA.AttributeOwner.PRIM: self.add_prim_attrib,
            HDATA.AttributeOwner.DETAIL: self.add_detail_attrib}

    def add_attrib(self, attrib_type, name, data):
        """Add attribute data to geo, should provide attribute's\
            type, name and data

        Args:
            attrib_type (AttributeOwner): Type of the attribute
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims\
                corresponding to each item in that attribute, ptnum/vtnum\
                    primnum etc, 2nd dim should be tuple size of this attribute
        """
        self.type_to_add_attrib[attrib_type](name, data)

    def add_point_attrib(self, name, data):
        """Add point attribute data to geo

        Args:
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims\
                equals number of points, 2nd dim should be tuple size of this attribute
        """
        count, tuple_size = data.shape
        if count != self.point_count:
            print("AddPointAttrib Error, Data length {0} not compatible with point count {1}".\
                format(count, self.point_count))
            return
        attrib_info = HDATA.AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.AttributeOwner.POINT
        self.part_info.point_attrib_count += 1

        #self.Attribs.append((attribInfo, name, data))
        self.attribs[(HDATA.AttributeOwner.POINT, name)] = (
            attrib_info, name, data)

    def add_vertex_attrib(self, name, data):
        """Add vertex attribute data to geo

        Args:
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims\
                equals number of vertices, 2nd dim should be tuple size of this attribute
        """
        count, tuple_size = data.shape
        if count != self.vertex_count:
            print("AddVertexAttrib Error, Data length {0} not compatible with vertex count {1}".\
                format(count, self.vertex_count))
            return
        attrib_info = HDATA.AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.AttributeOwner.VERTEX
        self.part_info.vertex_attrib_count += 1

        #self.Attribs.append((attribInfo, name, data))
        self.attribs[(HDATA.AttributeOwner.VERTEX, name)] = (
            attrib_info, name, data)

    def add_prim_attrib(self, name, data):
        """Add prim attribute data to geo

        Args:
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims\
                equals number of faces, 2nd dim should be tuple size of this attribute
        """
        count, tuple_size = data.shape
        if count != self.face_count:
            print("AddPrimAttrib Error, Data length {0} not compatible with prim count {1}".\
                format(count, self.face_count))
            return
        attrib_info = HDATA.AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.AttributeOwner.PRIM
        self.part_info.prim_attrib_count += 1

        #self.Attribs.append((attribInfo, name, data))
        self.attribs[(HDATA.AttributeOwner.PRIM, name)] = (
            attrib_info, name, data)

    def add_detail_attrib(self, name, data):
        """Add detail attribute data to geo

        Args:
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims\
                should be 1, 2nd dim should be tuple size of this attribute
        """
        count, tuple_size = data.shape
        if count != self.detail_count:
            print("add_detail_attrib Error, Data length {0} not compatible with detail count {1}".\
                format(count, self.detail_count))
            return
        attrib_info = HDATA.AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.AttributeOwner.DETAIL
        self.part_info.detail_attrib_count += 1

        #self.Attribs.append((attribInfo, name, data))
        self.attribs[(HDATA.AttributeOwner.DETAIL, name)] = (
            attrib_info, name, data)

    def get_attrib_data(self, attrib_type, name):
        """Get attribute data of certain type and name

        Args:
            attrib_type (AttributeOwner): Type of querying attribute
            name (str): Name of querying attribute

        Returns:
            ndarray(,): Data of querying attribute
        """
        _, _, data = self.attribs[(attrib_type, name)]
        return data

    def get_attrib_names(self):
        """Get all attribute name in this geo

        Returns:
            list((str,AttributeOwner)): All attributes containing in this geo
        """
        attrib_names = []
        for k, _ in self.attribs.items():
            attrib_type, name = k
            attrib_names.append([name, HDATA.AttributeOwner(attrib_type)])
        return attrib_names

    def commit_to_node(self, session, node_id):
        """Set this geo into hengine's node

        Args:
            session (int64): The session of Houdini you are interacting with.
            node_id (int): The node to add geo.
        """
        HAPI.set_part_info(session.hapi_session, node_id, self.part_info)

        for attrib_info, name, data in self.attribs.values():
            HAPI.add_attribute(session.hapi_session, node_id, name, attrib_info)
            HAPI.STORAGE_TYPE_TO_SET_ATTRIB[attrib_info.storage](
                session.hapi_session, node_id, name, attrib_info, data)

    def extract_from_sop(self, session, part_info, node_id, part_id=0):
        """Extract geometry from sop

        Args:
            session (int64): The session of Houdini you are interacting with.
            part_info (PartInfo): The info of part
            node_id (int): The node to add geo.
            part_id (int): Part id. Default to 0
        """
        self.part_info = part_info
        self.point_count = part_info.pointCount
        self.vertex_count = part_info.vertexCount
        self.face_count = part_info.faceCount

        #Fill attributes
        for attrib_type in range(0, HDATA.AttributeOwner.MAX):
            attrib_names = HAPI.get_attribute_names(
                session.hapi_session,
                node_id,
                self.part_info,
                attrib_type)
            for attrib_name in attrib_names:
                # do not extract private data
                if not attrib_name.startswith("__"):
                    attrib_info = HAPI.get_attribute_info(
                        session.hapi_session, node_id, part_id, attrib_name, attrib_type)
                    data = HAPI.STORAGE_TYPE_TO_GET_ATTRIB[attrib_info.storage](
                        session.hapi_session, node_id, part_id, attrib_name, attrib_info)
                    self.attribs[(attrib_type, attrib_name)] = (
                        attrib_info, attrib_name, data)



class HGeoMesh(HGeo):

    """A class representing hengine's mesh geometry

    Attributes:
        faces (np.ndarray): Faces data, should be in 2D such as\
                (face_count, vertex_each_face).
    """

    def __init__(self, vertices=None, faces=None):
        """Initialize

        Args:
            vertices (np.ndarray, optional): Verticed data, should be 2D:\
                (pount_count, 3). Defaults to None.
            faces (np.ndarray, optional): Faces data, should be in 2D such as\
                (face_count, vertex_each_face). Defaults to None.
        """
        super(HGeoMesh, self).__init__()
        if isinstance(vertices, np.ndarray) and isinstance(faces, np.ndarray):
            self.point_count = vertices.shape[0]
            self.vertex_count = faces.flatten().shape[0]
            self.face_count = faces.shape[0]
            self.faces = faces

            self.part_info.type = HDATA.PartType.MESH
            self.part_info.faceCount = self.face_count
            self.part_info.vertexCount = self.vertex_count
            self.part_info.pointCount = self.point_count

            self.add_attrib(HDATA.AttributeOwner.POINT, "P", vertices)

    def extract_from_sop(self, session, part_info, node_id, part_id=0):
        """Extract mesh from sop

        Args:
            session (int64): The session of Houdini you are interacting with.
            part_info (PartInfo): The info of part
            node_id (int): The node to add geo.
            part_id (int): Part id. Default to 0
        """
        super().extract_from_sop(session, part_info, node_id, part_id)

        self.faces = HAPI.get_faces(session.hapi_session, node_id, part_info)

    def commit_to_node(self, session, node_id):
        """Set this geo into hengine's node

        Args:
            session (int64): The session of Houdini you are interacting with.
            node_id (int): The node to add geo.
        """
        super().commit_to_node(session, node_id)

        HAPI.set_vertex_list(session.hapi_session, node_id, self.faces)
        HAPI.set_face_counts(session.hapi_session, node_id, \
            np.array([len(face) for face in self.faces]))
        HAPI.commit_geo(session.hapi_session, node_id)


class HGeoCurve(HGeo):

    """A class representing hengine's curve geometry

    Attributes:
        curve_knots (np.ndarray): Curve knots
        curve_count (np.ndarray): Curve counts
        curve_info (CurveInfo): CurveInfo
    """

    def __init__(self, vertices=None, curve_knots=None, # pylint: disable=too-many-arguments
                 is_periodic=False, order=4, curve_type=HDATA.CurveType.LINEAR):
        """Initialize

        Args:
            vertices (ndarray): Position of curve cvs, should be in 2D (vertices_count, 3)
            curve_knots (ndarray, optional): Knots of cvs. Defaults to None.
            order (int, optional): Order of curve. Defaults to 4.
            curve_type (CurveType, optional): Type of curve. \
                Defaults to HDATA.CurveType.LINEAR.
        """
        super(HGeoCurve, self).__init__()
        if isinstance(vertices, np.ndarray):
            self.point_count = vertices.shape[0]
            self.vertex_count = vertices.shape[0]
            self.face_count = 1
            self.curve_knots = curve_knots
            self.curve_count = np.repeat(vertices.shape[0], 1)

            self.part_info.type = HDATA.PartType.CURVE
            self.part_info.faceCount = self.face_count
            self.part_info.vertexCount = self.vertex_count
            self.part_info.pointCount = self.point_count

            self.curve_info = HDATA.CurveInfo()
            self.curve_info.curveType = curve_type
            self.curve_info.curveCount = 1
            self.curve_info.vertexCount = vertices.shape[0]
            self.curve_info.knotCount = (
                curve_knots.shape[0] if isinstance(curve_knots, np.ndarray) else 0)
            self.curve_info.isPeriodic = is_periodic
            self.curve_info.order = order
            self.curve_info.hasKnots = isinstance(curve_knots, np.ndarray)

            #self.AddPointAttrib("P", vertices)
            self.add_attrib(HDATA.AttributeOwner.POINT, "P", vertices)

    def commit_to_node(self, session, node_id):
        """Set this geo into hengine's node

        Args:
            session (int64): The session of Houdini you are interacting with.
            node_id (int): The node to add geo.
        """
        super().commit_to_node(session, node_id)

        HAPI.set_curve_info(session.hapi_session, node_id, self.curve_info)
        HAPI.set_curve_counts(session.hapi_session, node_id,\
            self.part_info.id, self.curve_count)
        HAPI.set_curve_knots(session.hapi_session, node_id,\
            self.part_info.id, self.curve_knots)

        HAPI.commit_geo(session.hapi_session, node_id)

    def extract_from_sop(self, session, part_info, node_id, part_id=0):
        """Extract curve from sop

        Args:
            session (int64): The session of Houdini you are interacting with.
            part_info (PartInfo): The info of part
            node_id (int): The node to add geo.
            part_id (int): Part id. Default to 0
        """
        super().extract_from_sop(session, part_info, node_id, part_id)
        self.curve_info = HAPI.get_curve_info(session.hapi_session, node_id, part_info.id)
        self.point_count = self.curve_info.vertexCount
        self.vertex_count = self.curve_info.vertexCount
        self.face_count = self.curve_info.curveCount
        self.curve_count = HAPI.get_curve_counts(session.hapi_session, node_id, \
            part_info.id, self.face_count)
        if self.curve_info.hasKnots:
            self.curve_knots = HAPI.get_curve_knots(session.hapi_session, node_id, \
                part_info.id, self.curve_info.knotCount)
