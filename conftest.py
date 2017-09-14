"""
Ensures the gettext _ builtin is available during tests.
"""
import os.path
import gettext


localedir = os.path.join('mu', 'locale')
gettext.translation('mu', localedir=localedir,
                    languages=['en'], fallback=True).install()
