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
    """A base class for houdini engine's parameter, including shared operation\
        for get name, label, range, size, etc.

    Attributes:
        session (HSession): HEngine session containing this node
        invisible (bool): invisible
        node_id (int): Current node id
        id (int): Current param name
    """

    def __init__(self, session, parm_info, node_id):
        """Init

        Args:
            session (HSession): HEngine session containing this node
            parm_info (ParmInfo): retrieved parm info of this parm
            node_id (int): node id containing this param
        """
        self.session = session
        self.node_id = node_id
        self.__parm_info = parm_info
        self.id = parm_info.id
        self.__name = HAPI.get_string(self.session.hapi_session, parm_info.nameSH)
        self.__label = HAPI.get_string(self.session.hapi_session, parm_info.labelSH)
        self.__hasMin = parm_info.hasMin
        self.__hasMax = parm_info.hasMax
        self.__invisible = parm_info.invisible
        self.__disabled = parm_info.disabled
        self.__min = parm_info.min
        self.__max = parm_info.max
        self.__size = parm_info.size

    @property
    def invisible(self):
        """Get invisible property of this parm

        Returns:
            Bool: invisible of parm
        """
        return self.__invisible

    def get_name(self):
        """Get name of this parm

        Returns:
            str: name of this parm
        """
        return self.__name

    def get_label(self):
        """Get label of this parm

        Returns:
            str: label of parm
        """
        return self.__label

    def has_range(self):
        """Get if has range in this parm

        Returns:
            [bool, bool]: if has min range or max range in this parm
        """
        return [self.__hasMin, self.__hasMax]

    def get_range(self):
        """Get range in this parm

        Returns:
            [float, float]: min anx max range of this parm
        """
        return [self.__min, self.__max]

    def get_value(self):
        """Get value in this parm

        Returns:
            depend on implement: value of this param
        """
        pass

    def set_value(self, value):
        """abstract method, set value for this param
        """
        pass

    def get_size(self):
        """Get size of this parm

        Returns:
            int: size of this parm
        """
        return self.__size

    def _check_range(self, value):
        """Check of a value is in valid range

        Args:
            value (int/float): value to check if meet valid range

        Returns:
            bool: if value is valid in range
        """
        min_valid = not self.__hasMin or (self.__hasMin and value >= self.__min)
        max_valid = not self.__hasMax or (self.__hasMax and value <= self.__max)
        if min_valid and max_valid:
            return True
        else:
            return False

class HParmFloat(HParm):
    """A class for houdini engine's float parameter
    """

    def set_value(self, value, index=0):
        """set value for this parameter

        Args:
            value (float/list/ndarray): value to set, if 'value' is a float, it will use index\
                to set corresponding tuple slot; if 'value' is a list or ndarray, it will fill every tuple slot\
                    of this parameter
            index (int, optional): tuple index to set if value is a float
        """
        if (isinstance(value, float) or isinstance(value, int)) and index >=0 and index < self.get_size():
            if not self._check_range(value):
                logging.warning("Trying to set {0} as {1}, it's outside of range {2}".format(self.get_name(), value, self.get_range()))
            HAPI.set_parm_float_value(\
                    self.session.hapi_session, self.node_id, self.get_name(), float(value), index)
        elif (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==self.get_size():
            for i in range(0, self.get_size()):
                if not self._check_range(float(value[i])):
                    logging.warning("Trying to set {0}.{1} as {2}, it's outside of range {3}".format(self.get_name(), i, value[i], self.get_range()))
                HAPI.set_parm_float_value(\
                    self.session.hapi_session, self.node_id, self.get_name(), float(value[i]), i)
        else:
            raise TypeError("Parameter to set is not float or list/ndarray of float")

    def get_value(self):
        """get value for this parameter

        Returns:
            float or list(float): current value of this parameter
        """
        if self.get_size() == 1:
            return HAPI.get_parm_float_value(self.session.hapi_session, self.node_id, self.get_name(), 0)
        else:
            values = []
            for index in range(self.get_size()):
                values.append(HAPI.get_parm_float_value(self.session.hapi_session, self.node_id, self.get_name(), index))
            return values

class HParmString(HParm):
    """A class for houdini engine's string parameter
    """

    def set_value(self, value, index=0):
        """set value for this parameter

        Args:
            value (float/list/ndarray): value to set, if 'value' is a str, it will use index\
                to set corresponding tuple slot; if 'value' is a list or ndarray, it will fill every tuple slot\
                    of this parameter
            index (int, optional): tuple index to set if value is a str
        """
        if isinstance(value, str) and index >=0 and index < self.get_size():
            HAPI.set_parm_string_value(\
                    self.session.hapi_session, self.node_id, self.id, value, index)
        elif (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==self.get_size():
            for i in range(0, self.get_size()):
                HAPI.set_parm_string_value(\
                    self.session.hapi_session, self.node_id, self.id, value[i], i)
        else:
            raise TypeError("Parameter to set is not string or list/ndarray of string")

    def get_value(self):
        """get value for this parameter

        Returns:
            str or list(str): current value of this parameter
        """
        if self.get_size() == 1:
            return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.get_name(), 0)
        else:
            values = []
            for index in range(self.get_size()):
                values.append(HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.get_name(), index))
            return values

