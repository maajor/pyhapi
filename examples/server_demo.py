# -*- coding: utf-8 -*-
"""a demo to run houdini server
Author  : Maajor
Email   : info@ma-yidong.com
"""
import os, time, datetime
from flask import Flask, request, send_file
import pyhapi as ph

app = Flask(__name__)

@ph.HSessionTask
async def session_task(session : ph.HSession, filename, seed):
    hda_asset = ph.HAsset(session, "hda/save_cube.hda")
    asset_node = hda_asset.instantiate(node_name="cube")
    asset_node.set_param_value("filename", "{0}".format(filename))
    asset_node.set_param_value("seed", seed)
    await asset_node.press_button_async("execute", status_report_interval=0.1)

@app.route('/sample', methods=['POST'])
def sample():
    seed = request.json['seed']
    filename = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
    fut = ph.HSessionManager.get_or_create_session_pool().enqueue_task(session_task, filename, seed)
    while not fut.done():
        time.sleep(0.1)
    try:
        succeed, e = fut.result()
        if succeed:
            return send_file("{0}.obj".format(filename))
        else:
            return repr(e), 401
    except Exception as e:
        print(e)

def main():
    session_pool = ph.HSessionManager.get_or_create_session_pool()
    session_pool.run_task_consumer_on_background()
    app.run(threaded=True, host='127.0.0.1')

if __name__ == "__main__":
    main()