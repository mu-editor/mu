"""
Language detection.

Uses the standard library's `locale` module on all platforms, including Windows
and Linux, except on macOS where a shell based command is used instead.
"""

import locale
import logging
import subprocess
import sys


_DEFAULT_LANG_CODE = 'en_GB'

_logger = logging.getLogger(__name__)


def language_code():
    """
    Returns the user's environment language as a language code string.
    (examples: 'en_GB', 'en_US', 'pt_PT', 'pt_BR', etc.)
    """

    # Systems running macOS need to use platform specific language detection.
    this_is_a_mac = sys.platform == 'darwin'

    try:
        lang_code = _lang_code_mac() if this_is_a_mac else _lang_code_generic()
    except Exception:
        lang_code = _DEFAULT_LANG_CODE
        _logger.warning('Language detection failed. Using %r', lang_code,
                        exc_info=True)
    else:
        if not lang_code:
            lang_code = _DEFAULT_LANG_CODE
            _logger.warning('No language detected. Using %r', lang_code)

    return lang_code


def _lang_code_generic():
    """
    Returns the user's language preference on the Windows and Linux plaforms,
    using the standard library's `locale` module.
    """
    lang_code, _encoding = locale.getdefaultlocale()
    return lang_code


def _lang_code_mac():
    """
    Returns the user's language preference as defined in the Language & Region
    preference pane in macOS's System Preferences.
    """

    # Uses the shell command `defaults read -g AppleLocale` that prints out a
    # language code to standard output. Assumptions about the command:
    # - It exists and is in the shell's PATH.
    # - It accepts those arguments.
    # - It returns a usable language code.
    #
    # Reference documentation:
    # - The man page for the `defaults` command on macOS.
    # - The macOS underlying API:
    #   https://developer.apple.com/documentation/foundation/nsuserdefaults.

    LANG_DETECT_COMMAND = 'defaults read -g AppleLocale'

    status, output = subprocess.getstatusoutput(LANG_DETECT_COMMAND)
    if status == 0:
        # Command was successful.
        lang_code = output
    else:
        _logger.warning('Language detection command failed: %r', output)
        lang_code = ''

    return lang_code
