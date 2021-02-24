#
# Download wheels corresponding to the baseline modes
#
import os
import sys
import glob
import logging
import platform
import subprocess

logger = logging.getLogger(__name__)

#
# List of base packages to support modes
# The first element should be the importable name (so "serial" rather than "pyserial")
# The second element is passed to `pip download|install`
# Any additional elements are passed to `pip` for specific purposes
#
mode_packages = [
    (
        "pgzero",
        "git+https://github.com/mu-editor/pgzero.git@mu-wheel",
    ),
    ("flask", "flask==1.1.2"),
    ("serial", "pyserial>=3.0"),
    ("qtconsole", "qtconsole==4.7.4"),
    ("nudatus", "nudatus>=0.0.3"),
    ("esptool", "esptool==3.*"),
]
WHEELS_DIRPATH = os.path.dirname(__file__)

# TODO: Temp app signing workaround https://github.com/mu-editor/mu/issues/1290
if sys.version_info[:2] == (3, 8) and platform.system() == "Darwin":
    mode_packages = [
        (
            "pygame",
            "https://github.com/mu-editor/pygame/releases/download/2.0.1/"
            "pygame-2.0.1-cp38-cp38-macosx_10_9_intel.whl",
        ),
        (
            "numpy",
            "numpy==1.20.1",
        ),
        (
            "pgzero",
            "https://github.com/mu-editor/pgzero/releases/download/mu-wheel/"
            "pgzero-1.2-py3-none-any.whl",
            "--no-index",
            "--find-links=" + WHEELS_DIRPATH,
        ),
    ] + mode_packages[1:]


def download(dirpath=WHEELS_DIRPATH):
    #
    # Download the wheels needed for modes
    #
    logger.debug("dirpath: %s", dirpath)

    #
    # Clear the directory of any existing wheels and source distributions
    # (this is especially important because there may have been wheels
    # left over from a test with a different Python version)
    #
    rm_files = (
        glob.glob(os.path.join(dirpath, "*.whl"))
        + glob.glob(os.path.join(dirpath, "*.gz"))
        + glob.glob(os.path.join(dirpath, "*.zip"))
    )
    for rm_filepath in rm_files:
        logger.debug("Removing %s", rm_filepath)
        os.remove(rm_filepath)

    logger.debug("mode_packages: %s", mode_packages)
    for name, pip_identifier, *extra_flags in mode_packages:
        logger.info(
            "Running pip download for %s / %s / %s",
            name,
            pip_identifier,
            extra_flags,
        )
        process = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--destination-directory",
                dirpath,
                pip_identifier,
            ]
            + extra_flags,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
        logger.debug(process.stdout.decode("utf-8"))

    #
    # Convert any sdists to wheels
    #
    for filepath in glob.glob(os.path.join(dirpath, "*")):
        if filepath.endswith(("gz", ".zip")):
            logger.info("Building wheel for %s", filepath)
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "wheel",
                    "--wheel-dir",
                    dirpath,
                    filepath,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True,
            )
            os.remove(filepath)
            logger.debug(process.stdout.decode("utf-8"))
