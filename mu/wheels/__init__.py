#
# Download wheels corresponding to the baseline modes
#
import os
import sys
import glob
import logging
import subprocess

logger = logging.getLogger(__name__)

mode_packages = [
    (
        "pgzero",
        "git+https://github.com/ntoll/pgzero.git@"
        "5bcfff44fb50a30f9c0194c76099786d9e31d906",
    ),
    ("Flask", "flask==1.1.2"),
    ("pyserial", "pyserial==3.4"),
    ("qtconsole", "qtconsole==4.7.4"),
    ("nudatus", "nudatus>=0.0.3"),
    ("esptool", "esptool==3.*"),
]
WHEELS_DIRPATH = os.path.dirname(__file__)


def download(dirpath=WHEELS_DIRPATH):
    #
    # Download the wheels needed for modes
    #
    logger.debug("dirpath: %s", dirpath)

    #
    # Clear the directory of any existing wheels (this is especially
    # important because there may have been wheels left over from a
    # test with a different Python version)
    #
    for wheel_filepath in glob.glob(os.path.join(dirpath, "*.whl")):
        logger.debug("Removing %s", wheel_filepath)
        os.remove(wheel_filepath)

    logger.debug("mode_packages: %s", mode_packages)
    for name, pip_identifier in mode_packages:
        logger.info("Running pip download for %s / %s", name, pip_identifier)
        process = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--destination-directory",
                dirpath,
                pip_identifier,
            ],
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
