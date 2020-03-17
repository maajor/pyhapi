# -*- coding: utf-8 -*-
"""Example of setting mesh data into hengine
Author  : Maajor
Email   : info@ma-yidong.com
"""
import numpy as np
import pyhapi as ph

def main():
    """Main
    """
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

    #create a node whose input is inputnode
    ph.HNode(session, "Sop/subdivide", "Cube Subdivider").connect_node_input(geo_inputnode)

    session.save_hip()

if __name__ == "__main__":
    main()
