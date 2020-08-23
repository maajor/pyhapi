# -*- coding: utf-8 -*-
"""Example of getting/setting params of HDA asset
Author  : Maajor
Email   : info@ma-yidong.com
"""
import logging
import pyhapi as ph

def main():
    """Main
    """
    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/SideFX_spaceship.otl")
    asset_node = hda_asset.instantiate(node_name="Spaceship")

    #Query node's parameters
    logging.info("Node has parameter count: {0}".format(len(asset_node.get_param_names())))
    for name in asset_node.get_param_names():
        logging.info("Query param: {0} has value: {1}".format(name, asset_node.get_param_value(name)))

    #Set node's parameters
    asset_node.set_param_value("seed", 1.0)
    asset_node.set_param_value("rop_geometry1_sopoutput", "$HIP/spaceship.obj")

    #Query node's parameter after set
    logging.info("Param: seed has value {0}".format(asset_node.get_param_value("seed")))
    logging.info("Param: rop_geometry1_sopoutput has value {0}".\
        format(asset_node.get_param_value("rop_geometry1_sopoutput")))

    #Press button
    asset_node.press_button("rop_geometry1_execute", status_report_interval=1.0)

    session.save_hip("spaceship.hip")

if __name__ == "__main__":
    main()
