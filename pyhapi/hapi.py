# -*- coding: utf-8 -*-
"""Wrapper for HAPI's APIs.
Author  : Maajor
Email   : hello_myd@126.com
"""
from ctypes import cdll, POINTER, c_int, c_int32, c_int64,\
    c_float, c_double, c_bool, byref, c_char_p, create_string_buffer
import asyncio
from datetime import datetime

import numpy as np

from . import hdata as HDATA

HAPI_LIB = cdll.LoadLibrary("libHAPIL")


def is_session_valid(session):
    """Wrapper for HAPI_IsSessionValid

    Checks whether the session identified by HAPI_Session::id \
        is a valid session opened in the implementation \
            identified by HAPI_Session::type.

    Args:
        session (int64): session id

    Returns:
        bool: if the session is valid
    """
    result = HAPI_LIB.HAPI_IsSessionValid(byref(session))
    return result == HDATA.Result.SUCCESS


def cleanup(session):
    """Wrapper for HAPI_Cleanup

    Clean up memory. \
        This will unload all assets and you will need to call HAPI_Initialize() \
            again to be able to use any HAPI methods again.

    Args:
        session (int64): session id
    """
    result = HAPI_LIB.HAPI_Cleanup(byref(session))
    assert result == HDATA.Result.SUCCESS,\
        "Cleanup Failed with {0}".format(HDATA.Result(result).name)


def close_session(session):
    """Wrapper for HAPI_CloseSession

    Closes a session. If the session has been established using RPC, \
        then the RPC connection is closed.

    Args:
        session (int64): session id
    """
    result = HAPI_LIB.HAPI_CloseSession(byref(session))
    assert result == HDATA.Result.SUCCESS,\
        "Close Session Failed with {0}".format(HDATA.Result(result).name)

def start_thrift_named_pipe_server(server_options):
    """Wrapper for HAPI_StartThriftNamedPipeServer

    Starts a Thrift RPC server process on the local host serving clients \
    on a Windows named pipe or a Unix domain socket and waits for it to start serving. \
        It is safe to create an RPC session using the specified pipe or \
            socket after this call succeeds.

    Args:
        server_options (ThriftServerOptions): server's option for start

    Returns:
        int: session id
    """
    processid = c_int32()
    result = HAPI_LIB.HAPI_StartThriftNamedPipeServer(
        byref(server_options), c_char_p("hapi".encode('utf-8')), byref(processid))
    assert result == HDATA.Result.SUCCESS,\
        "StartThriftNamedPipeServer Failed with {0}".format(
            HDATA.Result(result).name)
    print("Session Created with Process Id: {0}".format(processid.value))
    return processid


def create_thrift_named_pipe_session(session):
    """Wrapper for HAPI_CreateThriftNamedPipeSession
    Creates a Thrift RPC session using a Windows named 、
    pipe or a Unix domain socket as transport.

    Args:
        session (int64): session id
    """
    result = HAPI_LIB.HAPI_CreateThriftNamedPipeSession(
        byref(session), c_char_p("hapi".encode('utf-8')))
    assert result == HDATA.Result.SUCCESS,\
        "CreateThriftNamedPipeSession Failed with {0}".format(
            HDATA.Result(result).name)


