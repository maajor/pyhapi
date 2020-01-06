from . import *

def IsSessionValid(session):
    result = HAPIlib.HAPI_IsSessionValid(byref(session))
    return result == HAPI_Result.HAPI_RESULT_SUCCESS

def Cleanup(session):
    result = HAPIlib.HAPI_Cleanup(byref(session))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "Cleanup Failed with {0}".format(HAPI_Result(result).name)


def CloseSession(session):
    result = HAPIlib.HAPI_CloseSession(byref(session))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "Close Session Failed with {0}".format(HAPI_Result(result).name)

def CreateInProcessSession(session):
    '''
    Attributes
    ----------
    session : HAPI_Session

    Returns
    ----------
    bool: success
    '''
    return HAPIlib.HAPI_CreateInProcessSession(byref(session))

def StartThriftNamedPipeServer(serverOptions):
    '''
    Attributes
    ----------
    serverOptions : HAPI_ThriftServerOptions

    Returns
    ----------
    int: process id if success
    '''
    processid = c_int32()
    result = HAPIlib.HAPI_StartThriftNamedPipeServer(byref(serverOptions), c_char_p("hapi".encode('utf-8')), byref(processid))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "StartThriftNamedPipeServer Failed with {0}".format(HAPI_Result(result).name)
    print("Session Created with Process Id: {0}".format(processid.value))
    return processid

def CreateThriftNamedPipeSession(session):
    '''
    Attributes
    ----------
    session : HAPI_Session
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
    Attributes
    ----------
    session : HAPI_Session
    cookOption : HAPI_CookOptions
    use_cooking_thread : bool
    cooking_thread_stack_size : int
    houdini_environment_files : string
    otl_search_path : string 
    dso_search_path : string
    image_dso_search_path : string
    audio_dso_search_path : string
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
    ----------
    int: asset library id if success
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
    ----------
    int: asset count if success
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
    ----------
    string[]: asset names if success
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
    ----------
    int: node id if success
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

    Returns
    ----------
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

    Returns
    ----------
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

    Returns
    ----------
    int: node id if success
    '''
    result =  HAPIlib.HAPI_CookNode(byref(session), nodeid, byref(cook_option))
    await WaitCook(session)

async def WaitCook(session, statusReportInterval = 1):
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
    '''
    childCount = c_int32()
    result = HAPIlib.HAPI_ComposeChildNodeList( byref(session), nodeid, c_int(-1), c_int(-1), c_bool(False), byref(childCount))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "ComposeChildNodeList Failed with {0}".format(HAPI_Result(result).name)
    return childCount

def GetNodeInfo(session, nodeid):
    node_info = HAPI_NodeInfo()
    result = HAPIlib.HAPI_GetNodeInfo( byref(session), nodeid, byref(node_info));
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetNodeInfo Failed with {0}".format(HAPI_Result(result).name)
    return node_info

def GetParameters(session, nodeid, node_info):
    params = (HAPI_ParmInfo * node_info.parmCount)()
    result = HAPIlib.HAPI_GetParameters(byref(session), nodeid,  byref(params), c_int32(0), c_int32(node_info.parmCount))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetParameters Failed with {0}".format(HAPI_Result(result).name)
    return params

def GetParmIntValue(session, nodeid, parmname, tupleid = 0):
    val = c_int32()
    result = HAPIlib.HAPI_GetParmIntValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, byref(val))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetParmIntValue Failed with {0}".format(HAPI_Result(result).name)
    return val.value

def GetParmFloatValue(session, nodeid, parmname, tupleid = 0):
    val = c_float()
    result = HAPIlib.HAPI_GetParmFloatValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, byref(val))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetParmFloatValue Failed with {0}".format(HAPI_Result(result).name)
    return val.value

def GetParamStringValue(session, nodeid, parmname, tupleid = 0):
    stringsh = c_int32()
    result = HAPIlib.HAPI_GetParmStringValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, True, byref(stringsh))
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "GetParamStringValue Failed with {0}".format(HAPI_Result(result).name)
    return GetString(session, stringsh).decode()

def SetParmIntValue(session, nodeid, parmname, value, tupleid = 0):
    result = HAPIlib.HAPI_SetParmIntValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, value)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetParmIntValue Failed with {0}".format(HAPI_Result(result).name)
    return

def SetParmFloatValue(session, nodeid, parmname, value,  tupleid = 0):
    result = HAPIlib.HAPI_SetParmFloatValue(byref(session), nodeid, c_char_p(parmname.encode('utf-8')), tupleid, value)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetParmFloatValue Failed with {0}".format(HAPI_Result(result).name)
    return

def SetParamStringValue(session, nodeid, parmid, value, tupleid = 0):
    result = HAPIlib.HAPI_SetParmStringValue(byref(session), nodeid, c_char_p(value.encode('utf-8')), parmid, tupleid)
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SetParamStringValue Failed with {0}".format(HAPI_Result(result).name)
    return

def SaveHIPFile(session, hipname, lock_nodes = False):
    '''
    Attributes
    ----------
    session : HAPI_Session
    hipname : string
    lock_nodes : bool
    '''
    result = HAPIlib.HAPI_SaveHIPFile(byref(session),  c_char_p(hipname.encode('utf-8')), c_bool(lock_nodes) ) 
    assert result == HAPI_Result.HAPI_RESULT_SUCCESS, "SaveHIPFile Failed with {0}".format(HAPI_Result(result).name)

def GetCookOptions():
    cookOptions = HAPI_CookOptions()
    cookOptions.splitGeosByGroup = True;
    cookOptions.splitGeosByAttribute = False;
    cookOptions.splitAttrSH = 0;
    cookOptions.splitPointsByVertexAttributes = False;

    cookOptions.cookTemplatedGeos = True;
    cookOptions.maxVerticesPerPrimitive = 3;
    cookOptions.refineCurveToLinear = True;
    cookOptions.curveRefineLOD = 8;
    cookOptions.packedPrimInstancingMode = 2;

    cookOptions.handleBoxPartTypes = False;
    cookOptions.handleSpherePartTypes = False;
    return cookOptions

''' String '''

def _GetStringBufLength(session, string_handle, buffer_length):
    return HAPIlib.HAPI_GetStringBufLength(byref(session), string_handle, byref(buffer_length))

def _GetString(session, string_handle, string, length):
    return HAPIlib.HAPI_GetString(byref(session), string_handle, string, length)

def GetString(session, string_handle):
    result = ""
    bufferLength = c_int32()
    _GetStringBufLength( session, string_handle, bufferLength);
    buffers = create_string_buffer(bufferLength.value)
    _GetString ( session, string_handle, buffers, bufferLength );

    return buffers.value;

def _GetStatusString(session, status = HAPI_StatusType.HAPI_STATUS_COOK_RESULT, verbosity = HAPI_StatusVerbosity.HAPI_STATUSVERBOSITY_ERRORS):
    bufferLength = c_int32()
    result = HAPIlib.HAPI_GetStatusStringBufLength(byref(session), status, verbosity, byref(bufferLength))
    buffers = create_string_buffer(bufferLength.value)
    result = HAPIlib.HAPI_GetStatusString(byref(session), status, buffers, bufferLength)
    return buffers.value