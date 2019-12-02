"""
A script to coordinate the building of executable Windows installers using
the pynsist command.

Due to the need of having Mu's setup.py be the authoritative reference for
its third party package dependencies, the modus operandi is essentially the
following, all done under a temporary work directory:

* Work out if 32/64 bit build is required.
* Create an isolated virtual environment.
* pip install mu into it.
* Capture pip freeze --all output to identify pinned dependencies.
* Determine which of those are available as PyPI wheels.
* Generate a pynsist configuration file based on a builtin template:
  * Fill in {version} from Mu's __about__.py
  * Fill in {pypy_wheels} per the previous step list.
  * Fill in {packages} with the remaining dependencies.
  * ...and a few other, simpler, entries.
* Download the necessary tkinter based assets for the build.
* Install pynsist into the virtual environment.
* Kick off pynsist.
* Copy the resulting executable installer to the current working directory.

Copyright (c) 2018 Nicholas H.Tollervey.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import requests
import yarg


# The pynsist requirement spec that will be used to install pynsist in
# the temporary packaging virtual environment.

PYNSIST_REQ = "pynsist==2.3"

# The pynsist configuration file template that will be used. Of note,
# with regards to pynsist dependency collection and preparation:
# - {pypi_wheels} will be downloaded by pynsist from PyPI.
# - {packages} will be copied by pynsist from the current Python env.

PYNSIST_CFG_TEMPLATE = """
[Application]
name=Mu
version={version}
entry_point=mu.app:run
icon={icon_file}
publisher={publisher}
license_file={license_file}

[Command mu-debug]
entry_point=mu.app:debug

[Command pgzrun]
entry_point=pgzero.runner:main

[Python]
version=3.6.3
bitness={bitness}
format=bundled

[Include]
pypi_wheels=
    {pypi_wheels}

packages=
    tkinter
    _tkinter
    turtle
    {packages}

files=lib

[Build]
installer_name={installer_name}
"""


# URLs for tkinter assets, not included in Python's embeddable distribution
# pynsist fetches and uses, that we want to bundle with Mu.

URL = "https://github.com/mu-editor/mu_tkinter/releases/download/"
TKINTER_ASSETS_URLS = {
    "32": URL + "0.3/pynsist_tkinter_3.6_32bit.zip",
    "64": URL + "0.3/pynsist_tkinter_3.6_64bit.zip",
}


def create_packaging_venv(target_directory, name="mu-packaging-venv"):
    """
    Creates a Python virtual environment in the target_directry, returning
    the path to the newly created environment's Python executable.
    """
    fullpath = os.path.join(target_directory, name)
    subprocess.run([sys.executable, "-m", "venv", fullpath])
    if sys.platform == "win32":
        return os.path.join(fullpath, "Scripts", "python.exe")
    else:
        return os.path.join(fullpath, "bin", "python")


def pip_freeze(python, encoding):
    """
    Returns the "pip freeze --all" output as a list of strings.
    """
    print("Getting frozen requirements.")
    output = subprocess.check_output([python, "-m", "pip", "freeze", "--all"])
    text = output.decode(encoding)
    return text.splitlines()


def about_dict(repo_root):
    """
    Returns the Mu about dict: keys are the __variables__ in mu/__init__.py.
    """
    DUNDER_ASSIGN_RE = re.compile(r"""^__\w+__\s*=\s*['"].+['"]$""")
    about = {}
    with open(os.path.join(repo_root, "mu", "__init__.py")) as f:
        for line in f:
            if DUNDER_ASSIGN_RE.search(line):
                exec(line, about)
    return about


def pypi_wheels_in(requirements):
    """
    Returns a list of the entries in requirements which are distributed as
    wheels in PyPI (where requirements is a list of strings formatted like
    "name==version").
    """
    print("Checking for wheel availability at PyPI.")
    wheels = []
    for requirement in requirements:
        name, _, version = requirement.partition("==")
        print("-", requirement, end=" ")
        package = yarg.get(name)
        releases = package.release(version)
        if any(r.package_type == "wheel" for r in releases):
            wheels.append(requirement)
            feedback = "ok"
        else:
            feedback = "missing"
        print(feedback)
    return wheels


def packages_from(requirements, wheels):
    """
    Returns a list of the entires in requirements that aren't found in
    wheels (both assumed to be lists/iterables of strings formatted like
    "name==version").
    """
    packages = set(requirements) - set(wheels)
    return [p.partition("==")[0] for p in packages]


