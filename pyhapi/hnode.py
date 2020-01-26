# -*- coding: utf-8 -*-
"""Wrapper for houdini engine's node
Author  : Maajor
Email   : hello_myd@126.com

HNodeBase:
    A base class for houdini engine's node, including shared operation\
        for setting input/output, setting/getting geometry, get node \
            information etc.

HNode:
    A node user created for operator name or hda assets, could get/set\
        params, press button and cook.

HInputNode:
    A node dedicated to marshall geom datas

HExistingNode:
    A node created by hengine itself, such as child node of node instantiated\
        with HNode

Example usage:

import pyhapi as ph

#create houdini engine session
session = ph.HSessionManager.get_or_create_default_session()

#create an inputnode where you can set geometry
geo_inputnode = ph.HInputNode(session, "Cube")

#create an geo sop
another_box = ph.HNode(session, "geo", "ProgrammaticBox", parent_node=asset_node)

#connect input node into geo sop's input
another_box.connect_node_input(geo_inputnode)

#disconnect input node
another_box.disconnect_node_input(0).delete()

"""
from . import hapi as HAPI
from .hgeo import HGeoMesh

class HNodeBase():
    """A base class for houdini engine's node, including shared operation\
        for setting input/output, setting/getting geometry, get node \
            information etc.

    Attributes:
        session (HSession): HEngine session containing this node
        instantiated (bool): instantiated
        node_id (int): Current node id
        name (str): Current node name
    """

    def __init__(self, session):
        self.session = session
        self.instantiated = False
        self.node_id = -1
        self.name = ""

    def is_inited(self):
        """If this node is inited

        Returns:
            bool: If this node is inited
        """
        if not self.instantiated:
            print("Asset Not Instantiated")
        return self.instantiated

    def connect_node_input(self, node_to_connect, input_index=0, output_index=0):
        """Connect another node into this node's input

        Args:
            node_to_connect ([type]): The other node to connect to this node
            input_index (int, optional): This node's input index. Defaults to 0.
            output_index (int, optional): The other node's output index. Defaults to 0.

        Returns:
            HNodeBase: Current node itself
        """
        HAPI.connect_node_input(self.session.hapi_session,\
            self.node_id, node_to_connect.node_id, input_index, output_index)
        return self

    def disconnect_node_input(self, input_index=0):
        """Disconnet this node's input

        Args:
            input_index (int, optional): This node's input index. Defaults to 0.

        Returns:
            HNodeBase: Current node itself
        """
        HAPI.disconnect_node_input(self.session.hapi_session, self.node_id, input_index)
        return self

    def get_node_input(self, input_index=0):
        """Get information of input node

        Args:
            input_index (int, optional): This node's input index. Defaults to 0.

        Returns:
            HNodeBase: Input node
        """
        input_node_id = HAPI.query_node_input(self.session.hapi_session, self.node_id, input_index)
        return self.session.get_node(input_node_id)

    def get_child_nodes(self):
        """Get children node information

        Returns:
            [HNodeBase]: All children node of this node
        """
        child_count = HAPI.compose_child_node_list(self.session.hapi_session, self.node_id)
        child_nodes = HAPI.get_composed_child_node_list(self.session.hapi_session,\
             self.node_id, child_count)
        return [self.session.get_node(node_id) for node_id in child_nodes]

    def set_geometry(self, geo):
        """Set an HGeo to this node

        Args:
            geo (HGeo): Geometry to set into this node
        """
        geo.commit_to_node(self.session, self.node_id)

    def delete(self):
        """Delete current node
        """
        try:
            HAPI.delete_node(self.session.hapi_session, self.node_id)
            self.instantiated = False
        except AssertionError as error:
            print("HAPI excecution failed")
            print(error)


