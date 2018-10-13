# -*- coding: utf-8 -*-
"""
Tests for the module __init__ file.
"""
import os
import sys
import importlib
from unittest import mock

import pytest

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


@pytest.mark.parametrize('value, exc', [
    (None, TypeError('type error text')),
    (None, ValueError('value error text')),
    (('', ''), None),
])
def test_localedetect_getdefaultlocale_failure_calls_fail_handler(value, exc):
    """
    Test that either a Type/ValueError exception in the locale.getdefaultlocale
    call, or an empty language_code, are detected and that the fail_handler is
    called.
    """
    mock_locale = mock.MagicMock(return_value=value, side_effect=exc)
    mock_fail_handler = mock.Mock()

    with mock.patch('locale.getdefaultlocale', mock_locale):
        mu.localedetect.language_code(fail_handler=mock_fail_handler)

    assert mock_fail_handler.call_count == 1


@pytest.mark.parametrize('fallback, value, exc, expected', [
    ('fallback', 'a language code', None, 'a language code'),
    ('fallback', '', None, 'fallback'),
    ('fallback', None, Exception('fail handler failed!'), 'fallback'),
])
def test_localedetect_fail_handler_handling(fallback, value, exc, expected):
    """
    Test that when localedetect.language_detect uses the fail_handler, it
    returns its returned value; unless it's empty or it raises an exception: in
    that case, the passed in fallback value should be returned.
    """
    # Force fail_handler to be used
    mock_locale = mock.MagicMock(return_value=('',''))
    mock_fail_handler = mock.Mock(return_value=value, side_effect=exc)

    with mock.patch('locale.getdefaultlocale', mock_locale):
        lc = mu.localedetect.language_code(fallback=fallback,
                                           fail_handler=mock_fail_handler)

    assert lc == expected


def test_localedetect_default_fail_handler_unsupported_platform(caplog):
    """
    Test that localedetect.language_detect uses a platform dependent fail
    handler, by default, that, in unsupported platforms, will log a warning
    message, returning nothing. With that, localedetect.language_detect should
    return the passed in fallback value.
    """
    # Force fail_handler to be used
    mock_locale = mock.MagicMock(return_value=('',''))

    with mock.patch('locale.getdefaultlocale', mock_locale), \
        mock.patch('sys.platform', 'zx81'):
        lc = mu.localedetect.language_code(fallback='sinclair')

    # Assert message was logged: no platform detection exists for 'zx81'.
    expected_log_msg = "No platform specific language detection for 'zx81'."
    for record in caplog.records:
        if record.getMessage() == expected_log_msg:
            break
    else:
        assert False, 'Expected log message missing.'

    # Assert fallback value was returned.
    assert lc == 'sinclair'



def test_localedetect_default_fail_handler_supported_platform(caplog):
    """
    Test that localedetect.language_detect uses a platform dependent fail
    handler, by default, that, on supported platforms is named
    '_language_code_{sys.platform}.
    """
    # Force fail_handler to be used
    mock_locale = mock.MagicMock(return_value=('',''))
    mock_zx81 = mock.Mock(return_value='sinclair')

    try:
        mu.localedetect._language_code_zx81 = mock_zx81
        with mock.patch('locale.getdefaultlocale', mock_locale), \
            mock.patch('sys.platform', 'zx81'):
            lc = mu.localedetect.language_code()
    finally:
        del mu.localedetect._language_code_zx81

    assert mock_zx81.call_count == 1
    assert lc == 'sinclair'


def test_defaultlocale_type_error():
    """
    Test that a TypeError in the locale.getdefaultlocale is detected and
    the translation language is set to English by default.
    """
    old_lc_all = os.environ.get('LC_ALL', None)
    os.environ['LC_ALL'] = 'es_ES.UTF-8'
    mock_locale = mock.MagicMock(side_effect=TypeError('Ups'))

    with mock.patch('locale.getdefaultlocale', mock_locale), \
            mock.patch('gettext.translation') as translation:
        importlib.reload(mu)

    if old_lc_all:
        os.environ['LC_ALL'] = old_lc_all
    else:
        del os.environ['LC_ALL']
    assert translation.call_count == 1
    assert translation.call_args[1]['languages'] == ['en']


def test_defaultlocale_value_error():
    """
    Test that a ValueError is detected and the translation language is set
    to English by default.
    """
    old_lc_all = os.environ.get('LC_ALL', None)
    os.environ['LC_ALL'] = 'es_ES.UTF-8'
    mock_locale = mock.MagicMock(side_effect=ValueError('Ups'))

    with mock.patch('locale.getdefaultlocale', mock_locale), \
            mock.patch('gettext.translation') as translation:
        importlib.reload(mu)

    if old_lc_all:
        os.environ['LC_ALL'] = old_lc_all
    else:
        del os.environ['LC_ALL']
    assert translation.call_count == 1
    assert translation.call_args[1]['languages'] == ['en']


def test_defaultlocale_empty_raises_value_error():
    """
    If no language code is detected, then raise a ValueError to cause it to
    default to 'en'.
    """
    old_lc_all = os.environ.get('LC_ALL', None)
    os.environ['LC_ALL'] = 'es_ES.UTF-8'
    mock_locale = mock.MagicMock(return_value=('', ''))

    with mock.patch('locale.getdefaultlocale', mock_locale), \
            mock.patch('gettext.translation') as translation:
        importlib.reload(mu)

    if old_lc_all:
        os.environ['LC_ALL'] = old_lc_all
    else:
        del os.environ['LC_ALL']
    assert translation.call_count == 1
    assert translation.call_args[1]['languages'] == ['en']
