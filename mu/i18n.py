import os
import gettext

from PyQt5.QtCore import QLocale

# DEBUG/TRANSLATE: override the language code here (e.g. to Chinese).
# language_code = 'zh'
language_code = QLocale.system().name()

# Configure locale and language
# Define where the translation assets are to be found.
localedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "locale"))
gettext.translation(
    "mu", localedir=localedir, languages=[language_code], fallback=True
).install()
