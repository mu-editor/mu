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
    author='Nicholas Tollervey',
    author_email='ntoll@ntoll.org',
    url='https://github.com/mu-editor/mu',
    packages=['mu', 'mu.contrib', 'mu.resources', 'mu.modes', 'mu.debugger'],
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
            "mu-debug = mu.app:debug",
        ],
    },
    data_files=[('/usr/share/pixmaps', ['conf/mu.png', ]),
                ('/usr/share/applications', ['conf/mu.desktop', ])],
)
