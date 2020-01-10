"""Summary

Attributes
----------
StorageTypeToSetAttrib : TYPE
    Description
"""
from . import *

def IsSessionValid(session):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    result = HAPIlib.HAPI_IsSessionValid(byref(session))
    return result == HAPI_Result.HAPI_RESULT_SUCCESS

def Cleanup(session):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    """
    result = HAPIlib.HAPI_Cleanup(byref(session))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "Cleanup Failed with {0}".format(HAPI_Result(result).name)


def CloseSession(session):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    """
    result = HAPIlib.HAPI_CloseSession(byref(session))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "Close Session Failed with {0}".format(HAPI_Result(result).name)

def CreateInProcessSession(session):
    '''
    Attributes
    ----------
    session : HAPI_Session
    
    Returns
    -------
    bool: success
    
    Parameters
    ----------
    session : TYPE
        Description
    '''
    return HAPIlib.HAPI_CreateInProcessSession(byref(session))

def StartThriftNamedPipeServer(serverOptions):
    '''
    Attributes
    ----------
    serverOptions : HAPI_ThriftServerOptions
    
    Returns
    -------
    int: process id if success
    
    Parameters
    ----------
    serverOptions : TYPE
        Description
    '''
    processid = c_int32()
    result = HAPIlib.HAPI_StartThriftNamedPipeServer(byref(serverOptions), c_char_p("hapi".encode('utf-8')), byref(processid))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "StartThriftNamedPipeServer Failed with {0}".format(HAPI_Result(result).name)
    print("Session Created with Process Id: {0}".format(processid.value))
    return processid

def CreateThriftNamedPipeSession(session):
    '''
    Parameters
    ----------
    session : HAPI_Session
        Description
    '''
    result =  HAPIlib.HAPI_CreateThriftNamedPipeSession(byref(session), c_char_p("hapi".encode('utf-8')))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "CreateThriftNamedPipeSession Failed with {0}".format(HAPI_Result(result).name)

def Initialize(
    session, 
    cookOption, 
    use_cooking_thread = True, 
    cooking_thread_stack_size  = -1,
    houdini_environment_files = "",
    otl_search_path = "", 
    dso_search_path = "",
    image_dso_search_path = "",
    audio_dso_search_path = "" 
    ):
    '''
    Parameters
    ----------
    session : HAPI_Session
        Description
    cookOption : bool
        Description
    use_cooking_thread : bool, optional
        Description
    cooking_thread_stack_size : TYPE, optional
        Description
    houdini_environment_files : str, optional
        Description
    otl_search_path : str, optional
        Description
    dso_search_path : str, optional
        Description
    image_dso_search_path : str, optional
        Description
    audio_dso_search_path : str, optional
        Description
    '''
    result = HAPIlib.HAPI_Initialize( 
        byref(session), 
        byref(cookOption),
        c_bool(use_cooking_thread),
        c_int32(cooking_thread_stack_size),
        c_char_p(houdini_environment_files.encode('utf-8')),
        c_char_p(otl_search_path.encode('utf-8')),
        c_char_p(dso_search_path.encode('utf-8')),
        c_char_p(image_dso_search_path.encode('utf-8')),
        c_char_p(audio_dso_search_path.encode('utf-8')))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS or result == HAPI_Result.HAPI_RESULT_ALREADY_INITIALIZED, "Initialize Failed with {0}".format(HAPI_Result(result).name)


def LoadAssetLibraryFromFile(
    session, 
    filePath,
    allow_overwrite = True, 
    ):
    '''
    Attributes
    ----------
    session : HAPI_Session
    filePath : string
    library_id : int
    allow_overwrite : bool
    
    Returns
    -------
    int: asset library id if success
    
    Parameters
    ----------
    session : TYPE
        Description
    filePath : TYPE
        Description
    allow_overwrite : bool, optional
        Description
    '''
    assetLibId = c_int32()
    result = HAPIlib.HAPI_LoadAssetLibraryFromFile(byref(session), c_char_p(filePath.encode('utf-8')), c_bool(allow_overwrite), byref(assetLibId) )
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "LoadAssetLibraryFromFile Failed with {0}".format(HAPI_Result(result).name)
    return assetLibId

