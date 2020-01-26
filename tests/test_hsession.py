# -*- coding: utf-8 -*-
"""Test for creating and operations with hengine session
Author  : Maajor
Email   : hello_myd@126.com
"""
import pyhapi as ph

def test_init_session(init_session):
    """[summary]
    """
    #session1 = ph.HSessionManager.get_or_create_default_session()
    #assert session1 is not None
    session2 = ph.HSessionManager.get_or_create_default_session()
    assert session2 is not None
    assert init_session.process_id == session2.process_id

def test_save_hip(init_session):
    """[summary]
    """
    #session = ph.HSessionManager.get_or_create_default_session()
    init_session.save_hip()
