# -*- coding: utf-8 -*-
"""
Tests for the Editor and REPL logic.
"""
import sys
import os.path
import json
import pytest
import mu.logic
from PyQt5.QtWidgets import QMessageBox
from unittest import mock
from mu import __version__


SESSION = json.dumps({
    'theme': 'night',
    'mode': 'python',
    'paths': [
        'path/foo.py',
        'path/bar.py',
    ],
})


def test_CONSTANTS():
    """
    Ensure the expected constants exist.
    """
    assert mu.logic.HOME_DIRECTORY
    assert mu.logic.DATA_DIR
    assert mu.logic.WORKSPACE_NAME


def test_get_settings_app_path():
    """
    Find a settings file in the application location when run using Python.
    """
    fake_app_path = os.path.dirname(__file__)
    fake_app_script = os.path.join(fake_app_path, 'run.py')
    wrong_fake_path = 'wrong/path/to/executable'
    fake_local_settings = os.path.join(fake_app_path, 'settings.json')
    with mock.patch.object(sys, 'executable', wrong_fake_path), \
            mock.patch.object(sys, 'argv', [fake_app_script]):
        assert mu.logic.get_settings_path() == fake_local_settings


def test_get_settings_app_path_frozen():
    """
    Find a settings file in the application location when it has been frozen
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
        assert mu.logic.get_settings_path() == fake_local_settings


def test_get_settings_app_path_frozen_osx():
    """
    Find a settings file in the application location when it has been frozen
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
        assert mu.logic.get_settings_path() == fake_local_settings


def test_get_settings_data_path():
    """
    Find a settings file in the data location.
    """
    mock_open = mock.mock_open()
    mock_exists = mock.MagicMock()
    mock_exists.side_effect = [False, True]
    mock_json_dump = mock.MagicMock()
    with mock.patch('os.path.exists', mock_exists), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('json.dump', mock_json_dump), \
            mock.patch('mu.logic.DATA_DIR', 'fake_path'):
        assert mu.logic.get_settings_path() == os.path.join(
            'fake_path', 'settings.json')
    assert not mock_json_dump.called


def test_get_settings_no_files():
    """
    No settings files found, so create one.
    """
    mock_open = mock.mock_open()
    mock_json_dump = mock.MagicMock()
    with mock.patch('os.path.exists', return_value=False), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('json.dump', mock_json_dump), \
            mock.patch('mu.logic.DATA_DIR', 'fake_path'):
        assert mu.logic.get_settings_path() == os.path.join(
            'fake_path', 'settings.json')
    assert mock_json_dump.call_count == 1


