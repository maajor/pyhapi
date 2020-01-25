"""Summary
"""
from . import hapi as HAPI
from .hgeo import HGeoMesh

class HNodeBase():
    """[summary]

    Returns:
        [type]: [description]
    """

    def __init__(self, session):
        self.session = session
        self.instantiated = False
        self.node_id = -1
        self.name = ""

    def is_inited(self):
        """Summary

        Returns:
            TYPE: Description
        """
        if not self.instantiated:
            print("Asset Not Instantiated")
        return self.instantiated

    def connect_node_input(self, node_to_connect, input_index=0, output_index=0):
        """Summary

        Args:
            node_to_connect (HNode): Description
            input_index (int, optional): Description
            output_index (int, optional): Description
        """
        HAPI.connect_node_input(self.session.hapi_session,\
            self.node_id, node_to_connect.node_id, input_index, output_index)
        return self

    def disconnect_node_input(self, input_index=0):
        """Summary

        Args:
            node_to_connect (HNode): Description
            input_index (int, optional): Description
            output_index (int, optional): Description
        """
        HAPI.disconnect_node_input(self.session.hapi_session, self.node_id, input_index)
        return self

    def get_node_input(self, input_index=0):
        """[summary]

        Args:
            input_index (int, optional): [description]. Defaults to 0.

        Returns:
            [type]: [description]
        """
        input_node_id = HAPI.query_node_input(self.session.hapi_session, self.node_id, input_index)
        return self.session.get_node(input_node_id)

    def get_child_nodes(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        child_count = HAPI.compose_child_node_list(self.session.hapi_session, self.node_id)
        child_nodes = HAPI.get_composed_child_node_list(self.session.hapi_session,\
             self.node_id, child_count)
        return [self.session.get_node(node_id) for node_id in child_nodes]

    def set_geometry(self, geo):
        """Summary

        Args:
            geo (TYPE): Description
        """
        geo.commit_to_node(self.session, self.node_id)

    def delete(self):
        """Summary
        """
        try:
            HAPI.delete_node(self.session.hapi_session, self.node_id)
            self.instantiated = False
        except AssertionError as error:
            print("HAPI excecution failed")
            print(error)


class HNode(HNodeBase):
    """[summary]

    Returns:
        [type]: [description]
    """
    def __init__(self, session, operator_name, node_name, parent_node=None):
        """Summary

        Args:
            session (TYPE): Description
            operator_name (TYPE): Description
            node_name (TYPE): Description
        """
        super(HNode, self).__init__(session)
        self.node_id = HAPI.create_node(self.session.hapi_session, operator_name, node_name,\
            parent_node_id=parent_node.node_id if parent_node is not None else -1,\
                cook_on_creation=False)
        self.instantiated = True
        self.session.nodes[self.node_id] = self
        self.name = node_name
        self.get_params()

    def get_params(self):
        """Summary
        """
        self.node_info = HAPI.get_node_info(self.session.hapi_session, self.node_id)
        self.param_info = HAPI.get_parameters(\
            self.session.hapi_session, self.node_id, self.node_info)
        self.param_id_dict = {}
        for i in range(0, self.node_info.parmCount):
            namesh = self.param_info[i].labelSH
            namestr = HAPI.get_string(self.session.hapi_session, namesh)
            self.param_id_dict[namestr] = i

    def get_param_value(self, param_name):
        """Summary

        Args:
            param_name (TYPE): Description

        Returns:
            TYPE: Description
        """
        if not self.is_inited():
            return None
        paramid = self.param_id_dict[param_name]
        paraminfo = self.param_info[paramid]
        if paraminfo.IsInt():
            return HAPI.get_param_int_value(self.session.hapi_session, self.node_id, param_name)
        if paraminfo.isFloat():
            return HAPI.get_param_float_value(self.session.hapi_session, self.node_id, param_name)
        if paraminfo.isString():
            return HAPI.get_param_string_value(self.session.hapi_session, self.node_id, param_name)
        return None

    def set_param_value(self, param_name, value):
        """Summary

        Args:
            param_name (TYPE): Description
            value (TYPE): Description

        Returns:
            TYPE: Description
        """
        if not self.is_inited():
            return None
        paramid = self.param_id_dict[param_name]
        paraminfo = self.param_info[paramid]
        if paraminfo.IsInt():
            return HAPI.set_param_int_value(self.session.hapi_session, \
                self.node_id, param_name, value)
        if paraminfo.isFloat():
            return HAPI.set_param_float_value(\
                self.session.hapi_session, self.node_id, param_name, value)
        if paraminfo.isString():
            return HAPI.set_param_string_value(self.session.hapi_session, \
                self.node_id, paramid, value)
        return None

    def get_display_geos(self):
        """[summary]

        Returns:
            [type]: [description]
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
        """[summary]

        Returns:
            [type]: [description]
        """
        if not self.is_inited():
            return None
        HAPI.cook_node(self.session.hapi_session, self.session.cook_option, self.node_id)
        return self

    async def cook_async(self):
        """Summary

        Returns:
            TYPE: Description
        """
        if not self.is_inited():
            return
        await HAPI.cook_node_async(self.session.hapi_session, \
            self.session.cook_option, self.node_id)

    def press_button(self, param_name):
        """Summary

        Args:
            param_name (TYPE): Description

        Returns:
            TYPE: Description
        """
        if not self.is_inited():
            return
        #paramid = self.param_id_dict[param_name]
        #paraminfo = self.param_info[paramid]
        HAPI.set_param_int_value(self.session.hapi_session, self.node_id, param_name, 1)
        HAPI.wait_cook(self.session.hapi_session, 5.0)
        HAPI.set_param_int_value(self.session.hapi_session, self.node_id, param_name, 0)

    async def press_button_async(self, param_name):
        """Summary

        Args:
            param_name (TYPE): Description

        Returns:
            TYPE: Description
        """
        if not self.is_inited():
            return
        #paramid = self.param_id_dict[param_name]
        #paraminfo = self.param_info[paramid]
        HAPI.set_param_int_value(self.session.hapi_session, self.node_id, param_name, 1)
        await HAPI.wait_cook_async(self.session.hapi_session, 5.0)
        HAPI.set_param_int_value(self.session.hapi_session, self.node_id, param_name, 0)

class HInputNode(HNodeBase):

    """Summary

    Attributes:
        HAPISession (TYPE): Description
        Instantiated (bool): Description
        NodeId (TYPE): Description
        Session (TYPE): Description
    """

    def __init__(self, session, node_name):
        """Summary

        Args:
            session (TYPE): Description
            node_name (TYPE): Description
        """
        super(HInputNode, self).__init__(session)
        self.node_id = HAPI.create_input_node(self.session.hapi_session, node_name)
        self.instantiated = True
        self.name = node_name
        self.session.nodes[self.node_id] = self

class HExistingNode(HNodeBase):
    """[summary]

    Args:
        HNodeBase ([type]): [description]
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