def _GetAvailableAssetCount(session, assetLibId):
    '''
    Attributes
    ----------
    session : HAPI_Session
    assetLibId : int
    
    Returns
    -------
    int: asset count if success
    
    Parameters
    ----------
    session : TYPE
        Description
    assetLibId : TYPE
        Description
    '''
    assetCount = c_int32()
    result = HAPIlib.HAPI_GetAvailableAssetCount(byref(session), assetLibId, byref(assetCount));
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetAvailableAssetCount Failed with {0}".format(HAPI_Result(result).name)
    return assetCount

def GetAvailableAssets(session, assetLibId):
    '''
    Attributes
    ----------
    session : HAPI_Session
    assetLibId : int
    assetCount : int
    
    Returns
    -------
    string[]: asset names if success
    
    Parameters
    ----------
    session : TYPE
        Description
    assetLibId : TYPE
        Description
    '''
    assetCount = _GetAvailableAssetCount(session, assetLibId)

    asset_string_buffer = ( c_int32 * assetCount.value) ()

    result = HAPIlib.HAPI_GetAvailableAssets(byref(session), assetLibId, byref(asset_string_buffer), assetCount );
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetAvailableAssets Failed with {0}".format(HAPI_Result(result).name)

    asset_names = []
    for i in range(0, len(asset_string_buffer)):
        asset_name = GetString(session, asset_string_buffer[i])
        asset_names.append(asset_name)

    return asset_names

def CreateInputNode(session, node_label):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_label : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    nodeid = c_int32()
    result =  HAPIlib.HAPI_CreateInputNode( byref(session), byref(nodeid), c_char_p(node_label.encode('utf-8'))) 
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "CreateInputNode Failed with {0}".format(HAPI_Result(result).name)
    return nodeid

def CreateNode(
    session, 
    operator_name, 
    node_label, 
    parent_node_id = -1, 
    cook_on_creation = False
    ):
    '''
    Attributes
    ----------
    session : HAPI_Session
    operator_name: string
    node_label : string 
    parent_node_id : int
    cook_on_creation : bool
    
    Returns
    -------
    int: node id if success
    
    Parameters
    ----------
    session : TYPE
        Description
    operator_name : TYPE
        Description
    node_label : TYPE
        Description
    parent_node_id : TYPE, optional
        Description
    cook_on_creation : bool, optional
        Description
    '''
    nodeid = c_int32()
    result =  HAPIlib.HAPI_CreateNode( byref(session), c_int(parent_node_id), c_char_p(operator_name),  c_char_p(node_label.encode('utf-8')), c_bool(cook_on_creation),  byref(nodeid) ) 
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "CreateNode Failed with {0}".format(HAPI_Result(result).name)
    return nodeid

def DeleteNode(session, node_id):
    '''
    Attributes
    ----------
    session : HAPI_Session
    operator_name: string
    node_label : string 
    parent_node_id : int
    cook_on_creation : bool
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    
    No Longer Returned
    ------------------
    int: node id if success
    '''
    result =  HAPIlib.HAPI_DeleteNode( byref(session), node_id) 
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "DeleteNode Failed with {0}".format(HAPI_Result(result).name)

def CookNode(
    session, 
    cook_option, 
    nodeid
    ):
    '''
    Attributes
    ----------
    session : HAPI_Session
    cook_option: HAPI_CookOptions
    nodeid : int 
    
    Parameters
    ----------
    session : TYPE
        Description
    cook_option : TYPE
        Description
    nodeid : TYPE
        Description
    
    No Longer Returned
    ------------------
    int: node id if success
    '''
    result =  HAPIlib.HAPI_CookNode(byref(session), nodeid, byref(cook_option))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(WaitCook(session))
    loop.close()

async def CookNodeAsync(
    session, 
    cook_option, 
    nodeid
    ):
    '''
    Attributes
    ----------
    session : HAPI_Session
    cook_option: HAPI_CookOptions
    nodeid : int 
    
    Parameters
    ----------
    session : TYPE
        Description
    cook_option : TYPE
        Description
    nodeid : TYPE
        Description
    
    No Longer Returned
    ------------------
    int: node id if success
    '''
    result =  HAPIlib.HAPI_CookNode(byref(session), nodeid, byref(cook_option))
    await WaitCook(session)

