# -*- coding: utf-8 -*-
"""
Tests for the Editor and REPL logic.
"""
import sys
import os
import codecs
import contextlib
import json
import locale
import re
import shutil
import subprocess
import tempfile
from unittest import mock
import uuid

import pytest
import mu.logic
from PyQt5.QtWidgets import QMessageBox

from mu import __version__

SESSION = json.dumps({
    'theme': 'night',
    'mode': 'python',
    'paths': [
        'path/foo.py',
        'path/bar.py',
    ],
})


#
# Testing support functions
# These functions generate testing scenarios or mocks making
# the test more readable and easier to spot the element being
# tested from among the boilerplate setup code
#

def _generate_python_files(contents, dirpath):
    """Generate a series of .py files, one for each element in an iterable

    contents should be an iterable (typically a list) containing one
    string for each of a the number of files to be created. The files
    will be created in the dirpath directory passed in which will neither
    be created nor destroyed by this function.
    """
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
    """Create a temp directory and populate it with .py files, then remove it
    """
    dirpath = dirpath or tempfile.mkdtemp(prefix="mu-")
    yield list(_generate_python_files(contents, dirpath))
    shutil.rmtree(dirpath)


@contextlib.contextmanager
def generate_python_file(text="", dirpath=None):
    """Create a temp directory and populate it with on .py file, then remove it
    """
    dirpath = dirpath or tempfile.mkdtemp(prefix="mu-")
    for filepath in _generate_python_files([text], dirpath):
        yield filepath
        break
    shutil.rmtree(dirpath)


