# -*- coding: utf-8 -*-
"""Houdini Engine's internal data types
Author  : Maajor
Email   : info@ma-yidong.com
"""
from ctypes import Structure, Array,\
    c_int, c_int32, c_int64, c_float, c_bool
import enum
import numpy as np

class StructureWithEnums(Structure):
    """Add missing enum feature to ctypes Structures.
    ref:  https://gist.github.com/christoph2/9c390e5c094796903097
    """
    _map = {}

    def __getattribute__(self, name):
        _map = Structure.__getattribute__(self, '_map')
        value = Structure.__getattribute__(self, name)
        if name in _map:
            enum_class = _map[name]
            if isinstance(value, Array):
                return [enum_class(x) for x in value]
            return enum_class(value)
        return value

    def __str__(self):
        result = []
        result.append("struct {0} {{".format(self.__class__.__name__))
        for field in self._fields_:
            attr, attr_type = field
            if attr in self._map:
                attr_type = self._map[attr]
            value = getattr(self, attr)
            result.append("    {0} [{1}] = {2!r}".format(
                attr, attr_type.__name__, value))
        result.append("}")
        return '\n'.join(result)

    __repr__ = __str__


class LicenseType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_License
    """
    NONE = 0
    HOUDINI_ENGINE = 1
    HOUDINI = 2
    HOUDINI_FX = 3
    HOUDINI_ENGINE_INDIE = 4
    HOUDINI_INDIE = 5
    MAX = 6


class StatusType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_StatusType
    """
    CALL_RESULT = 0
    COOK_RESULT = 1
    COOK_STATE = 2
    MAX = 3


class StatusVerbosity(enum.IntEnum):
    """Equivalent of HAPI's HAPI_StatusVerbosity
    """
    ALL = 2
    ERRORS = 0
    WARNINGS = 1
    MESSAGES = 2


class Result(enum.IntEnum):
    """Equivalent of HAPI's HAPI_Result
    """
    SUCCESS = 0
    FAILURE = 1
    ALREADY_INITIALIZED = 2
    NOT_INITIALIZED = 3
    CANT_LOADFILE = 4
    PARM_SET_FAILED = 5
    INVALID_ARGUMENT = 6
    CANT_LOAD_GEO = 7
    CANT_GENERATE_PRESET = 8
    CANT_LOAD_PRESET = 9
    ASSET_DEF_ALREADY_LOADED = 10

    NO_LICENSE_FOUND = 110
    DISALLOWED_NC_LICENSE_FOUND = 120
    DISALLOWED_NC_ASSET_WITH_C_LICENSE = 130
    DISALLOWED_NC_ASSET_WITH_LC_LICENSE = 140
    DISALLOWED_LC_ASSET_WITH_C_LICENSE = 150
    DISALLOWED_HENGINEINDIE_W_3PARTY_PLUGIN = 160

    ASSET_INVALID = 200
    NODE_INVALID = 210

    USER_INTERRUPTED = 300

    INVALID_SESSION = 400


class ErrorCode(enum.IntEnum):
    """Equivalent of HAPI's HAPI_ErrorCode
    """
    ASSET_DEF_NOT_FOUND = 1 << 0
    PYTHON_NODE_ERROR = 1 << 1


class SessionType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_SessionType
    """
    INPROCESS = 0
    THRIFT = 1
    CUSTOM1 = 2
    CUSTOM2 = 3
    CUSTOM3 = 4
    MAX = 5


class State(enum.IntEnum):
    """Equivalent of HAPI's HAPI_State
    """
    READY = 0
    READY_WITH_FATAL_ERRORS = 1
    READY_WITH_COOK_ERRORS = 2
    STARTING_COOK = 3
    COOKING = 4
    STARTING_LOAD = 5
    LOADING = 6
    MAX = 7

    MAX_READY_STATE = READY_WITH_COOK_ERRORS


class PackedPrimInstancingMode(enum.IntEnum):
    """Equivalent of HAPI's HAPI_PackedPrimInstancingMode
    """
    INVALID = -1
    DISABLED = 0
    HIERARCHY = 1
    FLAT = 2
    MAX = 3


class Permissions(enum.IntEnum):
    """Equivalent of HAPI's HAPI_Permissions
    """
    NON_APPLICABLE = 0
    READ_WRITE = 1
    READ_ONLY = 2
    WRITE_ONLY = 3
    MAX = 4


class RampType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_RampType
    """
    INVALID = -1
    FLOAT = 0
    COLOR = 1
    MAX = 2


