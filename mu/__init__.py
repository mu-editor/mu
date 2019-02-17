import gettext
from os import path

from PyQt5.Qt import QLocale


def setup_gettext():
    """
    Sets up gettext translations, installing the global _() function.
    """
    # Where the translation assets are to be found.
    localedir = path.abspath(path.join(path.dirname(__file__), 'locale'))

    # Ask Qt for system language: returns an 'll_CC' string, where 'll' is a
    # 2-letter ISO 639 language, and CC is a 2/3-letter ISO 3166 country code.
    # DEBUG/TRANSLATE: Override with the LANG environment variable.
    language_code = QLocale.system().name()

    # Install the _() translation function.
    gettext.translation('mu', localedir=localedir,
                        languages=[language_code], fallback=True).install()


__version__ = '1.0.2'
