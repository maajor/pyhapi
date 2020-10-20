# -*- coding: utf-8 -*-\
"""pyhapi
Author  : Maajor
Email   : info@ma-yidong.com
"""
from .hdata import *
from .hgeo import HGeo, HGeoMesh, HGeoCurve, HGeoHeightfield, HGeoInstancer
from .hsession import HSession, HSessionManager
from .hnode import HNode, HInputNode, HHeightfieldInputNode, HHeightfieldInputVolumeNode
from .hasset import HAsset
from . import hapi as HAPI

__version__ = "0.0.2b1"


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
        # MacOS is currently unsupported
        #   Because I dont know the lib name...
        return False

    return os.path.exists(os.path.join(libpath,libdll) )

def __ensure_hapi_path(libpath):
    path_env = os.environ['PATH'].split(';')
    if not libpath or __check_libpath(libpath):
        if not os.path.normpath(libpath) in [os.path.normpath(p) for p in path_env]:
            path_env.append(libpath)
            os.environ['PATH']=';'.join(path_env)
        return True
    else:
        return any([__check_libpath(p) for p in path_env])
            

__library_initialized__ = False

def Initialize(lib_path = "", default_root_path = "", pipe_name="hapi"):
    if not __library_initialized__:
        assert __ensure_hapi_path(lib_path), "libHAPIL not found"
        
        from . import hapi

        SYS = platform.system()
        if SYS == "Windows":
            hapi.HAPI_LIB = cdll.LoadLibrary("libHAPIL")
        elif SYS == "Linux":
            hapi.HAPI_LIB = cdll.LoadLibrary("libHAPIL.so")

        HSessionManager._rootpath = default_root_path
        if not pipe_name.strip():
            pipe_name="hapi"
        HSessionManager._pipe_name = pipe_name

        __initialized__ = True
    else:
        print("HAPI is already initialized.")
    
    return True