# -*- coding: utf-8 -*-
"""Example of marshall out a heightfield
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
    hda_asset = ph.HAsset(session, "hda/heightfield_test.hda")
    asset_node = hda_asset.instantiate(node_name="HF").cook()

    #get node's all display geo, print volume's data shape and name
    all_geos = asset_node.get_display_geos()
    for geo in all_geos:
        if isinstance(geo, ph.HGeoHeightfield):
            logging.info(geo.volume.shape)
            logging.info(geo.volume_name)

    session.save_hip("modifiedScene.hip")

if __name__ == "__main__":
    main()
