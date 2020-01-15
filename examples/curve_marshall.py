import pyhapi as ph
import numpy as np

def main():
    session = ph.HSessionManager.GetOrCreateDefaultSession()

    #create an inputnode where you can set geometry
    geo_inputnode = ph.HInputNode(session, "Curve")

    #create a geocurve
    curve_geo = ph.HGeoCurve(
        vertices = np.array(
            [[-4.0, 0.0,  4.0],
             [-4.0, 0.0, -4.0],
             [ 4.0, 0.0, -4.0],
             [ 4.0, 0.0,  4.0]], dtype = np.float32),
        curve_knots = np.array(
            [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0], dtype = np.float32),
        curve_type = ph.HAPI_CurveType.HAPI_CURVETYPE_NURBS)

    #set this geocurve as geometry of inputnode
    geo_inputnode.SetGeometry(curve_geo)

    session.SaveHIP()
    
if __name__ == "__main__":
    main()