def initialize(session, cook_option, use_cooking_thread=True,\
    cooking_thread_stack_size=-1, houdini_environment_files="",\
    otl_search_path="", dso_search_path="",\
    image_dso_search_path="", audio_dso_search_path=""):
    """Wrapper for HAPI_Initialize

    Create the asset manager, set up environment variables, \
        and initialize the main Houdini scene. No license checking is during this step. \
            Only when you try to load an asset library (OTL) do we actually check for licenses.

    Args:
        session (int64): session id
        cook_option (CookOption): option for node cook
        use_cooking_thread (bool, optional): Use a separate thread for cooking of assets.\
             This allows for asynchronous cooking and larger stack size.. Defaults to True.
        cooking_thread_stack_size (int, optional): Set the stack size of the cooking thread.\
             Use -1 to set the stack size to the Houdini default. This value is in bytes. \
                 Defaults to -1.
        houdini_environment_files (str, optional): A list of paths,\
             separated by a ";" on Windows and a ":" on Linux and Mac,\
                  to .env files that follow the same syntax as the houdini.env file in Houdini's \
                      user prefs folder.These will be applied after the default houdini.env file \
                          and will overwrite the process' environment variable values. You an use \
                              this to enforce a stricter environment when running engine. \
                                  For more info, see: \
                                      http://www.sidefx.com/docs/houdini/basics/config_env. \
                                          Defaults to "".
        otl_search_path (str, optional): The directory where OTLs are searched for. \
            You can pass NULL here which will only use the default Houdini OTL search paths. \
                You can also pass in multiple paths separated by a ";" on Windows and a ":" \
                    on Linux and Mac. \
                    If something other than NULL is passed the default Houdini search paths \
                        will be appended to the end of the path string.. Defaults to "".
        dso_search_path (str, optional): The directory where generic DSOs (custom plugins) \
            are searched for. You can pass NULL here which will only use the default Houdini \
                DSO search paths. \
                You can also pass in multiple paths separated by a ";" on Windows and a ":" \
                    on Linux and Mac. \
                    If something other than NULL is passed the default Houdini search paths \
                        will be appended to the end of the path string.. Defaults to "".
        image_dso_search_path (str, optional): The directory where image DSOs (custom plugins) \
            are searched for. \
            You can pass NULL here which will only use the default Houdini DSO search paths. \
                You can also pass in multiple paths separated by a ";" on Windows and a ":" \
                    on Linux and Mac. If something other than NULL is passed the default Houdini \
                        search paths will be appended to the end of the path string.. \
                            Defaults to "".
        audio_dso_search_path (str, optional): The directory where audio DSOs (custom plugins)\
            are searched for. You can pass NULL here which will only use the default Houdini \
                DSO search paths. You can also pass in multiple paths separated by a ";" \
                    on Windows and a ":" on Linux and Mac. If something other than NULL \
                        is passed the default Houdini search paths will be appended to \
                            the end of the path string.. Defaults to "".
    """
    result = HAPI_LIB.HAPI_Initialize(
        byref(session),
        byref(cook_option),
        c_bool(use_cooking_thread),
        c_int32(cooking_thread_stack_size),
        c_char_p(houdini_environment_files.encode('utf-8')),
        c_char_p(otl_search_path.encode('utf-8')),
        c_char_p(dso_search_path.encode('utf-8')),
        c_char_p(image_dso_search_path.encode('utf-8')),
        c_char_p(audio_dso_search_path.encode('utf-8')))
    assert result in (HDATA.Result.SUCCESS,
                      HDATA.Result.ALREADY_INITIALIZED),\
        "Initialize Failed with {0}".format(HDATA.Result(result).name)


def load_asset_library_from_file(session, file_path, allow_overwrite=True):
    """Wrapper for HAPI_LoadAssetLibraryFromFile

    Loads a Houdini asset library (OTL) from a .otl file. \
        It does NOT create anything inside the Houdini scene.

    Args:
        session (int64): The session of Houdini you are interacting with.
        file_path (str): Absolute path to the .otl file.
        allow_overwrite (bool, optional): With this true, if the library file being \
            loaded contains asset definitions that have already been loaded they will \
                overwrite the existing definitions. . Defaults to True.

    Returns:
        int: Newly loaded otl id to be used
    """
    asset_lib_id = c_int32()
    result = HAPI_LIB.HAPI_LoadAssetLibraryFromFile(
        byref(session), c_char_p(file_path.encode('utf-8')),
        c_bool(allow_overwrite), byref(asset_lib_id))
    assert result == HDATA.Result.SUCCESS,\
        "LoadAssetLibraryFromFile Failed with {0}".format(
            HDATA.Result(result).name)
    return asset_lib_id


def _get_available_asset_count(session, asset_lib_id):
    asset_count = c_int32()
    result = HAPI_LIB.HAPI_GetAvailableAssetCount(
        byref(session), asset_lib_id, byref(asset_count))
    assert result == HDATA.Result.SUCCESS,\
        "GetAvailableAssetCount Failed with {0}".format(
            HDATA.Result(result).name)
    return asset_count


