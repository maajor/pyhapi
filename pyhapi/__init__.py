# -*- coding: utf-8 -*-\
"""pyhapi
Author  : Maajor
Email   : info@ma-yidong.com
"""
import logging
from .hdata import *
from .hgeo import HGeo, HGeoMesh, HGeoCurve, HGeoHeightfield, HGeoInstancer
from .hsession import HSession, HSessionManager, HSessionPool, HSessionTask
from .hnode import HNode, HInputNode, HHeightfieldInputNode, HHeightfieldInputVolumeNode
from .hasset import HAsset
from . import hapi as HAPI

__version__ = "0.0.3b1"


import platform
import os
from ctypes import cdll

def __check_libpath(libpath):
    if not (os.path.exists(libpath) and os.path.isdir(libpath)):
        return False
    
    sys_platform = platform.system()
    libdll = None
    if sys_platform == "Windows":
        libdll = "libHAPIL.dll"
    elif sys_platform == "Linux":
        libdll = "libHAPIL.so"
    else:
        libdll = "libHAPIL.dylib"

    return os.path.exists(os.path.join(libpath,libdll) )

def __ensure_hapi_path(libpath):
    path_env = os.environ['PATH'].split(';')
    if libpath or __check_libpath(libpath):
        print(not libpath)
        if not os.path.normpath(libpath) in [os.path.normpath(p) for p in path_env]:
            path_env.append(libpath)
            os.environ['PATH']=';'.join(path_env)
        return True
    else:
        return any([__check_libpath(p) for p in path_env])

# ensure "import pyhapi" will not give error even cannot find libHAPIL
# call HSessionManager.get_or_create_default_session() to initialize, make it free of calling Initialize function
__library_initialized__ = False
if __ensure_hapi_path(""):
    from . import hapi
    SYS = platform.system()
    if SYS == "Windows":
        hapi.HAPI_LIB = cdll.LoadLibrary("libHAPIL")
    elif SYS == "Linux":
        hapi.HAPI_LIB = cdll.LoadLibrary("libHAPIL.so")
    elif SYS == "Darwin":
        hapi.HAPI_LIB = cdll.LoadLibrary("libHAPIL.dylib")

    __library_initialized__ = True
    print("HAPI Found")
else:
    print("HAPI Not Found")