class HNode(HNodeBase):

    """A node user created for operator name or hda assets, could get/set\
        params, press button and cook.
    """
    def __init__(self, session, operator_name, node_name, parent_node=None):
        """Init

        Args:
            session (HSession): Session where this asset is loaded
            operator_name (str): Operator name of this node
            node_name (str): Name of this node
            parent_node (HNodeBase, optional): Parent node. Defaults to None.
        """
        super(HNode, self).__init__(session)
        self.node_id = HAPI.create_node(self.session.hapi_session, operator_name, node_name,\
            parent_node_id=parent_node.node_id if parent_node is not None else -1,\
                cook_on_creation=False)
        self.instantiated = True
        self.session.nodes[self.node_id] = self
        self.name = node_name
        self._get_params()

    def _get_params(self):
        self.node_info = HAPI.get_node_info(self.session.hapi_session, self.node_id)
        self.param_info = HAPI.get_parameters(\
            self.session.hapi_session, self.node_id, self.node_info)
        self.param_id_dict = {}
        for i in range(0, self.node_info.parmCount):
            namesh = self.param_info[i].labelSH
            namestr = HAPI.get_string(self.session.hapi_session, namesh)
            self.param_id_dict[namestr] = i

    def get_parm_value(self, param_name):
        """Get param value

        Args:
            param_name (str): Parameter name to retrieve

        Returns:
            int/float/str: Value of that param, depends on param type
        """
        if not self.is_inited():
            return None
        paramid = self.param_id_dict[param_name]
        paraminfo = self.param_info[paramid]
        if paraminfo.IsInt():
            return HAPI.get_parm_int_value(self.session.hapi_session, self.node_id, param_name)
        if paraminfo.isFloat():
            return HAPI.get_parm_float_value(self.session.hapi_session, self.node_id, param_name)
        if paraminfo.isString():
            return HAPI.get_parm_string_value(self.session.hapi_session, self.node_id, param_name)
        return None

    def set_parm_value(self, param_name, value):
        """Set parameter value

        Args:
            param_name ([type]): Parameter name to set
            value (int/float/str): Value to set to that param, \
                depends on param type

        Returns:
            bool: set successed
        """
        if not self.is_inited():
            return False
        paramid = self.param_id_dict[param_name]
        paraminfo = self.param_info[paramid]
        try:
            if paraminfo.IsInt():
                HAPI.set_parm_int_value(self.session.hapi_session, \
                    self.node_id, param_name, value)
            if paraminfo.isFloat():
                HAPI.set_parm_float_value(\
                    self.session.hapi_session, self.node_id, param_name, value)
            if paraminfo.isString():
                HAPI.set_parm_string_value(self.session.hapi_session, \
                    self.node_id, paramid, value)
            return True
        except AssertionError as error:
            print("HAPI excecution failed")
            print(error)
            return False

    def get_display_geos(self):
        """Get display geo of this node

        Returns:
            [HGeo]: List of geos in this node
        """
        all_geos = []
        #asset_info = HAPI.GetAssetInfo(self.session.HAPISession, self.node_id)
        child_sop_count = HAPI.compose_object_list(self.session.hapi_session, self.node_id)
        child_object_infos = HAPI.get_composed_object_list(self.session.hapi_session,\
            self.node_id, child_sop_count)
        for objectinfo in child_object_infos:
            geo_info = HAPI.get_display_geo_info(self.session.hapi_session, objectinfo.nodeId)
            for part_id in range(0, geo_info.partCount):
                extract_mesh = HGeoMesh()
                extract_mesh.extract_from_sop(self.session, geo_info.nodeId, part_id)
                all_geos.append(extract_mesh)
        return all_geos

    def cook(self):
        """Cook this node in sync/blocking manner

        Returns:
            HNodeBase: Current node itself
        """
        if not self.is_inited():
            return None
        HAPI.cook_node(self.session.hapi_session, self.session.cook_option, self.node_id)
        return self

    async def cook_async(self):
        """Cook this node in async/non-blocking manner

        Returns:
            HNodeBase: Current node itself
        """
        if not self.is_inited():
            return
        await HAPI.cook_node_async(self.session.hapi_session, \
            self.session.cook_option, self.node_id)

    def press_button(self, param_name):
        """Press button in this node in sync/blocking manner

        Args:
            param_name (str): Button name to press
        """
        if not self.is_inited():
            return
        #paramid = self.param_id_dict[param_name]
        #paraminfo = self.param_info[paramid]
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, param_name, 1)
        HAPI.wait_cook(self.session.hapi_session, 5.0)
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, param_name, 0)

    async def press_button_async(self, param_name):
        """Press button in this node in async/non-blocking manner

        Args:
            param_name (str): Button name to press
        """
        if not self.is_inited():
            return
        #paramid = self.param_id_dict[param_name]
        #paraminfo = self.param_info[paramid]
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, param_name, 1)
        await HAPI.wait_cook_async(self.session.hapi_session, 5.0)
        HAPI.set_parm_int_value(self.session.hapi_session, self.node_id, param_name, 0)

class HInputNode(HNodeBase):

    """A node dedicated to marshall geom datas
    """

    def __init__(self, session, node_name):
        super(HInputNode, self).__init__(session)
        self.node_id = HAPI.create_input_node(self.session.hapi_session, node_name)
        self.instantiated = True
        self.name = node_name
        self.session.nodes[self.node_id] = self

class HExistingNode(HNodeBase):
    """A node created by hengine itself, such as child node of node instantiated\
        with HNode
    """

    def __init__(self, session, node_id):
        super(HExistingNode, self).__init__(session)
        self.node_id = node_id
        try:
            self.node_info = HAPI.get_node_info(self.session.hapi_session, self.node_id)
            self.name = HAPI.get_string(self.session.hapi_session, self.node_info.nameSH)
            self.instantiated = True
        except AssertionError as error:
            print("HAPI excecution failed")
            self.instantiated = False
            print(error)
