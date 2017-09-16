import sys
from setuptools import setup
from mu import __version__


data_files = []
if sys.platform == 'linux':
    data_files = [('/etc/udev/rules.d', ['conf/90-usb-microbit.rules', ]),
                  ('/usr/share/pixmaps', ['conf/mu.png', ]),
                  ('/usr/share/applications', ['conf/mu.desktop', ])]

setup(
    name='mu',
    version=__version__,
    description='A simple editor for kids, teachers and new programmers.',
    author='Nicholas Tollervey',
    author_email='ntoll@ntoll.org',
    url='https://github.com/mu-editor/mu',
    packages=['mu', 'mu.contrib', 'mu.resources'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # These deps are not pinned to a version. We aren't too demanding about
        # what versions because we can more easily afford to build
        # compatibility into mu than our users can source alternative versions
        # of these packages. However, PyQt5/Qsci wheels are now available for
        # Windows, Mac and manylinux1, so listing these could now allow mu to
        # be pip-installable.
        'PyQt5',
        'QScintilla'
    ],
    classifiers=[
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'gui_scripts': [
            "mu = mu.app:run",
            "mu-debug = mu.app:debug",
        ],
    },
    data_files=data_files,
)
