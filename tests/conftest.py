# -*- coding: utf-8 -*-
"""Test fixture
Author  : Maajor
Email   : hello_myd@126.com
"""
import pytest

import pyhapi as ph

@pytest.fixture(scope='function')
def init_session():
    """Init houdini session

    Returns:
        HSession: session created
    """
    session = ph.HSessionManager.get_or_create_default_session()
    print('setup_function called.')
    assert session is not None
    return session

@pytest.fixture(scope='function')
def init_session_pool():
    """Init houdini session pool

    Returns:
        HSessionPool: session pool created
    """
    session_pool = ph.HSessionManager.get_or_create_session_pool(5)
    print('setup_function called.')
    assert session_pool is not None
    return session_pool
