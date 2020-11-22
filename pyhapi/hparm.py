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

class HParm():

    def __init__(self, session, parm_info, node_id):
        self.session = session
        self.node_id = node_id
        self.id = parm_info.id
        self.name = HAPI.get_string(self.session.hapi_session, parm_info.nameSH)
        self.label = HAPI.get_string(self.session.hapi_session, parm_info.labelSH)
        self.hasMin = parm_info.hasMin
        self.hasMax = parm_info.hasMax
        self.__invisible = parm_info.invisible
        self.disabled = parm_info.disabled
        self.min = parm_info.min
        self.max = parm_info.max
        self.size = parm_info.size

    @property
    def invisible(self):
        return self.__invisible

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

    def get_size(self):
        return self.size

class HParmFloat(HParm):

    def set_value(self, value, index=0):
        if value is not float:
            raise TypeError()
        HAPI.set_parm_float_value(\
                    self.session.hapi_session, self.node_id, self.name, float(value), index)

    def get_value(self):
        if self.size == 1:
            return HAPI.get_parm_float_value(self.session.hapi_session, self.node_id, self.name, 0)
        else:
            values = []
            for index in range(self.size):
                values.append(HAPI.get_parm_float_value(self.session.hapi_session, self.node_id, self.name, index))
            return values

class HParmString(HParm):

    def set_value(self, value, index=0):
        if value is not str:
            raise TypeError("Parameter to set is not string")
        HAPI.set_parm_string_value(self.session.hapi_session, \
                    self.node_id, self.id, value, 0)

    def get_value(self):
        if self.size == 1:
            return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.name, 0)
        else:
            values = []
            for index in range(self.size):
                values.append(HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.name, index))
            return values

class HParmInt(HParm):

    def set_value(self, value, index=0):
        if value is not int:
            raise TypeError("Parameter to set is not int")
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.name, int(value), index)

    def get_value(self):
        if self.size == 1:
            return HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, 0)
        else:
            values = []
            for index in range(self.size):
                values.append(HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, index))
            return values

class HParmNode(HParmString):

    def set_value(self, value):
        #if value is not HNodeBase:
        #    raise TypeError("Parameter to set is not node")
        HAPI.set_parm_node_value(self.session.hapi_session, \
                    self.node_id, self.name, value.node_id)

    def get_value(self):
        return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.name, 0)

class HParmVector2(HParm):

    def set_value(self, value):
        valid = (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==2
        if not valid:
            raise TypeError("Parameter to set need to be list or ndarray of length 2")
        HAPI.set_parm_float_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[0]), 0)
        HAPI.set_parm_float_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[1]), 1)

    def get_value(self):
        values = []
        for index in range(2):
            values.append(HAPI.get_parm_float_value(self.session.hapi_session, self.node_id, self.name, index))
        return values

class HParmVector3(HParm):

    def set_value(self, value):
        valid = (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==3
        if not valid:
            raise TypeError("Parameter to set need to be list or ndarray of length 3")
        HAPI.set_parm_float_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[0]), 0)
        HAPI.set_parm_float_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[1]), 1)
        HAPI.set_parm_float_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[2]), 2)

    def get_value(self):
        values = []
        for index in range(3):
            values.append(HAPI.get_parm_float_value(self.session.hapi_session, self.node_id, self.name, index))
        return values

class HParmVector4(HParm):

    def set_value(self, value):
        valid = (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==4
        if not valid:
            raise TypeError("Parameter to set need to be list or ndarray of length 4")
        HAPI.set_parm_float_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[0]), 0)
        HAPI.set_parm_float_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[1]), 1)
        HAPI.set_parm_float_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[2]), 2)
        HAPI.set_parm_float_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[3]), 3)

    def get_value(self):
        values = []
        for index in range(4):
            values.append(HAPI.get_parm_float_value(self.session.hapi_session, self.node_id, self.name, index))
        return values
        
class HParmIntVector2(HParm):
    
    def set_value(self, value):
        valid = (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==4
        if not valid:
            raise TypeError("Parameter to set need to be list or ndarray of length 4")
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.id, int(value[0]), 0)
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.id, int(value[1]), 1)

    def get_value(self):
        values = []
        for index in range(2):
            values.append(HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, index))
        return values

