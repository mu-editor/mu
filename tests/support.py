import os
import contextlib
import json
import shutil
import tempfile
import uuid

import mu.logic


def _generate_python_files(contents, dirpath):
    for i, c in enumerate(contents):
        name = uuid.uuid1().hex
        filepath = os.path.join(dirpath, "%03d-%s.py" % (1 + i, name))
        #
        # Write using newline="" so line-ending tests can work!
        # If a binary write is needed (eg for an encoding test) pass
        # a list of empty strings as contents and then write the bytes
        # as part of the test.
        #
        with open(filepath, "w", encoding=mu.logic.ENCODING, newline="") as f:
            f.write(c)
        yield filepath


@contextlib.contextmanager
def generate_python_files(contents, dirpath=None):
    dirpath = dirpath or tempfile.mkdtemp(prefix="mu-")
    yield list(_generate_python_files(contents, dirpath))
    shutil.rmtree(dirpath)


@contextlib.contextmanager
def generate_session(
    theme="day",
    mode="python",
    n_paths=0,
    filepath=None,
    **kwargs
):
    """Generate a temporary session file for one test

    By default, the session file will contain the data in SESSION_DATA above
    and will be created inside a temporary directory which will be removed
    afterwards. If filepath is specified a temporary the session file will
    be created with that fully-specified path and filename.

    If any paths are specified (referring to text files to reload from a
    previous session) and create_paths is True (the default) then empty files
    will be created at those filepaths, os.path.join-ed to a temporary
    directory.

    If None is passed to any of the parameters that item will not be included
    in the session data. Once all parameters have been considered if no session
    data is present, the file will *not* be created.

    By default, the file will be named according to the Mu default and placed
    in the temporary directory created for the test. If filepath is passed,
    the session file is created there instead.

    Any additional kwargs are created as items in the data (eg to generate
    invalid file contents)

    The session is yielded to the contextmanager so the typical usage is:

    with generate_session(mode="night") as session:
        # do some test
        assert <whatever>.mode == session['mode']
    """
    dirpath = tempfile.mkdtemp(prefix="mu-")
    session_data = {}
    if theme:
        session_data['theme'] = theme
    if mode:
        session_data['mode'] = mode
    if n_paths:
        paths = _generate_python_files(["" for p in range(n_paths)], dirpath)
        session_data['paths'] = list(paths)
    session_data.update(**kwargs)

    if filepath is None:
        filepath = os.path.join(dirpath, "session.json")
    if session_data:
        with open(filepath, "w") as f:
            f.write(json.dumps(session_data))
    session = dict(session_data)
    session['session_filepath'] = filepath
    yield session
    shutil.rmtree(dirpath)
