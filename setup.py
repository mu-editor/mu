import os
import re
from setuptools import setup


base_dir = os.path.dirname(__file__)


DUNDER_ASSIGN_RE = re.compile(r"""^__\w+__\s*=\s*['"].+['"]$""")
about = {}
with open(os.path.join(base_dir, 'mu', '__init__.py'), encoding='utf8') as f:
    for line in f:
        if DUNDER_ASSIGN_RE.search(line):
            exec(line, about)

with open(os.path.join(base_dir, 'README.rst'), encoding='utf8') as f:
    readme = f.read()
    # Replace the logo URL in the README with something that works in PyPI
    logo_url = 'https://mu.readthedocs.io/en/latest/_images/logo.png'
    readme = readme.replace('docs/logo.png', logo_url)

with open(os.path.join(base_dir, 'CHANGES.rst'), encoding='utf8') as f:
    changes = f.read()


install_requires = [
    'PyQt5==5.12.1;"arm" not in platform_machine',
    'QScintilla==2.11.1;"arm" not in platform_machine',
    'PyQtChart==5.12;"arm" not in platform_machine',
    'pycodestyle==2.4.0',
    'pyflakes==2.0.0',
    'pyserial==3.4',
    'qtconsole==4.4.3',
    'pgzero==1.2',
    'appdirs>=1.4.3',
    'gpiozero>=1.4.1',
    'guizero>=0.5.2',
    'pigpio>=1.40.post1',
    'semver>=2.8.0',
    'nudatus>=0.0.3',
    'black>=18.9b0;python_version > "3.5"',
]


extras_require = {
    'tests': [
        'pytest',
        'pytest-cov',
        'pytest-random-order>=1.0.0',
        'pytest-faulthandler',
        'coverage',
    ],
    'docs': [
        'sphinx',
    ],
    'package': [
        # Wheel building and PyPI uploading
        'wheel',
        'twine',
        # Windows native packaging (see win_installer.py).
        'requests==2.21.0;platform_system == "Windows"',
        'yarg==0.1.9;platform_system == "Windows"',
        # macOS native packaging (see Makefile)
        'briefcase==0.2.9;platform_system == "Darwin"',
    ],
    'utils': [
        'scrapy',
        'beautifulsoup4',
        'requests',
    ],
}

extras_require['dev'] = (
    extras_require['tests'] +
    extras_require['docs'] +
    extras_require['package']
)

extras_require['all'] = list({
    req
    for extra, reqs in extras_require.items()
    for req in reqs
})


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
    extras_require=extras_require,
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
