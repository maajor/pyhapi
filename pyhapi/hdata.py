from . import *

#https://gist.github.com/christoph2/9c390e5c094796903097
class StructureWithEnums(Structure):
    """Add missing enum feature to ctypes Structures.
    """
    _map = {}

    def __getattribute__(self, name):
        _map = Structure.__getattribute__(self, '_map')
        value = Structure.__getattribute__(self, name)
        if name in _map:
            EnumClass = _map[name]
            if isinstance(value, Array):
                return [EnumClass(x) for x in value]
            else:
                return EnumClass(value)
        else:
            return value

    def __str__(self):
        result = []
        result.append("struct {0} {{".format(self.__class__.__name__))
        for field in self._fields_:
            attr, attrType = field
            if attr in self._map:
                attrType = self._map[attr]
            value = getattr(self, attr)
            result.append("    {0} [{1}] = {2!r};".format(attr, attrType.__name__, value))
        result.append("};")
        return '\n'.join(result)

    __repr__ = __str__

class HAPI_License(enum.IntEnum):
    HAPI_LICENSE_NONE                                     = 0
    HAPI_LICENSE_HOUDINI_ENGINE                                     = 1
    HAPI_LICENSE_HOUDINI                         = 2
    HAPI_LICENSE_HOUDINI_FX                             = 3
    HAPI_LICENSE_HOUDINI_ENGINE_INDIE                               = 4
    HAPI_LICENSE_HOUDINI_INDIE                             = 5
    HAPI_LICENSE_MAX                            = 6

class HAPI_StatusType(enum.IntEnum):
    HAPI_STATUS_CALL_RESULT                                 = 0
    HAPI_STATUS_COOK_RESULT                                 = 1
    HAPI_STATUS_COOK_STATE                                  = 2
    HAPI_STATUS_MAX                                         = 3


class HAPI_StatusVerbosity(enum.IntEnum):
    HAPI_STATUSVERBOSITY_0 = 0
    HAPI_STATUSVERBOSITY_1 = 1
    HAPI_STATUSVERBOSITY_2 = 2
    HAPI_STATUSVERBOSITY_ALL = HAPI_STATUSVERBOSITY_2
    HAPI_STATUSVERBOSITY_ERRORS = HAPI_STATUSVERBOSITY_0
    HAPI_STATUSVERBOSITY_WARNINGS = HAPI_STATUSVERBOSITY_1
    HAPI_STATUSVERBOSITY_MESSAGES = HAPI_STATUSVERBOSITY_2

class HAPI_Result(enum.IntEnum):
    HAPI_RESULT_SUCCESS                                     = 0
    HAPI_RESULT_FAILURE                                     = 1
    HAPI_RESULT_ALREADY_INITIALIZED                         = 2
    HAPI_RESULT_NOT_INITIALIZED                             = 3
    HAPI_RESULT_CANT_LOADFILE                               = 4
    HAPI_RESULT_PARM_SET_FAILED                             = 5
    HAPI_RESULT_INVALID_ARGUMENT                            = 6
    HAPI_RESULT_CANT_LOAD_GEO                               = 7
    HAPI_RESULT_CANT_GENERATE_PRESET                        = 8
    HAPI_RESULT_CANT_LOAD_PRESET                            = 9
    HAPI_RESULT_ASSET_DEF_ALREADY_LOADED                    = 10

    HAPI_RESULT_NO_LICENSE_FOUND                            = 110
    HAPI_RESULT_DISALLOWED_NC_LICENSE_FOUND                 = 120
    HAPI_RESULT_DISALLOWED_NC_ASSET_WITH_C_LICENSE          = 130
    HAPI_RESULT_DISALLOWED_NC_ASSET_WITH_LC_LICENSE         = 140
    HAPI_RESULT_DISALLOWED_LC_ASSET_WITH_C_LICENSE          = 150
    HAPI_RESULT_DISALLOWED_HENGINEINDIE_W_3PARTY_PLUGIN     = 160

    HAPI_RESULT_ASSET_INVALID                               = 200
    HAPI_RESULT_NODE_INVALID                                = 210

    HAPI_RESULT_USER_INTERRUPTED                            = 300

    HAPI_RESULT_INVALID_SESSION                             = 400

class HAPI_ErrorCode(enum.IntEnum):
    HAPI_ERRORCODE_ASSET_DEF_NOT_FOUND                       = 1<<0
    HAPI_ERRORCODE_PYTHON_NODE_ERROR                        = 1<<1

