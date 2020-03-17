# -*- coding: utf-8 -*-
"""Example of setting curve data into hengine
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
    geo_inputnode = ph.HInputNode(session, "Curve")

    #create a geocurve
    curve_geo = ph.HGeoCurve(
        vertices=np.array(
            [[-4.0, 0.0, 4.0],
             [-4.0, 0.0, -4.0],
             [4.0, 0.0, -4.0],
             [4.0, 0.0, 4.0]], dtype=np.float32),
        curve_knots=np.array(
            [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32),
        curve_type=ph.CurveType.NURBS)

    #set this geocurve as geometry of inputnode
    geo_inputnode.set_geometry(curve_geo)

    session.save_hip()

if __name__ == "__main__":
    main()