def test_get_settings_no_files_cannot_create():
    """
    No settings files found, attempting to create one causes Mu to log and
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
        mu.logic.get_settings_path()
        msg = 'Unable to create settings file: ' \
              'fake_path{}settings.json'.format(os.path.sep)
        logger.error.assert_called_once_with(msg)


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
            mock.patch('os.makedirs', return_value=None) as mkd:
        e.setup(mock_modes)
        assert mkd.call_count == 1
        assert mkd.call_args_list[0][0][0] == 'foo'
    assert e.modes == mock_modes


def test_editor_restore_session():
    """
    A correctly specified session is restored properly.
    """
    view = mock.MagicMock()
    view.set_theme = mock.MagicMock()
    ed = mu.logic.Editor(view)
    ed._view.add_tab = mock.MagicMock()
    mock_mode = mock.MagicMock()
    mock_mode.save_timeout = 5
    ed.modes = {
        'python': mock_mode,
    }
    mock_open = mock.mock_open(read_data=SESSION)
    with mock.patch('builtins.open', mock_open), \
            mock.patch('os.path.exists', return_value=True):
        ed.restore_session()
    assert ed.theme == 'night'
    assert mock_open.return_value.read.call_count == 3
    assert ed._view.add_tab.call_count == 2
    view.set_theme.assert_called_once_with('night')


def test_editor_restore_session_missing_files():
    """
    Missing files that were opened tabs in the previous session are safely
    ignored when attempting to restore them.
    """
    fake_settings = os.path.join(os.path.dirname(__file__), 'settings.json')
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
    get_test_settings_path = mock.MagicMock()
    get_test_settings_path.return_value = fake_settings
    with mock.patch('os.path.exists', return_value=True), \
            mock.patch('mu.logic._', mock_gettext), \
            mock.patch('mu.logic.get_settings_path', get_test_settings_path):
        ed.restore_session()
    assert ed._view.add_tab.call_count == 0


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
    with mock.patch('os.path.exists', return_value=False), \
            mock.patch('mu.logic._', mock_gettext):
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
            mock.patch('mu.logic._', mock_gettext), \
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
    The current theme is 'night' so toggle to day. Expect the state to be
    updated and the appropriate call to the UI layer is made.
    """
    view = mock.MagicMock()
    view.set_theme = mock.MagicMock()
    ed = mu.logic.Editor(view)
    ed.theme = 'night'
    ed.toggle_theme()
    assert ed.theme == 'day'
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
    """
    view = mock.MagicMock()
    view.get_load_path = mock.MagicMock(return_value='foo.py')
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
    with mock.patch('builtins.open', mock_open):
        ed.load()
    assert view.get_load_path.call_count == 1
    view.add_tab.assert_called_once_with('foo.py', 'PYTHON', api)


def test_no_duplicate_load_python_file():
    """
    If the user specifies a file already loaded, ensure this is detected.
    """
    brown_script = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'scripts',
        'contains_brown.py'
    )

    editor_window = mock.MagicMock
    editor_window.show_message = mock.MagicMock()
    editor_window.focus_tab = mock.MagicMock()
    editor_window.add_tab = mock.MagicMock()

    brown_tab = mock.MagicMock()
    brown_tab.path = brown_script
    unsaved_tab = mock.MagicMock()
    unsaved_tab.path = None

    editor_window.widgets = ({unsaved_tab, brown_tab})

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
    view.add_tab.assert_called_once_with(None, 'RECOVERED', api)


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
    view = mock.MagicMock()
    view.current_tab = mock.MagicMock()
    view.current_tab.path = None
    view.current_tab.text = mock.MagicMock(return_value='foo')
    view.get_save_path = mock.MagicMock(return_value='foo.py')
    mock_open_atomic = mock.MagicMock()
    mock_open_atomic.return_value.__enter__ = lambda s: s
    mock_open_atomic.return_value.__exit__ = mock.Mock()
    mock_open_atomic.return_value.write = mock.MagicMock()
    ed = mu.logic.Editor(view)
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = '/fake/path'
    ed.modes = {
        'python': mock_mode,
    }
    with mock.patch('mu.logic.open_atomic', mock_open_atomic):
        ed.save()
    assert mock_open_atomic.call_count == 1
    mock_open_atomic.assert_called_with('foo.py', 'w', newline='')
    mock_open_atomic.return_value.write.assert_called_once_with('foo')
    view.get_save_path.assert_called_once_with('/fake/path')


def test_save_no_path_no_path_given():
    """
    If there's no path associated with the tab and the user cancels providing
    one, ensure the path is correctly re-set.
    """
    view = mock.MagicMock()
    view.current_tab = mock.MagicMock()
    view.current_tab.path = None
    view.get_save_path = mock.MagicMock(return_value='')
    ed = mu.logic.Editor(view)
    mock_mode = mock.MagicMock()
    mock_mode.workspace_dir.return_value = 'foo/bar'
    ed.modes = {
        'python': mock_mode,
    }
    ed.save()
    # The path isn't the empty string returned from get_save_path.
    assert view.current_tab.path is None


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
    mock_open_atomic = mock.MagicMock(side_effect=OSError())
    ed = mu.logic.Editor(view)
    with mock.patch('mu.logic.open_atomic', mock_open_atomic):
        ed.save()
    assert view.current_tab.setModified.call_count == 0
    assert view.show_message.call_count == 1


def test_save_python_file():
    """
    If the path is a Python file (ending in *.py) then save it and reset the
    modified flag.
    """
    view = mock.MagicMock()
    view.current_tab = mock.MagicMock()
    view.current_tab.path = 'foo.py'
    view.current_tab.text = mock.MagicMock(return_value='foo')
    view.get_save_path = mock.MagicMock()
    view.current_tab.setModified = mock.MagicMock(return_value=None)
    mock_open_atomic = mock.MagicMock()
    mock_open_atomic.return_value.__enter__ = lambda s: s
    mock_open_atomic.return_value.__exit__ = mock.Mock()
    mock_open_atomic.return_value.write = mock.MagicMock()
    ed = mu.logic.Editor(view)
    with mock.patch('mu.logic.open_atomic', mock_open_atomic):
        ed.save()
    mock_open_atomic.assert_called_once_with('foo.py', 'w', newline='')
    mock_open_atomic.return_value.write.assert_called_once_with('foo')
    assert view.get_save_path.call_count == 0
    view.current_tab.setModified.assert_called_once_with(False)


def test_save_with_no_file_extension():
    """
    If the path doesn't end in *.py then append it to the filename.
    """
    view = mock.MagicMock()
    view.current_tab = mock.MagicMock()
    view.current_tab.path = 'foo'
    view.current_tab.text = mock.MagicMock(return_value='foo')
    view.get_save_path = mock.MagicMock()
    mock_open_atomic = mock.MagicMock()
    mock_open_atomic.return_value.__enter__ = lambda s: s
    mock_open_atomic.return_value.__exit__ = mock.Mock()
    mock_open_atomic.return_value.write = mock.MagicMock()
    ed = mu.logic.Editor(view)
    with mock.patch('mu.logic.open_atomic', mock_open_atomic):
        ed.save()
    mock_open_atomic.assert_called_once_with('foo.py', 'w', newline='')
    mock_open_atomic.return_value.write.assert_called_once_with('foo')
    assert view.get_save_path.call_count == 0


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


def test_check_code():
    """
    Checking code correctly results in something the UI layer can parse.
    """
    view = mock.MagicMock()
    tab = mock.MagicMock()
    tab.path = 'foo.py'
    tab.text.return_value = 'import this\n'
    view.current_tab = tab
    flake = {2: {'line_no': 2, 'message': 'a message', }, }
    pep8 = {2: [{'line_no': 2, 'message': 'another message', }],
            3: [{'line_no': 3, 'message': 'yet another message', }]}
    with mock.patch('mu.logic.check_flake', return_value=flake), \
            mock.patch('mu.logic.check_pycodestyle', return_value=pep8):
        ed = mu.logic.Editor(view)
        ed.check_code()
        view.reset_annotations.assert_called_once_with()
        view.annotate_code.assert_has_calls([mock.call(flake, 'error'),
                                             mock.call(pep8, 'style')],
                                            any_order=True)


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
    with mock.patch('mu.logic.webbrowser.open_new', return_value=None) as wb:
        ed.show_help()
        wb.assert_called_once_with('http://codewith.mu/help/{}'.format(
                                   __version__))


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
    ed = mu.logic.Editor(view)
    ed.change_mode = mock.MagicMock()
    ed.select_mode(None)
    assert view.select_mode.call_count == 1
    assert ed.mode == 'foo'
    ed.change_mode.assert_called_once_with('foo')


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
        },
    ]
    ed.modes = {
        'python': mode,
    }
    ed.change_mode('python')
    view.change_mode.assert_called_once_with(mode)
    assert mock_button_bar.connect.call_count == 10
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
        },
    ]
    ed.modes = {
        'python': mode,
    }
    ed.change_mode('python')
    view.change_mode.assert_called_once_with(mode)
    assert mock_button_bar.connect.call_count == 10
    view.status_bar.set_mode.assert_called_once_with('python')
    view.stop_timer.assert_called_once_with()


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
    mock_open_atomic = mock.MagicMock()
    with mock.patch('mu.logic.open_atomic', mock_open_atomic):
        ed.autosave()
    assert mock_open_atomic.call_count == 1
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