async def WaitCook(session, statusReportInterval = 1):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    statusReportInterval : int, optional
        Description
    """
    print("-------------Start Cooking!---------------")
    cookStatus = c_int32()
    cookResult = HAPI_Result.HAPI_RESULT_ALREADY_INITIALIZED
    while True:
        cookResult = HAPIlib.HAPI_GetStatus(byref(session), 2, byref(cookStatus))
        continuestate = cookStatus.value > HAPI_State.HAPI_STATE_MAX_READY_STATE and cookResult == HAPI_Result.HAPI_RESULT_SUCCESS
        print("Cook Status at {0} : {1}".format(datetime.now().strftime('%H:%M:%S'), _GetStatusString(session,\
            HAPI_StatusType.HAPI_STATUS_COOK_STATE, HAPI_StatusVerbosity.HAPI_STATUSVERBOSITY_MESSAGES)))
        if not continuestate:
            break
        await asyncio.sleep(statusReportInterval)
    if cookStatus.value == HAPI_State.HAPI_STATE_READY_WITH_FATAL_ERRORS:
        print("Cook with Fatal Error: {0}".format(_GetStatusString(session)))
    print("-------------Finish Cooking!---------------")
    assert cookResult == HAPI_Result.HAPI_RESULT_SUCCESS and cookStatus.value == HAPI_State.HAPI_STATE_READY, "CookNode Failed with {0} and Cook Status is {1}".format(HAPI_Result(cookResult).name, HAPI_State(cookStatus.value).name)

def ComposeChildNodeList(session, nodeid):
    '''
    Attributes
    ----------
    session : HAPI_Session
    nodeid : int
    
    Parameters
    ----------
    session : TYPE
        Description
    nodeid : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    '''
    childCount = c_int32()
    result = HAPIlib.HAPI_ComposeChildNodeList( byref(session), nodeid, c_int(-1), c_int(-1), c_bool(False), byref(childCount))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "ComposeChildNodeList Failed with {0}".format(HAPI_Result(result).name)
    return childCount

def GetNodeInfo(session, nodeid):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    nodeid : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    node_info = HAPI_NodeInfo()
    result = HAPIlib.HAPI_GetNodeInfo( byref(session), nodeid, byref(node_info));
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetNodeInfo Failed with {0}".format(HAPI_Result(result).name)
    return node_info

def GetParameters(session, nodeid, node_info):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    nodeid : TYPE
        Description
    node_info : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    params = (HAPI_ParmInfo * node_info.parmCount)()
    result = HAPIlib.HAPI_GetParameters(byref(session), nodeid,  byref(params), c_int32(0), c_int32(node_info.parmCount))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetParameters Failed with {0}".format(HAPI_Result(result).name)
    return params

def GetParmIntValue(session, nodeid, parmname, tupleid = 0):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    nodeid : TYPE
        Description
    parmname : TYPE
        Description
    tupleid : int, optional
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    val = c_int32()
    result = HAPIlib.HAPI_GetParmIntValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, byref(val))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetParmIntValue Failed with {0}".format(HAPI_Result(result).name)
    return val.value

def GetParmFloatValue(session, nodeid, parmname, tupleid = 0):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    nodeid : TYPE
        Description
    parmname : TYPE
        Description
    tupleid : int, optional
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    val = c_float()
    result = HAPIlib.HAPI_GetParmFloatValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, byref(val))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetParmFloatValue Failed with {0}".format(HAPI_Result(result).name)
    return val.value

def GetParamStringValue(session, nodeid, parmname, tupleid = 0):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    nodeid : TYPE
        Description
    parmname : TYPE
        Description
    tupleid : int, optional
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    stringsh = c_int32()
    result = HAPIlib.HAPI_GetParmStringValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, True, byref(stringsh))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetParamStringValue Failed with {0}".format(HAPI_Result(result).name)
    return GetString(session, stringsh).decode()

def SetParmIntValue(session, nodeid, parmname, value, tupleid = 0):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    nodeid : TYPE
        Description
    parmname : TYPE
        Description
    value : TYPE
        Description
    tupleid : int, optional
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    result = HAPIlib.HAPI_SetParmIntValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, value)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetParmIntValue Failed with {0}".format(HAPI_Result(result).name)
    return

def SetParmFloatValue(session, nodeid, parmname, value,  tupleid = 0):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    nodeid : TYPE
        Description
    parmname : TYPE
        Description
    value : TYPE
        Description
    tupleid : int, optional
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    result = HAPIlib.HAPI_SetParmFloatValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, value)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetParmFloatValue Failed with {0}".format(HAPI_Result(result).name)
    return

def SetParamStringValue(session, nodeid, parmid, value, tupleid = 0):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    nodeid : TYPE
        Description
    parmid : TYPE
        Description
    value : TYPE
        Description
    tupleid : int, optional
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    result = HAPIlib.HAPI_SetParmStringValue(byref(session), nodeid, c_char_p(value.encode('utf-8')), parmid, tupleid)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetParamStringValue Failed with {0}".format(HAPI_Result(result).name)
    return

def SetPartInfo(session, node_id, part_info):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    part_info : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    result = HAPIlib.HAPI_SetPartInfo(byref(session), node_id, 0, byref(part_info))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetPartInfo Failed with {0}".format(HAPI_Result(result).name)
    return

def AddAttribute(session, node_id, name, attrib_info):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    result = HAPIlib.HAPI_AddAttribute(byref(session), node_id, 0, c_char_p(name.encode('utf-8')), byref(attrib_info))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "AddAttribute Failed with {0}".format(HAPI_Result(result).name)
    return

def SetAttributeFloatData(session, node_id, name, attrib_info, data):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    floatp = POINTER(c_float)
    result = HAPIlib.HAPI_SetAttributeFloatData(byref(session), node_id, 0, c_char_p(name.encode('utf-8')), byref(attrib_info), data.flatten().ctypes.data_as(floatp), 0, attrib_info.count)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetAttributeFloatData Failed with {0}".format(HAPI_Result(result).name)
    return

def SetAttributeFloat64Data(session, node_id, name, attrib_info, data):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    floatp = POINTER(c_float64)
    result = HAPIlib.HAPI_SetAttributeFloat64Data(byref(session), node_id, 0, c_char_p(name.encode('utf-8')), byref(attrib_info), data.flatten().ctypes.data_as(floatp), 0, attrib_info.count)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetAttributeFloatData Failed with {0}".format(HAPI_Result(result).name)
    return

def SetAttributeInt64Data(session, node_id, name, attrib_info, data):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    intp = POINTER(c_int64)
    result = HAPIlib.HAPI_SetAttributeInt64Data(byref(session), node_id, 0, c_char_p(name.encode('utf-8')), byref(attrib_info), data.flatten().ctypes.data_as(intp), 0, attrib_info.count)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetAttributeFloatData Failed with {0}".format(HAPI_Result(result).name)
    return

def SetAttributeIntData(session, node_id, name, attrib_info, data):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    intp = POINTER(c_int)
    result = HAPIlib.HAPI_SetAttributeIntData(byref(session), node_id, 0, c_char_p(name.encode('utf-8')), byref(attrib_info), data.flatten().ctypes.data_as(intp), 0, attrib_info.count)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetAttributeFloatData Failed with {0}".format(HAPI_Result(result).name)
    return

def SetAttributeStringData(session, node_id, name, attrib_info, data):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    charp = POINTER(c_char_p)
    result = HAPIlib. HAPI_SetAttributeStringData(byref(session), node_id, 0, c_char_p(name.encode('utf-8')), byref(attrib_info), data.flatten().ctypes.data_as(charp), 0, attrib_info.count)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetAttributeFloatData Failed with {0}".format(HAPI_Result(result).name)
    return

StorageTypeToSetAttrib = {
    HAPI_StorageType.HAPI_STORAGETYPE_INT     : SetAttributeIntData,
    HAPI_StorageType.HAPI_STORAGETYPE_INT64   : SetAttributeInt64Data,
    HAPI_StorageType.HAPI_STORAGETYPE_FLOAT   : SetAttributeFloatData,
    HAPI_StorageType.HAPI_STORAGETYPE_FLOAT64 : SetAttributeFloat64Data,
    HAPI_StorageType.HAPI_STORAGETYPE_STRING  : SetAttributeStringData
    }

def SetVertexList(session, node_id, vertex_list_array):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    vertex_list_array : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    intp = POINTER(c_int)
    result = HAPIlib.HAPI_SetVertexList(byref(session), node_id, 0, vertex_list_array.flatten().ctypes.data_as(intp), 0, np.size(vertex_list_array))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetVertexList Failed with {0}".format(HAPI_Result(result).name)
    return

def SetFaceCounts(session, node_id, face_counts_array):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    face_counts_array : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    intp = POINTER(c_int)
    result = HAPIlib.HAPI_SetFaceCounts(byref(session), node_id, 0, face_counts_array.ctypes.data_as(intp), 0, face_counts_array.shape[0])
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetFaceCounts Failed with {0}".format(HAPI_Result(result).name)
    return

def CommitGeo(session, node_id):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    """
    result = HAPIlib.HAPI_CommitGeo(byref(session), node_id)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "CommitGeo Failed with {0}".format(HAPI_Result(result).name)


