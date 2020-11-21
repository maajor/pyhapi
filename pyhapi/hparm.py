# -*- coding: utf-8 -*-
"""Wrapper for houdini engine's parameter.
Author  : Maajor
Email   : info@ma-yidong.com

"""
import numpy as np
import logging
import functools
import operator
from ctypes import c_float

from . import hdata as HDATA
from . import hapi as HAPI
from .hnode import HNodeBase

class HParm():

    def __init__(self, session, parm_info, node_id):
        self.session = session
        self.node_id = node_id
        self.id = parm_info.id
        self.name = HAPI.get_string(self.session.hapi_session, parm_info.nameSH)
        self.label = HAPI.get_string(self.session.hapi_session, parm_info.labelSH)
        self.hasMin = parm_info.hasMin
        self.hasMax = parm_info.hasMax
        self.invisible = parm_info.invisible
        self.disabled = parm_info.disabled
        self.min = parm_info.min
        self.max = parm_info.max

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label

    def has_range(self):
        return [self.hasMin, self.hasMax]

    def get_range(self):
        return [self.min, self.max]

    def get_value(self):
        raise NotImplementedError()

    def set_value(self):
        raise NotImplementedError()

class HParmFloat(HParm):

    def get_size(self):
        pass

    def set_value(self, value):
        if value is not float:
            raise TypeError()
        HAPI.set_parm_float_value(\
                    self.session.hapi_session, self.node_id, self.name, float(value), tupleid)

    def get_value(self):
        return HAPI.get_parm_float_value(self.session.hapi_session, self.node_id, self.name, 0)

class HParmString(HParm):

    def set_value(self, value):
        if value is not str:
            raise TypeError("Parameter to set is not string")
        HAPI.set_parm_string_value(self.session.hapi_session, \
                    self.node_id, self.id, value, 0)

    def get_value(self):
        return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.name, 0)

class HParmInt(HParm):

    def get_size(self):
        pass

    def set_value(self, value):
        if value is not int:
            raise TypeError("Parameter to set is not int")
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.name, int(value), 0)

    def get_value(self):
        return HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, 0)

class HParmNode(HParmString):

    def set_value(self, value):
        if value is not HNodeBase:
            raise TypeError("Parameter to set is not node")
        HAPI.set_parm_node_value(self.session.hapi_session, \
                    self.node_id, self.name, value.node_id)

    def get_value(self):
        return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.name, 0)

class HParmVector2(HParm):
    pass
class HParmVector3(HParm):
    pass
class HParmVector4(HParm):
    pass
class HParmIntVector2(HParm):
    pass
class HParmIntVector3(HParm):
    pass
class HParmIntVector4(HParm):
    pass
class HParmColor(HParm):
    pass
class HParmColorAlpha(HParm):
    pass
class HParmFile(HParmString):
    pass
class HParmFileDirectory(HParmString):
    pass
class HParmFileGeometry(HParmString):
    pass
class HParmFileImage(HParmString):
    pass
class HParmRampFloat(HParm):
    pass
class HParmRampColor(HParm):
    pass
class HParmButton(HParmInt):
    pass
class HParmToggle(HParmInt):
    pass
class HParmOrderedMenu(HParmInt):
    pass

PARM_TYPE_TO_HPARM = {
    HDATA.ParmType.INT : HParmInt,
    HDATA.ParmType.TOGGLE : HParmToggle,
    HDATA.ParmType.BUTTON : HParmButton,
    HDATA.ParmType.FLOAT : HParmFloat,
    HDATA.ParmType.COLOR : HParmColor,
    HDATA.ParmType.STRING : HParmString,
    HDATA.ParmType.PATH_FILE : HParmFile,
    HDATA.ParmType.PATH_FILE_GEO  : HParmFileGeometry,
    HDATA.ParmType.PATH_FILE_IMAGE : HParmFileImage,
    HDATA.ParmType.NODE  : HParmNode
}

class HParmFactory():

    def __init__(self, session, node_id):
        self.session = session
        self.node_id = node_id

    def get_parm(self, parm_info):
        if parm_info.choiceCount > 0:
            parm = HParmOrderedMenu(self.session, parm_info, self.node_id)
        elif parm_info.type in PARM_TYPE_TO_HPARM:
            parm = PARM_TYPE_TO_HPARM[parm_info.type](self.session, parm_info, self.node_id)
        else:
            parm = HParm(self.session, parm_info, self.node_id)
        return parm
