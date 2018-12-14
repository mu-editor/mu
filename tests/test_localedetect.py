# -*- coding: utf-8 -*-
"""
Tests for the localedetect module.
"""
from unittest import mock

import pytest

from mu import localedetect


_DEFAULT_LANG_CODE = localedetect._DEFAULT_LANG_CODE

_TEST_MATRIX_PLATFORM_DEFAULT = [
    # | locale.getdefaultlocale      |
    # | lang_code | char | exception | expected result |
    ('es_ES', 'UTF-8', None, 'es_ES'),
    ('fr_FR', 'ISO-8859-1', None, 'fr_FR'),
    ('', '', None, _DEFAULT_LANG_CODE),
    (None, None, Exception('ups'), _DEFAULT_LANG_CODE),
]

@pytest.mark.parametrize('lang_code, encoding, exc, expected',
                         _TEST_MATRIX_PLATFORM_DEFAULT)
def test_language_code_default_platform(lang_code, encoding, exc, expected):
    """
    langdetect.language_code() returns the expected values for multiple
    combinations of locale.getdefaultlocale() behaviour under non macOS
    platforms.
    """
    mock_getdefaultlocale = mock.Mock(return_value=(lang_code, encoding),
                                      side_effect=exc)

    with mock.patch('locale.getdefaultlocale', mock_getdefaultlocale),\
            mock.patch('sys.platform', 'default'):
        result = localedetect.language_code()

    assert mock_getdefaultlocale.call_count == 1
    assert result == expected


_TEST_MATRIX_PLATFORM_MAC = [
    # | subprocess.getstatusoutput  |
    # | status | output | exception | expected result |
    (0, 'es_ES', None, 'es_ES'),
    (0, '', None, _DEFAULT_LANG_CODE),
    (127, '-bash: defaults: command not found', None, _DEFAULT_LANG_CODE),
    (None, None, Exception('ups'), _DEFAULT_LANG_CODE),
]

@pytest.mark.parametrize('status, output, exc, expected',
                         _TEST_MATRIX_PLATFORM_MAC)
def test_language_code_mac_platform(status, output, exc, expected):
    """
    langdetect.language_code() returns the expected values for multiple
    combinations of subprocess.getstatusoutput() behaviour on the macOS
    platform.
    """
    mock_getstatusoutput = mock.Mock(return_value=(status, output),
                                     side_effect=exc)

    with mock.patch('subprocess.getstatusoutput', mock_getstatusoutput),\
            mock.patch('sys.platform', 'darwin'):
        result = localedetect.language_code()

    assert mock_getstatusoutput.call_count == 1
    assert result == expected