def SaveHIPFile(session, hipname, lock_nodes = False):
    '''
    Attributes
    ----------
    session : HAPI_Session
    hipname : string
    lock_nodes : bool
    
    Parameters
    ----------
    session : TYPE
        Description
    hipname : TYPE
        Description
    lock_nodes : bool, optional
        Description
    '''
    result = HAPIlib.HAPI_SaveHIPFile(byref(session),  c_char_p(hipname.encode('utf-8')), c_bool(lock_nodes) ) 
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SaveHIPFile Failed with {0}".format(HAPI_Result(result).name)

def GetCookOptions():
    """Summary
    
    Returns
    -------
    TYPE
        Description
    """
    cookOptions = HAPI_CookOptions()
    cookOptions.splitGeosByGroup              = True
    cookOptions.splitGeosByAttribute          = False
    cookOptions.splitAttrSH                   = 0
    cookOptions.splitPointsByVertexAttributes = False
    cookOptions.cookTemplatedGeos             = True
    cookOptions.maxVerticesPerPrimitive       = 3
    cookOptions.refineCurveToLinear           = True
    cookOptions.curveRefineLOD                = 8
    cookOptions.packedPrimInstancingMode      = 2
    cookOptions.handleBoxPartTypes            = False
    cookOptions.handleSpherePartTypes         = False
    return cookOptions

