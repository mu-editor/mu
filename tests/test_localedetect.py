# -*- coding: utf-8 -*-
"""
Tests for the localedetect module.
"""
import subprocess
import sys
from unittest import mock

import pytest

from mu import localedetect


_GETDEFAULTLOCALE_FAILURES = [
    # (return value, side effect) tuples
    (None, TypeError('getdefaultlocale() raised this')),
    (None, ValueError('getdefaultlocale() raised this')),
    (('', ''), None),
]


@pytest.mark.parametrize('gdl_rv, gdl_se', _GETDEFAULTLOCALE_FAILURES)
def test_language_code_bad_getdefaultlocale_calls_fail_handler(gdl_rv, gdl_se):
    """
    If the locale.getdefaultlocale() call used by the language_code() function
    either a) raises a Type/ValueError or b) returns an empty language code,
    the passed in fail_handler is called.
    """
    mock_getdefaultlocale = mock.MagicMock(return_value=gdl_rv,
                                           side_effect=gdl_se)
    mock_fail_handler = mock.Mock()

    with mock.patch('locale.getdefaultlocale', mock_getdefaultlocale):
        localedetect.language_code(fail_handler=mock_fail_handler)

    assert mock_fail_handler.call_count == 1


@pytest.mark.parametrize('fallback, value, exc, expected', [
    ('fallback_lang', 'nice_lang', None, 'nice_lang'),
    ('fallback_lang', '', None, 'fallback_lang'),
    ('fallback_lang', None, Exception('Fail handler failed'), 'fallback_lang'),
])
def test_language_code_fail_handler_handling(fallback, value, exc, expected):
    """
    When language_code() uses the fail_handler, it returns either whatever
    the fail_handler returns, unless that raises an exception or returns an
    empty/false-y value: it such cases, language_code() returns the passed in
    fallback value.
    """
    # Force fail_handler to be used
    mock_getdefaultlocale = mock.MagicMock(return_value=('', ''))
    mock_fail_handler = mock.Mock(return_value=value, side_effect=exc)

    with mock.patch('locale.getdefaultlocale', mock_getdefaultlocale):
        lang_code = localedetect.language_code(fallback=fallback,
                                               fail_handler=mock_fail_handler)

    assert lang_code == expected


def test_language_code_default_fail_handler_unsupported_platform(caplog):
    """
    The language_code() function uses a platform dependent fail handler, by
    default, that, on unsupported platforms, will log a warning message,
    returning nothing; in such cases, language_code() returns the passed in
    fallback value.
    """
    # Force fail_handler to be used
    mock_getdefaultlocale = mock.MagicMock(return_value=('', ''))

    # Fake 'zx81' platform which is (unfortunatelly?) an unsupported platform.
    with mock.patch('locale.getdefaultlocale', mock_getdefaultlocale), \
            mock.patch('sys.platform', 'zx81'):
        lang_code = localedetect.language_code(fallback='sinclair')

    # Assert message was logged: no platform detection exists for 'zx81'.
    expected_log_msg = "No platform specific language detection for 'zx81'."
    for record in caplog.records:
        if record.getMessage() == expected_log_msg:
            break
    else:
        pytest.fail('Expected log message missing.')

    # Assert fallback value was returned.
    assert lang_code == 'sinclair'


def test_language_code_default_fail_handler_supported_platform():
    """
    The language_code() function uses a platform dependent fail handler that,
    by default, on supported platforms, is named _language_code_{sys.platform}.
    """
    # Force fail_handler to be used
    mock_getdefaultlocale = mock.MagicMock(return_value=('', ''))
    mock_language_code_zx81 = mock.Mock(return_value='sinclair')

    try:
        localedetect._language_code_zx81 = mock_language_code_zx81
        with mock.patch('locale.getdefaultlocale', mock_getdefaultlocale), \
                mock.patch('sys.platform', 'zx81'):
            lang_code = localedetect.language_code()
    finally:
        del localedetect._language_code_zx81

    assert mock_language_code_zx81.call_count == 1
    assert lang_code == 'sinclair'


@pytest.mark.skipif(sys.platform != 'darwin',
                    reason='Platform specific test for macOS.')
def test_language_code_macos():
    """
    The _language_code_darwin() function returns the same string as the macOS
    command line "defaults read -g AppleLocale".
    """
    mu_lang_code = localedetect._language_code_darwin()
    cmd_line_lang_code = subprocess.getoutput('defaults read -g AppleLocale')

    assert mu_lang_code == cmd_line_lang_code


@pytest.mark.parametrize('gdl_rv, gdl_se', _GETDEFAULTLOCALE_FAILURES)
@pytest.mark.parametrize('fh_rv, fh_se', [
    (None, Exception('fail_handler raised this')),
    ('', None),
])
def test_language_code_failures_return_en_GB(gdl_rv, gdl_se, fh_rv, fh_se):
    """
    The language_code() function returns 'en_GB' if any failure during its
    execution is found:
    - locale.getdefaultlocale() raising Type/ValueError or returning an empty
      language code.
    - fail_handler() raising any exceptionor returning an empty language code.
    """
    mock_getdefaultlocale = mock.Mock(return_value=gdl_rv, side_effect=gdl_se)
    mock_fail_handler = mock.Mock(return_value=fh_rv, side_effect=fh_se)

    with mock.patch('locale.getdefaultlocale', mock_getdefaultlocale):
        lang_code = localedetect.language_code(fail_handler=mock_fail_handler)

    assert lang_code == 'en_GB'