class ParmType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_ParmType
    """
    INT = 0
    MULTIPARMLIST = 1
    TOGGLE = 2
    BUTTON = 3

    FLOAT = 4
    COLOR = 5

    STRING = 6
    PATH_FILE = 7
    PATH_FILE_GEO = 8
    PATH_FILE_IMAGE = 9

    NODE = 10

    FOLDERLIST = 11
    FOLDERLIST_RADIO = 12

    FOLDER = 13
    LABEL = 14
    SEPARATOR = 15
    PATH_FILE_DIR = 16

    MAX = 17

    INT_START = INT
    INT_END = BUTTON

    FLOAT_START = FLOAT
    FLOAT_END = COLOR

    STRING_START = STRING
    STRING_END = NODE

    PATH_START = PATH_FILE
    PATH_END = PATH_FILE_IMAGE

    NODE_START = NODE
    NODE_END = NODE

    CONTAINER_START = FOLDERLIST
    CONTAINER_END = FOLDERLIST_RADIO

    NONVALUE_START = FOLDER
    NONVALUE_END = SEPARATOR


class PrmScriptType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_PrmScriptType
    """
    INT = 0
    FLOAT = 1
    ANGLE = 2
    STRING = 3
    FILE = 4
    DIRECTORY = 5
    IMAGE = 6
    GEOMETRY = 7
    TOGGLE = 8
    BUTTON = 9
    VECTOR2 = 10
    VECTOR3 = 11
    VECTOR4 = 12
    INTVECTOR2 = 13
    INTVECTOR3 = 14
    INTVECTOR4 = 15
    UV = 16
    UVW = 17
    DIR = 18
    COLOR = 19
    COLOR4 = 20
    OPPATH = 21
    OPLIST = 22
    OBJECT = 23
    OBJECTLIST = 24
    RENDER = 25
    SEPARATOR = 26
    GEOMETRY_DATA = 27
    KEY_VALUE_DICT = 28
    LABEL = 29
    RGBAMASK = 30
    ORDINAL = 31
    RAMP_FLT = 32
    RAMP_RGB = 33
    FLOAT_LOG = 34
    INT_LOG = 35
    DATA = 36
    FLOAT_MINMAX = 37
    INT_MINMAX = 38
    INT_STARTEND = 39
    BUTTONSTRIP = 40
    ICONSTRIP = 41
    GROUPRADIO = 1000
    GROUPCOLLAPSIBLE = 1001
    GROUPSIMPLE = 1002
    GROUP = 1003


class ChoiceListType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_ChoiceListType
    """
    NONE = 0
    NORMAL = 1
    MINI = 2
    REPLACE = 3
    TOGGLE = 4


class PresetType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_PresetType
    """
    INVALID = -1
    BINARY = 0
    IDX = 1
    MAX = 2


class NodeType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_NodeType
    """
    ANY = -1
    NONE = 0
    OBJ = 1 << 0
    SOP = 1 << 1
    CHOP = 1 << 2
    ROP = 1 << 3
    SHOP = 1 << 4
    COP = 1 << 5
    VOP = 1 << 6
    DOP = 1 << 7
    TOP = 1 << 8


class NodeFlags(enum.IntEnum):
    """Equivalent of HAPI's HAPI_NodeFlags
    """
    ANY = -1
    NONE = 0
    DISPLAY = 1 << 0
    RENDER = 1 << 1
    TEMPLATED = 1 << 2
    LOCKED = 1 << 3
    EDITABLE = 1 << 4
    BYPASS = 1 << 5
    NETWORK = 1 << 6

    OBJ_GEOMETRY = 1 << 7
    OBJ_CAMERA = 1 << 8
    OBJ_LIGHT = 1 << 9
    OBJ_SUBNET = 1 << 10

    SOP_CURVE = 1 << 11
    SOP_GUIDE = 1 << 12

    TOP_NONSCHEDULER = 1 << 13


class GroupType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_GroupType
    """
    INVALID = -1
    POINT = 0
    PRIM = 1
    MAX = 2