def get_available_assets(session, asset_lib_id):
    """Get the names of the assets contained in an asset library.
    The asset names will contain additional information about the type of asset, \
        namespace, and version, along with the actual asset name. \
            For example, if you have an Object type asset, in the "hapi" namespace, \
                of version 2.0, named "foo", the asset name returned here \
                    will be: hapi::Object/foo::2.0

    Args:
        session (int64): The session of Houdini you are interacting with.
        asset_lib_id (int): Newly loaded otl id to be used

    Returns:
        list(str): names of available assets name
    """
    asset_count = _get_available_asset_count(session, asset_lib_id)

    asset_string_buffer = (c_int32 * asset_count.value)()

    result = HAPI_LIB.HAPI_GetAvailableAssets(
        byref(session), asset_lib_id, byref(asset_string_buffer), asset_count)
    assert result == HDATA.Result.SUCCESS,\
        "GetAvailableAssets Failed with {0}".format(
            HDATA.Result(result).name)

    asset_names = []
    for buffer in asset_string_buffer:
        asset_name = get_string(session, buffer)
        asset_names.append(asset_name)

    return asset_names


def create_input_node(session, node_label):
    """Wrapper for HAPI_CreateInputNode
    Creates a simple geometry SOP node that can accept geometry input.
    This will create a dummy OBJ node with a Null SOP inside that you can set
    the geometry of using the geometry SET APIs.
    You can then connect this node to any other node as a geometry input.

    Args:
        session (int64): The session of Houdini you are interacting with.
        node_label ( str): Give this input node a name for easy debugging. \
            The node's parent OBJ node and the Null SOP node will both get \
                this given name with "input_" prepended. You can also pass \
                    NULL in which case the name will be "input#" where # is \
                    some number.

    Returns:
        int : Newly created node's id
    """
    node_id = c_int32()
    result = HAPI_LIB.HAPI_CreateInputNode(
        byref(session), byref(node_id), c_char_p(node_label.encode('utf-8')))
    assert result == HDATA.Result.SUCCESS,\
        "CreateInputNode Failed with {0}".format(
            HDATA.Result(result).name)
    return node_id.value


def create_node(session, operator_name, node_label="", parent_node_id=-1, cook_on_creation=False):
    """Wrapper for HAPI_CreateNode
    Create a node inside a node network. \
        Nodes created this way will have their HAPI_NodeInfo::createdPostAssetLoad \
            set to true.

    Args:
        session (int64): The session of Houdini you are interacting with.
        operator_name (str): The name of the node operator type.
        node_label (str, optional): The label of the newly created node. Defaults to "".
        parent_node_id (int, optional): [description]. Defaults to -1.
        cook_on_creation (bool, optional): [description]. Defaults to False.

    Returns:
        int: The returned node id of the just-created node.
    """
    node_id = c_int32()
    result = HAPI_LIB.HAPI_CreateNode(
        byref(session), c_int(parent_node_id), c_char_p(
            operator_name.encode('utf-8')),
        c_char_p(node_label.encode('utf-8')), c_bool(cook_on_creation), byref(node_id))
    assert result == HDATA.Result.SUCCESS,\
        "CreateNode Failed with {0}".format(HDATA.Result(result).name)
    return node_id.value


def delete_node(session, node_id):
    """Wrapper for HAPI_DeleteNode
    Delete a node from a node network.\
         Only nodes with their HAPI_NodeInfo::createdPostAssetLoad \
             set to true can be deleted this way.
    Args:
        session (int64): The session of Houdini you are interacting with.
        node_id (int): The node to delete.
    """
    result = HAPI_LIB.HAPI_DeleteNode(byref(session), node_id)
    assert result == HDATA.Result.SUCCESS,\
        "DeleteNode Failed with {0}".format(HDATA.Result(result).name)


def cook_node(session, cook_option, node_id):
    """Wrapper for HAPI_CookNode, a sync/blocking call
    Initiate a cook on this node. \
        Note that this may trigger cooks on other nodes if they are connected.

    Args:
        session (int64): The session of Houdini you are interacting with.
        cook_option (CookOption): option for node cook
        node_id (int): The node to cook.
    """
    result = HAPI_LIB.HAPI_CookNode(
        byref(session), node_id, byref(cook_option))
    assert result == HDATA.Result.SUCCESS,\
        "CookNode Failed with {0}".format(HDATA.Result(result).name)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_cook_async(session))


async def cook_node_async(session, cook_option, node_id):
    """Wrapper for HAPI_CookNode, an async call
    Initiate a cook on this node. \
        Note that this may trigger cooks on other nodes if they are connected.

    Args:
        session (int64): The session of Houdini you are interacting with.
        cook_option (CookOption): option for node cook
        node_id (int): The node to cook.
    """
    result = HAPI_LIB.HAPI_CookNode(
        byref(session), node_id, byref(cook_option))
    assert result == HDATA.Result.SUCCESS,\
        "CookNodeAsync Failed with {0}".format(HDATA.Result(result).name)
    await wait_cook_async(session)

