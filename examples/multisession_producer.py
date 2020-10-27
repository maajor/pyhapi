# -*- coding: utf-8 -*-
"""Example of start HSessionPool and consume task producer
Author  : Maajor
Email   : info@ma-yidong.com
"""
import logging
import asyncio
import random
import pyhapi as ph

@ph.HSessionTask
async def session_task(session : ph.HSession, index1, index2):
    print("execute {0} - {1}".format(index1, index2))
    hda_asset = ph.HAsset(session, "hda/save_cube.hda")
    asset_node = hda_asset.instantiate(node_name="cube")
    asset_node.set_param_value("filename", "{0}-{1}".format(index1, index2))
    await asset_node.press_button_async("execute", status_report_interval=0.1)

async def producer():
    while True:
        val1 = random.randint(1, 10)
        val2 = random.randint(10, 20)
        await asyncio.sleep(random.random())
        await ph.HSessionManager.get_or_create_session_pool().enqueue_task_async(session_task, val1, val2)

def main():
    """Main
    """
    logging.basicConfig(level=logging.INFO)
    session_pool = ph.HSessionManager.get_or_create_session_pool()

    # run producer and consumer forever
    session_pool.run_on_task_producer(producer)

if __name__ == "__main__":
    main()
