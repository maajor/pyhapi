# -*- coding: utf-8 -*-
"""Test for creating and operations with hengine nodes
Author  : Maajor
Email   : hello_myd@126.com
"""
import numpy as np

import pyhapi as ph

def test_create_input_node_and_set_curve(init_session):
    """Create input node and marshall in curve
    """
    geo_inputnode = ph.HInputNode(init_session, "Curve")
    curve_geo = ph.HGeoCurve(
        vertices=np.array(
            [[-4.0, 0.0, 4.0],
             [-4.0, 0.0, -4.0],
             [4.0, 0.0, -4.0],
             [4.0, 0.0, 4.0]], dtype=np.float32),
        curve_knots=np.array(
            [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32),
        curve_type=ph.CurveType.NURBS)
    geo_inputnode.set_geometry(curve_geo)
    assert geo_inputnode is not None


def test_create_input_node_and_set_mesh(init_session):
    """Create input node and marshall in mesh
    """
    geo_inputnode = ph.HInputNode(init_session, "Cube")
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
    geo_inputnode.set_geometry(cube_geo)
    assert geo_inputnode is not None

def test_connect_nodes(init_session):
    """Test connect nodes
    """
    geo_inputnode = ph.HInputNode(init_session, "Cube")
    subdnode = ph.HNode(init_session, "Sop/subdivide", "Cube Subdivider").\
        connect_node_input(geo_inputnode)
    assert subdnode is not None

def test_init_hasset(init_session):
    """Test instantiate HDA asset
    """
    hda_asset = ph.HAsset(init_session, "hda/FourShapes.hda")
    asset_node = hda_asset.instantiate(node_name="Processor").cook()
    assert asset_node is not None

def test_child_nodes(init_session):
    """Test get child nodes
    """
    hda_asset = ph.HAsset(init_session, "hda/FourShapes.hda")
    asset_node = hda_asset.instantiate(node_name="Processor").cook()
    child_nodes = asset_node.get_child_nodes()
    assert len(child_nodes) == 4

def test_get_node_geo(init_session):
    """Test get node geo
    """
    hda_asset = ph.HAsset(init_session, "hda/FourShapes.hda")
    asset_node = hda_asset.instantiate(node_name="TestObject").cook()
    asset_geos = asset_node.get_display_geos()
    _ps = asset_geos[0].get_attrib_data(ph.AttributeOwner.POINT, "P")
    _x, _y = _ps.shape
    assert _x == 8 and _y == 3