def wait_cook(session, status_report_interval=1):
    """An sync call to wait for cooking return result

    Args:
        session (int64): The session of Houdini you are interacting with.
        status_report_interval (int, optional): time interval in seconds to query cook status. \
            Defaults to 1.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_cook_async(session, status_report_interval))

async def wait_cook_async(session, status_report_interval=1):
    """An async call to wait for cooking return result

    Args:
        session (int64): The session of Houdini you are interacting with.
        status_report_interval (int, optional): time interval in seconds to query cook status. \
            Defaults to 1.
    """
    print("-------------Start Cooking!---------------")
    cook_status = c_int32()
    cook_result = HDATA.Result.ALREADY_INITIALIZED
    while True:
        cook_result = HAPI_LIB.HAPI_GetStatus(
            byref(session), 2, byref(cook_status))
        continuestate = cook_status.value > HDATA.State.MAX_READY_STATE\
            and cook_result == HDATA.Result.SUCCESS
        print("Cook Status at {0} : {1}".format(datetime.now().\
            strftime('%H:%M:%S'), _get_status_string(session,\
                HDATA.StatusType.COOK_STATE,\
                    HDATA.StatusVerbosity.MESSAGES)))
        if not continuestate:
            break
        await asyncio.sleep(status_report_interval)
    if cook_status.value == HDATA.State.READY_WITH_FATAL_ERRORS:
        print("Cook with Fatal Error: {0}".format(_get_status_string(session)))
    print("-------------Finish Cooking!---------------")
    assert cook_result == HDATA.Result.SUCCESS and\
        cook_status.value == HDATA.State.READY,\
        "CookNode Failed with {0} and Cook Status is {1}".\
        format(HDATA.Result(cook_result).name,
               HDATA.State(cook_status.value).name)

def query_node_input(session, node_id, input_index=0):
    """Wrapper for HAPI_QueryNodeInput
    Query which node is connected to another node's input.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to cook.
        input_index (int, optional): [description]. Defaults to 0.

    Returns:
        int: The node id of connection
    """
    connect_node_id = c_int32()
    result = HAPI_LIB.HAPI_QueryNodeInput(
        byref(session), c_int(node_id), c_int(input_index), byref(connect_node_id))
    assert result == HDATA.Result.SUCCESS,\
        "QueryNodeInput Failed with {0}".format(HDATA.Result(result).name)
    return connect_node_id.value


def connect_node_input(session, node_id, node_id_to_connect, input_index=0, output_index=0):
    """Wrapper for HAPI_ConnectNodeInput
    Connect two nodes together.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to connect.
        node_id_to_connect (int): The node to connect to node_id's input.
        input_index (int, optional): The input index. Defaults to 0.
        output_index (int, optional): The output index. Defaults to 0.
    """
    result = HAPI_LIB.HAPI_ConnectNodeInput(
        byref(session), c_int(node_id), c_int(input_index),
        c_int(node_id_to_connect), c_int(output_index))
    assert result == HDATA.Result.SUCCESS,\
        "ConnectNodeInput Failed with {0}".format(
            HDATA.Result(result).name)


def disconnect_node_input(session, node_id, input_index=0):
    """Wrapper for HAPI_DisconnectNodeInput
    Disconnect a node input.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to disconnect.
        input_index (int, optional): The input index to disconnect. Defaults to 0.
    """
    result = HAPI_LIB.HAPI_DisconnectNodeInput(
        byref(session), c_int(node_id), c_int(input_index))
    assert result == HDATA.Result.SUCCESS,\
        "DisconnectNodeInput Failed with {0}".format(
            HDATA.Result(result).name)


def get_composed_child_node_list(session, node_id, count):
    """Wrapper for HAPI_GetComposedChildNodeList
    Get the composed list of child node ids from the previous call to HAPI_ComposeChildNodeList().

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to get.
        count (int): The number of children in the composed list

    Returns:
        list(int): The array of node id for the child nodes.
    """
    id_buffer = (c_int32 * count)()
    result = HAPI_LIB.HAPI_GetComposedChildNodeList(
        byref(session), node_id, byref(id_buffer), c_int(count))
    assert result == HDATA.Result.SUCCESS,\
        "GetComposedChildNodeList Failed with {0}".format(
            HDATA.Result(result).name)
    return id_buffer


def compose_child_node_list(session, node_id, node_type=HDATA.NodeType.ANY,\
    node_flag=HDATA.NodeFlags.ANY):
    """Wrapper for HAPI_ComposeChildNodeList
    Compose a list of child nodes based on given filters.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to get.
        node_type (NodeType, optional): The node type by which to filter the children. \
            Defaults to HDATA.NodeType.ANY.
        node_flag (NodeFlags, optional): The node flags by which to filter the children. \
            Defaults to HDATA.NodeFlags.ANY.
    """
    child_count = c_int32()
    result = HAPI_LIB.HAPI_ComposeChildNodeList(
        byref(session), node_id, c_int(node_type), c_int(node_flag),
        c_bool(False), byref(child_count))
    assert result == HDATA.Result.SUCCESS,\
        "ComposeChildNodeList Failed with {0}".format(
            HDATA.Result(result).name)
    return child_count.value


def get_display_geo_info(session, node_id):
    """Wrapper for HAPI_GetDisplayGeoInfo
    Get the display geo (SOP) node inside an Object node. \
        If there there are multiple display SOP nodes, only the first one is returned. \
            If the node is a display SOP itself, even if a network, \
                it will return its own geo info. If the node is a SOP \
                    but not a network and not the display SOP, this function will fail.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to get.

    Returns:
        GeoInfo: the geoinfo of queried node
    """
    geo_info = HDATA.GeoInfo()
    result = HAPI_LIB.HAPI_GetDisplayGeoInfo(
        byref(session), node_id, byref(geo_info))
    assert result == HDATA.Result.SUCCESS,\
        "GetDisplayGeoInfo Failed with {0}".format(
            HDATA.Result(result).name)
    return geo_info


def get_part_info(session, node_id, part_id):
    """Wrapper for HAPI_GetPartInfo
    Get a particular part info struct.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to get.
        part_id (int): The part id.

    Returns:
        PartInfo: the partinfo of queried node
    """
    part_info = HDATA.PartInfo()
    result = HAPI_LIB.HAPI_GetPartInfo(
        byref(session), node_id, part_id, byref(part_info))
    assert result == HDATA.Result.SUCCESS,\
        "GetPartInfo Failed with {0}".format(HDATA.Result(result).name)
    return part_info


def get_composed_object_list(session, node_id, count):
    """Wrapper for HAPI_GetComposedObjectList
    Fill an array of HAPI_ObjectInfo structs.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to get.
        count (int): The number of children in the list

    Returns:
        list(ObjectInfo): Array of ObjectInfo of querying
    """
    object_info_buffer = (HDATA.ObjectInfo * count)()
    result = HAPI_LIB.HAPI_GetComposedObjectList(
        byref(session), node_id, byref(object_info_buffer),
        c_int(0), c_int(count))
    assert result == HDATA.Result.SUCCESS,\
        "GetComposedObjectList Failed with {0}".format(
            HDATA.Result(result).name)
    return object_info_buffer


def compose_object_list(session, node_id):
    """Wrapper for HAPI_ComposeObjectList
    Compose a list of child object nodes given a parent node id.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to get.

    Returns:
        int: child count of querying node
    """
    child_count = c_int32()
    result = HAPI_LIB.HAPI_ComposeObjectList(
        byref(session), node_id, None, byref(child_count))
    assert result == HDATA.Result.SUCCESS,\
        "ComposeObjectList Failed with {0}".format(
            HDATA.Result(result).name)
    return child_count.value


def get_node_info(session, node_id):
    """Wrapper for HAPI_GetNodeInfo
    Fill an NodeInfo struct.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to get.

    Returns:
        NodeInfo: NodeInfo of querying node
    """
    node_info = HDATA.NodeInfo()
    result = HAPI_LIB.HAPI_GetNodeInfo(
        byref(session), node_id, byref(node_info))
    assert result == HDATA.Result.SUCCESS,\
        "GetNodeInfo Failed with {0}".format(HDATA.Result(result).name)
    return node_info


def get_asset_info(session, node_id):
    """Wrapper for HAPI_GetAssetInfo
    Fill an AssetInfo struct from a node.

    Args:
        session (int): The session of Houdini you are interacting with.
        node_id (int): The node to get.

    Returns:
        AssetInfo: AssetInfo of querying node
    """
    asset_info = HDATA.AssetInfo()
    result = HAPI_LIB.HAPI_GetAssetInfo(
        byref(session), c_int(node_id), byref(asset_info))
    assert result == HDATA.Result.SUCCESS,\
        "GetAssetInfo Failed with {0}".format(HDATA.Result(result).name)
    return asset_info


def get_parameters(session, node_id, node_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        node_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    params = (HDATA.ParmInfo * node_info.parmCount)()
    result = HAPI_LIB.HAPI_GetParameters(
        byref(session), node_id, byref(params), c_int32(0), c_int32(node_info.parmCount))
    assert result == HDATA.Result.SUCCESS,\
        "GetParameters Failed with {0}".format(HDATA.Result(result).name)
    return params


def get_param_int_value(session, node_id, parmname, tupleid=0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
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
    result = HAPI_LIB.HAPI_GetParmIntValue(
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, byref(val))
    assert result == HDATA.Result.SUCCESS,\
        "GetParmIntValue Failed with {0}".format(
            HDATA.Result(result).name)
    return val.value


def get_param_float_value(session, node_id, parmname, tupleid=0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
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
    result = HAPI_LIB.HAPI_GetParmFloatValue(
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, byref(val))
    assert result == HDATA.Result.SUCCESS,\
        "GetParmFloatValue Failed with {0}".format(
            HDATA.Result(result).name)
    return val.value


def get_param_string_value(session, node_id, parmname, tupleid=0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
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
    result = HAPI_LIB.HAPI_GetParmStringValue(
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, True, byref(stringsh))
    assert result == HDATA.Result.SUCCESS,\
        "GetParamStringValue Failed with {0}".format(
            HDATA.Result(result).name)
    return get_string(session, stringsh)


def set_param_int_value(session, node_id, parmname, value, tupleid=0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
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
    result = HAPI_LIB.HAPI_SetParmIntValue(
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, value)
    assert result == HDATA.Result.SUCCESS,\
        "SetParmIntValue Failed with {0}".format(
            HDATA.Result(result).name)


def set_param_float_value(session, node_id, parmname, value, tupleid=0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
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
    result = HAPI_LIB.HAPI_SetParmFloatValue(
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, value)
    assert result == HDATA.Result.SUCCESS,\
        "SetParmFloatValue Failed with {0}".format(
            HDATA.Result(result).name)


def set_param_string_value(session, node_id, parmid, value, tupleid=0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
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
    result = HAPI_LIB.HAPI_SetParmStringValue(
        byref(session), node_id, c_char_p(value.encode('utf-8')), parmid, tupleid)
    assert result == HDATA.Result.SUCCESS,\
        "SetParamStringValue Failed with {0}".format(
            HDATA.Result(result).name)


def set_part_info(session, node_id, part_info):
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
    result = HAPI_LIB.HAPI_SetPartInfo(
        byref(session), node_id, 0, byref(part_info))
    assert result == HDATA.Result.SUCCESS,\
        "SetPartInfo Failed with {0}".format(HDATA.Result(result).name)


def set_curve_info(session, node_id, curve_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        curve_info ([type]): [description]
    """
    result = HAPI_LIB.HAPI_SetCurveInfo(
        byref(session), node_id, 0, byref(curve_info))
    assert result == HDATA.Result.SUCCESS,\
        "SetCurveInfo Failed with {0}".format(HDATA.Result(result).name)


