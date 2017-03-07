import os
from setuptools import setup
from mu import __version__

#
# The data files are *nix-specific. We use os.name rather than sys.platform
# or the platform module as we don't care which Unix is in use. If it turns
# out that we do, then a switch to os.uname or sys.platform might be in order.
#
if os.name == "posix":
    data_files = [('/etc/udev/rules.d', ['conf/90-usb-microbit.rules', ]),
                  ('/usr/share/pixmaps', ['conf/mu.png', ]),
                  ('/usr/share/applications', ['conf/mu.desktop', ])]
else:
    data_files = []

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
        ],
    },
    data_files=data_files,
)
