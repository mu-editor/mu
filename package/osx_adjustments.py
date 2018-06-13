"""
A script to adjust the contents of the .app directory before being turned into
a distributable disk image. These steps are:

* Replace the path to Python. 
* [TODO] Sign the app.
"""
import os.path


DEFAULT_PATH = '"exec" "`dirname $0`/../Resources/bin/python3.6" "$0" "$@"'


def replace_python_path(filename, path=DEFAULT_PATH):
    """
    Given a filename, replaces the second line with the path.
    """
    with open(path) as f:
        lines = f.readlines()
    lines[1] = path
    with open(path, 'w') as f:
        path.writelines(lines)


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    launcher = os.path.join(parent_dir, 'macOS', 'mu-editor.app', 'Contents',
                            'MacOS', 'mu-editor')
    replace_python_path(launcher)
