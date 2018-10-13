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


def language_code(fallback=_FALLBACK_LANG_CODE, fail_handler=None):
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
        fail_handler = fail_handler or _platform_fail_handler()
        _logger.warning('Failed locale.getdefaultlocale() call. '
                        'Trying fail handler %r.', fail_handler)
        try:
            language_code = fail_handler()
        except Exception as e:
            _logger.warning('Fail handler also failed: %s. '
                            'Falling back to %r', e, fallback)
            language_code = fallback

    # Return the fallback value if language_code is empty.
    return language_code or fallback


def _platform_fail_handler():
    """
    Returns a callable, the platform specific language detection function, if
    it exists in this module. Otherwise, returns a function that just logs the
    unavailability of such a platform specific function.
    """
    def _no_platform_handler():
        """
        Used as the fallback platform specific language detection handler.
        """
        _logger.warning('No platform specific language detection for %r.',
                        sys.platform)

    return getattr(sys.modules[__name__],
                   '_language_code_{}'.format(sys.platform),
                   _no_platform_handler)


def _language_code_darwin():
    """
    Returns the user's language preference as defined in the Language & Region
    preference pane in macOS's System Preferences.
    """

    # Uses native macOS APIs to read the user's language preference per
    # https://developer.apple.com/documentation/foundation/nsuserdefaults.

    # Rubicon-ObjC (https://pypi.org/project/rubicon-objc/) is a pure Python
    # package used to dynamically access the native macOS APIs without the need
    # for a C compiler. This should simplify testing, deployment and packaging.

    # Platform specific imports here avoid import failures on other platforms.
    import ctypes
    from rubicon import objc

    PREF_NAME = 'AppleLocale'

    lib_path = ctypes.util.find_library('Foundation')
    ctypes.cdll.LoadLibrary(lib_path)

    NSUserDefaults = objc.ObjCClass('NSUserDefaults')
    standard_user_defaults = NSUserDefaults.standardUserDefaults
    language_code = str(standard_user_defaults.stringForKey_(PREF_NAME))

    return language_code
