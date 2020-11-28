# -*- coding: utf-8 -*-
"""Example of getting/setting hparms of HDA asset
Author  : Maajor
Email   : info@ma-yidong.com
"""
import logging
import pyhapi as ph

def print_all_params(asset_node):
    for parm in asset_node.get_visible_params():
        if isinstance(parm, ph.HParmChoice):
            print("{0} is type {1}, has choice {2}".format(parm.get_name(), asset_node.get_param_type(parm.get_name()), parm.get_choice_values()))
        elif isinstance(parm, ph.HParmButton):
            print("{0} is button, has name {1}".format(parm.get_name(), parm.get_label()))
        elif isinstance(parm, ph.HParmLabel):
            print("{0} is label, has label {1}".format(parm.get_name(), parm.get_label()))
        else:
            print("{0} is type {1}, has default value {2}".format(parm.get_name(), asset_node.get_param_type(parm.get_name()), parm.get_value()))

def main():
    """Main
    """
    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #load hda asset and instantiate
    hda_asset = ph.HAsset(session, "hda/dummy_params.hda")
    asset_node = hda_asset.instantiate(node_name="params")

    #Query node's parameters
    logging.info("Node has parameter count: {0}".format(len(asset_node.get_param_names())))

    print_all_params(asset_node)

    for parm in asset_node.get_visible_params():
        if isinstance(parm, ph.HParmChoice):
            parm.set_value(index=1)
        elif isinstance(parm, ph.HParmInt):
            parm.set_value(value=3)
        elif isinstance(parm, ph.HParmFloat):
            parm.set_value(value=4.0)
        elif isinstance(parm, ph.HParmString):
            #asset_node.set_param_value(parm.name, "hi")
            parm.set_value(value="hi")

    asset_node.set_param_value("intvec3", [1, 1, 1])
    asset_node.set_param_value("vec4", [0.5, 0.6, 0.7, 0.8])
    asset_node.set_param_value("color", [0.3, 0.4, 0.5])
    asset_node.set_param_value("toggle", True)
    asset_node.set_param_value("strings5", ["str0", "str1", "str2", "str3", "str4"])
    asset_node.press_button("button")

    print_all_params(asset_node)

    session.save_hip("debug.hip")
        

if __name__ == "__main__":
    main()
