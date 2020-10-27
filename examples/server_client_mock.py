# -*- coding: utf-8 -*-
"""Run after server_demo.py to mock client request
Author  : Maajor
Email   : info@ma-yidong.com
"""

import requests
import os

url='http://127.0.0.1:5000/sample'
payload = {
    "seed":"0"
}
r=requests.post(url, json=payload)
print(r.status_code)
if r.status_code < 400:
    with open("return.obj", "wb") as f:
        f.write(r.content)