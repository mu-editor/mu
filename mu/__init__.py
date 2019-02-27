import gettext
import os

from PyQt5.QtCore import QLocale


# Configure locale and language
# Define where the translation assets are to be found.
localedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'locale'))
language_code = QLocale.system().name()
# DEBUG/TRANSLATE: override the language code here (e.g. to Chinese).
# language_code = 'zh'
gettext.translation('mu', localedir=localedir,
                    languages=[language_code], fallback=True).install()


# IMPORTANT
# ---------
# Keep these metadata assignments simple and single-line. They are parsed
# somewhat naively by setup.py and the Windows installer generation script.

__title__ = 'mu-editor'
__description__ = 'A simple Python editor for beginner programmers.'

__version__ = '1.0.2'

__license__ = 'GPL3'
__url__ = 'https://github.com/mu-editor/mu'

__author__ = 'Nicholas H.Tollervey'
__email__ = 'ntoll@ntoll.org'