''' String '''

def _GetStringBufLength(session, string_handle, buffer_length):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    string_handle : TYPE
        Description
    buffer_length : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    return HAPIlib.HAPI_GetStringBufLength(byref(session), string_handle, byref(buffer_length))

def _GetString(session, string_handle, string, length):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    string_handle : TYPE
        Description
    string : TYPE
        Description
    length : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    return HAPIlib.HAPI_GetString(byref(session), string_handle, string, length)

def GetString(session, string_handle):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    string_handle : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    result = ""
    bufferLength = c_int32()
    _GetStringBufLength( session, string_handle, bufferLength);
    buffers = create_string_buffer(bufferLength.value)
    _GetString ( session, string_handle, buffers, bufferLength );

    return buffers.value;

def _GetStatusString(session, status = HAPI_StatusType.HAPI_STATUS_COOK_RESULT, verbosity = HAPI_StatusVerbosity.HAPI_STATUSVERBOSITY_ERRORS):
    """Summary
    
    Parameters
    ----------
    session : TYPE
        Description
    status : TYPE, optional
        Description
    verbosity : TYPE, optional
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    bufferLength = c_int32()
    result = HAPIlib.HAPI_GetStatusStringBufLength(byref(session), status, verbosity, byref(bufferLength))
    buffers = create_string_buffer(bufferLength.value)
    result = HAPIlib.HAPI_GetStatusString(byref(session), status, buffers, bufferLength)
    return buffers.value