class HParmInt(HParm):
    """A class for houdini engine's int parameter
    """

    def set_value(self, value, index=0):
        """set value for this parameter

        Args:
            value (float/list/ndarray): value to set, if 'value' is a int, it will use index\
                to set corresponding tuple slot; if 'value' is a list or ndarray, it will fill every tuple slot\
                    of this parameter
            index (int, optional): tuple index to set if value is a int
        """
        if (isinstance(value, float) or isinstance(value, int)) and index >=0 and index < self.get_size():
            if not self._check_range(value):
                logging.warning("Trying to set {0} as {1}, it's outside of range {2}".format(self.get_name(), value, self.get_range()))
            HAPI.set_parm_int_value(\
                    self.session.hapi_session, self.node_id, self.get_name(), int(value), index)
        elif (isinstance(value, list) or isinstance(value, np.ndarray)) and len(value)==self.get_size():
            for i in range(0, self.get_size()):
                if not self._check_range(int(value[i])):
                    logging.warning("Trying to set {0}.{1} as {2}, it's outside of range {3}".format(self.get_name(), i, value[i], self.get_range()))
                HAPI.set_parm_int_value(\
                    self.session.hapi_session, self.node_id, self.get_name(), int(value[i]), i)
        else:
            raise TypeError("Parameter to set is not int or list/ndarray of int")

    def get_value(self):
        """get value for this parameter

        Returns:
            int or list(int): current value of this parameter
        """
        if self.get_size() == 1:
            return HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.get_name(), 0)
        else:
            values = []
            for index in range(self.get_size()):
                values.append(HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.get_name(), index))
            return values

class HParmNode(HParm):
    """A class for houdini engine's node parameter
    """

    def set_value(self, value):
        """set value for this parameter

        Args:
            value (HNodeBase): value to set
        """
        #if value is not HNodeBase:
        #    raise TypeError("Parameter to set is not node")
        HAPI.set_parm_node_value(self.session.hapi_session, \
                    self.node_id, self.get_name(), value.node_id)

    def get_value(self):
        """get value for this parameter

        Returns:
            str: current value of this parameter
        """
        return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.get_name(), 0)

class HParmLogFloat(HParmFloat):
    """A class for houdini engine's vector2 parameter
    """
    pass
class HParmLogInt(HParmInt):
    """A class for houdini engine's vector2 parameter
    """
    pass
class HParmVector2(HParmFloat):
    """A class for houdini engine's vector2 parameter
    """
    pass
class HParmVector3(HParmFloat):
    """A class for houdini engine's vector3 parameter
    """
    pass
class HParmVector4(HParmFloat):
    """A class for houdini engine's vector4 parameter
    """
    pass
class HParmIntVector2(HParmInt):
    """A class for houdini engine's int vector2 parameter
    """
    pass
class HParmIntVector3(HParmInt):
    """A class for houdini engine's int vector3  parameter
    """
    pass
class HParmIntVector4(HParmInt):
    """A class for houdini engine's int vector4 parameter
    """
    pass
class HParmColor(HParmVector3):
    """A class for houdini engine's color parameter,\
        inherit HParmVector3 and behaviors like HParmVector3
    """
    pass
class HParmColorAlpha(HParmVector4):
    """A class for houdini engine's color alpha parameter,\
        inherit HParmVector4 and behaviors like HParmVector4
    """
    pass
class HParmFile(HParmString):
    """A class for houdini engine's file parameter,\
        inherit HParmString and behaviors like HParmString
    """
    pass
class HParmFileDirectory(HParmString):
    """A class for houdini engine's file directory parameter,\
        inherit HParmString and behaviors like HParmString
    """
    pass
class HParmFileGeometry(HParmString):
    """A class for houdini engine's file geometry parameter,\
        inherit HParmString and behaviors like HParmString
    """
    pass
class HParmFileImage(HParmString):
    """A class for houdini engine's file image parameter,\
        inherit HParmString and behaviors like HParmString
    """
    pass
class HParmRampFloat(HParm):
    """A class for houdini engine's ramp float parameter, not implemented
    """
    pass
class HParmRampColor(HParm):
    """A class for houdini engine's ramp color parameter, not implemented
    """
    pass

