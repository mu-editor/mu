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

__version__ = '1.0.2'