def set_curve_counts(session, node_id, part_id, curve_count):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        curve_count ([type]): [description]
    """
    intp = POINTER(c_int)
    result = HAPI_LIB.HAPI_SetCurveCounts(
        byref(session), node_id, part_id,
        curve_count.flatten().ctypes.data_as(intp), 0, curve_count.shape[0])
    assert result == HDATA.Result.SUCCESS,\
        "SetCurveCounts Failed with {0}".format(HDATA.Result(result).name)


def set_curve_knots(session, node_id, part_id, curve_knots):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        curve_knots ([type]): [description]
    """
    if not isinstance(curve_knots, np.ndarray):
        return
    intp = POINTER(c_int)
    result = HAPI_LIB.HAPI_SetCurveKnots(
        byref(session), node_id, part_id,
        curve_knots.flatten().ctypes.data_as(intp), 0, curve_knots.shape[0])
    assert result == HDATA.Result.SUCCESS,\
        "SetCurveKnots Failed with {0}".format(HDATA.Result(result).name)
    return


def add_attribute(session, node_id, name, attrib_info):
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
    result = HAPI_LIB.HAPI_AddAttribute(
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')), byref(attrib_info))
    assert result == HDATA.Result.SUCCESS,\
        "AddAttribute Failed with {0}".format(HDATA.Result(result).name)


def set_attribute_float_data(session, node_id, name, attrib_info, data):
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
    result = HAPI_LIB.HAPI_SetAttributeFloatData(
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),
        byref(attrib_info), data.flatten().ctypes.data_as(floatp), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(
            HDATA.Result(result).name)


def set_attribute_float64_data(session, node_id, name, attrib_info, data):
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
    floatp = POINTER(c_double)
    result = HAPI_LIB.HAPI_SetAttributeFloat64Data(
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),
        byref(attrib_info), data.flatten().ctypes.data_as(floatp), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(
            HDATA.Result(result).name)


def set_attribute_int64_data(session, node_id, name, attrib_info, data):
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
    result = HAPI_LIB.HAPI_SetAttributeInt64Data(
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),
        byref(attrib_info), data.flatten().ctypes.data_as(intp), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(
            HDATA.Result(result).name)


def set_attribute_int_data(session, node_id, name, attrib_info, data):
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
    result = HAPI_LIB.HAPI_SetAttributeIntData(
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),
        byref(attrib_info), data.flatten().ctypes.data_as(intp), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(
            HDATA.Result(result).name)


def set_attribute_string_data(session, node_id, name, attrib_info, data):
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
    result = HAPI_LIB. HAPI_SetAttributeStringData(
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),
        byref(attrib_info), data.flatten().ctypes.data_as(charp), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(
            HDATA.Result(result).name)


STORAGE_TYPE_TO_SET_ATTRIB = {
    HDATA.StorageType.INT: set_attribute_int_data,
    HDATA.StorageType.INT64: set_attribute_int64_data,
    HDATA.StorageType.FLOAT: set_attribute_float_data,
    HDATA.StorageType.FLOAT64: set_attribute_float64_data,
    HDATA.StorageType.STRING: set_attribute_string_data
}


def get_attribute_names(session, node_id, part_info,\
    attrib_type=HDATA.AttributeOwner.POINT):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_info ([type]): [description]
        attrib_type ([type], optional): [description].

    Returns:
        [type]: [description]
    """
    attrib_count = part_info.attributeCounts[attrib_type]
    string_handle_buffer = (c_int32 * attrib_count)()
    result = HAPI_LIB. HAPI_GetAttributeNames(
        byref(session), node_id, part_info.id, attrib_type,
        byref(string_handle_buffer), attrib_count)
    assert result == HDATA.Result.SUCCESS,\
        "GetAttributeNames Failed with {0}".format(
            HDATA.Result(result).name)
    attrib_names = []
    for string_handle in string_handle_buffer:
        attrib_names.append(get_string(session, string_handle))
    return attrib_names


def get_attribute_info(session, node_id, part_id, name, attrib_type):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_type ([type]): [description]

    Returns:
        [type]: [description]
    """
    attrib_info = HDATA.AttributeInfo()
    result = HAPI_LIB.HAPI_GetAttributeInfo(
        byref(session), c_int(node_id), c_int(part_id),
        c_char_p(name.encode('utf-8')), attrib_type, byref(attrib_info))
    assert result == HDATA.Result.SUCCESS,\
        "GetAttributeInfo Failed with {0}".format(
            HDATA.Result(result).name)
    return attrib_info


def get_attribute_int_data(session, node_id, part_id, name, attrib_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_buffer = (c_int32 * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),
        byref(attrib_info), -1, byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "GetAttributeIntData Failed with {0}".format(
            HDATA.Result(result).name)
    data_np = np.frombuffer(data_buffer, np.int32)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))


