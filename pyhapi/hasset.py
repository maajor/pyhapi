"""Summary
"""
from . import hapi as HAPI
from .hnode import HNode

class HAsset():
    """Summary

    Returns:
        [type]: [description]
    """

    def __init__(self, session, hdapath):
        """Summary

        Args:
            session (TYPE): Description
            hdapath (TYPE): Description
        """
        self.instantiated = False
        self.hda_path = hdapath
        self.session = session
        asset_lib_id = HAPI.load_asset_library_from_file(
            session.hapi_session, self.hda_path)
        self.asset_names = HAPI.get_available_assets(
            session.hapi_session, asset_lib_id)

    def instantiate(self, node_name="Node", operator_id=0):
        """Summary

        Args:
            node_name (str, optional): Description
            operator_id (int, optional): Description

        Returns:
            TYPE: Description
        """
        node = HNode(self.session, self.asset_names[operator_id], node_name)
        return node

    def get_assets_names(self):
        """[summary]
        """
        return self.asset_names
