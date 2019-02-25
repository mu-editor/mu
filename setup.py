import os
from setuptools import setup


base_dir = os.path.dirname(__file__)


about = {}
with open(os.path.join(base_dir, 'mu', '__about__.py')) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, 'README.rst')) as f:
    readme = f.read()
    # Replace the logo URL in the README with something that works in PyPI
    logo_url = 'https://mu.readthedocs.io/en/latest/_images/logo.png'
    readme = readme.replace('docs/logo.png', logo_url)

with open(os.path.join(base_dir, 'CHANGES.rst')) as f:
    changes = f.read()


install_requires = [
    'pyqt5==5.11.3;"arm" not in platform_machine',
    'qscintilla==2.10.8;"arm" not in platform_machine',
    'PyQtChart==5.11.3;"arm" not in platform_machine',
    'pycodestyle==2.4.0',
    'pyflakes==2.0.0',
    'pyserial==3.4',
    'qtconsole==4.3.1',
    'pgzero==1.2',
    'appdirs>=1.4.3',
    'gpiozero>=1.4.1',
    'guizero>=0.5.2',
    'pigpio>=1.40.post1',
    'semver>=2.8.0',
    'nudatus>=0.0.3',
    'black>=18.9b0;python_version > "3.5"',
]


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description='{}\n\n{}'.format(readme, changes),
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__url__'],
    license=about['__license__'],
    packages=['mu', 'mu.contrib', 'mu.resources', 'mu.modes', 'mu.debugger',
              'mu.interface', 'mu.modes.api', ],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Text Editors',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)',
    ],
    entry_points={
        'console_scripts': [
            "mu-editor = mu.app:run",
        ],
    },
    options={  # Briefcase packaging options for OSX
        'app': {
            'formal_name': 'mu-editor',
            'bundle': 'mu.codewith.editor',
        },
        'macos': {
            'icon': 'package/icons/mac_icon',
        }
    }
)
