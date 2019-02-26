"""
A script to coordinate the building of executable Windows installers using
the pynsist command.

Due to the need of having Mu's setup.py be the authoritative reference for
its third party package dependencies, the modus operandi is essentially the
following, all done under a temporary work directory:

* Work out if 32/64 bit build is required.
* Create an isolated virtual environment.
* pip install mu into it
* Capture pip freeze output to identify pinned dependencies.
* Determine which of those are available as PyPI wheels.
* Generate a pynsist configuration file based on a builtin template:
  * Fill in {version} from Mu's __about__.py
  * Fill in {pypy_wheels} per the previous step list.
  * Fill in {packages} with the non-available PyPI wheels, if any.
* Download the necessary tkinter based assets for the build.
* Install pynsist into the virtual environment.
* Kick off pynsist.

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

import glob
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import textwrap
import zipfile

import requests
import yarg


PYNSIST_CFG_TEMPLATE = """
[Application]
name=Mu
version={version}
entry_point=mu.app:run
icon={icon_file}
publisher=Nicholas H.Tollervey
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

{packages_optional}

files=lib

[Build]
installer_name={installer_name}
"""


URL = 'https://github.com/mu-editor/mu_tkinter/releases/download/'
ASSETS = {
    '32': URL + '0.3/pynsist_tkinter_3.6_32bit.zip',
    '64': URL + '0.3/pynsist_tkinter_3.6_64bit.zip',
}


def download_file(url):
    """
    Download the URL and return the filename.
    """
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


def unzip_file(filename):
    """
    Given a filename, unzip it into the current working directory.
    """
    with zipfile.ZipFile(filename) as z:
        z.extractall()


def create_packaging_venv(name='mu-packaging-venv'):
    """
    """
    print(f'Creating {name} virtual environment...')
    subprocess.run([sys.executable, '-m', 'venv', name])
    return os.path.join(name, 'Scripts', 'python.exe')


def install_mu(python_executable, repo_root):
    """
    """
    print(f'Installing mu with {python_executable}...')
    subprocess.run([python_executable, '-m', 'pip', 'install', repo_root])


def pip_freeze(python_executable, exclude, encoding):
    """
    Returns the "pip freeze" output as a list of strings.
    """
    print('Getting frozen requirements...')
    output = subprocess.check_output([python_executable, '-m', 'pip', 'freeze', '--all'])
    text = output.decode(encoding)
    return [
        line for line in text.splitlines()
        if line.partition('==')[0] != exclude
    ]


def about_dict(repo_root):
    """
    Returns the Mu about dict with keys from the variables in mu/__about__.py.
    """
    about = {}
    with open(os.path.join(repo_root, 'mu', '__about__.py')) as f:
        exec(f.read(), about)
    return about


def wheels_in(requirements):
    """
    TODO: WRITE ME!
    """
    print('Checking for wheel availability at PyPI...')
    wheels = []
    for requirement in requirements:
        name, _, version = requirement.partition('==')
        print(f'  - {requirement}: ', end='')
        package = yarg.get(name)
        releases = package.release(version)
        if any(r.package_type == 'wheel' for r in releases):
            wheels.append(requirement)
            feedback = 'ok'
        else:
            feedback = 'missing'
        print(feedback)
    return wheels


def packages_from(requirements, wheels):
    """
    """
    rset = set(requirements)
    wset = set(wheels)
    pset = rset - wset
    return [p.partition('==')[0] for p in pset]


def create_pynsist_cfg_file(encoding, **kw):
    """
    TODO: WRITE ME!
    """
    filename = 'pynsist.cfg'
    pynsist_cfg_payload = PYNSIST_CFG_TEMPLATE.format(**kw)
    with open(filename, 'wt', encoding=encoding) as f:
        f.write(pynsist_cfg_payload)
    print('Created pynsist.cfg file:')
    print(pynsist_cfg_payload)
    return filename


def run(bitness, repo_root):
    """
    TODO: REVIEW THIS!
    Given a certain bitness, coordinate the downloading and unzipping of the
    appropriate assets.
    """
    starting_cwd = os.getcwd()
    with tempfile.TemporaryDirectory(suffix='.mu-pynsist') as work_dir:
        print('Changing working directory to', work_dir)
        os.chdir(work_dir)

        mu_about = about_dict(repo_root)
        mu_package_name = mu_about['__title__']
        mu_version = mu_about['__version__']

        python_exec = create_packaging_venv()
        install_mu(python_exec, repo_root)

        requirements = pip_freeze(python_exec, exclude=mu_package_name, encoding='latin1')
        wheels = wheels_in(requirements)
        packages = packages_from(requirements, wheels)

        if packages:
            packages_payload = '\n    '.join(packages)
            packages_optional = 'packages=\n    {}'.format(packages_payload)
        else:
            packages_optional = ''

        icon_file = os.path.join(repo_root, 'package', 'icons', 'win_icon.ico')
        license_file = os.path.join(repo_root, 'LICENSE')

        installer_name = f'{mu_package_name}_{mu_version}_win{bitness}.exe'

        pynsist_cfg_filename = create_pynsist_cfg_file(
            encoding='latin1',
            installer_name=installer_name,
            version=mu_version,
            icon_file=icon_file,
            license_file=license_file,
            bitness=bitness,
            pypi_wheels='\n    '.join(wheels),
            packages_optional=packages_optional,
        )

        print('Downloading tkinter for {}bit platform.'.format(bitness))
        filename = download_file(ASSETS[bitness])

        print('Unzipping {}.'.format(filename))
        unzip_file(filename)

        print('Installing pynsist.')
        subprocess.run([python_exec, '-m', 'pip', 'install', 'pynsist'])

        print('Running pynsist')
        subprocess.run([python_exec, '-m', 'nsist', pynsist_cfg_filename])

        shutil.copy(
            os.path.join('build', 'nsis', installer_name),
            starting_cwd,
        )
        os.chdir(starting_cwd)

    print(f'Completed. Installer file is {installer_name}.')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Supply bitness (32 or 64) and path to setup.py.')
        
    bitness, setup_py_path = sys.argv[1:]
    if bitness not in ASSETS:
        sys.exit(f'Invalid bitness {bitness}: use 32 or 64.')
    if not setup_py_path.endswith('setup.py'):
        sys.exit(f'Invalid path to setup.py: {setup_py_path}.')

    repo_root = os.path.abspath(os.path.dirname(setup_py_path))
    run(bitness, repo_root)
