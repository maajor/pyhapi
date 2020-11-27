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
        self.parm_info = parm_info
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

    def set_value(self, value):
        raise NotImplementedError()

    def get_size(self):
        return self.size

class HParmFloat(HParm):

    def set_value(self, value, index=0):
        if isinstance(value, float) and index >=0 and index < self.size:
            HAPI.set_parm_float_value(\
                    self.session.hapi_session, self.node_id, self.name, float(value), index)
        elif (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==self.size:
            for i in range(0, self.size):
                HAPI.set_parm_float_value(\
                    self.session.hapi_session, self.node_id, self.name, float(value[i]), i)
        else:
            raise TypeError("Parameter to set is not float or list/ndarray of float")

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
        if isinstance(value, str) and index >=0 and index < self.size:
            HAPI.set_parm_string_value(\
                    self.session.hapi_session, self.node_id, self.name, value, index)
        elif (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==self.size:
            for i in range(0, self.size):
                HAPI.set_parm_string_value(\
                    self.session.hapi_session, self.node_id, self.name, value[i], i)
        else:
            raise TypeError("Parameter to set is not string or list/ndarray of string")

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
        if isinstance(value, int) and index >=0 and index < self.size:
            HAPI.set_parm_int_value(\
                    self.session.hapi_session, self.node_id, self.name, value, index)
        elif (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==self.size:
            for i in range(0, self.size):
                HAPI.set_parm_int_value(\
                    self.session.hapi_session, self.node_id, self.name, int(value[i]), i)
        else:
            raise TypeError("Parameter to set is not int or list/ndarray of int")

    def get_value(self):
        if self.size == 1:
            return HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, 0)
        else:
            values = []
            for index in range(self.size):
                values.append(HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, index))
            return values

class HParmNode(HParm):

    def set_value(self, value):
        #if value is not HNodeBase:
        #    raise TypeError("Parameter to set is not node")
        HAPI.set_parm_node_value(self.session.hapi_session, \
                    self.node_id, self.name, value.node_id)

    def get_value(self):
        return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.name, 0)

class HParmVector2(HParmFloat):
    pass
class HParmVector3(HParmFloat):
    pass
class HParmVector4(HParmFloat):
    pass
class HParmIntVector2(HParmInt):
    pass
class HParmIntVector3(HParmInt):
    pass
class HParmIntVector4(HParmInt):
    pass
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

class HParmChoice(HParm):
    
    def __init__(self, session, parm_info, node_id, param_choice_lists):
        super(HParmChoice, self).__init__(session, parm_info, node_id)
        choices = param_choice_lists[parm_info.id]
        self.choice_labels = []
        self.choice_values = []
        for choice in choices:
            self.choice_labels.append(HAPI.get_string(session.hapi_session, choice.labelSH))
            self.choice_values.append(HAPI.get_string(session.hapi_session, choice.valueSH))

    def get_choice_labels(self):
        return self.choice_labels

    def get_choice_values(self):
        return self.choice_values

class HParmIntChoice(HParmChoice):

    def __init__(self, session, parm_info, node_id, param_choice_lists):
        super(HParmIntChoice, self).__init__(session, parm_info, node_id, param_choice_lists)
        self.choice_values = list(range(0, parm_info.choiceCount))

    def set_value(self, index):
        if not isinstance(index, int):
            raise TypeError("Index to set is not int")
        if index < 0 or index >= len(self.choice_values):
            raise IndexError("Index should be between 0 and {0}".format(len(self.choice_values)))
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.name, int(self.choice_values[index]), 0)

    def get_value(self):
        return HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.name, 0)

class HParmStringChoice(HParmChoice):
    
    def __init__(self, session, parm_info, node_id, param_choice_lists):
        super(HParmStringChoice, self).__init__(session, parm_info, node_id, param_choice_lists)
        choices = param_choice_lists[parm_info.id]
        self.choice_values = []
        for choice in choices:
            self.choice_values.append(HAPI.get_string(session.hapi_session, choice.valueSH))

    def set_value(self, index):
        if not isinstance(index, int):
            raise TypeError("Index to set is not int")
        if index < 0 or index >= len(self.choice_values):
            raise IndexError("Index should be between 0 and {0}".format(len(self.choice_values)))
        HAPI.set_parm_string_value(self.session.hapi_session, \
                    self.node_id, self.name, self.choice_values[index], 0)

    def get_value(self):
        return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.name, 0)

class HParmLabel(HParm):

    def set_value(self):
        raise NotImplementedError("Do not set value for label")

    def get_value(self, value):
        raise NotImplementedError("Do not get value from label")


PARMTYPE_TO_HPARM = {
    HDATA.PrmScriptType.INT : HParmInt,
    HDATA.PrmScriptType.FLOAT : HParmFloat,
    # missing ANGLE
    HDATA.PrmScriptType.STRING : HParmString,
    HDATA.PrmScriptType.FILE : HParmFile,
    HDATA.PrmScriptType.IMAGE : HParmFileImage,
    HDATA.PrmScriptType.DIRECTORY : HParmFileDirectory,
    HDATA.PrmScriptType.GEOMETRY  : HParmFileGeometry,
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
    # HDATA.PrmScriptType.RAMP_FLT : HParmRampFloat,
    # HDATA.PrmScriptType.RAMP_RGB  : HParmRampColor,
    HDATA.PrmScriptType.LABEL : HParmLabel
}

class HParmFactory():

    def __init__(self, session, node_id):
        self.session = session
        self.node_id = node_id
        self.param_choice_lists = {}

        choice_lists = HAPI.get_parm_choice_lists(self.session.hapi_session, self.node_id)
        self.param_choice_lists.clear()
        for c in choice_lists:
            if c.parentParmId not in self.param_choice_lists:
                self.param_choice_lists[c.parentParmId] = []
            self.param_choice_lists[c.parentParmId].append(c)

    def get_parm(self, parm_info):
        if parm_info.is_non_value() or parm_info.type == HDATA.ParmType.FOLDERLIST:
            parm = None
        elif parm_info.scriptType is HDATA.PrmScriptType.TOGGLE: # toggle has choice count, check beforehand
            parm = HParmToggle(self.session, parm_info, self.node_id)
        elif parm_info.choiceCount > 0 and parm_info.is_int():
            parm = HParmIntChoice(self.session, parm_info, self.node_id, self.param_choice_lists)
        elif parm_info.choiceCount > 0 and parm_info.is_string():
            parm = HParmStringChoice(self.session, parm_info, self.node_id, self.param_choice_lists)
        elif parm_info.scriptType in PARMTYPE_TO_HPARM.keys():
            parm = PARMTYPE_TO_HPARM[parm_info.scriptType](self.session, parm_info, self.node_id)
        else:
            #parm = HParm(self.session, parm_info, self.node_id)
            parm = None
        return parm
