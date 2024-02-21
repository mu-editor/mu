#!/usr/bin/env python3
"""Update the copy of pgzhelper in Pygame Zero.

pgzhelper is not yet packaged on PyPI; this script exists to mirror it into the
local repository to make it easily installable.

"""
import json
import base64
import subprocess
from urllib.parse import urljoin
from urllib.request import build_opener


FILE = 'pgzhelper.py'
DEST = 'mu/resources/pygamezero/pgzhelper.py'
REPO_URL = 'https://api.github.com/repos/roboticsware/pgzhelper/'
HEADER = '''"""pgzhelper - Enhance Pygame Zero with additional capabilities.

This module is directly copied from

    https://github.com/roboticsware/pgzhelper

at revision {sha}
and used under CC0.

"""
# flake8: noqa: E501
'''


# Customise the opener here if you need to
opener = build_opener()


def read_json(url):
    """Download and decode a JSON resource from the given URL."""
    resp = opener.open(url)
    charset = resp.headers.get_content_charset()
    data = resp.read().decode(charset)
    return json.loads(data)


def get_tree():
    """Download the repository tree, returning a decoded JSON structure."""
    print('Downloading repository tree...')
    url = urljoin(REPO_URL, 'git/trees/HEAD')
    return read_json(url)


def get_file(file):
    """Download the tree state and named file.

    Return a tuple of the current repo version hash and the file's data.

    """
    tree = get_tree()
    for f in tree['tree']:
        if f['path'] == file:
            break
    else:
        raise ValueError("Could not find pgzhelper module to download.")

    url = f['url']
    print('Downloading', file, 'module...')
    blob = read_json(url)
    data = base64.b64decode(blob['content']).decode('utf8')
    return tree['sha'], data


def update_local():
    """Download a new copy of the file and write it to DEST.

    Include a header based on the template HEADER.

    """
    sha, data = get_file(FILE)
    header = HEADER.format(sha=sha)
    with open(DEST, 'w', encoding='utf8') as f:
        f.write(header + data)
    print("Updated", FILE, "to revision", sha[:7])
    autopep8()


def autopep8():
    """Use autopep8 to fix formatting problems."""
    print("Running autopep8")
    subprocess.check_call(['autopep8', '-i', DEST])


if __name__ == '__main__':
    update_local()
