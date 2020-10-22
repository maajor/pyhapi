# -*- coding: utf-8 -*-
"""Example of getting/setting params of HDA asset
Author  : Maajor
Email   : info@ma-yidong.com
"""
import logging
import asyncio
import pyhapi as ph

@ph.HSessionTask
async def session_task(session, index1, index2):
    print("execute {0} - {1}".format(index1, index2))
    hda_asset = ph.HAsset(session, "hda/save_cube.hda")
    asset_node = hda_asset.instantiate(node_name="cube")
    asset_node.set_param_value("filename", "{0}-{1}".format(index1, index2))
    await asset_node.press_button_async("execute", status_report_interval=0.1)

def main():
    """Main
    """
    logging.basicConfig(level=logging.INFO)
    session_pool = ph.HSessionManager.get_or_create_session_pool(3)

    session_pool.run_task_consumer_in_background()

    for i in range(5):
        session_pool.enqueue_task(session_task, i, i)

if __name__ == "__main__":
    main()