class HAPI_SessionType(enum.IntEnum):
    HAPI_SESSION_INPROCESS = 0
    HAPI_SESSION_THRIFT = 1
    HAPI_SESSION_CUSTOM1 = 2
    HAPI_SESSION_CUSTOM2 = 3
    HAPI_SESSION_CUSTOM3 = 4
    HAPI_SESSION_MAX = 5

class HAPI_State(enum.IntEnum):
    HAPI_STATE_READY                                        = 0
    HAPI_STATE_READY_WITH_FATAL_ERRORS                      = 1
    HAPI_STATE_READY_WITH_COOK_ERRORS                       = 2
    HAPI_STATE_STARTING_COOK                                = 3
    HAPI_STATE_COOKING                                      = 4
    HAPI_STATE_STARTING_LOAD                                = 5
    HAPI_STATE_LOADING                                      = 6
    HAPI_STATE_MAX                                          = 7

    HAPI_STATE_MAX_READY_STATE                              = HAPI_STATE_READY_WITH_COOK_ERRORS

class HAPI_PackedPrimInstancingMode(enum.IntEnum):
    HAPI_PACKEDPRIM_INSTANCING_MODE_INVALID                  = -1
    HAPI_PACKEDPRIM_INSTANCING_MODE_DISABLED                 = 0
    HAPI_PACKEDPRIM_INSTANCING_MODE_HIERARCHY                = 1
    HAPI_PACKEDPRIM_INSTANCING_MODE_FLAT                     = 2
    HAPI_PACKEDPRIM_INSTANCING_MODE_MAX                      = 3

class HAPI_Permissions(enum.IntEnum):
    HAPI_PERMISSIONS_NON_APPLICABLE                  = 0
    HAPI_PERMISSIONS_READ_WRITE                 = 1
    HAPI_PERMISSIONS_READ_ONLY                = 2
    HAPI_PERMISSIONS_WRITE_ONLY                     = 3
    HAPI_PERMISSIONS_MAX                      = 4

class HAPI_RampType(enum.IntEnum):
    HAPI_RAMPTYPE_INVALID                  = -1
    HAPI_RAMPTYPE_FLOAT                 = 0
    HAPI_RAMPTYPE_COLOR                = 1
    HAPI_RAMPTYPE_MAX                     = 2

class HAPI_ParmType(enum.IntEnum):
    HAPI_PARMTYPE_INT                                       = 0
    HAPI_PARMTYPE_MULTIPARMLIST  = 1
    HAPI_PARMTYPE_TOGGLE = 2
    HAPI_PARMTYPE_BUTTON = 3

    HAPI_PARMTYPE_FLOAT = 4
    HAPI_PARMTYPE_COLOR = 5

    HAPI_PARMTYPE_STRING = 6
    HAPI_PARMTYPE_PATH_FILE = 7
    HAPI_PARMTYPE_PATH_FILE_GEO = 8
    HAPI_PARMTYPE_PATH_FILE_IMAGE = 9

    HAPI_PARMTYPE_NODE      = 10

    HAPI_PARMTYPE_FOLDERLIST   = 11
    HAPI_PARMTYPE_FOLDERLIST_RADIO    = 12

    HAPI_PARMTYPE_FOLDER    = 13
    HAPI_PARMTYPE_LABEL  = 14
    HAPI_PARMTYPE_SEPARATOR = 15
    HAPI_PARMTYPE_PATH_FILE_DIR  = 16

    HAPI_PARMTYPE_MAX = 17

    HAPI_PARMTYPE_INT_START = HAPI_PARMTYPE_INT
    HAPI_PARMTYPE_INT_END = HAPI_PARMTYPE_BUTTON

    HAPI_PARMTYPE_FLOAT_START = HAPI_PARMTYPE_FLOAT
    HAPI_PARMTYPE_FLOAT_END = HAPI_PARMTYPE_COLOR

    HAPI_PARMTYPE_STRING_START = HAPI_PARMTYPE_STRING
    HAPI_PARMTYPE_STRING_END = HAPI_PARMTYPE_NODE

    HAPI_PARMTYPE_PATH_START = HAPI_PARMTYPE_PATH_FILE
    HAPI_PARMTYPE_PATH_END = HAPI_PARMTYPE_PATH_FILE_IMAGE

    HAPI_PARMTYPE_NODE_START = HAPI_PARMTYPE_NODE
    HAPI_PARMTYPE_NODE_END = HAPI_PARMTYPE_NODE

    HAPI_PARMTYPE_CONTAINER_START = HAPI_PARMTYPE_FOLDERLIST
    HAPI_PARMTYPE_CONTAINER_END = HAPI_PARMTYPE_FOLDERLIST_RADIO

    HAPI_PARMTYPE_NONVALUE_START = HAPI_PARMTYPE_FOLDER
    HAPI_PARMTYPE_NONVALUE_END = HAPI_PARMTYPE_SEPARATOR

