# -*- coding: utf-8 -*-
"""[summary]
"""
import pytest

import pyhapi as ph

def test_init_session():
    """[summary]
    """
    session = ph.HSessionManager.get_or_create_default_session()
    assert session is not None

def test_save_hip():
    """[summary]
    """
    session = ph.HSessionManager.get_or_create_default_session()
    session.save_hip()
