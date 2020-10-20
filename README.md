# pyhapi
[![Downloads](https://pepy.tech/badge/pyhapi)](https://pepy.tech/project/pyhapi)

Object-Oriented Python Wrapper for Houdini Engine's C API

# Documentation  

Please visit [pyhapi documentation](https://pyhapi.readthedocs.io).  

# Install  
## 1. setup PATH  
* For Windows  
PIP should automaticaly setup path, otherwise run ```powershell setpath.ps1```  
* For Linux  
Add ```/opt/hfs<version>/dsolib/``` to LD_LIBRARY_PATH  
Example:  
```export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/hfs17.5/dsolib/```  

## 2. install through PyPI  
```$ pip install pyhapi```

# Supported Platforms  
* Windows  
* Linux  

# Dependency  
* Python: >3.6  
* Numpy: >= 1.15 
* Houdini >= 17.5
  * License supported:
    * Houdini FX
    * Houdini Core
    * Houdini Engine
  * License NOT supported:
    * Houdini Engine Indie
    * Houdini Indie
    * Houdini Apprentice

# Features
* Instantiate node/HDA  
* Node connect operation  
* Node parameter get/set  
* Node async cooking   
* Marshall in/out curve  
* Marshall in/out mesh  
  
Following feature in Houdini Engine is NOT supported yet:  
* Marshall in/out volume  
* PDG execution

# Example Usage  

Please see documentation for detailed tutorial.  ****

## Create a session  
```
import pyhapi as ph
session = ph.HSessionManager.get_or_create_default_session()
```
See more in  
[Example: node_networks_operations](https://github.com/maajor/pyhapi/blob/master/examples/node_networks_operations.py) 

## Instantiate a HDA  
```
hda_asset = ph.HAsset(session, "hda/FourShapes.hda")
asset_node = hda_asset.instantiate(node_name="TestObject").cook()
```

## Set parameter of node  
```
asset_node.set_param_value("seed", 1.0)
asset_node.set_param_value("foo_attrib", "foo_str")
asset_node.press_button("foo_execute")
```
See more in  
[Example: hda_params_getset](https://github.com/maajor/pyhapi/blob/master/examples/hda_params_getset.py)  

## Save HIP file  
```
session.save_hip("debug.hip")
```

## Marshall data
see more in   
[Example: curve_marshall_input](https://github.com/maajor/pyhapi/blob/master/examples/curve_marshall_input.py)  
[Example: curve_marshall_output](https://github.com/maajor/pyhapi/blob/master/examples/curve_marshall_output.py)  
[Example: mesh_marshall_input](https://github.com/maajor/pyhapi/blob/master/examples/mesh_marshall_input.py)  
[Example: mesh_marshall_output](https://github.com/maajor/pyhapi/blob/master/examples/mesh_marshall_output.py)  
[Example: heightfield_marshal_input](https://github.com/maajor/pyhapi/blob/master/examples/heightfield_marshall_input.py)  
[Example: heightfield_marshal_output](https://github.com/maajor/pyhapi/blob/master/examples/heightfield_marshall_output.py)  

