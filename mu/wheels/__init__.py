#
# Download wheels corresponding to the baseline modes
#
import os
import sys
import glob
import subprocess

mode_packages = [
    ("pgzero", ""),
    ("Flask", "==1.1.2"),
    ("pyserial", "==3.4"),
    ("qtconsole", "==4.7.4"),
    ("nudatus", ">=0.0.3"),
]
wheels_dirpath = os.path.dirname(__file__)


def download(dirpath):
    #
    # Download the wheels needed for modes
    #
    for package in mode_packages:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--dest",
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
                    wheels_dirpath,
                    filepath,
                ],
                check=True,
            )
            os.remove(filepath)
