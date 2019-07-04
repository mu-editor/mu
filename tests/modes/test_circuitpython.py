# -*- coding: utf-8 -*-
"""
Tests for the CircuitPython mode.
"""
import pytest
import ctypes
from mu.modes.circuitpython import CircuitPythonMode
from mu.modes.api import ADAFRUIT_APIS, SHARED_APIS
from unittest import mock


def test_circuitpython_mode():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    assert am.name == 'CircuitPython'
    assert am.description is not None
    assert am.icon == 'circuitpython'
    assert am.editor == editor
    assert am.view == view

    actions = am.actions()
    assert len(actions) == 2
    assert actions[0]['name'] == 'serial'
    assert actions[0]['handler'] == am.toggle_repl
    assert actions[1]['name'] == 'plotter'
    assert actions[1]['handler'] == am.toggle_plotter
    assert 'code' not in am.module_names


def test_circuitpython_mode_no_charts():
    """
    If QCharts is not available, ensure the plotter feature is not available.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with mock.patch('mu.modes.circuitpython.CHARTS', False):
        actions = am.actions()
        assert len(actions) == 1
        assert actions[0]['name'] == 'serial'
        assert actions[0]['handler'] == am.toggle_repl


def test_workspace_dir_posix_exists():
    """
    Simulate being on os.name == 'posix' and a call to "mount" returns a
    record indicating a connected device.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open('tests/modes/mount_exists.txt', 'rb') as fixture_file:
        fixture = fixture_file.read()
        with mock.patch('os.name', 'posix'):
            with mock.patch('mu.modes.circuitpython.check_output',
                            return_value=fixture):
                assert am.workspace_dir() == '/media/ntoll/CIRCUITPY'


def test_workspace_dir_posix_no_mount_command():
    """
    When the user doesn't have administrative privileges on OSX then the mount
    command isn't on their path. In which case, check Mu uses the more
    explicit /sbin/mount instead.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open('tests/modes/mount_exists.txt', 'rb') as fixture_file:
        fixture = fixture_file.read()
    mock_check = mock.MagicMock(side_effect=[FileNotFoundError, fixture])
    with mock.patch('os.name', 'posix'), \
            mock.patch('mu.modes.circuitpython.check_output', mock_check):
        assert am.workspace_dir() == '/media/ntoll/CIRCUITPY'
        assert mock_check.call_count == 2
        assert mock_check.call_args_list[0][0][0] == 'mount'
        assert mock_check.call_args_list[1][0][0] == '/sbin/mount'


def test_workspace_dir_posix_missing():
    """
    Simulate being on os.name == 'posix' and a call to "mount" returns a
    no records associated with a micro:bit device.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open('tests/modes/mount_missing.txt', 'rb') as fixture_file:
        fixture = fixture_file.read()
        with mock.patch('os.name', 'posix'):
            with mock.patch('mu.modes.circuitpython.check_output',
                            return_value=fixture),\
                    mock.patch('mu.modes.circuitpython.'
                               'MicroPythonMode.workspace_dir') as mpm:
                mpm.return_value = 'foo'
                assert am.workspace_dir() == 'foo'


def test_workspace_dir_nt_exists():
    """
    Simulate being on os.name == 'nt' and a disk with a volume name 'CIRCUITPY'
    exists indicating a connected device.
    """
    mock_windll = mock.MagicMock()
    mock_windll.kernel32 = mock.MagicMock()
    mock_windll.kernel32.GetVolumeInformationW = mock.MagicMock()
    mock_windll.kernel32.GetVolumeInformationW.return_value = None
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with mock.patch('os.name', 'nt'):
        with mock.patch('os.path.exists', return_value=True):
            return_value = ctypes.create_unicode_buffer('CIRCUITPY')
            with mock.patch('ctypes.create_unicode_buffer',
                            return_value=return_value):
                ctypes.windll = mock_windll
                assert am.workspace_dir() == 'A:\\'


def test_workspace_dir_nt_missing():
    """
    Simulate being on os.name == 'nt' and a disk with a volume name 'CIRCUITPY'
    does not exist for a device.
    """
    mock_windll = mock.MagicMock()
    mock_windll.kernel32 = mock.MagicMock()
    mock_windll.kernel32.GetVolumeInformationW = mock.MagicMock()
    mock_windll.kernel32.GetVolumeInformationW.return_value = None
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with mock.patch('os.name', 'nt'):
        with mock.patch('os.path.exists', return_value=True):
            return_value = ctypes.create_unicode_buffer(1024)
            with mock.patch('ctypes.create_unicode_buffer',
                            return_value=return_value), \
                    mock.patch('mu.modes.circuitpython.'
                               'MicroPythonMode.workspace_dir') as mpm:
                mpm.return_value = 'foo'
                ctypes.windll = mock_windll
                assert am.workspace_dir() == 'foo'


def test_workspace_dir_unknown_os():
    """
    Raises a NotImplementedError if the host OS is not supported.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with mock.patch('os.name', 'foo'):
        with pytest.raises(NotImplementedError) as ex:
            am.workspace_dir()
    assert ex.value.args[0] == 'OS "foo" not supported.'


def test_api():
    """
    Ensure the correct API definitions are returned.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    assert am.api() == SHARED_APIS + ADAFRUIT_APIS