class HAPI_PrmScriptType(enum.IntEnum):
    HAPI_PRM_SCRIPT_TYPE_INT = 0   
    HAPI_PRM_SCRIPT_TYPE_FLOAT = 1 
    HAPI_PRM_SCRIPT_TYPE_ANGLE = 2
    HAPI_PRM_SCRIPT_TYPE_STRING = 3
    HAPI_PRM_SCRIPT_TYPE_FILE = 4
    HAPI_PRM_SCRIPT_TYPE_DIRECTORY = 5
    HAPI_PRM_SCRIPT_TYPE_IMAGE = 6
    HAPI_PRM_SCRIPT_TYPE_GEOMETRY = 7
    HAPI_PRM_SCRIPT_TYPE_TOGGLE = 8
    HAPI_PRM_SCRIPT_TYPE_BUTTON = 9
    HAPI_PRM_SCRIPT_TYPE_VECTOR2 = 10
    HAPI_PRM_SCRIPT_TYPE_VECTOR3 = 11
    HAPI_PRM_SCRIPT_TYPE_VECTOR4 = 12
    HAPI_PRM_SCRIPT_TYPE_INTVECTOR2 = 13
    HAPI_PRM_SCRIPT_TYPE_INTVECTOR3 = 14
    HAPI_PRM_SCRIPT_TYPE_INTVECTOR4 = 15
    HAPI_PRM_SCRIPT_TYPE_UV = 16
    HAPI_PRM_SCRIPT_TYPE_UVW = 17
    HAPI_PRM_SCRIPT_TYPE_DIR = 18
    HAPI_PRM_SCRIPT_TYPE_COLOR = 19
    HAPI_PRM_SCRIPT_TYPE_COLOR4 = 20
    HAPI_PRM_SCRIPT_TYPE_OPPATH = 21
    HAPI_PRM_SCRIPT_TYPE_OPLIST = 22
    HAPI_PRM_SCRIPT_TYPE_OBJECT = 23
    HAPI_PRM_SCRIPT_TYPE_OBJECTLIST = 24
    HAPI_PRM_SCRIPT_TYPE_RENDER = 25
    HAPI_PRM_SCRIPT_TYPE_SEPARATOR = 26
    HAPI_PRM_SCRIPT_TYPE_GEOMETRY_DATA = 27
    HAPI_PRM_SCRIPT_TYPE_KEY_VALUE_DICT = 28
    HAPI_PRM_SCRIPT_TYPE_LABEL = 29
    HAPI_PRM_SCRIPT_TYPE_RGBAMASK = 30
    HAPI_PRM_SCRIPT_TYPE_ORDINAL = 31
    HAPI_PRM_SCRIPT_TYPE_RAMP_FLT = 32
    HAPI_PRM_SCRIPT_TYPE_RAMP_RGB = 33
    HAPI_PRM_SCRIPT_TYPE_FLOAT_LOG = 34
    HAPI_PRM_SCRIPT_TYPE_INT_LOG = 35
    HAPI_PRM_SCRIPT_TYPE_DATA = 36
    HAPI_PRM_SCRIPT_TYPE_FLOAT_MINMAX = 37
    HAPI_PRM_SCRIPT_TYPE_INT_MINMAX = 38
    HAPI_PRM_SCRIPT_TYPE_INT_STARTEND = 39
    HAPI_PRM_SCRIPT_TYPE_BUTTONSTRIP = 40
    HAPI_PRM_SCRIPT_TYPE_ICONSTRIP = 41
    HAPI_PRM_SCRIPT_TYPE_GROUPRADIO = 1000
    HAPI_PRM_SCRIPT_TYPE_GROUPCOLLAPSIBLE = 1001
    HAPI_PRM_SCRIPT_TYPE_GROUPSIMPLE = 1002
    HAPI_PRM_SCRIPT_TYPE_GROUP  = 1003