def get_attribute_int64_data(session, node_id, part_id, name, attrib_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_buffer = (c_int64 * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),
        byref(attrib_info), -1, byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "GetAttributeInt64Data Failed with {0}".format(
            HDATA.Result(result).name)
    data_np = np.frombuffer(data_buffer, np.int64)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))


def get_attribute_float_data(session, node_id, part_id, name, attrib_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_buffer = (c_float * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),
        byref(attrib_info), -1, byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "GetAttributeFloatData Failed with {0}".format(
            HDATA.Result(result).name)
    data_np = np.frombuffer(data_buffer, np.float32)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))


def get_attribute_float64_data(session, node_id, part_id, name, attrib_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_buffer = (c_double * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),
        byref(attrib_info), -1, byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "GetAttributeFloat64Data Failed with {0}".format(
            HDATA.Result(result).name)
    data_np = np.frombuffer(data_buffer, np.float64)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))


def get_attribute_string_data(session, node_id, part_id, name, attrib_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_buffer = (c_char_p * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),
        byref(attrib_info), -1, byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.Result.SUCCESS,\
        "GetAttributeStringData Failed with {0}".format(
            HDATA.Result(result).name)
    data_np = np.frombuffer(data_buffer, np.bytes_)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))


STORAGE_TYPE_TO_GET_ATTRIB = {
    HDATA.StorageType.INT: get_attribute_int_data,
    HDATA.StorageType.INT64: get_attribute_int64_data,
    HDATA.StorageType.FLOAT: get_attribute_float_data,
    HDATA.StorageType.FLOAT64: get_attribute_float64_data,
    HDATA.StorageType.STRING: get_attribute_string_data
}


