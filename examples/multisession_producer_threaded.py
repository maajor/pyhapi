# -*- coding: utf-8 -*-
"""Example of start HSessionPool and consume task producer on multiple threads
Author  : Maajor
Email   : info@ma-yidong.com
"""
import logging
import asyncio
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import pyhapi as ph

@ph.HSessionTask
async def session_task(session : ph.HSession, index1, index2):
    print("execute {0} - {1}".format(index1, index2))
    hda_asset = ph.HAsset(session, "hda/save_cube.hda")
    asset_node = hda_asset.instantiate(node_name="cube")
    asset_node.set_param_value("filename", "{0}-{1}".format(index1, index2))
    await asset_node.press_button_async("execute", status_report_interval=0.1)

def producer(pool, n):
    while True:
        val1 = random.randint(1, 10)
        val2 = random.randint(10, 20)
        time.sleep(5*random.random())
        print("Task Start on {0}-{1}".format(n, threading.currentThread().getName()))
        try:
            fut = pool.enqueue_task(session_task, val1, val2)
            # block this producer thread
            while not fut.done():
                time.sleep(0.5)
        except Exception as e:
            logging.exception(e)
        finally:
            print("Task Completed on {0}-{1}".format(n, threading.currentThread().getName()))

def main():
    """Main
    """
    logging.basicConfig(level=logging.INFO)
    session_pool = ph.HSessionManager.get_or_create_session_pool()

    # run consumer on background thread forever
    session_pool.run_task_consumer_on_background()

    executor = ThreadPoolExecutor(max_workers=4)
    for i in range(0,4):
        executor.submit(producer, session_pool, i)

if __name__ == "__main__":
    main()
