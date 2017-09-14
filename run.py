#!/usr/bin/env python3
import locale
import os.path
import gettext


# Configure locale and language
localedir = os.path.join('mu', 'locale')
try:
    current_locale, encoding = locale.getdefaultlocale()
    language_code = current_locale[:2]
except Exception as ex:
    language_code = 'en'  # fall back to English.
gettext.translation('mu', localedir=localedir,
                    languages=[language_code], fallback=True).install()


# Import and run Mu.
from mu.app import run


if __name__ == "__main__":
    run()
