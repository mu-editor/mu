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
import sys
import requests
import zipfile
import subprocess


URL = 'https://github.com/mu-editor/mu_tkinter/releases/download/'
ASSETS_32 = URL + '0.3/pynsist_tkinter_3.6_32bit.zip'
ASSETS_64 = URL + '0.3/pynsist_tkinter_3.6_64bit.zip'


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


def run(bitness):
    """
    Given a certain bitness, coordinate the downloading and unzipping of the
    appropriate assets.
    """
    print('Downloading tkinter for {}bit platform.'.format(bitness))
    if bitness == 32:
        filename = download_file(ASSETS_32)
    else:
        filename = download_file(ASSETS_64)
    print('Unzipping {}.'.format(filename))
    unzip_file(filename)
    print('Running pynsist')
    subprocess.call(['pynsist', 'win_installer{}.cfg'.format(bitness)])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            bitness = int(sys.argv[1])
            if bitness not in (32, 64):
                raise ValueError
            run(bitness)
        except ValueError:
            print('Accepted bitness: 32 or 64')
    else:
        print('Download the tkinter assets needed to create a Windows '
              'installer. Supply either 32 or 64 as an argument to indicate '
              'bitness.')
