# -*- coding: utf-8 -*-
"""Example of marshall in a heightfield
Author  : Maajor
Email   : info@ma-yidong.com
"""
import logging
import pyhapi as ph
import numpy as np

def main():
    """Main
    """
    logging.basicConfig(level=logging.INFO)
    session = ph.HSessionManager.get_or_create_default_session()

    #create a heightfield input node, used to marshal in height and mask
    #it will create three node for height, mask and merge.
    height_input_node = ph.HHeightfieldInputNode(session, "height_input", 500, 500, 1)

    #a random height marshal into height node
    height_geo = ph.HGeoHeightfield(
        np.random.random_sample((500, 500, 1)).astype(np.float32)*100,
        "height")
    height_geo.commit_to_node(session, height_input_node.height_node.node_id)

    #a random mask marshal into mask node
    mask_geo = ph.HGeoHeightfield(
        np.random.random_sample((500, 500, 1)).astype(np.float32),
        "mask")
    mask_geo.commit_to_node(session, height_input_node.mask_node.node_id)

    #create a heightfield input volume node, usually used to marshal in custom mask
    heightvolume_input_node = ph.HHeightfieldInputVolumeNode(session, "water_mask", 500, 500, 1)

    #a random mask marshal in as water mask
    water_mask = ph.HGeoHeightfield(
        np.random.random_sample((500, 500, 1)).astype(np.float32)*0.5,
        "water_mask")
    water_mask.commit_to_node(session, heightvolume_input_node.node_id)

    #merge the watermask into heightfield input node
    #now the heightfield has three layer: height, mask and water_mask
    height_input_node.merge_node\
        .connect_node_input(heightvolume_input_node, input_index=2)\
        .cook()

    session.save_hip("test_terrain.hip")

if __name__ == "__main__":
    main()