def set_vertex_list(session, node_id, vertex_list_array):
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
    result = HAPI_LIB.HAPI_SetVertexList(
        byref(session), node_id, 0, vertex_list_array.flatten().ctypes.data_as(intp),
        0, np.size(vertex_list_array))
    assert result == HDATA.Result.SUCCESS,\
        "SetVertexList Failed with {0}".format(HDATA.Result(result).name)


def set_face_counts(session, node_id, face_counts_array):
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
    result = HAPI_LIB.HAPI_SetFaceCounts(
        byref(session), node_id, 0, face_counts_array.ctypes.data_as(intp),
        0, face_counts_array.shape[0])
    assert result == HDATA.Result.SUCCESS,\
        "SetFaceCounts Failed with {0}".format(HDATA.Result(result).name)


def commit_geo(session, node_id):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    """
    result = HAPI_LIB.HAPI_CommitGeo(byref(session), node_id)
    assert result == HDATA.Result.SUCCESS,\
        "CommitGeo Failed with {0}".format(HDATA.Result(result).name)


def save_hip_file(session, hipname, lock_nodes=False):
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
    result = HAPI_LIB.HAPI_SaveHIPFile(
        byref(session), c_char_p(hipname.encode('utf-8')), c_bool(lock_nodes))
    assert result == HDATA.Result.SUCCESS,\
        "SaveHIPFile Failed with {0}".format(HDATA.Result(result).name)


def get_cook_options():
    """Summary

    Returns
    -------
    TYPE
        Description
    """
    cook_options = HDATA.CookOptions()
    cook_options.splitGeosByGroup = True
    cook_options.splitGeosByAttribute = False
    cook_options.splitAttrSH = 0
    cook_options.splitPointsByVertexAttributes = False
    cook_options.cookTemplatedGeos = True
    cook_options.maxVerticesPerPrimitive = 3
    cook_options.refineCurveToLinear = True
    cook_options.curveRefineLOD = 8
    cook_options.packedPrimInstancingMode = 2
    cook_options.handleBoxPartTypes = False
    cook_options.handleSpherePartTypes = False
    return cook_options


def _get_string_buf_length(session, string_handle, buffer_length):
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
    return HAPI_LIB.HAPI_GetStringBufLength(byref(session), string_handle, byref(buffer_length))


def _get_string(session, string_handle, string, length):
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
    return HAPI_LIB.HAPI_GetString(byref(session), string_handle, string, length)


def get_string(session, string_handle):
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
    buffer_length = c_int32()
    _get_string_buf_length(session, string_handle, buffer_length)
    buffers = create_string_buffer(buffer_length.value)
    _get_string(session, string_handle, buffers, buffer_length)

    return buffers.value.decode()


def _get_status_string(session, status=HDATA.StatusType.COOK_RESULT,\
    verbosity=HDATA.StatusVerbosity.ERRORS):
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
    buffer_length = c_int32()
    result = HAPI_LIB.HAPI_GetStatusStringBufLength(
        byref(session), status, verbosity, byref(buffer_length))
    assert result == HDATA.Result.SUCCESS,\
        "GetStatusStringBufLength Failed with {0}".format(
            HDATA.Result(result).name)
    buffers = create_string_buffer(buffer_length.value)
    result = HAPI_LIB.HAPI_GetStatusString(
        byref(session), status, buffers, buffer_length)
    assert result == HDATA.Result.SUCCESS,\
        "GetStatusString Failed with {0}".format(
            HDATA.Result(result).name)
    return buffers.value
