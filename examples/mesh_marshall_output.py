# -*- coding: utf-8 -*-
"""Example of extracting mesh data from hengine's node
Author  : Maajor
Email   : info@ma-yidong.com
"""
import pyhapi as ph

def main():
    """Main
    """
    session = ph.HSessionManager.get_or_create_default_session()

    # load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/FourShapes.hda")
    asset_node = hda_asset.instantiate(node_name="TestObject").cook()
    asset_geos = asset_node.get_display_geos()

    for geo in asset_geos:
        print("Geo {0} has attribute {1}".format(geo, geo.get_attrib_names()))

    print(asset_geos[0].get_attrib_data(ph.AttributeOwner.POINT, "P"))

    session.save_hip("modifiedScene2.hip")


if __name__ == "__main__":
    main()
