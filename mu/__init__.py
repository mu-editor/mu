import gettext
import os

from . import localedetect

# Configure locale and language
# Define where the translation assets are to be found.
localedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'locale'))
language_code = localedetect.language_code()
# DEBUG/TRANSLATE: override the language code here (e.g. to Chinese).
# language_code = 'zh'
gettext.translation('mu', localedir=localedir,
                    languages=[language_code], fallback=True).install()

__version__ = '1.0.3'
