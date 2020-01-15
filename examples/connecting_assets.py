import pyhapi as ph
import numpy as np

def main():
    session = ph.HSessionManager.GetOrCreateDefaultSession()

    #create an inputnode where you can set geometry
    geo_inputnode = ph.HInputNode(session, "Cube")

    #create a geomesh
    cube_geo = ph.HGeoMesh(
        vertices = np.array(
            [[ 0.0, 0.0, 0.0], 
             [ 0.0, 0.0, 1.0],  
             [ 0.0, 1.0, 0.0], 
             [ 0.0, 1.0, 1.0],  
             [ 1.0, 0.0, 0.0],  
             [ 1.0, 0.0, 1.0],  
             [ 1.0, 1.0, 0.0], 
             [ 1.0, 1.0, 1.0]], dtype = np.float32),
        has_knot = True
        faces = np.array(
            [[ 0, 2, 6, 4],
             [ 2, 3, 7, 6],
             [ 2, 0, 1, 3],
             [ 1, 5, 7, 3],
             [ 5, 4, 6, 7],
             [ 0, 4, 5, 1]], dtype = np.int32))

    #set this geomesh as geometry of inputnode
    geo_inputnode.SetGeometry(cube_geo)

    #create a subd node whose input is inputnode
    sub_node = ph.HNode(session,  "Sop/subdivide", "Cube Subdivider").ConnectNodeInput(geo_inputnode)

    session.SaveHIP()
    
if __name__ == "__main__":
    main()