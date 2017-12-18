# -*- coding: utf-8 -*-
"""
Tests for the Adafruit mode.
"""
import pytest
import ctypes
from mu.modes.adafruit import AdafruitMode
from mu.modes.api import ADAFRUIT_APIS, SHARED_APIS
from unittest import mock


def test_adafruit_mode():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = AdafruitMode(editor, view)
    assert am.name == 'Adafruit CircuitPython'
    assert am.description is not None
    assert am.icon == 'adafruit'
    assert am.editor == editor
    assert am.view == view

    actions = am.actions()
    assert len(actions) == 1
    assert actions[0]['name'] == 'repl'
    assert actions[0]['handler'] == am.toggle_repl


def test_workspace_dir_posix_exists():
    """
    Simulate being on os.name == 'posix' and a call to "mount" returns a
    record indicating a connected device.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = AdafruitMode(editor, view)
    with open('tests/modes/mount_exists.txt', 'rb') as fixture_file:
        fixture = fixture_file.read()
        with mock.patch('os.name', 'posix'):
            with mock.patch('mu.modes.adafruit.check_output',
                            return_value=fixture):
                assert am.workspace_dir() == '/media/ntoll/CIRCUITPY'


def test_workspace_dir_posix_missing():
    """
    Simulate being on os.name == 'posix' and a call to "mount" returns a
    no records associated with a micro:bit device.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = AdafruitMode(editor, view)
    with open('tests/modes/mount_missing.txt', 'rb') as fixture_file:
        fixture = fixture_file.read()
        with mock.patch('os.name', 'posix'):
            with mock.patch('mu.modes.adafruit.check_output',
                            return_value=fixture),\
                    mock.patch('mu.modes.adafruit.'
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
    am = AdafruitMode(editor, view)
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
    am = AdafruitMode(editor, view)
    with mock.patch('os.name', 'nt'):
        with mock.patch('os.path.exists', return_value=True):
            return_value = ctypes.create_unicode_buffer(1024)
            with mock.patch('ctypes.create_unicode_buffer',
                            return_value=return_value), \
                    mock.patch('mu.modes.adafruit.'
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
    am = AdafruitMode(editor, view)
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
    am = AdafruitMode(editor, view)
    assert am.api() == SHARED_APIS + ADAFRUIT_APIS