class HAPI_ChoiceListType(enum.IntEnum):
    HAPI_CHOICELISTTYPE_NONE = 0
    HAPI_CHOICELISTTYPE_NORMAL = 1
    HAPI_CHOICELISTTYPE_MINI = 2
    HAPI_CHOICELISTTYPE_REPLACE = 3
    HAPI_CHOICELISTTYPE_TOGGLE = 4

class HAPI_PresetType(enum.IntEnum):
    HAPI_PRESETTYPE_INVALID = -1
    HAPI_PRESETTYPE_BINARY = 0
    HAPI_PRESETTYPE_IDX = 1
    HAPI_PRESETTYPE_MAX = 2

class HAPI_NodeType(enum.IntEnum):
    HAPI_NODETYPE_ANY       = -1
    HAPI_NODETYPE_NONE      = 0
    HAPI_NODETYPE_OBJ       = 1 << 0
    HAPI_NODETYPE_SOP       = 1 << 1
    HAPI_NODETYPE_CHOP      = 1 << 2
    HAPI_NODETYPE_ROP       = 1 << 3
    HAPI_NODETYPE_SHOP      = 1 << 4
    HAPI_NODETYPE_COP       = 1 << 5
    HAPI_NODETYPE_VOP       = 1 << 6
    HAPI_NODETYPE_DOP       = 1 << 7
    HAPI_NODETYPE_TOP       = 1 << 8

class HAPI_NodeFlags(enum.IntEnum):
    HAPI_NODEFLAGS_ANY          = -1
    HAPI_NODEFLAGS_NONE         = 0
    HAPI_NODEFLAGS_DISPLAY      = 1 << 0
    HAPI_NODEFLAGS_RENDER       = 1 << 1
    HAPI_NODEFLAGS_TEMPLATED    = 1 << 2
    HAPI_NODEFLAGS_LOCKED       = 1 << 3
    HAPI_NODEFLAGS_EDITABLE     = 1 << 4
    HAPI_NODEFLAGS_BYPASS       = 1 << 5
    HAPI_NODEFLAGS_NETWORK      = 1 << 6

    HAPI_NODEFLAGS_OBJ_GEOMETRY = 1 << 7
    HAPI_NODEFLAGS_OBJ_CAMERA   = 1 << 8
    HAPI_NODEFLAGS_OBJ_LIGHT    = 1 << 9
    HAPI_NODEFLAGS_OBJ_SUBNET   = 1 << 10

    HAPI_NODEFLAGS_SOP_CURVE    = 1 << 11
    HAPI_NODEFLAGS_SOP_GUIDE    = 1 << 12

    HAPI_NODEFLAGS_TOP_NONSCHEDULER = 1 << 13

    
class HAPI_GroupType(enum.IntEnum):
    HAPI_GROUPTYPE_INVALID = -1
    HAPI_GROUPTYPE_POINT = 0
    HAPI_GROUPTYPE_PRIM = 1
    HAPI_GROUPTYPE_MAX = 2

class HAPI_AttributeOwner(enum.IntEnum):
    HAPI_ATTROWNER_INVALID = -1
    HAPI_ATTROWNER_VERTEX = 0
    HAPI_ATTROWNER_POINT = 1
    HAPI_ATTROWNER_PRIM = 2
    HAPI_ATTROWNER_DETAIL = 3
    HAPI_ATTROWNER_MAX = 4

class HAPI_CurveType(enum.IntEnum):
    HAPI_CURVETYPE_INVALID = -1
    HAPI_CURVETYPE_LINEAR = 0
    HAPI_CURVETYPE_NURBS = 1
    HAPI_CURVETYPE_BEZIER = 2
    HAPI_CURVETYPE_MAX = 3

class HAPI_VolumeType(enum.IntEnum):
    HAPI_VOLUMETYPE_INVALID = -1
    HAPI_VOLUMETYPE_HOUDINI = 0
    HAPI_VOLUMETYPE_VDB = 1
    HAPI_VOLUMETYPE_MAX = 2