class AttributeOwner(enum.IntEnum):
    """Equivalent of HAPI's HAPI_AttributeOwner
    """
    INVALID = -1
    VERTEX = 0
    POINT = 1
    PRIM = 2
    DETAIL = 3
    MAX = 4

class CurveType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_CurveType
    """
    INVALID = -1
    LINEAR = 0
    NURBS = 1
    BEZIER = 2
    MAX = 3


class VolumeType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_VolumeType
    """
    INVALID = -1
    HOUDINI = 0
    VDB = 1
    MAX = 2


class StorageType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_StorageType
    """
    INVALID = -1
    INT = 0
    INT64 = 1
    FLOAT = 2
    FLOAT64 = 3
    STRING = 4
    MAX = 5


class AttributeTypeInfo(enum.IntEnum):
    """Equivalent of HAPI's HAPI_AttributeTypeInfo
    """
    INVALID = -1
    NONE = 0
    POINT = 1
    HPOINT = 2
    VECTOR = 3
    NORMAL = 4
    COLOR = 5
    QUATERNION = 6
    MATRIX3 = 7
    MATRIX = 8
    ST = 9
    HIDDEN = 10
    BOX2 = 11
    BOX = 12
    TEXTURE = 13
    MAX = 14


class HGeoType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_GeoType
    """
    INVALID = -1
    DEFAULT = 0
    INTERMEDIATE = 1
    INPUT = 2
    CURVE = 3
    MAX = 4


class PartType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_PartType
    """
    INVALID = -1
    MESH = 0
    CURVE = 1
    VOLUME = 2
    INSTANCER = 3
    BOX = 4
    SPHERE = 3
    MAX = 4


class InputType(enum.IntEnum):
    """Equivalent of HAPI's HAPI_InputType
    """
    INVALID = -1
    TRANSFORM = 0
    GEOMETRY = 1
    MAX = 2

class RSTOrder(enum.IntEnum):
    """Equivalent of HAPI's HAPI_RSTOrder
    """
    HAPI_TRS = 0
    HAPI_TSR = 1
    HAPI_RTS = 2
    HAPI_RST = 3
    HAPI_STR = 4
    HAPI_SRT = 5
    HAPI_RSTORDER_DEFAULT = 5


NP_TYPE_TO_HSTORAGE_TYPE = {
    np.dtype('int32'): StorageType.INT,
    np.dtype('int64'): StorageType.INT64,
    np.dtype('float32'): StorageType.FLOAT,
    np.dtype('float64'): StorageType.FLOAT64,
    np.dtype('bytes_'): StorageType.STRING}


class PartInfo(StructureWithEnums):
    """Equivalent of HAPI's HAPI_PartInfo
    """
    _fields_ = [('id', c_int32),
                ('nameSH', c_int32),
                ('type', c_int32),
                ('faceCount', c_int32),
                ('vertexCount', c_int32),
                ('pointCount', c_int32),
                ('attributeCounts', c_int32 * 4),
                ('isInstanced', c_bool),
                ('instancedPartCount', c_int32),
                ('instanceCount', c_int32),
                ('hasChanged', c_bool)]
    _map = {
        "type":  PartType
    }

    def __init__(self):
        """Init
        """
        super(PartInfo, self).__init__()
        self.attributeCounts[0] = 0
        self.attributeCounts[1] = 0
        self.attributeCounts[2] = 0
        self.attributeCounts[3] = 0

    @property
    def point_attrib_count(self):
        """Get point attribute count

        Returns:
            int: point attribute count
        """
        return self.attributeCounts[AttributeOwner.POINT]

    @point_attrib_count.setter
    def point_attrib_count(self, value):
        """Set point attribute count

        Args:
            value (int): point attribute count
        """
        self.attributeCounts[AttributeOwner.POINT] = value

    @property
    def vertex_attrib_count(self):
        """Get vertex attribute count

        Returns:
            int: vertex attribute count
        """
        return self.attributeCounts[AttributeOwner.VERTEX]

    @vertex_attrib_count.setter
    def vertex_attrib_count(self, value):
        """Set vertex attribute count

        Args:
            value (int): vertex attribute count
        """
        self.attributeCounts[AttributeOwner.VERTEX] = value

    @property
    def prim_attrib_count(self):
        """Get prim attribute count

        Returns:
            int: prim attribute count
        """
        return self.attributeCounts[AttributeOwner.PRIM]

    @prim_attrib_count.setter
    def prim_attrib_count(self, value):
        """Set prim attribute count

        Args:
            value (int): prim attribute count
        """
        self.attributeCounts[AttributeOwner.PRIM] = value

    @property
    def detail_attrib_count(self):
        """Get detail attribute count

        Returns:
            int: detail attribute count
        """
        return self.attributeCounts[AttributeOwner.DETAIL]

    @detail_attrib_count.setter
    def detail_attrib_count(self, value):
        """Set detail attribute count

        Args:
            value (int): detail attribute count
        """
        self.attributeCounts[AttributeOwner.DETAIL] = value


class CurveInfo(StructureWithEnums): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_CurveInfo
    """
    _fields_ = [('curveType', c_int32),
                ('curveCount', c_int32),
                ('vertexCount', c_int32),
                ('knotCount', c_int32),
                ('isPeriodic', c_bool),
                ('isRational', c_bool),
                ('order', c_int32),
                ('hasKnots', c_bool)]
    _map = {
        "curveType":  CurveType
    }

