Install
==========

pyhapi depends on:

- Python: >3.6  
- Numpy: >= 1.15 
- Houdini: 17.5
    - License supported:
        - Houdini FX
        - Houdini Core
        - Houdini Engine
    - License NOT supported:
        - Houdini Engine Indie
        - Houdini Indie
        - Houdini Apprentice

The recommended method of installation is using pip_.

.. code-block:: shell

   pip install pyhapi

Also you need to setup houdini engine's path

Linux
----------------------
Add */opt/hfs<version>/dsolib/* to *LD_LIBRARY_PATH* 

Example:

.. code-block:: shell

   export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/hfs17.5/dsolib/


Windows
----------------------

You could run batch file https://github.com/maajor/pyhapi/blob/master/sethoupath.ps1 

or  

Add *C:/Program Files/Side Effects Software/Houdini <version>/custom/houdini/dsolib* and *C:/Program Files/Side Effects Software/Houdini <version>/bin*  to Environment Path  

.. _Python: https://www.python.org/
.. _pip: https://pip.pypa.io/