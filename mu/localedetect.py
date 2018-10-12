"""
Language detection.

Uses standard library's locale module, falling back to platform specific
techniques when locale.getdefaultlocale() returns no useful information.
"""

import locale
import logging
import sys


_FALLBACK_LANG_CODE = 'en_GB'

_logger = logging.getLogger(__name__)


def language_code(fallback=_FALLBACK_LANG_CODE):
    """
    Returns the user's environment language as a language code string.
    (examples: 'en_GB', 'en_US', 'pt_PT', 'pt_BR', etc.)
    """
    try:
        # Use the operating system's locale.
        language_code, _encoding = locale.getdefaultlocale()
        if not language_code:
            raise ValueError()
    except (TypeError, ValueError):
        # Commonly fails on macOS which does not set LANG / LC_ALL env vars.
        _logger.warning('Failed locale.getdefaultlocale() call: '
                        'trying platform specific language detection.')
        try:
            language_code = _platform_language_code(fallback)
        except Exception as e:
            _logger.warning('Platform specific language detection failed: %s. '
                            'Falling back to %r', e, fallback)
            language_code = fallback

    return language_code


def _platform_language_code(fallback):
    """
    Returns the user's environment language code by delegating to platform
    specific detection functions, falling back to the passed in value when
    no plaform specific code is found.
    """
    try:
        platform = sys.platform
        function_name = '_language_code_{}'.format(platform)
        function = getattr(sys.modules[__name__], function_name)
    except AttributeError:
        _logger.warning('No platform specific language detection for %r: '
                        'falling back to %r', platform, fallback)
        language_code = fallback
    else:
        language_code = function(fallback)

    return language_code


def _language_code_darwin(fallback):
    """
    Returns the user's language preference as defined in the Language & Region
    preference pane in macOS's System Preferences.
    """

    # Uses native macOS APIs to read the user's language preference per
    # https://developer.apple.com/documentation/foundation/nsuserdefaults.

    # Rubicon-ObjC (https://pypi.org/project/rubicon-objc/) is a pure Python
    # package used to dynamically access the native macOS APIs without the need
    # for a C compiler which should simplify testing, deployment and packaging.

    # Platform specific imports avoid import failures on other platforms.
    import ctypes
    from rubicon import objc

    PREF_NAME = 'AppleLocale'

    lib_path = ctypes.util.find_library('Foundation')
    _Foundation = ctypes.cdll.LoadLibrary(lib_path)

    NSUserDefaults = objc.ObjCClass('NSUserDefaults')
    standard_user_defaults = NSUserDefaults.standardUserDefaults
    language_code = standard_user_defaults.stringForKey_(PREF_NAME) or fallback

    return language_code
