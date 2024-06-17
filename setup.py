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
    "PyQt5==5.15.10"
    + '; sys_platform != "linux" '
    + 'or ("arm" not in platform_machine and "aarch" not in platform_machine)',
    "QScintilla==2.14.1"
    + '; sys_platform != "linux" '
    + 'or ("arm" not in platform_machine and "aarch" not in platform_machine)',
    "PyQtChart==5.15.6"
    + '; sys_platform != "linux" '
    + 'or ("arm" not in platform_machine and "aarch" not in platform_machine)',
    # ipykernel has to be < v6 (<5.99 used because <6 installs v6.0.0rc2) for
    # macOS 10.13 compatibility (v6+ depends on debugpy), v5.5.6 resolves
    # ipython/ipykernel#759. Line can be removed with PyQt6 (macOS 10.14+).
    # ipykernel version has to be mirrored in mu/wheels/__init__.py
    "ipykernel>=5.5.6,<5.99",
    "qtconsole~=5.4",
    # In Python 3.12 the deprecated 'imp' module was removed from the stdlib.
    # ipykernel only moved to importlib in v6.10, so this is a "forward-port"
    "zombie_imp>=0.0.2;python_version>='3.12'",
    # adafruit-board-toolkit is used to find serial ports and help identify
    # CircuitPython boards in the CircuitPython mode.
    "adafruit-board-toolkit~=1.1",
    "pyserial~=3.5",
    "nudatus>=0.0.3",
    # `flake8` is actually a testing/packaging dependency that, among other
    # packages, brings in `pycodestyle` and `pyflakes` which are runtime
    # dependencies. For the sake of "locality", it is being declared here,
    # though. Regarding these packages' versions, please refer to:
    # http://flake8.pycqa.org/en/latest/faq.html#why-does-flake8-use-ranges-for-its-dependencies
    "flake8 >= 3.8.3",
    # Clamp click max version to workaround incompatibility with black<22.1.0
    "click<=8.0.4",
    "black>=19.10b0,<22.1.0",
    "platformdirs>=2.0.0,<3.0.0",
    "semver>=2.8.0",
    # virtualenv vendors pip, we need at least pip v19.3 to install some
    # rust based dependencies. virtualenv >=v20 is required for the --symlinks
    # flag needed by AppImage, and it packs pip v20.0.2.
    "virtualenv>=20.0.0",
    #
    # Needed for packaging
    #
    "wheel",
    # Needed to deploy from web mode
    "requests>=2.0.0",
    #
    # Needed to resolve an issue with paths in the user virtual environment
    #
    "pywin32; sys_platform=='win32'",
    # pkg_resources has been removed in Python 3.12, until we move to importlib
    # we need it via setuptools: https://github.com/mu-editor/mu/issues/2485
    "setuptools",
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
    "docs": ["sphinx"],
    "package": [
        # Wheel building and PyPI uploading
        "wheel",
        "twine",
    ],
    "i18n": ["babel"],
    "utils": ["scrapy", "beautifulsoup4", "requests"],
}

extras_require["dev"] = (
    extras_require["tests"]
    + extras_require["docs"]
    + extras_require["package"]
    + extras_require["i18n"]
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
    python_requires=">=3.7,<3.13",
    install_requires=install_requires,
    extras_require=extras_require,
    package_data={"mu.wheels": ["*.whl", "*.zip"]},
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
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