class HAPI_StorageType(enum.IntEnum):
    HAPI_STORAGETYPE_INVALID = -1
    HAPI_STORAGETYPE_INT = 0
    HAPI_STORAGETYPE_INT64 = 1
    HAPI_STORAGETYPE_FLOAT = 2
    HAPI_STORAGETYPE_FLOAT64 = 3
    HAPI_STORAGETYPE_STRING = 4
    HAPI_STORAGETYPE_MAX = 5

class HAPI_AttributeTypeInfo(enum.IntEnum):
    HAPI_ATTRIBUTE_TYPE_INVALID = -1
    HAPI_ATTRIBUTE_TYPE_NONE = 0
    HAPI_ATTRIBUTE_TYPE_POINT = 1
    HAPI_ATTRIBUTE_TYPE_HPOINT = 2
    HAPI_ATTRIBUTE_TYPE_VECTOR = 3
    HAPI_ATTRIBUTE_TYPE_NORMAL = 4
    HAPI_ATTRIBUTE_TYPE_COLOR = 5
    HAPI_ATTRIBUTE_TYPE_QUATERNION = 6
    HAPI_ATTRIBUTE_TYPE_MATRIX3 = 7
    HAPI_ATTRIBUTE_TYPE_MATRIX = 8
    HAPI_ATTRIBUTE_TYPE_ST = 9
    HAPI_ATTRIBUTE_TYPE_HIDDEN = 10
    HAPI_ATTRIBUTE_TYPE_BOX2 = 11
    HAPI_ATTRIBUTE_TYPE_BOX = 12
    HAPI_ATTRIBUTE_TYPE_TEXTURE = 13
    HAPI_ATTRIBUTE_TYPE_MAX = 14

class HAPI_GeoType(enum.IntEnum):
    HAPI_GEOTYPE_INVALID = -1
    HAPI_GEOTYPE_DEFAULT = 0
    HAPI_GEOTYPE_INTERMEDIATE = 1
    HAPI_GEOTYPE_INPUT = 2
    HAPI_GEOTYPE_CURVE = 3
    HAPI_GEOTYPE_MAX = 4

class HAPI_PartType(enum.IntEnum):
    HAPI_PARTTYPE_INVALID = -1
    HAPI_PARTTYPE_MESH = 0
    HAPI_PARTTYPE_CURVE = 1
    HAPI_PARTTYPE_VOLUME = 2
    HAPI_PARTTYPE_INSTANCER = 3
    HAPI_PARTTYPE_BOX = 4
    HAPI_PARTTYPE_SPHERE = 3
    HAPI_PARTTYPE_MAX = 4

class HAPI_InputType(enum.IntEnum):
    HAPI_INPUT_INVALID = -1
    HAPI_INPUT_TRANSFORM = 0
    HAPI_INPUT_GEOMETRY = 1
    HAPI_INPUT_MAX = 2

class HAPI_PartInfo(StructureWithEnums): 
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
         "type":  HAPI_PartType
    }

    def __init__(self):
        self.attributeCounts[0] = 0
        self.attributeCounts[1] = 0
        self.attributeCounts[2] = 0
        self.attributeCounts[3] = 0

    @property
    def pointAttribCount(self): 
        return self.attributeCounts[HAPI_AttributeOwner.HAPI_ATTROWNER_POINT] 
       
    @pointAttribCount.setter 
    def pointAttribCount(self, v):  
        self.attributeCounts[HAPI_AttributeOwner.HAPI_ATTROWNER_POINT]  = v 

    @property
    def vertexAttribCount(self): 
        return self.attributeCounts[HAPI_AttributeOwner.HAPI_ATTROWNER_VERTEX] 
       
    @vertexAttribCount.setter 
    def vertexAttribCount(self, v):  
        self.attributeCounts[HAPI_AttributeOwner.HAPI_ATTROWNER_VERTEX]  = v 

    @property
    def primAttribCount(self): 
        return self.attributeCounts[HAPI_AttributeOwner.HAPI_ATTROWNER_PRIM] 
       
    @primAttribCount.setter 
    def primAttribCount(self, v):  
        self.attributeCounts[HAPI_AttributeOwner.HAPI_ATTROWNER_PRIM]  = v 

    @property
    def detailAttribCount(self): 
        return self.attributeCounts[HAPI_AttributeOwner.HAPI_ATTROWNER_DETAIL] 
       
    @detailAttribCount.setter 
    def detailAttribCount(self, v):  
        self.attributeCounts[HAPI_AttributeOwner.HAPI_ATTROWNER_DETAIL]  = v 

