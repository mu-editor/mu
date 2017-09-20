from setuptools import setup
from mu import __version__


with open('README.rst') as f:
    readme = f.read()
with open('CHANGES.rst') as f:
    changes = f.read()


setup(
    name='mu',
    version=__version__,
    description='A simple editor for beginner programmers.',
    long_description='{}\n\n{}'.format(readme, changes),
    author='Nicholas H.Tollervey',
    author_email='ntoll@ntoll.org',
    url='https://github.com/mu-editor/mu',
    license='GPL3',
    packages=['mu', 'mu.contrib', 'mu.resources', 'mu.modes', 'mu.debugger',
              'mu.interface', ],
    install_requires=['pycodestyle', 'pyflakes', 'pyserial', 'pyqt5',
                      'qscintilla', 'qtconsole', 'matplotlib==2.0.2', ],
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
