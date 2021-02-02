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
    # A fork of pgzero that works with any version of pygame >= 1.9.6
    (
        "git+https://github.com/ntoll/pgzero.git"
        "@5bcfff44fb50a30f9c0194c76099786d9e31d906",
        "",
    ),
    # Pin to a known version of pygame
    ("pygame", "==2.0.1"),
    ("Flask", "==1.1.2"),
    ("pyserial", "==3.4"),
    ("qtconsole", "==4.7.4"),
    ("nudatus", ">=0.0.3"),
    ("black", '>=19.10b0;python_version>"3.5"'),
]
WHEELS_DIRPATH = os.path.dirname(__file__)


def download(dirpath=WHEELS_DIRPATH):
    #
    # Download the wheels needed for modes
    #
    logger.debug("WHEELS_DIRPATH: %s", WHEELS_DIRPATH)
    logger.debug("mode_packages: %s", mode_packages)
    for package in mode_packages:
        print("download:package", package)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--destination-directory",
                dirpath,
                "%s%s" % package,
            ],
            check=True,
        )

    #
    # Convert any sdists to wheels
    #
    for filepath in glob.glob(os.path.join(dirpath, "*")):
        if filepath.endswith(("gz", ".zip")):
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
                check=True,
            )
            os.remove(filepath)
