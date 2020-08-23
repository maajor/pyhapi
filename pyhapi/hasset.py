# -*- coding: utf-8 -*-
"""Interface for interacting with houdini digital assets (hda)
Author  : Maajor
Email   : info@ma-yidong.com

HAsset:
    Representing an HDA asset

Example usage:

import pyhapi as ph

#create a houdini engine session
session = ph.HSessionManager.get_or_create_default_session()

hda_asset = ph.HAsset(session, "hda/FourShapes.hda")
asset_node = hda_asset.instantiate(node_name="Processor").cook()
"""
from . import hapi as HAPI
from .hnode import HNode

class HAsset():
    """An class representing an HDA asset.

    Attributes:
        instantiated (bool): if this asset has instantiated node
        hda_path (str): Path of this asset
        session (HSession): Session where this asset is loaded
        asset_names ([str]): names of operator in this asset
    """

    def __init__(self, session, hdapath):
        """Initialize

        Args:
            session (int64): The session of Houdini you are interacting with.
            hdapath (str): Path of loading hda
        """
        self.instantiated = False
        self.hda_path = hdapath
        self.session = session
        asset_lib_id = HAPI.load_asset_library_from_file(
            session.hapi_session, self.hda_path)
        self.asset_names = HAPI.get_available_assets(
            session.hapi_session, asset_lib_id)

    def instantiate(self, node_name="Node", operator_id=0):
        """Instantiate an operator in this node

        Args:
            node_name (str, optional): Assign a name for this node. Defaults to "Node".
            operator_id (int, optional): Operator id you want to instantiate in this asset. \
                Defaults to 0.

        Returns:
            HNode: Node instantiated
        """
        node = HNode(self.session, self.asset_names[operator_id], node_name)
        return node

    def get_assets_names(self):
        """Get all operator names in this asset
        """
        return self.asset_names
