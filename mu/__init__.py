import gettext
import locale
import os

# Configure locale and language
# Define where the translation assets are to be found.
localedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'locale'))
# Use the operating system's locale.
current_locale, encoding = locale.getdefaultlocale()
# Get the language code.
language_code = current_locale[:2]
# DEBUG/TRANSLATE: override the language code here (e.g. to Chinese).
# language_code = 'zh'
gettext.translation('mu', localedir=localedir,
                    languages=[language_code], fallback=True).install()

__version__ = '1.0.0.beta.15'
