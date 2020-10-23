# -*- coding: utf-8 -*-
"""Test for creating and operations with hengine session pool
Author  : Maajor
Email   : hello_myd@126.com
"""
import pyhapi as ph

def test_init_session_pool(init_session_pool):
    """[summary]
    """
    assert init_session_pool._session_count == 5