@contextlib.contextmanager
def generate_session(
    theme="day",
    mode="python",
    file_contents=None,
    filepath=None,
    **kwargs
):
    """Generate a temporary session file for one test

    By default, the session file will be created inside a temporary directory
    which will be removed afterwards. If filepath is specified the session
    file will be created with that fully-specified path and filename.

    If an iterable of file contents is specified (referring to text files to
    be reloaded from a previous session) then files will be created in the
    a directory with the contents provided.

    If None is passed to any of the parameters that item will not be included
    in the session data. Once all parameters have been considered if no session
    data is present, the file will *not* be created.

    Any additional kwargs are created as items in the data (eg to generate
    invalid file contents)

    The mu.logic.get_session_path function is mocked to return the
    temporary filepath from this session.

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
    if file_contents:
        paths = _generate_python_files(file_contents, dirpath)
        session_data['paths'] = list(paths)
    session_data.update(**kwargs)

    if filepath is None:
        filepath = os.path.join(dirpath, "session.json")
    if session_data:
        with open(filepath, "w") as f:
            f.write(json.dumps(session_data))
    session = dict(session_data)
    session['session_filepath'] = filepath
    with mock.patch("mu.logic.get_session_path", return_value=filepath):
        yield session
    shutil.rmtree(dirpath)


def mocked_view(text, path, newline):
    """Create a mocked view with path, newline and text
    """
    view = mock.MagicMock()
    view.current_tab = mock.MagicMock()
    view.current_tab.path = path
    view.current_tab.newline = newline
    view.current_tab.text = mock.MagicMock(return_value=text)
    view.add_tab = mock.MagicMock()
    view.get_save_path = mock.MagicMock(return_value=path)
    view.get_load_path = mock.MagicMock()
    view.add_tab = mock.MagicMock()
    return view


def mocked_editor(mode="python", text=None, path=None, newline=None):
    """Return a mocked editor with a mocked view

    This is intended to assist the several tests where a mocked editor
    is needed but where the length of setup code to get there tends to
    obscure the intent of the test
    """
    view = mocked_view(text, path, newline)
    ed = mu.logic.Editor(view)
    ed.select_mode = mock.MagicMock()
    mock_mode = mock.MagicMock()
    mock_mode.save_timeout = 5
    mock_mode.workspace_dir.return_value = '/fake/path'
    mock_mode.api.return_value = ["API Specification"]
    ed.modes = {
        mode: mock_mode,
    }
    return ed


def test_CONSTANTS():
    """
    Ensure the expected constants exist.
    """
    assert mu.logic.HOME_DIRECTORY
    assert mu.logic.DATA_DIR
    assert mu.logic.WORKSPACE_NAME


def test_write_and_flush():
    """
    Ensure the write and flush function tries to write to the filesystem and
    flush so the write happens immediately.
    """
    mock_fd = mock.MagicMock()
    mock_content = mock.MagicMock()
    with mock.patch('mu.logic.os.fsync') as fsync:
        mu.logic.write_and_flush(mock_fd, mock_content)
        fsync.assert_called_once_with(mock_fd)
    mock_fd.write.assert_called_once_with(mock_content)
    mock_fd.flush.assert_called_once_with()


def test_get_admin_file_path():
    """
    Finds an admin file in the application location, when Mu is run as if
    NOT frozen by PyInstaller.
    """
    fake_app_path = os.path.dirname(__file__)
    fake_app_script = os.path.join(fake_app_path, 'run.py')
    wrong_fake_path = 'wrong/path/to/executable'
    fake_local_settings = os.path.join(fake_app_path, 'settings.json')
    with mock.patch.object(sys, 'executable', wrong_fake_path), \
            mock.patch.object(sys, 'argv', [fake_app_script]):
        result = mu.logic.get_admin_file_path('settings.json')
        assert result == fake_local_settings


def test_get_admin_file_path_frozen():
    """
    Find an admin file in the application location when it has been frozen
    using PyInstaller.
    """
    fake_app_path = os.path.dirname(__file__)
    fake_app_script = os.path.join(fake_app_path, 'mu.exe')
    wrong_fake_path = 'wrong/path/to/executable'
    fake_local_settings = os.path.join(fake_app_path, 'settings.json')
    with mock.patch.object(sys, 'frozen', create=True, return_value=True), \
            mock.patch('platform.system', return_value='not_Darwin'), \
            mock.patch.object(sys, 'executable', fake_app_script), \
            mock.patch.object(sys, 'argv', [wrong_fake_path]):
        result = mu.logic.get_admin_file_path('settings.json')
        assert result == fake_local_settings


def test_get_admin_file_path_frozen_osx():
    """
    Find an admin file in the application location when it has been frozen
    using PyInstaller on macOS (as the path is different in the app bundle).
    """
    fake_app_path = os.path.join(os.path.dirname(__file__), 'a', 'b', 'c')
    fake_app_script = os.path.join(fake_app_path, 'mu.exe')
    wrong_fake_path = 'wrong/path/to/executable'
    fake_local_settings = os.path.abspath(os.path.join(
        fake_app_path, '..', '..', '..', 'settings.json'))
    with mock.patch.object(sys, 'frozen', create=True, return_value=True), \
            mock.patch('platform.system', return_value='Darwin'), \
            mock.patch.object(sys, 'executable', fake_app_script), \
            mock.patch.object(sys, 'argv', [wrong_fake_path]):
        result = mu.logic.get_admin_file_path('settings.json')
        assert result == fake_local_settings


def test_get_admin_file_path_with_data_path():
    """
    Find an admin file in the data location.
    """
    mock_open = mock.mock_open()
    mock_exists = mock.MagicMock()
    mock_exists.side_effect = [False, True]
    mock_json_dump = mock.MagicMock()
    with mock.patch('os.path.exists', mock_exists), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('json.dump', mock_json_dump), \
            mock.patch('mu.logic.DATA_DIR', 'fake_path'):
        result = mu.logic.get_admin_file_path('settings.json')
        assert result == os.path.join('fake_path', 'settings.json')
    assert not mock_json_dump.called


def test_get_admin_file_path_no_files():
    """
    No admin file found, so create one.
    """
    mock_open = mock.mock_open()
    mock_json_dump = mock.MagicMock()
    with mock.patch('os.path.exists', return_value=False), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('json.dump', mock_json_dump), \
            mock.patch('mu.logic.DATA_DIR', 'fake_path'):
        result = mu.logic.get_admin_file_path('settings.json')
        assert result == os.path.join('fake_path', 'settings.json')
    assert mock_json_dump.call_count == 1


def test_get_admin_file_path_no_files_cannot_create():
    """
    No admin file found, attempting to create one causes Mu to log and
    make do.
    """
    mock_open = mock.MagicMock()
    mock_open.return_value.__enter__.side_effect = FileNotFoundError('Bang')
    mock_open.return_value.__exit__ = mock.Mock()
    mock_json_dump = mock.MagicMock()
    with mock.patch('os.path.exists', return_value=False), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('json.dump', mock_json_dump), \
            mock.patch('mu.logic.DATA_DIR', 'fake_path'), \
            mock.patch('mu.logic.logger', return_value=None) as logger:
        mu.logic.get_admin_file_path('settings.json')
        msg = 'Unable to create admin file: ' \
              'fake_path{}settings.json'.format(os.path.sep)
        logger.error.assert_called_once_with(msg)


def test_get_session_path():
    """
    Ensure the result of calling get_admin_file_path with session.json returns
    the expected result.
    """
    mock_func = mock.MagicMock(return_value='foo')
    with mock.patch('mu.logic.get_admin_file_path', mock_func):
        assert mu.logic.get_session_path() == 'foo'
        mock_func.assert_called_once_with('session.json')


def test_get_settings_path():
    """
    Ensure the result of calling get_admin_file_path with settings.json returns
    the expected result.
    """
    mock_func = mock.MagicMock(return_value='foo')
    with mock.patch('mu.logic.get_admin_file_path', mock_func):
        assert mu.logic.get_settings_path() == 'foo'
        mock_func.assert_called_once_with('settings.json')


def test_check_flake():
    """
    Ensure the check_flake method calls PyFlakes with the expected code
    reporter.
    """
    mock_r = mock.MagicMock()
    mock_r.log = [{'line_no': 2, 'column': 0, 'message': 'b'}]
    with mock.patch('mu.logic.MuFlakeCodeReporter', return_value=mock_r), \
            mock.patch('mu.logic.check', return_value=None) as mock_check:
        result = mu.logic.check_flake('foo.py', 'some code')
        assert result == {2: mock_r.log}
        mock_check.assert_called_once_with('some code', 'foo.py', mock_r)


def test_check_flake_needing_expansion():
    """
    Ensure the check_flake method calls PyFlakes with the expected code
    reporter.
    """
    mock_r = mock.MagicMock()
    msg = "'microbit.foo' imported but unused"
    mock_r.log = [{'line_no': 2, 'column': 0, 'message': msg}]
    with mock.patch('mu.logic.MuFlakeCodeReporter', return_value=mock_r), \
            mock.patch('mu.logic.check', return_value=None) as mock_check:
        code = 'from microbit import *'
        result = mu.logic.check_flake('foo.py', code)
        assert result == {}
        mock_check.assert_called_once_with(mu.logic.EXPANDED_IMPORT, 'foo.py',
                                           mock_r)


def test_check_flake_with_builtins():
    """
    If a list of assumed builtin symbols is passed, any "undefined name"
    messages for them are ignored.
    """
    mock_r = mock.MagicMock()
    mock_r.log = [{'line_no': 2, 'column': 0,
                  'message': "undefined name 'foo'"}]
    with mock.patch('mu.logic.MuFlakeCodeReporter', return_value=mock_r), \
            mock.patch('mu.logic.check', return_value=None) as mock_check:
        result = mu.logic.check_flake('foo.py', 'some code',
                                      builtins=['foo', ])
        assert result == {}
        mock_check.assert_called_once_with('some code', 'foo.py', mock_r)


def test_check_pycodestyle():
    """
    Ensure the expected result if generated from the PEP8 style validator.
    """
    code = "import foo\n\n\n\n\n\ndef bar():\n    pass\n"  # Generate E303
    result = mu.logic.check_pycodestyle(code)
    assert len(result) == 1
    assert result[6][0]['line_no'] == 6
    assert result[6][0]['column'] == 0
    assert ' above this line' in result[6][0]['message']
    assert result[6][0]['code'] == 'E303'


def test_MuFlakeCodeReporter_init():
    """
    Check state is set up as expected.
    """
    r = mu.logic.MuFlakeCodeReporter()
    assert r.log == []


def test_MuFlakeCodeReporter_unexpected_error():
    """
    Check the reporter handles unexpected errors.
    """
    r = mu.logic.MuFlakeCodeReporter()
    r.unexpectedError('foo.py', 'Nobody expects the Spanish Inquisition!')
    assert len(r.log) == 1
    assert r.log[0]['line_no'] == 0
    assert r.log[0]['filename'] == 'foo.py'
    assert r.log[0]['message'] == 'Nobody expects the Spanish Inquisition!'


def test_MuFlakeCodeReporter_syntax_error():
    """
    Check the reporter handles syntax errors in a humane and kid friendly
    manner.
    """
    msg = ('Syntax error. Python cannot understand this line. Check for '
           'missing characters!')
    r = mu.logic.MuFlakeCodeReporter()
    r.syntaxError('foo.py', 'something incomprehensible to kids', '2', 3,
                  'source')
    assert len(r.log) == 1
    assert r.log[0]['line_no'] == 1
    assert r.log[0]['message'] == msg
    assert r.log[0]['column'] == 2
    assert r.log[0]['source'] == 'source'


def test_MuFlakeCodeReporter_flake_matched():
    """
    Check the reporter handles flake (regular) errors that match the expected
    message structure.
    """
    r = mu.logic.MuFlakeCodeReporter()
    err = "foo.py:4: something went wrong"
    r.flake(err)
    assert len(r.log) == 1
    assert r.log[0]['line_no'] == 3
    assert r.log[0]['column'] == 0
    assert r.log[0]['message'] == 'something went wrong'


def test_MuFlakeCodeReporter_flake_un_matched():
    """
    Check the reporter handles flake errors that do not conform to the expected
    message structure.
    """
    r = mu.logic.MuFlakeCodeReporter()
    err = "something went wrong"
    r.flake(err)
    assert len(r.log) == 1
    assert r.log[0]['line_no'] == 0
    assert r.log[0]['column'] == 0
    assert r.log[0]['message'] == 'something went wrong'


def test_REPL_posix():
    """
    The port is set correctly in a posix environment.
    """
    with mock.patch('os.name', 'posix'):
        r = mu.logic.REPL('ttyACM0')
        assert r.port == '/dev/ttyACM0'


def test_REPL_nt():
    """
    The port is set correctly in an nt (Windows) environment.
    """
    with mock.patch('os.name', 'nt'):
        r = mu.logic.REPL('COM0')
        assert r.port == 'COM0'


def test_REPL_unsupported():
    """
    A NotImplementedError is raised on an unsupported OS.
    """
    with mock.patch('os.name', 'SPARC'):
        with pytest.raises(NotImplementedError):
            mu.logic.REPL('tty0')


def test_editor_init():
    """
    Ensure a new instance is set-up correctly and creates the required folders
    upon first start.
    """
    view = mock.MagicMock()
    # Check the editor attempts to create required directories if they don't
    # already exist.
    with mock.patch('os.path.exists', return_value=False), \
            mock.patch('os.makedirs', return_value=None) as mkd:
        e = mu.logic.Editor(view)
        assert e._view == view
        assert e.theme == 'day'
        assert mkd.call_count == 1
        assert mkd.call_args_list[0][0][0] == mu.logic.DATA_DIR


def test_editor_setup():
    """
    An editor should have a modes attribute.
    """
    view = mock.MagicMock()
    e = mu.logic.Editor(view)
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = 'foo'
    mock_modes = {
        'python': mock_mode,
    }
    with mock.patch('os.path.exists', return_value=False), \
            mock.patch('os.makedirs', return_value=None) as mkd, \
            mock.patch('shutil.copy') as mock_shutil:
        e.setup(mock_modes)
        assert mkd.call_count == 3
        assert mkd.call_args_list[0][0][0] == 'foo'
        assert mock_shutil.call_count == 3
    assert e.modes == mock_modes


def test_editor_restore_session():
    """
    A correctly specified session is restored properly.
    """
    mode, theme = "python", "night"
    file_contents = ["", ""]
    ed = mocked_editor(mode)

    with generate_session(theme, mode, file_contents):
        ed.restore_session()

    assert ed.theme == theme
    assert ed._view.add_tab.call_count == len(file_contents)
    ed._view.set_theme.assert_called_once_with(theme)


def test_editor_restore_session_missing_files():
    """
    Missing files that were opened tabs in the previous session are safely
    ignored when attempting to restore them.
    """
    fake_session = os.path.join(os.path.dirname(__file__), 'session.json')
    view = mock.MagicMock()
    ed = mu.logic.Editor(view)
    ed._view.add_tab = mock.MagicMock()
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = '/fake/path'
    mock_mode.save_timeout = 5
    ed.modes = {
        'python': mock_mode,
    }
    mock_gettext = mock.MagicMock()
    mock_gettext.return_value = '# Write your code here :-)'
    get_test_session_path = mock.MagicMock()
    get_test_session_path.return_value = fake_session
    with mock.patch('os.path.exists', return_value=True), \
            mock.patch('mu.logic.get_session_path', get_test_session_path):
        ed.restore_session()
    assert ed._view.add_tab.call_count == 0


def test_editor_restore_session_invalid_mode():
    """
    As Mu's modes are added and/or renamed, invalid mode names may need to be
    ignored (this happens regularly when changing versions when developing
    Mu itself).
    """
    valid_mode, invalid_mode = "python", uuid.uuid1().hex
    ed = mocked_editor(valid_mode)
    with generate_session(mode=invalid_mode):
        ed.restore_session()
    ed.select_mode.assert_called_once_with(None)


def test_editor_restore_session_no_session_file():
    """
    If there's no prior session file (such as upon first start) then simply
    start up the editor with an empty untitled tab.
    """
    view = mock.MagicMock()
    view.tab_count = 0
    ed = mu.logic.Editor(view)
    ed._view.add_tab = mock.MagicMock()
    ed.select_mode = mock.MagicMock()
    mock_mode = mock.MagicMock()
    api = ['API specification', ]
    mock_mode.api.return_value = api
    mock_mode.workspace_dir.return_value = '/fake/path'
    mock_mode.save_timeout = 5
    ed.modes = {
        'python': mock_mode,
    }
    mock_gettext = mock.MagicMock()
    mock_gettext.return_value = '# Write your code here :-)'
    with mock.patch('os.path.exists', return_value=False):
        ed.restore_session()
    py = '# Write your code here :-)'.format(
        os.linesep, os.linesep)
    ed._view.add_tab.assert_called_once_with(None, py, api)
    ed.select_mode.assert_called_once_with(None)


def test_editor_restore_session_invalid_file():
    """
    A malformed JSON file is correctly detected and app behaves the same as if
    there was no session file.
    """
    view = mock.MagicMock()
    view.tab_count = 0
    ed = mu.logic.Editor(view)
    ed._view.add_tab = mock.MagicMock()
    mock_mode = mock.MagicMock()
    api = ['API specification', ]
    mock_mode.api.return_value = api
    mock_mode.workspace_dir.return_value = '/fake/path'
    mock_mode.save_timeout = 5
    ed.modes = {
        'python': mock_mode,
    }
    mock_open = mock.mock_open(
        read_data='{"paths": ["path/foo.py", "path/bar.py"]}, invalid: 0}')
    mock_gettext = mock.MagicMock()
    mock_gettext.return_value = '# Write your code here :-)'
    with mock.patch('builtins.open', mock_open), \
            mock.patch('os.path.exists', return_value=True):
        ed.restore_session()
    py = '# Write your code here :-)'
    ed._view.add_tab.assert_called_once_with(None, py, api)


def test_editor_open_focus_passed_file():
    """
    A file passed in by the OS is opened
    """
    view = mock.MagicMock()
    view.tab_count = 0
    ed = mu.logic.Editor(view)
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = '/fake/path'
    mock_mode.save_timeout = 5
    ed.modes = {
        'python': mock_mode,
    }
    ed._load = mock.MagicMock()
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'scripts',
        'contains_red.py'
    )
    ed.select_mode = mock.MagicMock()
    ed.restore_session(file_path)
    ed._load.assert_called_once_with(file_path)


def test_editor_session_and_open_focus_passed_file():
    """
    A passed in file is merged with session, opened last
    so it receives focus
    It will be the middle position in the session
    """
    view = mock.MagicMock()
    ed = mu.logic.Editor(view)
    ed.modes = mock.MagicMock()
    ed.direct_load = mock.MagicMock()
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = '/fake/path'
    mock_mode.save_timeout = 5
    ed.modes = {
        'python': mock_mode,
    }
    ed.select_mode = mock.MagicMock()
    settings = json.dumps({
        "paths": ["path/foo.py",
                  "path/bar.py"]}, )
    mock_open = mock.mock_open(read_data=settings)
    with mock.patch('builtins.open', mock_open), \
            mock.patch('os.path.exists', return_value=True):
        ed.restore_session(passed_filename='path/foo.py')

    # direct_load should be called twice (once for each path)
    assert ed.direct_load.call_count == 2
    # However, "foo.py" as the passed_filename should be direct_load-ed
    # at the end so it has focus, despite being the first file listed in
    # the restored session.
    assert ed.direct_load.call_args_list[0][0][0] == 'path/bar.py'
    assert ed.direct_load.call_args_list[1][0][0] == 'path/foo.py'


def test_toggle_theme_to_night():
    """
    The current theme is 'day' so toggle to night. Expect the state to be
    updated and the appropriate call to the UI layer is made.
    """
    view = mock.MagicMock()
    view.set_theme = mock.MagicMock()
    ed = mu.logic.Editor(view)
    ed.theme = 'day'
    ed.toggle_theme()
    assert ed.theme == 'night'
    view.set_theme.assert_called_once_with(ed.theme)


def test_toggle_theme_to_day():
    """
    The current theme is 'contrast' so toggle to day. Expect the state to be
    updated and the appropriate call to the UI layer is made.
    """
    view = mock.MagicMock()
    view.set_theme = mock.MagicMock()
    ed = mu.logic.Editor(view)
    ed.theme = 'contrast'
    ed.toggle_theme()
    assert ed.theme == 'day'
    view.set_theme.assert_called_once_with(ed.theme)


def test_toggle_theme_to_contrast():
    """
    The current theme is 'night' so toggle to contrast. Expect the state to be
    updated and the appropriate call to the UI layer is made.
    """
    view = mock.MagicMock()
    view.set_theme = mock.MagicMock()
    ed = mu.logic.Editor(view)
    ed.theme = 'night'
    ed.toggle_theme()
    assert ed.theme == 'contrast'
    view.set_theme.assert_called_once_with(ed.theme)


def test_new():
    """
    Ensure an untitled tab is added to the UI.
    """
    view = mock.MagicMock()
    view.add_tab = mock.MagicMock()
    mock_mode = mock.MagicMock()
    api = ['API specification', ]
    mock_mode.api.return_value = api
    ed = mu.logic.Editor(view)
    ed.modes = {
        'python': mock_mode,
    }
    ed.new()
    view.add_tab.assert_called_once_with(None, '', api)


def test_load_python_file():
    """
    If the user specifies a Python file (*.py) then ensure it's loaded and
    added as a tab.

    The Python code loaded will have a Mu encoding cookie prepended to it
    or have its own one replaced by a Mu cookie
    """
    text, newline = "python", "\n"
    ed = mocked_editor()
    with generate_python_file(text) as filepath:
        ed._view.get_load_path.return_value = filepath
        with mock.patch("mu.logic.read_and_decode") as mock_read:
            mock_read.return_value = text, newline
            ed.load()

    mock_read.assert_called_once_with(filepath)
    ed._view.add_tab.assert_called_once_with(
        filepath,
        mu.logic.ENCODING_COOKIE + mu.logic.NEWLINE + text,
        ed.modes[ed.mode].api(),
        newline)


def test_no_duplicate_load_python_file():
    """
    If the user specifies a file already loaded, ensure this is detected.
    """
    brown_script = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'scripts',
        'contains_brown.py'
    )

    editor_window = mock.MagicMock()
    editor_window.show_message = mock.MagicMock()
    editor_window.focus_tab = mock.MagicMock()
    editor_window.add_tab = mock.MagicMock()

    brown_tab = mock.MagicMock()
    brown_tab.path = brown_script
    unsaved_tab = mock.MagicMock()
    unsaved_tab.path = None

    editor_window.widgets = [unsaved_tab, brown_tab]

    editor_window.get_load_path = mock.MagicMock(return_value=brown_script)
    # Create the "editor" that'll control the "window".
    editor = mu.logic.Editor(view=editor_window)
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = '/fake/path'
    editor.modes = {
        'python': mock_mode,
    }

    editor.load()
    message = 'The file "{}" is already open.'.format(os.path.basename(
                                                      brown_script))
    editor_window.show_message.assert_called_once_with(message)
    editor_window.add_tab.assert_not_called()


def test_load_hex_file():
    """
    If the user specifies a hex file (*.hex) then ensure it's loaded and
    added as a tab.
    """
    view = mock.MagicMock()
    view.get_load_path = mock.MagicMock(return_value='foo.hex')
    view.add_tab = mock.MagicMock()
    ed = mu.logic.Editor(view)
    mock_mode = mock.MagicMock()
    api = ['API specification', ]
    mock_mode.api.return_value = api
    mock_mode.workspace_dir.return_value = '/fake/path'
    ed.modes = {
        'python': mock_mode,
    }
    mock_open = mock.mock_open(read_data='PYTHON')
    hex_file = 'RECOVERED'
    with mock.patch('builtins.open', mock_open), \
            mock.patch('mu.logic.uflash.extract_script',
                       return_value=hex_file) as s:
        ed.load()
    assert view.get_load_path.call_count == 1
    assert s.call_count == 1
    view.add_tab.assert_called_once_with(None, 'RECOVERED', api, os.linesep)


#
# When loading files Mu makes a note of the majority line-ending convention
# in use in the file. When it is saved, that convention is used.
#
def test_load_stores_newline():
    """
    When a file is loaded, its newline convention should be held on the tab
    for use when saving.
    """
    newline = "r\n"
    text = newline.join("the cat sat on the mat".split())
    editor = mocked_editor()
    with generate_python_file("abc\r\ndef") as filepath:
        editor._view.get_load_path.return_value = filepath
        editor.load()

    assert editor._view.add_tab.called_with(
        filepath, text, editor.modes[editor.mode].api(), "\r\n")


def test_save_restores_newline():
    """
    When a file is saved the newline convention noted originally should
    be used.
    """
    newline = "\r\n"
    test_text = mu.logic.NEWLINE.join(
        [mu.logic.ENCODING_COOKIE] +
        "the cat sat on the mat".split()
    )
    with generate_python_file(test_text) as filepath:
        with mock.patch("mu.logic.save_and_encode") as mock_save:
            ed = mocked_editor(text=test_text, newline=newline, path=filepath)
            ed.save()
            assert mock_save.called_with(test_text, filepath, newline)


def test_load_error():
    """
    Ensure that anything else is just ignored.
    """
    view = mock.MagicMock()
    view.get_load_path = mock.MagicMock(return_value='foo.py')
    view.add_tab = mock.MagicMock()
    ed = mu.logic.Editor(view)
    mock_open = mock.MagicMock(side_effect=FileNotFoundError())
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = '/fake/path'
    ed.modes = {
        'python': mock_mode,
    }
    with mock.patch('builtins.open', mock_open):
        ed.load()
    assert view.get_load_path.call_count == 1
    assert view.add_tab.call_count == 0


def test_save_no_tab():
    """
    If there's no active tab then do nothing.
    """
    view = mock.MagicMock()
    view.current_tab = None
    ed = mu.logic.Editor(view)
    ed.save()
    # If the code fell through then the tab state would be modified.
    assert view.current_tab is None


def test_save_no_path():
    """
    If there's no path associated with the tab then request the user provide
    one.
    """
    text, path, newline = "foo", "foo.py", "\n"
    ed = mocked_editor(text=text, path=None, newline=newline)
    ed._view.get_save_path.return_value = path
    with mock.patch("mu.logic.save_and_encode") as mock_save:
        ed.save()
    ed._view.get_save_path.assert_called()
    mock_save.assert_called_with(text, path, newline)


def test_save_no_path_no_path_given():
    """
    If there's no path associated with the tab and the user cancels providing
    one, ensure the path is correctly re-set.
    """
    text, newline = "foo", "\n"
    ed = mocked_editor(text=text, path=None, newline=newline)
    ed._view.get_save_path.return_value = ''
    ed.save()
    # The path isn't the empty string returned from get_save_path.
    assert ed._view.current_tab.path is None


def test_save_file_with_exception():
    """
    If the file cannot be written, return an error message.
    """
    view = mock.MagicMock()
    view.current_tab = mock.MagicMock()
    view.current_tab.path = 'foo.py'
    view.current_tab.text = mock.MagicMock(return_value='foo')
    view.current_tab.setModified = mock.MagicMock(return_value=None)
    view.show_message = mock.MagicMock()
    mock_open = mock.MagicMock(side_effect=OSError())
    ed = mu.logic.Editor(view)
    with mock.patch('builtins.open', mock_open):
        ed.save()
    assert view.current_tab.setModified.call_count == 0
    assert view.show_message.call_count == 1


def test_save_python_file():
    """
    If the path is a Python file (ending in *.py) then save it and reset the
    modified flag.
    """
    path, contents, newline = "foo.py", "foo", "\n"
    view = mock.MagicMock()
    view.current_tab = mock.MagicMock()
    view.current_tab.path = path
    view.current_tab.text = mock.MagicMock(return_value=contents)
    view.current_tab.newline = "\n"
    view.get_save_path = mock.MagicMock(return_value=path)
    view.current_tab.setModified = mock.MagicMock(return_value=None)
    ed = mu.logic.Editor(view)
    with mock.patch("mu.logic.save_and_encode") as mock_save:
        ed.save()

    mock_save.assert_called_once_with(contents, path, newline)
    assert view.get_save_path.call_count == 0
    view.current_tab.setModified.assert_called_once_with(False)


def test_save_with_no_file_extension():
    """
    If the path doesn't end in *.py then append it to the filename.
    """
    text, path, newline = "foo", "foo", "\n"
    ed = mocked_editor(text=text, path=path, newline=newline)
    with mock.patch('mu.logic.save_and_encode') as mock_save:
        ed.save()
    mock_save.assert_called_once_with(text, path + ".py", newline)
    ed._view.get_save_path.call_count == 0


def test_save_with_non_py_file_extension():
    """
    If the path ends in an extension, save it using the extension
    """
    text, path, newline = "foo", "foo.txt", "\n"
    ed = mocked_editor(text=text, path=path, newline=newline)
    ed._view.get_save_path.return_value = path
    with mock.patch('mu.logic.save_and_encode') as mock_save:
        ed.save()
    mock_save.assert_called_once_with(text, path, newline)
    ed._view.get_save_path.call_count == 0


def test_get_tab_existing_tab():
    """
    Ensure that an existing tab is returned if its path matches.
    """
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.path = 'foo'
    view.widgets = [mock_tab, ]
    ed = mu.logic.Editor(view)
    view.focus_tab.reset_mock()
    tab = ed.get_tab('foo')
    assert tab == mock_tab
    view.focus_tab.assert_called_once_with(mock_tab)


def test_get_tab_new_tab():
    """
    If the path is not represented by an existing tab, ensure it is loaded and
    the new tab is returned.
    """
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.path = 'foo'
    view.widgets = [mock_tab, ]
    ed = mu.logic.Editor(view)
    ed.direct_load = mock.MagicMock()
    tab = ed.get_tab('bar')
    ed.direct_load.assert_called_once_with('bar')
    assert tab == view.current_tab


def test_zoom_in():
    """
    Ensure the UI layer is zoomed in.
    """
    view = mock.MagicMock()
    view.zoom_in = mock.MagicMock(return_value=None)
    ed = mu.logic.Editor(view)
    ed.zoom_in()
    assert view.zoom_in.call_count == 1


def test_zoom_out():
    """
    Ensure the UI layer is zoomed out.
    """
    view = mock.MagicMock()
    view.zoom_out = mock.MagicMock(return_value=None)
    ed = mu.logic.Editor(view)
    ed.zoom_out()
    assert view.zoom_out.call_count == 1


def test_check_code_on():
    """
    Checking code correctly results in something the UI layer can parse.
    """
    view = mock.MagicMock()
    tab = mock.MagicMock()
    tab.has_annotations = False
    tab.path = 'foo.py'
    tab.text.return_value = 'import this\n'
    view.current_tab = tab
    flake = {2: {'line_no': 2, 'message': 'a message', }, }
    pep8 = {2: [{'line_no': 2, 'message': 'another message', }],
            3: [{'line_no': 3, 'message': 'yet another message', }]}
    mock_mode = mock.MagicMock()
    mock_mode.builtins = None
    with mock.patch('mu.logic.check_flake', return_value=flake), \
            mock.patch('mu.logic.check_pycodestyle', return_value=pep8):
        ed = mu.logic.Editor(view)
        ed.modes = {'python': mock_mode, }
        ed.check_code()
        assert tab.has_annotations is True
        view.reset_annotations.assert_called_once_with()
        view.annotate_code.assert_has_calls([mock.call(flake, 'error'),
                                             mock.call(pep8, 'style')],
                                            any_order=True)


def test_check_code_no_problems():
    """
    If no problems are found in the code, ensure a status message is shown to
    the user to confirm the fact. See #337
    """
    view = mock.MagicMock()
    tab = mock.MagicMock()
    tab.has_annotations = False
    tab.path = 'foo.py'
    tab.text.return_value = 'import this\n'
    view.current_tab = tab
    flake = {}
    pep8 = {}
    mock_mode = mock.MagicMock()
    mock_mode.builtins = None
    with mock.patch('mu.logic.check_flake', return_value=flake), \
            mock.patch('mu.logic.check_pycodestyle', return_value=pep8):
        ed = mu.logic.Editor(view)
        ed.show_status_message = mock.MagicMock()
        ed.modes = {'python': mock_mode, }
        ed.check_code()
        assert ed.show_status_message.call_count == 1


def test_check_code_off():
    """
    If the tab already has annotations, toggle them off.
    """
    view = mock.MagicMock()
    tab = mock.MagicMock()
    tab.has_annotations = True
    view.current_tab = tab
    ed = mu.logic.Editor(view)
    ed.check_code()
    assert tab.has_annotations is False
    view.reset_annotations.assert_called_once_with()


def test_check_code_no_tab():
    """
    Checking code when there is no tab containing code aborts the process.
    """
    view = mock.MagicMock()
    view.current_tab = None
    ed = mu.logic.Editor(view)
    ed.check_code()
    assert view.annotate_code.call_count == 0


def test_show_help():
    """
    Help should attempt to open up the user's browser and point it to the
    expected help documentation.
    """
    view = mock.MagicMock()
    ed = mu.logic.Editor(view)
    with mock.patch('mu.logic.webbrowser.open_new', return_value=None) as wb, \
            mock.patch('mu.logic.locale.getdefaultlocale',
                       return_value=('en_GB', 'UTF-8')):
        ed.show_help()
        version = '.'.join(__version__.split('.')[:2])
        url = 'https://codewith.mu/en/help/{}'.format(version)
        wb.assert_called_once_with(url)


def test_quit_modified_cancelled_from_button():
    """
    If the user quits and there's unsaved work, and they cancel the "quit" then
    do nothing.
    """
    view = mock.MagicMock()
    view.modified = True
    view.show_confirmation = mock.MagicMock(return_value=QMessageBox.Cancel)
    ed = mu.logic.Editor(view)
    mock_open = mock.MagicMock()
    mock_open.return_value.__enter__ = lambda s: s
    mock_open.return_value.__exit__ = mock.Mock()
    mock_open.return_value.write = mock.MagicMock()
    with mock.patch('sys.exit', return_value=None), \
            mock.patch('builtins.open', mock_open):
        ed.quit()
    assert view.show_confirmation.call_count == 1
    assert mock_open.call_count == 0


def test_quit_modified_cancelled_from_event():
    """
    If the user quits and there's unsaved work, and they cancel the "quit" then
    do nothing.
    """
    view = mock.MagicMock()
    view.modified = True
    view.show_confirmation = mock.MagicMock(return_value=QMessageBox.Cancel)
    ed = mu.logic.Editor(view)
    mock_open = mock.MagicMock()
    mock_open.return_value.__enter__ = lambda s: s
    mock_open.return_value.__exit__ = mock.Mock()
    mock_open.return_value.write = mock.MagicMock()
    mock_event = mock.MagicMock()
    mock_event.ignore = mock.MagicMock(return_value=None)
    with mock.patch('sys.exit', return_value=None), \
            mock.patch('builtins.open', mock_open):
        ed.quit(mock_event)
    assert view.show_confirmation.call_count == 1
    assert mock_event.ignore.call_count == 1
    assert mock_open.call_count == 0


def test_quit_modified_ok():
    """
    If the user quits and there's unsaved work that's ignored then proceed to
    save the session.
    """
    view = mock.MagicMock()
    view.modified = True
    view.show_confirmation = mock.MagicMock(return_value=True)
    ed = mu.logic.Editor(view)
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = 'foo/bar'
    mock_mode.get_hex_path.return_value = 'foo/bar'
    mock_debug_mode = mock.MagicMock()
    mock_debug_mode.is_debugger = True
    ed.modes = {
        'python': mock_mode,
        'microbit': mock_mode,
        'debugger': mock_debug_mode,
    }
    ed.mode = 'debugger'
    mock_open = mock.MagicMock()
    mock_open.return_value.__enter__ = lambda s: s
    mock_open.return_value.__exit__ = mock.Mock()
    mock_open.return_value.write = mock.MagicMock()
    mock_event = mock.MagicMock()
    mock_event.ignore = mock.MagicMock(return_value=None)
    with mock.patch('sys.exit', return_value=None), \
            mock.patch('builtins.open', mock_open):
        ed.quit(mock_event)
    mock_debug_mode.stop.assert_called_once_with()
    assert view.show_confirmation.call_count == 1
    assert mock_event.ignore.call_count == 0
    assert mock_open.call_count == 1
    assert mock_open.return_value.write.call_count > 0


def test_quit_save_tabs_with_paths():
    """
    When saving the session, ensure those tabs with associated paths are
    logged in the session file.
    """
    view = mock.MagicMock()
    view.modified = True
    view.show_confirmation = mock.MagicMock(return_value=True)
    w1 = mock.MagicMock()
    w1.path = 'foo.py'
    view.widgets = [w1, ]
    ed = mu.logic.Editor(view)
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = 'foo/bar'
    mock_mode.get_hex_path.return_value = 'foo/bar'
    ed.modes = {
        'python': mock_mode,
        'microbit': mock_mode,
    }
    mock_open = mock.MagicMock()
    mock_open.return_value.__enter__ = lambda s: s
    mock_open.return_value.__exit__ = mock.Mock()
    mock_open.return_value.write = mock.MagicMock()
    mock_event = mock.MagicMock()
    mock_event.ignore = mock.MagicMock(return_value=None)
    with mock.patch('sys.exit', return_value=None), \
            mock.patch('builtins.open', mock_open):
        ed.quit(mock_event)
    assert view.show_confirmation.call_count == 1
    assert mock_event.ignore.call_count == 0
    assert mock_open.call_count == 1
    assert mock_open.return_value.write.call_count > 0
    recovered = ''.join([i[0][0] for i
                        in mock_open.return_value.write.call_args_list])
    session = json.loads(recovered)
    assert 'foo.py' in session['paths']


def test_quit_save_theme():
    """
    When saving the session, ensure the theme is logged in the session file.
    """
    view = mock.MagicMock()
    view.modified = True
    view.show_confirmation = mock.MagicMock(return_value=True)
    w1 = mock.MagicMock()
    w1.path = 'foo.py'
    view.widgets = [w1, ]
    ed = mu.logic.Editor(view)
    ed.theme = 'night'
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = 'foo/bar'
    mock_mode.get_hex_path.return_value = 'foo/bar'
    ed.modes = {
        'python': mock_mode,
        'microbit': mock_mode,
    }
    mock_open = mock.MagicMock()
    mock_open.return_value.__enter__ = lambda s: s
    mock_open.return_value.__exit__ = mock.Mock()
    mock_open.return_value.write = mock.MagicMock()
    mock_event = mock.MagicMock()
    mock_event.ignore = mock.MagicMock(return_value=None)
    with mock.patch('sys.exit', return_value=None), \
            mock.patch('builtins.open', mock_open):
        ed.quit(mock_event)
    assert view.show_confirmation.call_count == 1
    assert mock_event.ignore.call_count == 0
    assert mock_open.call_count == 1
    assert mock_open.return_value.write.call_count > 0
    recovered = ''.join([i[0][0] for i
                        in mock_open.return_value.write.call_args_list])
    session = json.loads(recovered)
    assert session['theme'] == 'night'


def test_quit_calls_sys_exit():
    """
    Ensure that sys.exit(0) is called.
    """
    view = mock.MagicMock()
    view.modified = True
    view.show_confirmation = mock.MagicMock(return_value=True)
    w1 = mock.MagicMock()
    w1.path = 'foo.py'
    view.widgets = [w1, ]
    ed = mu.logic.Editor(view)
    ed.theme = 'night'
    ed.modes = {
        'python': mock.MagicMock(),
        'microbit': mock.MagicMock(),
    }
    mock_open = mock.MagicMock()
    mock_open.return_value.__enter__ = lambda s: s
    mock_open.return_value.__exit__ = mock.Mock()
    mock_open.return_value.write = mock.MagicMock()
    mock_event = mock.MagicMock()
    mock_event.ignore = mock.MagicMock(return_value=None)
    with mock.patch('sys.exit', return_value=None) as ex, \
            mock.patch('builtins.open', mock_open):
        ed.quit(mock_event)
    ex.assert_called_once_with(0)


def test_show_logs():
    """
    Ensure the expected log file is displayed to the end user.
    """
    view = mock.MagicMock()
    ed = mu.logic.Editor(view)
    mock_open = mock.mock_open()
    with mock.patch('builtins.open', mock_open):
        ed.show_logs(None)
        mock_open.assert_called_once_with(mu.logic.LOG_FILE, 'r')
        assert view.show_logs.call_count == 1


def test_select_mode():
    """
    It's possible to select and update to a new mode.
    """
    view = mock.MagicMock()
    view.select_mode.return_value = 'foo'
    mode = mock.MagicMock()
    mode.is_debugger = False
    ed = mu.logic.Editor(view)
    ed.modes = {
        'python': mode,
    }
    ed.change_mode = mock.MagicMock()
    ed.select_mode(None)
    assert view.select_mode.call_count == 1
    assert ed.mode == 'foo'
    ed.change_mode.assert_called_once_with('foo')


def test_select_mode_debug_mode():
    """
    It's NOT possible to select and update to a new mode if you're in debug
    mode.
    """
    view = mock.MagicMock()
    mode = mock.MagicMock()
    mode.debugger = True
    ed = mu.logic.Editor(view)
    ed.modes = {
        'debugger': mode,
    }
    ed.mode = 'debugger'
    ed.change_mode = mock.MagicMock()
    ed.select_mode(None)
    assert ed.mode == 'debugger'
    assert ed.change_mode.call_count == 0


def test_change_mode():
    """
    It should be possible to change modes in the expected fashion (buttons get
    correctly connected to event handlers).
    """
    view = mock.MagicMock()
    mock_button_bar = mock.MagicMock()
    view.button_bar = mock_button_bar
    view.change_mode = mock.MagicMock()
    ed = mu.logic.Editor(view)
    mode = mock.MagicMock()
    mode.save_timeout = 5
    mode.actions.return_value = [
        {
            'name': 'name',
            'handler': 'handler',
            'shortcut': 'Ctrl+X',
        },
    ]
    ed.modes = {
        'python': mode,
    }
    ed.change_mode('python')
    view.change_mode.assert_called_once_with(mode)
    assert mock_button_bar.connect.call_count == 11
    view.status_bar.set_mode.assert_called_once_with('python')
    view.set_timer.assert_called_once_with(5, ed.autosave)


def test_change_mode_no_timer():
    """
    It should be possible to change modes in the expected fashion (buttons get
    correctly connected to event handlers).
    """
    view = mock.MagicMock()
    mock_button_bar = mock.MagicMock()
    view.button_bar = mock_button_bar
    view.change_mode = mock.MagicMock()
    ed = mu.logic.Editor(view)
    mode = mock.MagicMock()
    mode.save_timeout = 0
    mode.actions.return_value = [
        {
            'name': 'name',
            'handler': 'handler',
            'shortcut': 'Ctrl+X',
        },
    ]
    ed.modes = {
        'python': mode,
    }
    ed.change_mode('python')
    view.change_mode.assert_called_once_with(mode)
    assert mock_button_bar.connect.call_count == 11
    view.status_bar.set_mode.assert_called_once_with('python')
    view.stop_timer.assert_called_once_with()


def test_change_mode_reset_breakpoints():
    """
    When changing modes, if the new mode does NOT require a debugger, then
    breakpoints should be reset.
    """
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.breakpoint_lines = set([1, 2, 3, ])
    view.widgets = [mock_tab, ]
    ed = mu.logic.Editor(view)
    mode = mock.MagicMock()
    mode.has_debugger = False
    mode.is_debugger = False
    mode.save_timeout = 5
    ed.modes = {
        'microbit': mode,
    }
    ed.change_mode('microbit')
    assert mock_tab.breakpoint_lines == set()
    mock_tab.reset_annotations.assert_called_once_with()


def test_autosave():
    """
    Ensure the autosave callback does the expected things to the tabs.
    """
    view = mock.MagicMock()
    view.modified = True
    mock_tab = mock.MagicMock()
    mock_tab.path = 'foo'
    mock_tab.isModified.return_value = True
    view.widgets = [mock_tab, ]
    ed = mu.logic.Editor(view)
    with mock.patch('mu.logic.save_and_encode') as mock_save:
        ed.autosave()
    assert mock_save.call_count == 1
    mock_tab.setModified.assert_called_once_with(False)


def test_check_usb():
    """
    Ensure the check_usb callback actually checks for connected USB devices.
    """
    view = mock.MagicMock()
    ed = mu.logic.Editor(view)
    mode = mock.MagicMock()
    mode.find_device.return_value = '/dev/ttyUSB0'
    ed.modes = {
        'microbit': mode,
    }
    ed.show_status_message = mock.MagicMock()
    ed.check_usb()
    expected = ("Connection from a new device detected. "
                "Please switch to Microbit mode.")
    ed.show_status_message.assert_called_once_with(expected)


def test_show_status_message():
    """
    Ensure the method calls the status_bar in the view layer.
    """
    msg = "Hello, World!"
    view = mock.MagicMock()
    ed = mu.logic.Editor(view)
    ed.show_status_message(msg, 8)
    view.status_bar.set_message.assert_called_once_with(msg, 8000)


def test_debug_toggle_breakpoint_as_debugger():
    """
    If a breakpoint is toggled in debug mode, pass it to the toggle_breakpoint
    method in the debug client.
    """
    view = mock.MagicMock()
    ed = mu.logic.Editor(view)
    mock_debugger = mock.MagicMock()
    mock_debugger.has_debugger = False
    mock_debugger.is_debugger = True
    ed.modes = {
        'debugger': mock_debugger,
    }
    ed.mode = 'debugger'
    ed.debug_toggle_breakpoint(1, 10, False)
    mock_debugger.toggle_breakpoint.assert_called_once_with(10,
                                                            view.current_tab)


def test_debug_toggle_breakpoint_on():
    """
    Toggle the breakpoint on when not in debug mode by tracking it in the
    tab.breakpoint_lines set.
    """
    view = mock.MagicMock()
    view.current_tab.breakpoint_lines = set()
    ed = mu.logic.Editor(view)
    mock_debugger = mock.MagicMock()
    mock_debugger.has_debugger = True
    mock_debugger.is_debugger = False
    ed.modes = {
        'python': mock_debugger,
    }
    ed.mode = 'python'
    ed.debug_toggle_breakpoint(1, 10, False)
    view.current_tab.markerAdd.\
        assert_called_once_with(10, view.current_tab.BREAKPOINT_MARKER)
    assert 10 in view.current_tab.breakpoint_lines


def test_debug_toggle_breakpoint_off():
    """
    Toggle the breakpoint off when not in debug mode by tracking it in the
    tab.breakpoint_lines set.
    """
    view = mock.MagicMock()
    view.current_tab.breakpoint_lines = set([10, ])
    ed = mu.logic.Editor(view)
    mock_debugger = mock.MagicMock()
    mock_debugger.has_debugger = True
    mock_debugger.is_debugger = False
    ed.modes = {
        'python': mock_debugger,
    }
    ed.mode = 'python'
    ed.debug_toggle_breakpoint(1, 10, False)
    view.current_tab.markerDelete.\
        assert_called_once_with(10, view.current_tab.BREAKPOINT_MARKER)
    assert len(view.current_tab.breakpoint_lines) == 0


def test_rename_tab_no_tab_id():
    """
    If no tab id is supplied (i.e. this method was triggered by the shortcut
    instead of the double-click event), then use the tab currently in focus.
    """
    view = mock.MagicMock()
    view.get_save_path.return_value = 'foo'
    mock_tab = mock.MagicMock()
    mock_tab.path = 'old.py'
    view.current_tab = mock_tab
    ed = mu.logic.Editor(view)
    ed.save = mock.MagicMock()
    ed.rename_tab()
    view.get_save_path.assert_called_once_with('old.py')
    assert mock_tab.path == 'foo.py'
    ed.save.assert_called_once_with()


def test_rename_tab():
    """
    If there's a tab id, the function being tested is reacting to a double-tap
    so make sure the expected tab is grabbed from the view.
    """
    view = mock.MagicMock()
    view.get_save_path.return_value = 'foo'
    mock_tab = mock.MagicMock()
    mock_tab.path = 'old.py'
    view.tabs.widget.return_value = mock_tab
    ed = mu.logic.Editor(view)
    ed.save = mock.MagicMock()
    ed.rename_tab(1)
    view.get_save_path.assert_called_once_with('old.py')
    view.tabs.widget.assert_called_once_with(1)
    assert mock_tab.path == 'foo.py'
    ed.save.assert_called_once_with()


def test_rename_tab_avoid_duplicating_other_tab_name():
    """
    If the user attempts to rename the tab to a filename used by another tab
    then show an error message and don't rename anything.
    """
    view = mock.MagicMock()
    view.get_save_path.return_value = 'foo'
    mock_other_tab = mock.MagicMock()
    mock_other_tab.path = 'foo.py'
    view.widgets = [mock_other_tab, ]
    mock_tab = mock.MagicMock()
    mock_tab.path = 'old.py'
    view.tabs.widget.return_value = mock_tab
    ed = mu.logic.Editor(view)
    ed.rename_tab(1)
    view.show_message.assert_called_once_with('Could not rename file.',
                                              'A file of that name is already '
                                              'open in Mu.')
    assert mock_tab.path == 'old.py'


def test_logic_independent_import_logic():
    """
    It should be possible to import the logic and app
    modules from the mu package independently of each
    other.
    """
    subprocess.run([sys.executable, "-c", "from mu import logic"], check=True)


def test_logic_independent_import_app():
    """
    It should be possible to import the logic and app
    modules from the mu package independently of each
    other.
    """
    subprocess.run([sys.executable, "-c", "from mu import app"], check=True)


#
# Tests for newline detection
# Mu should detect the majority newline convention
# in a loaded file and use that convention when writing
# the file out again. Internally all newlines are MU_NEWLINE
#

def test_read_newline_no_text():
    """If the file being loaded is empty, use the platform default newline
    """
    with generate_python_file() as filepath:
        text, newline = mu.logic.read_and_decode(filepath)
        assert text.count("\r\n") == 0
        assert newline == os.linesep


def test_read_newline_all_unix():
    """If the file being loaded has only the Unix convention, use that
    """
    with generate_python_file("abc\ndef") as filepath:
        text, newline = mu.logic.read_and_decode(filepath)
        assert text.count("\r\n") == 0
        assert newline == "\n"


def test_read_newline_all_windows():
    """If the file being loaded has only the Windows convention, use that
    """
    with generate_python_file("abc\r\ndef") as filepath:
        text, newline = mu.logic.read_and_decode(filepath)
        assert text.count("\r\n") == 0
        assert newline == "\r\n"


def test_read_newline_most_unix():
    """If the file being loaded has mostly the Unix convention, use that
    """
    with generate_python_file("\nabc\r\ndef\n") as filepath:
        text, newline = mu.logic.read_and_decode(filepath)
        assert text.count("\r\n") == 0
        assert newline == "\n"


def test_read_newline_most_windows():
    """If the file being loaded has mostly the Windows convention, use that
    """
    with generate_python_file("\r\nabc\ndef\r\n") as filepath:
        text, newline = mu.logic.read_and_decode(filepath)
        assert text.count("\r\n") == 0
        assert newline == "\r\n"


def test_read_newline_equal_match():
    """If the file being loaded has an equal number of Windows and
    Unix newlines, use the platform default
    """
    with generate_python_file("\r\nabc\ndef") as filepath:
        text, newline = mu.logic.read_and_decode(filepath)
        assert text.count("\r\n") == 0
        assert newline == os.linesep


#
# When writing Mu should honour the line-ending convention found inbound
#
def test_write_newline_to_unix():
    """If the file had Unix newlines it should be saved with Unix newlines

    (In principle this check is unnecessary as Unix newlines are currently
    the Mu internal default; but we leave it here in case that situation
    changes)
    """
    with generate_python_file() as filepath:
        test_string = "\r\n".join("the cat sat on the mat".split())
        mu.logic.save_and_encode(test_string, filepath, "\n")
        with open(filepath, newline="") as f:
            text = f.read()
            assert text.count("\r\n") == 0
            #
            # There will be one more line-ending because of the encoding cookie
            #
            assert text.count("\n") == 1 + test_string.count("\r\n")


def test_write_newline_to_windows():
    """If the file had Windows newlines it should be saved with Windows newlines
    """
    with generate_python_file() as filepath:
        test_string = "\n".join("the cat sat on the mat".split())
        mu.logic.save_and_encode(test_string, filepath, "\r\n")
        with open(filepath, newline="") as f:
            text = f.read()
            assert len(re.findall("[^\r]\n", text)) == 0
            #
            # There will be one more line-ending because of the encoding cookie
            #
            assert text.count("\r\n") == 1 + test_string.count("\n")


#
# Generate a Unicode test string which includes all the usual
# 7-bit characters but also an 8th-bit range which tends to
# trip things up between encodings
#
BYTES_TEST_STRING = bytes(range(0x20, 0x80)) + bytes(range(0xa0, 0xff))
UNICODE_TEST_STRING = BYTES_TEST_STRING.decode("iso-8859-1")


#
# Tests for encoding detection
# Mu should detect:
# - BOM (UTF8/16)
# - Encoding cooke, eg # -*- coding: utf-8 -*-
# - fallback to the platform default (locale.getpreferredencoding())
#
def test_read_utf8bom():
    """Successfully decode from utf-8 encoded with BOM
    """
    with generate_python_file() as filepath:
        with open(filepath, "w", encoding="utf-8-sig") as f:
            f.write(UNICODE_TEST_STRING)
        text, _ = mu.logic.read_and_decode(filepath)
        assert text == UNICODE_TEST_STRING


def test_read_utf16bebom():
    """Successfully decode from utf-16 BE encoded with BOM
    """
    with generate_python_file() as filepath:
        with open(filepath, "wb") as f:
            f.write(codecs.BOM_UTF16_BE)
            f.write(UNICODE_TEST_STRING.encode("utf-16-be"))
        text, _ = mu.logic.read_and_decode(filepath)
        assert text == UNICODE_TEST_STRING


def test_read_utf16lebom():
    """Successfully decode from utf-16 LE encoded with BOM
    """
    with generate_python_file() as filepath:
        with open(filepath, "wb") as f:
            f.write(codecs.BOM_UTF16_LE)
            f.write(UNICODE_TEST_STRING.encode("utf-16-le"))
        text, _ = mu.logic.read_and_decode(filepath)
        assert text == UNICODE_TEST_STRING


def test_read_encoding_cookie():
    """Successfully decode from iso-8859-1 with an encoding cookie
    """
    encoding_cookie = mu.logic.ENCODING_COOKIE.replace(
        mu.logic.ENCODING, "iso-8859-1")
    test_string = encoding_cookie + UNICODE_TEST_STRING
    with generate_python_file() as filepath:
        with open(filepath, "wb") as f:
            f.write(test_string.encode("iso-8859-1"))
        text, _ = mu.logic.read_and_decode(filepath)
        assert text == test_string


def test_read_encoding_default():
    """Successfully decode from the default locale
    """
    test_string = UNICODE_TEST_STRING.encode(locale.getpreferredencoding())
    with generate_python_file() as filepath:
        with open(filepath, "wb") as f:
            f.write(test_string)
        text, _ = mu.logic.read_and_decode(filepath)
        assert text == UNICODE_TEST_STRING


#
# When writing, Mu should use utf-8 (without a BOM) and ensure the text is
# prefixed with a PEP 263 encoding cookie
# If the file already has an encoding cookie it should be replaced by
# the Mu cookie
#
def test_write_utf8():
    """The text should be saved encoded as utf8
    """
    with generate_python_file() as filepath:
        mu.logic.save_and_encode(UNICODE_TEST_STRING, filepath)
        with open(filepath, encoding="utf-8") as f:
            text = f.read()
            assert text == mu.logic.ENCODING_COOKIE + UNICODE_TEST_STRING


def test_write_encoding_cookie_no_cookie():
    """If the text has no cookie of its own the first line of the saved
    file will be the Mu encoding cookie
    """
    test_string = "This is a test"
    with generate_python_file() as filepath:
        mu.logic.save_and_encode(test_string, filepath)
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                assert line == mu.logic.ENCODING_COOKIE
                break
            else:
                assert False, "No cookie found"


def test_write_encoding_cookie_existing_cookie():
    """If the text has a cookie of its own it will be replaced by the Mu cookie
    """
    cookie = mu.logic.ENCODING_COOKIE.replace(mu.logic.ENCODING, "iso-8859-1")
    test_string = cookie + "This is a test"
    with generate_python_file() as filepath:
        mu.logic.save_and_encode(test_string, filepath)
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                assert line == mu.logic.ENCODING_COOKIE
                break
            else:
                assert False, "No cookie found"
