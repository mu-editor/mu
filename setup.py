import platform
from setuptools import setup
from mu import __version__


with open('README.rst') as f:
    readme = f.read()
    # Replace the logo URL in the README with something that works in PyPI
    logo_url = 'https://mu.readthedocs.io/en/latest/_images/logo.png'
    readme = readme.replace('docs/logo.png', logo_url)
with open('CHANGES.rst') as f:
    changes = f.read()

install_requires = ['pycodestyle==2.3.1', 'pyflakes==1.6.0',
                    'pyserial==3.4', 'pyqt5==5.10.1', 'qscintilla>=2.10',
                    'qtconsole==4.3.1', 'matplotlib==2.1.2',
                    'pgzero==1.2', 'PyQtChart>=5.10', 'appdirs>=1.4.3',
                    'gpiozero>=1.4.1', 'guizero>=0.4.5',
                    'pigpio>=1.40.post1', 'Pillow>=5.0.0',
                    'requests>=2.18.4']

# Exclude packages not available for ARM in PyPI/piwheels (Raspberry Pi)
try:
    machine = platform.machine()
    if machine.lower().startswith('arm'):
        exclude = ('pyqt5', 'qscintilla', 'qtconsole', 'PyQtChart')
        install_requires = [requirement for requirement in install_requires
                            if not requirement.startswith(exclude)]
except Exception as e:
    # Something unexpected happened, so simply keep all requires
    pass


setup(
    name='mu-editor',
    version=__version__,
    description='A simple Python editor for beginner programmers.',
    long_description='{}\n\n{}'.format(readme, changes),
    author='Nicholas H.Tollervey',
    author_email='ntoll@ntoll.org',
    url='https://github.com/mu-editor/mu',
    license='GPL3',
    packages=['mu', 'mu.contrib', 'mu.resources', 'mu.modes', 'mu.debugger',
              'mu.interface', 'mu.modes.api', ],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
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
            "mu-debug = mu.app:debug",
        ],
    }
)
