import os
import re
from setuptools import setup


base_dir = os.path.dirname(__file__)


DUNDER_ASSIGN_RE = re.compile(r"""^__\w+__\s*=\s*['"].+['"]$""")
about = {}
with open(os.path.join(base_dir, "mu", "__init__.py"), encoding="utf8") as f:
    for line in f:
        if DUNDER_ASSIGN_RE.search(line):
            exec(line, about)

with open(os.path.join(base_dir, "README.rst"), encoding="utf8") as f:
    readme = f.read()

with open(os.path.join(base_dir, "CHANGES.rst"), encoding="utf8") as f:
    changes = f.read()


install_requires = [
    #
    # The core 'install_requires' should only be things
    # which are needed for the main editor to function.
    #
    "PyQt5==5.13.2"
    + ';"arm" not in platform_machine and "aarch" not in platform_machine',
    "QScintilla==2.11.3"
    + ';"arm" not in platform_machine and "aarch" not in platform_machine',
    "PyQtChart==5.13.1"
    + ';"arm" not in platform_machine and "aarch" not in platform_machine',
    # FIXME: jupyter-client added for Py3.5 compatibility, to be dropped after
    # Mu v1.1 release. So, qtconsole < 5 and jupyter-client < 6.2 (issue #1444)
    "jupyter-client>=4.1,<6.2",
    "qtconsole==4.7.7",
    #
    # adafruit-board-toolkit is used to find serial ports and help identify
    # CircuitPython boards in the CircuitPython mode.
    "adafruit-board-toolkit>=1.0.1",
    "pyserial>=3.5",
    "nudatus>=0.0.3",
    # `flake8` is actually a testing/packaging dependency that, among other
    # packages, brings in `pycodestyle` and `pyflakes` which are runtime
    # dependencies. For the sake of "locality", it is being declared here,
    # though. Regarding these packages' versions, please refer to:
    # http://flake8.pycqa.org/en/latest/faq.html#why-does-flake8-use-ranges-for-its-dependencies
    "flake8 >= 3.8.3",
    "black>=19.10b0;python_version>'3.5'",
    "appdirs>=1.4.3",
    "semver>=2.8.0",
    #
    # Needed for creating the runtime virtual environment
    #
    "virtualenv>=16.0.0",
    #
    # Needed for packaging
    #
    "wheel",
]


extras_require = {
    "tests": [
        "pytest>=4.6",
        "pytest-cov",
        "pytest-random-order>=1.0.0",
        "pytest-faulthandler",
        "pytest-timeout",
        "coverage",
    ],
    "docs": [
        "sphinx",
    ],
    "package": [
        # Wheel building and PyPI uploading
        "wheel",
        "twine",
    ],
    "utils": ["scrapy", "beautifulsoup4", "requests"],
}

extras_require["dev"] = (
    extras_require["tests"]
    + extras_require["docs"]
    + extras_require["package"]
)

extras_require["all"] = list(
    {req for extra, reqs in extras_require.items() for req in reqs}
)


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description="{}\n\n{}".format(readme, changes),
    author=about["__author__"],
    author_email=about["__email__"],
    url=about["__url__"],
    license=about["__license__"],
    packages=[
        "mu",
        "mu.contrib",
        "mu.resources",
        "mu.modes",
        "mu.debugger",
        "mu.interface",
        "mu.modes.api",
        "mu.wheels",
    ],
    python_requires=">=3.5,<3.9",
    install_requires=install_requires,
    extras_require=extras_require,
    package_data={"mu.wheels": ["*.whl"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Education",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Text Editors",
        "Topic :: Text Editors :: Integrated Development Environments (IDE)",
    ],
    entry_points={"console_scripts": ["mu-editor = mu.app:run"]},
)
