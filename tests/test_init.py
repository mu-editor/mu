# -*- coding: utf-8 -*-
"""
Tests for the module __init__ file.
"""
import os
import sys
import importlib
from unittest import mock

import mu


def test_gettext_translation():
    """
    Test the right translation is set based on the LC_ALL environmental
    variable.
    """
    if sys.platform == 'win32':
        # Unix only test.
        return
    old_lc_all = os.environ.get('LC_ALL', None)
    os.environ['LC_ALL'] = 'es_ES.UTF-8'

    with mock.patch('gettext.translation') as translation:
        importlib.reload(mu)

    if old_lc_all:
        os.environ['LC_ALL'] = old_lc_all
    else:
        del os.environ['LC_ALL']
    assert translation.call_count == 1
    assert translation.call_args[1]['languages'] == ['es_ES']
