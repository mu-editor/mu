import gettext
import locale
import os

# Configure locale and language
# Define where the translation assets are to be found.
localedir = os.path.join('mu', 'locale')
# Use the operating system's locale.
current_locale, encoding = locale.getdefaultlocale()
# Get the language code.
language_code = current_locale[:2]
# DEBUG/TRANSLATE: override the language code here (e.g. to Spanish).
# language_code = 'es'
gettext.translation('mu', localedir=localedir,
                    languages=[language_code], fallback=True).install()

__version__ = '1.0.0.beta.15'