class Transform(StructureWithEnums): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_Transform
    """
    _fields_ = [('position', c_float * 3),
                ('rotationQuaternion', c_float * 4),
                ('scale', c_float * 3),
                ('shear', c_float * 3),
                ('rstorder', c_int32)]
    _map = {
        "rstorder":  RSTOrder
    }

    def __init__(self):
        super(Transform, self).__init__()
        self.position[0] = 0
        self.position[1] = 0
        self.position[2] = 0
        self.rotationQuaternion[0] = 0
        self.rotationQuaternion[1] = 0
        self.rotationQuaternion[2] = 0
        self.rotationQuaternion[3] = 1
        self.scale[0] = 1
        self.scale[1] = 1
        self.scale[2] = 1
        self.shear[0] = 0
        self.shear[1] = 0
        self.shear[2] = 0
        self.rstorder = RSTOrder.HAPI_RSTORDER_DEFAULT

class VolumeTileInfo(Structure): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_VolumeTileInfo
    """
    _fields_ = [('minX', c_int32),
                ('minY', c_int32),
                ('minZ', c_int32),
                ('isValid', c_bool)]

class VolumeInfo(StructureWithEnums): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_VolumeInfo
    """
    _fields_ = [('nameSH', c_int32),
                ('type', c_int32),
                ('xLength', c_int32),
                ('yLength', c_int32),
                ('zLength', c_int32),
                ('minX', c_int32),
                ('minY', c_int32),
                ('minZ', c_int32),
                ('tupleSize', c_int32),
                ('storage', c_int32),
                ('tileSize', c_int32),
                ('transform', Transform),
                ('hasTaper', c_bool),
                ('xTaper', c_float),
                ('yTaper', c_float)]
    _map = {
        "type":  VolumeType,
        "storage": StorageType,
    }

class AttributeInfo(StructureWithEnums): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_AttributeInfo
    """
    _fields_ = [('exists', c_bool),
                ('owner', c_int32),
                ('storage', c_int32),
                ('originalOwner', c_int32),
                ('count', c_int32),
                ('tupleSize', c_int32),
                ('typeInfo', c_int32)]
    _map = {
        "owner": AttributeOwner,
        "storage": StorageType,
        "originalOwner": AttributeOwner,
        "typeInfo": AttributeTypeInfo
    }


