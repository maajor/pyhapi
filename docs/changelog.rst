Changelog
========================================

0.0.4b2
-----------------------

* Fix path cannot find bug on Linux

0.0.4b1
-----------------------

* Add HParmLogFloat and HParmLogInt to support log parm
* Add return exception support for HSessionPool

0.0.4b0
-----------------------

* Add HParm class, make parameters object-oriented. supporting get range, implememt basic types of params include
    * vec2, vec3, vec4, intvec2, intvec3, intvec4, color, coloralpha, choice, label, toggle
* Fix bug on getting string attributes


0.0.3b1
-----------------------

* Update HSessionPool to support threaded task producer
    * Add example to create flask houdini server
* Fix some bugs on setting parameter fail onto node

0.0.3b0
-----------------------

* Add HSessionPool to async process multiple tasks
    * Support consumer/producer pattern

0.0.2b2
-----------------------

* Support instancer geometry
* Support choice parm of assets
* Improve instantialize with message, pipename and root path

0.0.2b1
-----------------------

* Make async cook use new event loop

0.0.2b0
-----------------------

* Add HHeightfieldInputNode and HHeightfieldInputVolumeNode for marshall in/out heightfield

0.0.1b1
-----------------------

* Add load_hip method to HSession
* HExistingNode could get/set params

0.0.1b0
-----------------------
First beta release

Support features:  

* Instantiate node/HDA  
* Node connect operation  
* Node parameter get/set  
* Node async cooking   
* Marshall in/out curve  
* Marshall in/out mesh  
  
NOT supported yet:  

* Marshall in/out volume  
* PDG execution