class HAPI_AttributeInfo(StructureWithEnums): 
    _fields_ = [('exists', c_bool),  
                ('owner', c_int32),
                ('storage', c_int32),
                ('originalOwner', c_int32),
                ('count', c_int32),
                ('tupleSize', c_int32),
                ('typeInfo', c_int32)]
    _map = {
         "owner":  HAPI_AttributeOwner,
         "storage":  HAPI_StorageType,
         "originalOwner":  HAPI_AttributeOwner,
         "typeInfo":  HAPI_AttributeTypeInfo
    }

class SessionConnectionState(enum.IntEnum):
    NOT_CONNECTED = 0
    CONNECTED = 1
    FAILED_TO_CONNECT = 2

class HAPI_ThriftServerOptions(Structure):  
    _fields_ = [('autoClose', c_bool),  
                ('timeoutMs', c_float)]  

class HAPI_Session(StructureWithEnums):  
    _fields_ = [('type', c_int),  
                ('id', c_int64)]
    _map = {
         "type":  HAPI_SessionType
    }

class HAPI_CookOptions(Structure):  
    _fields_ = [('splitGeosByGroup', c_bool),  
                ('splitGeosByAttribute', c_bool),
                ('splitAttrSH', c_int32),
                ('maxVerticesPerPrimitive', c_int32),
                ('refineCurveToLinear', c_bool),
                ('curveRefineLOD', c_float),
                ('clearErrorsAndWarnings', c_bool),
                ('cookTemplatedGeos', c_bool),
                ('splitPointsByVertexAttributes', c_bool),
                ('handleBoxPartTypes', c_bool),
                ('handleSpherePartTypes', c_bool),
                ('checkPartChanges', c_bool),
                ('extraFlags', c_int32)]

class HAPI_NodeInfo(StructureWithEnums):  
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
         "type":  HAPI_NodeType
    }

class HAPI_ParmInfo(StructureWithEnums):  
    _fields_ = [('id', c_int32),  
                ('parentId', c_int32),
                ('childIndex', c_int32),
                ('type', c_int),
                ('scriptType', c_int),
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
                ('labelNone', c_bool),
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
         "type":  HAPI_ParmType,
         "scriptType" : HAPI_PrmScriptType,
         "permissions" : HAPI_Permissions,
         "choiceListType" : HAPI_ChoiceListType,
         "inputNodeType" : HAPI_NodeType,
         "inputNodeFlag" : HAPI_NodeFlags,
         "rampType" : HAPI_RampType
    }

    def IsInt(self):
        return (self.type >= HAPI_ParmType.HAPI_PARMTYPE_INT_START and\
            self.type <= HAPI_ParmType.HAPI_PARMTYPE_INT_END)\
            or self.type == HAPI_ParmType.HAPI_PARMTYPE_MULTIPARMLIST\
            or self.type == HAPI_ParmType.HAPI_PARMTYPE_FOLDERLIST_RADIO


    def isFloat(self):
        return (self.type >= HAPI_ParmType.HAPI_PARMTYPE_FLOAT_START and\
            self.type <= HAPI_ParmType.HAPI_PARMTYPE_FLOAT_END)
        
    def isString(self):
        return (self.type >= HAPI_ParmType.HAPI_PARMTYPE_STRING_START and\
                self.type <= HAPI_ParmType.HAPI_PARMTYPE_STRING_END)\
                or self.type == HAPI_ParmType.HAPI_PARMTYPE_LABEL\
                or self.type == HAPI_ParmType.HAPI_PARMTYPE_PATH_FILE_DIR
        
    def isPath(self):
        return (self.type >= HAPI_ParmType.HAPI_PARMTYPE_PATH_START and\
                self.type <= HAPI_ParmType.HAPI_PARMTYPE_PATH_END)\
                or self.type == HAPI_ParmType.HAPI_PARMTYPE_PATH_FILE_DIR

    def isNode(self):
        return (self.type >= HAPI_ParmType.HAPI_PARMTYPE_NODE_START and\
                self.type <= HAPI_ParmType.HAPI_PARMTYPE_NODE_END)

    def isNonValue(self):
        return (self.type >= HAPI_ParmType.HAPI_PARMTYPE_NONVALUE_START and\
                self.type <= HAPI_ParmType.HAPI_PARMTYPE_NONVALUE_END)