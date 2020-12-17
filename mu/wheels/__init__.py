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
    #
    # There's a Windows compiler bug atm which means
    # that numpy 1.19.4 will fail at runtime
    #
    ("numpy", "<1.19.4"),
    ("pgzero", ""),
    ("Flask", "==1.1.2"),
    ("pyserial", "==3.4"),
    ("qtconsole", "==4.7.4"),
    ("nudatus", ">=0.0.3"),
    ("black", ">=19.10b0"),
]
WHEELS_DIRPATH = os.path.dirname(__file__)


def download(dirpath=WHEELS_DIRPATH):
    #
    # Download the wheels needed for modes
    #
    print("download:WHEELS_DIRPATH", WHEELS_DIRPATH)
    print("download:mode_packages", mode_packages)
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

    #
    # FIXME: for now, we need numpy==1.19.3 as there's a Windows bug which
    # prevents us from using >=1.19.4
    # https://developercommunity.visualstudio.com/
    # content/problem/1207405/
    # fmod-after-an-update-to-windows-2004-is-causing-a.html
    #
    # We explicitly download 1.19.3 but then pygame pulls in 1.19.4 as one
    # of its deps
    #
    # So, for now, we just find and delete the numpy 1.19.4 wheels
    #
    for numpy_1194 in glob.glob(os.path.join(dirpath, "numpy-1.19.4*.whl")):
        logger.warn("Found numpy 1.19.4; deleting %s", numpy_1194)
        os.remove(numpy_1194)
