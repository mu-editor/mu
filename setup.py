from setuptools import setup
from mu import __version__


setup(
    name='mu',
    version=__version__,
    description='A simple editor for kids, teachers and new programmers.',
    author='Nicholas Tollervey',
    author_email='ntoll@ntoll.org',
    url='https://github.com/ntoll/mu',
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
        'console_scripts': [
            "mu = mu.app:run",
        ],
    },
    data_files=[('/etc/udev/rules.d', ['conf/90-usb-microbit.rules', ]),
                ('/usr/share/pixmaps', ['conf/mu.png', ]),
                ('/usr/share/applications', ['conf/mu.desktop', ])],
)
