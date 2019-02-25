"""
A script to coordinate the building of executable Windows installers using
the pynsist command.

The modus operandi is essentially the following:

* Work out if 32/64 bit build is required.
* Download the necessary tkinter based assets for the build.
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

import os
import platform
import shutil
import subprocess
import sys
import tempfile
import textwrap
import zipfile

import requests


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

files=lib
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


def frozen_requirements(repo_root, encoding, venv_name='mu-venv'):
    """
    Returns the "pip freeze" output as a string after setting up
    a temporary virtual environment where the Mu is installed.
    """
    print(f'Creating {venv_name} virtual environment...')
    subprocess.run([sys.executable, '-m', 'venv', venv_name])
    print(f'Installing mu into {venv_name}...')
    venv_python = os.path.join(venv_name, 'Scripts', 'python.exe')
    subprocess.run([venv_python, '-m', 'pip', 'install', repo_root])
    print('Getting frozen requirements...')
    result = subprocess.check_output([venv_python, '-m', 'pip', 'freeze'])
    result = result.decode(encoding)
    print(f'Removing {venv_name} virtual environment...')
    shutil.rmtree(venv_name, ignore_errors=True)
    return result


def platform_bitness():
    """
    Returns the Python executable bitness, as a string: '32' or '64'.
    Raises a RuntimeError if the platform module reports differently.
    """
    bitness, _ = platform.architecture()
    result = bitness[:2]
    if result not in ('32', '64'):
        raise RuntimeError(f'Unsupported platform.architecture: {bitness}')
    print('Python bitness:', result)
    return result


def mu_version(repo_root):
    """
    Returns the Mu version string as declared in mu/__about__.py.
    """
    about = {}
    with open(os.path.join(repo_root, 'mu', '__about__.py')) as f:
        exec(f.read(), about)
    return about['__version__']


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


def run(repo_root):
    """
    TODO: REVIEW THIS!
    Given a certain bitness, coordinate the downloading and unzipping of the
    appropriate assets.
    """
    starting_cwd = os.getcwd()
    with tempfile.TemporaryDirectory(suffix='.mu-pynsist') as work_dir:
        print('Working directory:', work_dir)
        os.chdir(work_dir)

        icon_file = os.path.join(repo_root, 'package', 'icons', 'win_icon.ico')
        license_file = os.path.join(repo_root, 'LICENSE')
        bitness = platform_bitness()
        requirements = frozen_requirements(repo_root, encoding='latin1')

        pynsist_cfg_filename = create_pynsist_cfg_file(
            encoding='latin1',
            version=mu_version(repo_root),
            icon_file=icon_file,
            license_file=license_file,
            bitness=bitness,
            pypi_wheels=textwrap.indent(requirements, ' '*4),
        )

        print('Downloading tkinter for {}bit platform.'.format(bitness))
        filename = download_file(ASSETS[bitness])

        print('Unzipping {}.'.format(filename))
        unzip_file(filename)

        print('Running pynsist')
        subprocess.call(['pynsist', pynsist_cfg_filename])

        print('DONE!!!')
        import time; time.sleep(60)

        os.chdir(starting_cwd)


if __name__ == '__main__':
    if len(sys.argv) != 2 or not sys.argv[1].endswith('setup.py'):
        sys.exit('Supply the setup.py file as an argument, please.')
    repo_root = os.path.abspath(os.path.dirname(sys.argv[1]))
    run(repo_root)