class HParmIntVector3(HParm):
    
    def set_value(self, value):
        valid = (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==4
        if not valid:
            raise TypeError("Parameter to set need to be list or ndarray of length 4")
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[0]), 0)
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[1]), 1)
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[2]), 2)

    def get_value(self):
        values = []
        for index in range(3):
            values.append(HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, index))
        return values

class HParmIntVector4(HParm):
    
    def set_value(self, value):
        valid = (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==4
        if not valid:
            raise TypeError("Parameter to set need to be list or ndarray of length 4")
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[0]), 0)
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[1]), 1)
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[2]), 2)
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.id, float(value[3]), 3)

    def get_value(self):
        values = []
        for index in range(4):
            values.append(HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, index))
        return values

class HParmColor(HParmVector3):
    pass
class HParmColorAlpha(HParmVector4):
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

class HParmButton(HParm):

    def press(self, status_report_interval=5.0, status_verbosity=HDATA.StatusVerbosity.ALL):
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, self.name, 1)
        HAPI.wait_cook(self.session.hapi_session, status_report_interval, status_verbosity)
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, self.name, 0)

    async def press_async(self, status_report_interval=5.0, status_verbosity=HDATA.StatusVerbosity.ALL):
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, self.name, 1)
        await HAPI.wait_cook_async(self.session.hapi_session, status_report_interval, status_verbosity)
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, self.name, 0)

class HParmToggle(HParm):

    def set_value(self, value):
        if (value is not int) and (value is not bool):
            raise TypeError("Parameter to set is not int")
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.name, int(value), 0)

    def get_value(self):
        val = HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, 0)
        return True if val == 1 else False

class HParmChoice(HParmInt):
    pass

class HParmIntChoice(HParmInt):
    pass

class HParmStringChoice(HParmString):
    pass

PARMTYPE_TO_HPARM = {
    HDATA.PrmScriptType.INT : HParmInt,
    HDATA.PrmScriptType.FLOAT : HParmFloat,
    # missing ANGLE
    HDATA.PrmScriptType.STRING : HParmString,
    HDATA.PrmScriptType.FILE : HParmFile,
    HDATA.PrmScriptType.IMAGE : HParmFileImage,
    HDATA.PrmScriptType.DIRECTORY : HParmFileImage,
    HDATA.PrmScriptType.GEOMETRY  : HParmFileDirectory,
    HDATA.PrmScriptType.TOGGLE : HParmToggle,
    HDATA.PrmScriptType.BUTTON : HParmButton,
    HDATA.PrmScriptType.VECTOR2 : HParmVector2,
    HDATA.PrmScriptType.VECTOR3 : HParmVector3,
    HDATA.PrmScriptType.VECTOR4 : HParmVector4,
    HDATA.PrmScriptType.INTVECTOR2 : HParmIntVector2,
    HDATA.PrmScriptType.INTVECTOR3 : HParmIntVector3,
    HDATA.PrmScriptType.INTVECTOR4 : HParmIntVector4,
    # missing UV, UVW, DIR
    HDATA.PrmScriptType.COLOR : HParmColor,
    HDATA.PrmScriptType.COLOR4 : HParmColorAlpha,
    HDATA.PrmScriptType.OPPATH  : HParmNode,
    # missing OPLIST, OBJECT ...etc
    HDATA.PrmScriptType.RAMP_FLT : HParmRampFloat,
    HDATA.PrmScriptType.RAMP_RGB  : HParmRampColor,
}

class HParmFactory():

    def __init__(self, session, node_id):
        self.session = session
        self.node_id = node_id

    def get_parm(self, parm_info):
        if parm_info.choiceCount > 0 and parm_info.is_int():
            parm = HParmIntChoice(self.session, parm_info, self.node_id)
        elif parm_info.choiceCount > 0 and parm_info.is_string():
            parm = HParmStringChoice(self.session, parm_info, self.node_id)
        elif parm_info.scriptType in PARMTYPE_TO_HPARM.keys():
            parm = PARMTYPE_TO_HPARM[parm_info.scriptType](self.session, parm_info, self.node_id)
        elif parm_info.is_non_value():
            parm = None
        else:
            #parm = HParm(self.session, parm_info, self.node_id)
            parm = None
        return parm
