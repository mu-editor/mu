from setuptools import setup
from mu import __version__


with open('README.rst') as f:
    readme = f.read()
with open('CHANGES.rst') as f:
    changes = f.read()


setup(
    name='mu-editor',
    version=__version__,
    description='A simple editor for beginner programmers.',
    long_description='{}\n\n{}'.format(readme, changes),
    author='Nicholas H.Tollervey',
    author_email='ntoll@ntoll.org',
    url='https://github.com/mu-editor/mu',
    license='GPL3',
    packages=['mu', 'mu.contrib', 'mu.resources', 'mu.modes', 'mu.debugger',
              'mu.interface', 'mu.modes.api', ],
    install_requires=['pycodestyle==2.3.1', 'pyflakes==1.6.0',
                      'pyserial==3.4', 'pyqt5==5.9', 'qscintilla==2.10.1',
                      'qtconsole==4.3.1', 'matplotlib==2.0.2', ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Education',
        'Topic :: Software Development :: Embedded Systems',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts': [
            "mu = mu.app:run",
            "mu-debug = mu.app:debug",
        ],
    }
)
