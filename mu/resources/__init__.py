from pkg_resources import resource_filename, resource_string

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QDir

QDir.addSearchPath('images', resource_filename(__name__, 'images'))
QDir.addSearchPath('css', resource_filename(__name__, 'css'))
QDir.addSearchPath('svg', resource_filename(__name__, 'svg'))


def path(name):
    return resource_filename(__name__, "images/" + name)


def load_icon(name):
    """Load an icon from the resources directory."""
    return QIcon(path(name))


def load_pixmap(name):
    """Load a pixmap from the resources directory."""
    return QPixmap(path(name))


def load_stylesheet(name):
    """Load a CSS stylesheet from the resources directory."""
    return resource_string(__name__, "css/" + name).decode('utf8')


def load_svg(name):
    """Load SVG text from the resources directory."""
    return resource_string(__name__, "svg/" + name)
