# pyhapi
Object-Oriented Python Wrapper for Houdini Engine's C API

# Install  
```$pip install pyhapi```

# Example Usage  

1. To create a session  
```
import pyhapi as ph
session = ph.HSessionManager.get_or_create_default_session()
```
See more in ```/examples/node_networks_operations.py```  

2. To instantiate a HDA  
```
hda_asset = ph.HAsset(session, "hda/FourShapes.hda")
asset_node = hda_asset.instantiate(node_name="TestObject").cook()
```

3. To set parameter of node  
```
asset_node.set_param_value("seed", 1.0)
asset_node.set_param_value("foo_attrib", "foo_str")
asset_node.press_button("foo_execute")
```
See more in ```/examples/hda_params_getset.py``` 

4. To input a mesh
```
geo_inputnode = ph.HInputNode(session, "Cube")

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
```
See more in   
```/examples/mesh_marshall_input.py```  
```/examples/mesh_marshall_output.py```  
```/examples/curve_marshall_input.py```  
```/examples/curve_marshall_output.py```  

5. To save HIP file  
```
session.save_hip("debug.hip")
```

# Supported Platforms  
* Windows  
* Linux  

# Dependency  
* Python: >3.6  
* Numpy: >= 1.15 
* Houdini: 17.5, license supported:
  * Houdini FX
  * Houdini Core
  * Houdini Engine