class SessionConnectionState(enum.IntEnum):
    """[summary]
    """
    NOT_CONNECTED = 0
    CONNECTED = 1
    FAILED_TO_CONNECT = 2


class ThriftServerOptions(Structure): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_ThriftServerOptions
    """
    _fields_ = [('autoClose', c_bool),
                ('timeoutMs', c_float)]


class Session(StructureWithEnums): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_Session
    """
    _fields_ = [('type', c_int),
                ('id', c_int64)]
    _map = {
        "type":  SessionType
    }


class AssetInfo(Structure): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_AssetInfo
    """
    _fields_ = [('nodeId', c_int32),
                ('objectNodeId', c_int32),
                ('hasEverCooked', c_bool),
                ('nameSH', c_int32),
                ('labelSH', c_int32),
                ('filePathSH', c_int32),
                ('versionSH', c_int32),
                ('fullOpNameSH', c_int32),
                ('helpTextSH', c_int32),
                ('helpURLSH', c_int32),
                ('objectCount', c_int32),
                ('handleCount', c_int32),
                ('transformInputCount', c_int32),
                ('geoInputCount', c_int32),
                ('geoOutputCount', c_int32),
                ('haveObjectsChanged', c_int32),
                ('haveMaterialsChanged', c_int32)]


class ObjectInfo(Structure): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_ObjectInfo
    """
    _fields_ = [('nameSH', c_int32),
                ('objectInstancePathSH', c_int32),
                ('hasTransformChanged', c_bool),
                ('haveGeosChanged', c_bool),
                ('isVisible', c_bool),
                ('isInstancer', c_bool),
                ('isInstanced', c_bool),
                ('geoCount', c_int32),
                ('nodeId', c_int32),
                ('objectToInstanceId', c_int32)]


class GeoInfo(StructureWithEnums): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_GeoInfo
    """
    _fields_ = [('type', c_int32),
                ('nameSH', c_int32),
                ('nodeId', c_int32),
                ('isEditable', c_bool),
                ('isTemplated', c_bool),
                ('isDisplayGeo', c_bool),
                ('hasGeoChanged', c_bool),
                ('hasMaterialChanged', c_bool),
                ('pointGroupCount', c_int32),
                ('primitiveGroupCount', c_int32),
                ('partCount', c_int32)]
    _map = {
        "type": HGeoType
    }


class CookOptions(StructureWithEnums): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_CookOptions
    """
    _fields_ = [('splitGeosByGroup', c_bool),
                ('splitGeosByAttribute', c_bool),
                ('splitAttrSH', c_int32),
                ('maxVerticesPerPrimitive', c_int32),
                ('refineCurveToLinear', c_bool),
                ('curveRefineLOD', c_float),
                ('clearErrorsAndWarnings', c_bool),
                ('cookTemplatedGeos', c_bool),
                ('splitPointsByVertexAttributes', c_bool),
                ('packedPrimInstancingMode', c_int32),
                ('handleBoxPartTypes', c_bool),
                ('handleSpherePartTypes', c_bool),
                ('checkPartChanges', c_bool),
                ('extraFlags', c_int32)]
    _map = {
        'packedPrimInstancingMode' : PackedPrimInstancingMode
    }

class NodeInfo(StructureWithEnums): # pylint: disable=too-few-public-methods
    """Equivalent of HAPI's HAPI_NodeInfo
    """
    _fields_ = [('id', c_int32),
                ('parentId', c_int32),
                ('nameSH', c_int32),
                ('type', c_int),
                ('isValid', c_bool),
                ('totalCookCount', c_int32),
                ('uniqueHoudiniNodeId', c_int32),
                ('internalNodePathSH', c_int32),
                ('parmCount', c_int32),
                ('parmIntValueCount', c_int32),
                ('parmFloatValueCount', c_int32),
                ('parmStringValueCount', c_int32),
                ('parmChoiceCount', c_int32),
                ('childNodeCount', c_int32),
                ('inputCount', c_int32),
                ('outputCount', c_int32),
                ('createdPostAssetLoad', c_bool),
                ('isTimeDependent', c_bool)]
    _map = {
        "type": NodeType
    }


