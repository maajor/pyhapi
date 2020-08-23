# -*- coding: utf-8 -*-
"""Example of marshall out curve
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
    hda_asset = ph.HAsset(session, "hda/nurbs_curve.hda")
    asset_node = hda_asset.instantiate(node_name="Curve").cook()

    #get node's all display geo, print curveinfo and P
    all_geos = asset_node.get_display_geos()
    for geo in all_geos:
        logging.info(geo.get_attrib_data(ph.AttributeOwner.POINT, "P"))
        if isinstance(geo, ph.HGeoCurve):
            logging.info(geo.curve_info)

    session.save_hip("modifiedScene.hip")

if __name__ == "__main__":
    main()
