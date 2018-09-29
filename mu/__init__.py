import gettext
import locale
import os

# Configure locale and language
# Define where the translation assets are to be found.
localedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'locale'))
try:
    # Use the operating system's locale.
    language_code, encoding = locale.getdefaultlocale()
    if not language_code:
        raise ValueError()
except (TypeError, ValueError):
    language_code = 'en'
# DEBUG/TRANSLATE: override the language code here (e.g. to Chinese).
# language_code = 'zh'
gettext.translation('mu', localedir=localedir,
                    languages=[language_code], fallback=True).install()

__version__ = '1.0.0'