def create_pynsist_cfg(python, repo_root, filename, encoding="latin1"):
    """
    Creates a pynsist configuration file from the PYNSIST_CFG_TEMPLATE
    built-in template. Determines dependencies by running pip freeze,
    which are then split between those distributed as PyPI wheels and
    others. Returns the name of the resulting installer executable, as
    set into the pynsist configuration file.
    """
    mu_about = about_dict(repo_root)
    mu_package_name = mu_about["__title__"]
    mu_version = mu_about["__version__"]
    mu_author = mu_about["__author__"]

    icon_file = os.path.join(repo_root, "package", "icons", "win_icon.ico")
    license_file = os.path.join(repo_root, "LICENSE")

    # On Linux Debian systems "pkg-resources" is erroneously reported.
    # This is a bug in Debian's patched version of pip.
    excluded_packages = {mu_package_name, "pkg-resources", "noise"}
    # Packages that only install on Windows, but not on Linux.
    force_include_packages = {"pywin32==227"}

    requirements = [
        # Those from pip freeze except the Mu package itself.
        line
        for line in pip_freeze(python, encoding=encoding)
        if line.partition("==")[0] not in excluded_packages
    ]
    for p in force_include_packages:
        if p not in requirements:
            requirements.append(p)
    wheels = pypi_wheels_in(requirements)
    packages = packages_from(requirements, wheels)

    installer_exe = "{}_{}bit.exe".format(mu_package_name, bitness)

    pynsist_cfg_payload = PYNSIST_CFG_TEMPLATE.format(
        version=mu_version,
        icon_file=icon_file,
        license_file=license_file,
        publisher=mu_author,
        bitness=bitness,
        pypi_wheels="\n    ".join(wheels),
        packages="\n    ".join(packages),
        installer_name=installer_exe,
    )
    with open(filename, "wt", encoding=encoding) as f:
        f.write(pynsist_cfg_payload)
    print("Wrote pynsist configuration file", filename)
    print("Contents:")
    print(pynsist_cfg_payload)
    print("End of pynsist configuration file.")

    return installer_exe


def download_file(url, target_directory):
    """
    Download the URL to the target_directory and return the filename.
    """
    local_filename = os.path.join(target_directory, url.split("/")[-1])
    r = requests.get(url, stream=True)
    with open(local_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


def unzip_file(filename, target_directory):
    """
    Given a filename, unzip it into the given target_directory.
    """
    with zipfile.ZipFile(filename) as z:
        z.extractall(target_directory)


def run(bitness, repo_root):
    """
    Given a certain bitness and the Mu's repository root directory, generate
    a pynsist configuration file (locking the dependencies set in setup.py),
    download and extract the tkinter related assets, and run pynsist.
    """
    with tempfile.TemporaryDirectory(prefix="mu-pynsist-") as work_dir:
        print("Temporary working directory at", work_dir)

        print("Creating the packaging virtual environment.")
        venv_python = create_packaging_venv(work_dir)

        print("Updating pip in the virtual environment", venv_python)
        subprocess.run(
            [venv_python, "-m", "pip", "install", "--upgrade", "pip"]
        )

        print("Installing mu with", venv_python)
        subprocess.run([venv_python, "-m", "pip", "install", repo_root])

        pynsist_cfg = os.path.join(work_dir, "pynsist.cfg")
        print("Creating pynsist configuration file", pynsist_cfg)
        installer_exe = create_pynsist_cfg(venv_python, repo_root, pynsist_cfg)

        url = TKINTER_ASSETS_URLS[bitness]
        print("Downloading {}bit tkinter assets from {}.".format(bitness, url))
        filename = download_file(url, work_dir)

        print("Unzipping tkinter assets to", work_dir)
        unzip_file(filename, work_dir)

        print("Installing pynsist.")
        subprocess.run([venv_python, "-m", "pip", "install", PYNSIST_REQ])

        mu_pynsist_script = os.path.join(repo_root, "package", "mu_nsist.py")
        print("Running custom pynsist script at", mu_pynsist_script)
        subprocess.run([venv_python, mu_pynsist_script, pynsist_cfg])

        destination_dir = os.path.join(repo_root, "dist")
        print("Copying installer file to", destination_dir)
        os.makedirs(destination_dir, exist_ok=True)
        shutil.copy(
            os.path.join(work_dir, "build", "nsis", installer_exe),
            destination_dir,
        )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Supply bitness (32 or 64) and path to setup.py.")

    bitness, setup_py_path = sys.argv[1:]
    if bitness not in TKINTER_ASSETS_URLS:
        sys.exit("Unsupported bitness {}: use 32 or 64.".format(bitness))
    if not setup_py_path.endswith("setup.py"):
        sys.exit("Invalid path to setup.py:", setup_py_path)

    repo_root = os.path.abspath(os.path.dirname(setup_py_path))
    run(bitness, repo_root)