class ParmInfo(StructureWithEnums):
    """Equivalent of HAPI's HAPI_ParmInfo
    """
    _fields_ = [('id', c_int32),
                ('parentId', c_int32),
                ('childIndex', c_int32),
                ('type', c_int),
                ('scriptType', c_int),
                ('typeInfoSH', c_int32),
                ('permissions', c_int32),
                ('tagCount', c_int32),
                ('size', c_int32),
                ('choiceListType', c_int32),
                ('choiceCount', c_int32),
                ('nameSH', c_int32),
                ('labelSH', c_int32),
                ('templateNameSH', c_int32),
                ('helpSH', c_int32),
                ('hasMin', c_bool),
                ('hasMax', c_bool),
                ('hasUIMin', c_bool),
                ('hasUIMax', c_bool),
                ('min', c_float),
                ('max', c_float),
                ('UIMin', c_float),
                ('UIMax', c_float),
                ('invisible', c_bool),
                ('disabled', c_bool),
                ('spare', c_bool),
                ('joinNext', c_bool),
                ('labelNone', c_bool),
                ('intValuesIndex', c_int32),
                ('floatValuesIndex', c_int32),
                ('stringValuesIndex', c_int32),
                ('choiceIndex', c_int32),
                ('inputNodeType', c_int32),
                ('inputNodeFlag', c_int32),
                ('isChildOfMultiParm', c_bool),
                ('instanceNum', c_int32),
                ('instanceLength', c_int32),
                ('instanceCount', c_int32),
                ('instanceStartOffset', c_int32),
                ('rampType', c_int32),
                ('visibilityConditionSH', c_int32),
                ('disabledConditionSH', c_int32)]
    _map = {
        "type": ParmType,
        "scriptType": PrmScriptType,
        "permissions": Permissions,
        "choiceListType": ChoiceListType,
        "inputNodeType": NodeType,
        "inputNodeFlag": NodeFlags,
        "rampType": RampType
    }


    def is_int(self):
        """If this attribute is int type

        Returns:
            bool: If this attribute is int type
        """
        return (self.type >= ParmType.INT_START and
                self.type <= ParmType.INT_END)\
            or self.type == ParmType.MULTIPARMLIST\
            or self.type == ParmType.FOLDERLIST_RADIO

    def is_float(self):
        """If this attribute is float type

        Returns:
            bool: If this attribute is float type
        """
        return self.type >= ParmType.FLOAT_START and\
            self.type <= ParmType.FLOAT_END

    def is_string(self):
        """If this attribute is string type

        Returns:
            bool: If this attribute is string type
        """
        return (self.type >= ParmType.STRING_START and
                self.type <= ParmType.STRING_END)\
            or self.type == ParmType.LABEL\
            or self.type == ParmType.PATH_FILE_DIR

    def is_path(self):
        """If this attribute is path type

        Returns:
            bool: If this attribute is path type
        """
        return (self.type >= ParmType.PATH_START and
                self.type <= ParmType.PATH_END)\
            or self.type == ParmType.PATH_FILE_DIR

    def is_node(self):
        """If this attribute is node type

        Returns:
            bool: If this attribute is node type
        """
        return self.type >= ParmType.NODE_START and\
            self.type <= ParmType.NODE_END

    def is_non_value(self):
        """If this attribute is non-value

        Returns:
            bool: If this attribute is non-value
        """
        return self.type >= ParmType.NONVALUE_START and\
            self.type <= ParmType.NONVALUE_END



class ParmChoiceInfo(StructureWithEnums):
    """Equivalent of HAPI's HAPI_ParmChoiceInfo
    """
    _fields_ = [
        ('parentParmId', c_int32),
        ('labelSH', c_int32),
        ('valueSH', c_int32)]
