# -*- coding: utf-8 -*-
"""Example of connect, disconnect, add node andd delete node
Author  : Maajor
Email   : info@ma-yidong.com
"""
import logging
import pyhapi as ph

def log_childnodes(asset_node):
    """Log node's child nodes name
    Args:
        asset_node (HNodeBase): A node to log its children
    """
    logging.info("Child nodes include: {0}".format(",".join([node.name\
        for node in asset_node.get_child_nodes()])))

def main():
    """Main
    """
    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/FourShapes.hda")
    asset_node = hda_asset.instantiate(node_name="Processor").cook()
    log_childnodes(asset_node)

    #create a sop node, set input
    another_box = ph.HNode(session, "geo", "ProgrammaticBox", parent_node=asset_node)
    input_node = another_box\
    		.connect_node_input(asset_node.get_child_nodes()[0])\
		    .cook()\
		    .get_node_input(0)
    logging.info("ProgrammaticBox's input node is {0}".format(input_node.name))
    log_childnodes(asset_node)

    #delete sop node
    another_box\
    		.disconnect_node_input(0)\
    		.delete()
    log_childnodes(asset_node)

    session.save_hip("modifiedScene.hip")


if __name__ == "__main__":
    main()
