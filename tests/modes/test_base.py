# -*- coding: utf-8 -*-
"""
Tests for the BaseMode class.
"""
import os
import pytest
import mu
from mu.modes.base import BaseMode, MicroPythonMode, REPL
from unittest import mock


def test_base_mode():
    """
    Sanity check for the parent class of all modes.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    bm = BaseMode(editor, view)
    assert bm.name == 'UNNAMED MODE'
    assert bm.description == 'DESCRIPTION NOT AVAILABLE.'
    assert bm.icon == 'help'
    assert bm.is_debugger is False
    assert bm.editor == editor
    assert bm.view == view
    assert bm.actions() == NotImplemented
    assert bm.workspace_dir()
    assert bm.api() == NotImplemented
    assert bm.builtins is None


def test_base_mode_workspace_dir():
    """
    Return settings file workspace value.
    """
    # read from our demo settings.json
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='tests/settings.json'), \
            mock.patch('os.path.isdir', return_value=True):
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == '/home/foo/mycode'


def test_base_mode_workspace_not_present():
    """
    No workspace key in settings file, return default folder.
    """
    default_workspace = os.path.join(mu.logic.HOME_DIRECTORY,
                                     mu.logic.WORKSPACE_NAME)
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='tests/settingswithoutworkspace.json'):
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace


def test_base_mode_workspace_invalid_value():
    """
    Invalid workspace key in settings file, return default folder.
    """
    default_workspace = os.path.join(mu.logic.HOME_DIRECTORY,
                                     mu.logic.WORKSPACE_NAME)
    # read from our demo settings.json
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='tests/settings.json'), \
            mock.patch('os.path.isdir', return_value=False), \
            mock.patch('mu.modes.base.logger', return_value=None) as logger:
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace
        assert logger.error.call_count == 1


def test_base_mode_workspace_invalid_json():
    """
    Invalid workspace key in settings file, return default folder.
    """
    default_workspace = os.path.join(mu.logic.HOME_DIRECTORY,
                                     mu.logic.WORKSPACE_NAME)
    mock_open = mock.mock_open(read_data='{"workspace": invalid}')
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='a.json'), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('mu.modes.base.logger', return_value=None) as logger:
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace
        assert logger.error.call_count == 1


def test_base_mode_workspace_no_settings_file():
    """
    Invalid settings file, return default folder.
    """
    default_workspace = os.path.join(mu.logic.HOME_DIRECTORY,
                                     mu.logic.WORKSPACE_NAME)
    mock_open = mock.MagicMock(side_effect=FileNotFoundError())
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='tests/settings.json'), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('mu.modes.base.logger', return_value=None) as logger:
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace
        assert logger.error.call_count == 1


def test_micropython_mode_find_device():
    """
    Ensure it's possible to detect a device and return the expected port.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mock_port = mock.MagicMock()
    for vid, pid in mm.valid_boards:
        mock_port.vid = vid
        mock_port.productIdentifier = mock.MagicMock()
        mock_port.productIdentifier.return_value = pid
        mock_port.vendorIdentifier = mock.MagicMock()
        mock_port.vendorIdentifier.return_value = vid
        mock_port.portName = mock.MagicMock(return_value='COM0')
        with mock.patch('mu.modes.base.QSerialPortInfo.availablePorts',
                        return_value=[mock_port, ]):
            assert mm.find_device() == 'COM0'


def test_micropython_mode_find_device_no_ports():
    """
    There are no connected devices so return None.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    with mock.patch('mu.modes.base.QSerialPortInfo.availablePorts',
                    return_value=[]):
        assert mm.find_device() is None


def test_micropython_mode_find_microbit_no_device():
    """
    None of the connected devices is a valid board so return None.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mock_port = mock.MagicMock()
    mock_port.productIdentifier = mock.MagicMock(return_value=666)
    mock_port.vendorIdentifier = mock.MagicMock(return_value=999)
    with mock.patch('mu.modes.base.QSerialPortInfo.availablePorts',
                    return_value=[mock_port, ]):
        assert mm.find_device() is None


def test_micropython_mode_add_repl_already_exists():
    """
    Ensure the editor raises a RuntimeError if the repl already exists.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.repl = True
    with pytest.raises(RuntimeError):
        mm.add_repl()


def test_micropython_mode_add_repl_no_port():
    """
    If it's not possible to find a connected micro:bit then ensure a helpful
    message is enacted.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value=False)
    mm.add_repl()
    assert view.show_message.call_count == 1
    message = 'Could not find an attached device.'
    assert view.show_message.call_args[0][0] == message


def test_micropython_mode_add_repl_ioerror():
    """
    Sometimes when attempting to connect to the device there is an IOError
    because it's still booting up or connecting to the host computer. In this
    case, ensure a useful message is displayed.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    ex = IOError('BOOM')
    view.add_micropython_repl = mock.MagicMock(side_effect=ex)
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value='COM0')
    mm.add_repl()
    assert view.show_message.call_count == 1
    assert view.show_message.call_args[0][0] == str(ex)


def test_micropython_mode_add_repl_exception():
    """
    Ensure that any non-IOError based exceptions are logged.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    ex = Exception('BOOM')
    view.add_micropython_repl = mock.MagicMock(side_effect=ex)
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value='COM0')
    with mock.patch('mu.modes.base.logger', return_value=None) as logger:
        mm.add_repl()
        logger.error.assert_called_once_with(ex)


def test_micropython_mode_add_repl():
    """
    Nothing goes wrong so check the _view.add_micropython_repl gets the
    expected argument.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_micropython_repl = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value='COM0')
    with mock.patch('os.name', 'nt'):
        mm.add_repl()
    assert view.show_message.call_count == 0
    assert view.add_micropython_repl.call_args[0][0].port == 'COM0'


def test_micropython_mode_remove_repl_is_none():
    """
    If there's no repl to remove raise a RuntimeError.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.repl = None
    with pytest.raises(RuntimeError):
        mm.remove_repl()


def test_micropython_mode_remove_repl():
    """
    If there is a repl, make sure it's removed as expected and the state is
    updated.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.remove_repl = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.repl = True
    mm.remove_repl()
    assert view.remove_repl.call_count == 1
    assert mm.repl is None


def test_micropython_mode_toggle_repl_on():
    """
    There is no repl, so toggle on.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.add_repl = mock.MagicMock()
    mm.repl = None
    mm.toggle_repl(None)
    assert mm.add_repl.call_count == 1


def test_micropython_mode_toggle_repl_off():
    """
    There is a repl, so toggle off.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.remove_repl = mock.MagicMock()
    mm.repl = True
    mm.toggle_repl(None)
    assert mm.remove_repl.call_count == 1


def test_REPL_init():
    """
    Ensure the correct port name is set depending on OS.
    """
    with mock.patch('os.name', 'posix'):
        r = REPL('tty')
        assert r.port == '/dev/tty'
    with mock.patch('os.name', 'nt'):
        r = REPL('COM0')
        assert r.port == 'COM0'
    with mock.patch('os.name', 'foo'):
        with pytest.raises(NotImplementedError) as ex:
            r = REPL('COM0')
    assert ex.value.args[0] == 'OS "foo" not supported.'