class HParmButton(HParm):
    """A class for houdini engine's button parameter
    """

    def press(self, status_report_interval=5.0, status_verbosity=HDATA.StatusVerbosity.ALL):
        """Press button in sync/blocking manner

        Args:
            param_name (str): Button name to press
            status_report_interval (float): Time interval \
                in seconds to report status
        """
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, self.get_name(), 1)
        HAPI.wait_cook(self.session.hapi_session, status_report_interval, status_verbosity)
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, self.get_name(), 0)

    async def press_async(self, status_report_interval=5.0, status_verbosity=HDATA.StatusVerbosity.ALL):
        """Press button in async/non-blocking manner

        Args:
            param_name (str): Button name to press
            status_report_interval (float): Time interval \
                in seconds to report status
        """
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, self.get_name(), 1)
        await HAPI.wait_cook_async(self.session.hapi_session, status_report_interval, status_verbosity)
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, self.get_name(), 0)

    def set_value(self, value):
        """set value for this parameter, it will log a error as button has no value

        Args:
            value (): value to set
        """
        logging.error("Cannot set value to a button {0}, please use press() or press_async() methods".format(self.get_name()))

    def get_value(self):
        """get value for this parameter, it will log a error as button has no value
        """
        logging.error("Cannot get value of a button {0}".format(self.get_name()))

class HParmToggle(HParm):
    """A class for houdini engine's toggle parameter
    """

    def set_value(self, value):
        """set value for this parameter

        Args:
            value (HNodeBase): value to set
        """
        if (not isinstance(value, int)) and (not isinstance(value, bool)):
            raise TypeError("Parameter to set is not int")
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.get_name(), int(value), 0)

    def get_value(self):
        """get value for this parameter

        Returns:
            bool: current value of this parameter
        """
        val = HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.get_name(), 0)
        return True if val == 1 else False

class HParmChoice(HParm):
    """A class for houdini engine's choice parameter
    """
    
    def __init__(self, session, parm_info, node_id, param_choice_lists):
        super(HParmChoice, self).__init__(session, parm_info, node_id)
        choices = param_choice_lists[parm_info.id]
        self.choice_labels = []
        self.choice_values = []
        for choice in choices:
            self.choice_labels.append(HAPI.get_string(session.hapi_session, choice.labelSH))

    def get_choice_labels(self):
        """get value for this parameter

        Returns:
            list(str): choice's correspoinding labels
        """
        return self.choice_labels

    def get_choice_values(self):
        """get value for this parameter

        Returns:
           list(int/str): choice's correspoinding values
        """
        return self.choice_values

class HParmIntChoice(HParmChoice):
    """A class for houdini engine's int choice parameter
    """

    def __init__(self, session, parm_info, node_id, param_choice_lists):
        super(HParmIntChoice, self).__init__(session, parm_info, node_id, param_choice_lists)
        self.choice_values = list(range(0, parm_info.choiceCount))

    def set_value(self, index):
        """set value for this parameter

        Args:
            value (int): choice index to set
        """
        if not isinstance(index, int):
            raise TypeError("Index to set is not int")
        if index < 0 or index >= len(self.choice_values):
            raise IndexError("Index should be between 0 and {0}".format(len(self.choice_values)))
        HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, self.get_name(), int(self.choice_values[index]), 0)

    def get_value(self):
        """get value for this parameter

        Returns:
            int: current value of this parameter
        """
        return HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, self.get_name(), 0)

class HParmStringChoice(HParmChoice):
    """A class for houdini engine's string choice parameter
    """

    def __init__(self, session, parm_info, node_id, param_choice_lists):
        super(HParmStringChoice, self).__init__(session, parm_info, node_id, param_choice_lists)
        choices = param_choice_lists[parm_info.id]
        for choice in choices:
            self.choice_values.append(HAPI.get_string(session.hapi_session, choice.valueSH))

    def set_value(self, index):
        """set value for this parameter

        Args:
            index (int): choice index to set
        """
        if not isinstance(index, int):
            raise TypeError("Index to set is not int")
        if index < 0 or index >= len(self.choice_values):
            raise IndexError("Index should be between 0 and {0}".format(len(self.choice_values)))
        HAPI.set_parm_string_value(self.session.hapi_session, \
                    self.node_id, self.get_name(), self.choice_values[index], 0)

    def get_value(self):
        """get value for this parameter

        Returns:
            str: current value of this parameter
        """
        return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, self.get_name(), 0)

class HParmLabel(HParm):
    """A class for houdini engine's label choice parameter
    """

    def set_value(self, value):
        """set value for this parameter, will raise error

        Args:
            value (): value to set
        """
        raise NotImplementedError("Do not set value for label")

    def get_value(self):
        """get value for this parameter, will raise error
        """
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
    HDATA.PrmScriptType.LABEL : HParmLabel,
    HDATA.PrmScriptType.FLOAT_LOG : HParmLogFloat,
    HDATA.PrmScriptType.INT_LOG : HParmLogInt
}

class HParmFactory():
    """A class to create HParm according to ParmInfo
    """

    def __init__(self, session, node_id):
        """set value for this parameter

        Args:
            session (HSession): session of this node
            node_id (int) : id of this node
        """
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
        """Create a HParm from info

        Args:
            parm_info (ParmInfo): parm info of this parm

        Returns:
            HParm: parm class of this parm
        """
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
