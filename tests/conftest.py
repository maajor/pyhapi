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
