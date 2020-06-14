"""
This is a custom version of the PyNsist script which overrides only those
aspects of the building of the installer for the purposes of making Mu work
correctly on Windows.

The customisations are:

* Unzip the python36.zip file into a directory called python36.zip, to mitigate
  a bug in setuptools.
* Delete any "*._pth" files in the Python directory, since these interfere with
  the paths available to Mu and automatically put the interpreter into
  isolated mode.
* Ensure the launcher passes the "-Es" flags into Python to ignore any
  PYTHON* environment variables and to ignore the user's site directory.

This final step ensures Python is running "isolated" from settings which may
be from an existing installed "system" Python.
"""
import io
import logging
import ntpath
import os
import shutil
import sys
import winreg
import zipfile

from nsist import InstallerBuilder
from nsist.configreader import get_installer_builder_args
from nsist.util import download, get_cache_dir

pjoin = os.path.join
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_makensis_win():
    """Locate makensis.exe on Windows by querying the registry"""
    try:
        nsis_install_dir = winreg.QueryValue(
            winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\NSIS"
        )
    except OSError:
        nsis_install_dir = winreg.QueryValue(
            winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\NSIS"
        )

    return pjoin(nsis_install_dir, "makensis.exe")


class InputError(ValueError):
    def __init__(self, param, value, expected):
        self.param = param
        self.value = value
        self.expected = expected

    def __str__(self):
        return "{e.value!r} is not valid for {e.param}, expected {e.expected}".format(
            e=self
        )


class MuInstallerBuilder(InstallerBuilder):
    """Controls building an installer specific for Mu. Inherits and overrides
    from the nsis.InstallerBuilder class which drives this process.

    See the documentation on that class for all the details.
    """

    def fetch_python_embeddable(self):
        """Fetch the embeddable Windows build for the specified Python version

        It will be unpacked into the build directory.

        In addition, any ``*._pth`` files found therein will have the pkgs path
        appended to them.
        """
        url, filename = self._python_download_url_filename()
        cache_file = get_cache_dir(ensure_existence=True) / filename
        if not cache_file.is_file():
            logger.info("Downloading embeddable Python build...")
            logger.info("Getting %s", url)
            download(url, cache_file)

        print("Using " + str(cache_file))

        logger.info("Unpacking Python...")
        python_dir = pjoin(self.build_dir, "Python")

        with zipfile.ZipFile(str(cache_file)) as z:
            z.extractall(python_dir)

        # Ensure stdlib is an unzipped folder called pythonXY.zip (where X, Y
        # are MAJOR MINOR version numbers).
        version = "".join(self.py_version.split(".")[:2])
        stdlibzip = "python{}.zip".format(version)
        zipped = os.path.abspath(pjoin(python_dir, stdlibzip))
        temp_target = os.path.abspath(pjoin(python_dir, "tempstdlib"))
        with zipfile.ZipFile(zipped) as z:
            z.extractall(temp_target)
        # Rename the unzipped directory to pythonXY.zip
        os.remove(zipped)
        os.rename(temp_target, zipped)

        # Delete all *._pth files. See:
        # https://docs.python.org/3/using/windows.html#finding-modules
        # for more information.
        pth_files = [
            os.path.abspath(pjoin(python_dir, f))
            for f in os.listdir(python_dir)
            if os.path.isfile(pjoin(python_dir, f)) and f.endswith("._pth")
        ]
        for pth in pth_files:
            print("Removing " + pth)
            os.remove(pth)

        self.install_dirs.append(("Python", "$INSTDIR"))

    def prepare_shortcuts(self):
        """Prepare shortcut files in the build directory.

        If entry_point is specified, write the script. If script is specified,
        copy to the build directory. Prepare target and parameters for these
        shortcuts.

        Also copies shortcut icons.
        """
        files = set()
        for scname, sc in self.shortcuts.items():
            if not sc.get("target"):
                if sc.get("entry_point"):
                    sc["script"] = script = (
                        scname.replace(" ", "_")
                        + ".launch.py"
                        + ("" if sc["console"] else "w")
                    )

                    specified_preamble = sc.get("extra_preamble", None)
                    if isinstance(specified_preamble, str):
                        # Filename
                        extra_preamble = io.open(
                            specified_preamble, encoding="utf-8"
                        )
                    elif specified_preamble is None:
                        extra_preamble = io.StringIO()  # Empty
                    else:
                        # Passed a StringIO or similar object
                        extra_preamble = specified_preamble

                    self.write_script(
                        sc["entry_point"],
                        pjoin(self.build_dir, script),
                        extra_preamble.read().rstrip(),
                    )
                else:
                    shutil.copy2(sc["script"], self.build_dir)

                target = "$INSTDIR\Python\python{}.exe"
                sc["target"] = target.format("" if sc["console"] else "w")
                sc["parameters"] = '"-Es" "%s"' % ntpath.join(
                    "$INSTDIR", sc["script"]
                )
                files.add(os.path.basename(sc["script"]))

            shutil.copy2(sc["icon"], self.build_dir)
            sc["icon"] = os.path.basename(sc["icon"])
            files.add(sc["icon"])
        self.install_files.extend([(f, "$INSTDIR") for f in files])


def main(argv=None):
    """Make an installer from the command line.

    This parses command line arguments and a config file, and calls
    :func:`all_steps` with the extracted information.
    """
    logger.setLevel(logging.INFO)
    logger.handlers = [logging.StreamHandler()]

    import argparse

    argp = argparse.ArgumentParser(prog="pynsist")
    argp.add_argument("config_file")
    argp.add_argument(
        "--no-makensis",
        action="store_true",
        help="Prepare files and folders, stop before calling makensis. For debugging.",
    )
    options = argp.parse_args(argv)

    dirname, config_file = os.path.split(options.config_file)
    if dirname:
        os.chdir(dirname)

    from nsist import configreader

    try:
        cfg = configreader.read_and_validate(config_file)
    except configreader.InvalidConfig as e:
        logger.error("Error parsing configuration file:")
        logger.error(str(e))
        sys.exit(1)

    args = get_installer_builder_args(cfg)

    try:
        ec = MuInstallerBuilder(**args).run(makensis=(not options.no_makensis))
    except InputError as e:
        logger.error("Error in config values:")
        logger.error(str(e))
        sys.exit(1)

    return ec


if __name__ == "__main__":
    main()
