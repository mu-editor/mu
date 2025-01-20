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
    assert am.name == "CircuitPython"
    assert am.description is not None
    assert am.icon == "circuitpython"
    assert am.editor == editor
    assert am.view == view

    with mock.patch("mu.modes.circuitpython.CHARTS", True):
        actions = am.actions()
    assert len(actions) == 3
    assert actions[0]["name"] == "run"
    assert actions[0]["handler"] == am.run
    assert actions[1]["name"] == "serial"
    assert actions[1]["handler"] == am.toggle_repl
    assert actions[2]["name"] == "plotter"
    assert actions[2]["handler"] == am.toggle_plotter
    assert "code" not in am.module_names


def test_circuitpython_mode_no_charts():
    """
    If QCharts is not available, ensure the plotter feature is not available.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with mock.patch("mu.modes.circuitpython.CHARTS", False):
        actions = am.actions()
        assert len(actions) == 2
        assert actions[0]["name"] == "run"
        assert actions[0]["handler"] == am.run
        assert actions[1]["name"] == "serial"
        assert actions[1]["handler"] == am.toggle_repl


def test_workspace_dir_posix_exists():
    """
    Simulate being on os.name == 'posix' and a call to "mount" returns a
    record indicating a connected device.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open("tests/modes/mount_exists.txt", "rb") as fixture_file:
        fixture = fixture_file.read()
        with mock.patch("os.name", "posix"):
            with mock.patch(
                "mu.modes.circuitpython.check_output", return_value=fixture
            ):
                assert am.workspace_dir() == "/media/ntoll/CIRCUITPY"


def test_workspace_dir_posix_no_mount_command():
    """
    When the user doesn't have administrative privileges on OSX then the mount
    command isn't on their path. In which case, check Mu uses the more
    explicit /sbin/mount instead.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open("tests/modes/mount_exists.txt", "rb") as fixture_file:
        fixture = fixture_file.read()
    mock_check = mock.MagicMock(side_effect=[FileNotFoundError, fixture])
    with mock.patch("os.name", "posix"), mock.patch(
        "mu.modes.circuitpython.check_output", mock_check
    ):
        assert am.workspace_dir() == "/media/ntoll/CIRCUITPY"
        assert mock_check.call_count == 2
        assert mock_check.call_args_list[0][0][0] == "mount"
        assert mock_check.call_args_list[1][0][0] == "/sbin/mount"


def test_workspace_dir_posix_permission_denied():
    """
    When the mount command results in a Permission Denied error, show a
    message and use default workspace dir.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open("tests/modes/mount_exists.txt", "rb") as fixture_file:
        fixture = fixture_file.read()
    mock_check = mock.MagicMock(side_effect=[PermissionError, fixture])
    with mock.patch("os.name", "posix"), mock.patch(
        "mu.modes.circuitpython.check_output", mock_check
    ):
        assert am.workspace_dir() == "/media/ntoll/CIRCUITPY"
        assert mock_check.call_count == 2
        assert mock_check.call_args_list[0][0][0] == "mount"
        assert mock_check.call_args_list[1][0][0] == "/sbin/mount"
    assert view.show_message.call_count == 1


def test_workspace_dir_posix_exception_raised():
    """
    When the mount command results in an unexpected exception, log the error
    and use the default workspace dir.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open("tests/modes/mount_exists.txt", "rb") as fixture_file:
        fixture = fixture_file.read()
    mock_check = mock.MagicMock(side_effect=[ValueError, fixture])
    with mock.patch("os.name", "posix"), mock.patch(
        "mu.modes.circuitpython.check_output", mock_check
    ):
        assert am.workspace_dir() == "/media/ntoll/CIRCUITPY"
        assert mock_check.call_count == 2
        assert mock_check.call_args_list[0][0][0] == "mount"
        assert mock_check.call_args_list[1][0][0] == "/sbin/mount"


def test_workspace_dir_posix_missing():
    """
    Simulate being on os.name == 'posix' and a call to "mount" returns a
    no records associated with a micro:bit device.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open("tests/modes/mount_missing.txt", "rb") as fixture_file:
        fixture = fixture_file.read()
        with mock.patch("os.name", "posix"):
            with mock.patch(
                "mu.modes.circuitpython.check_output", return_value=fixture
            ), mock.patch(
                "mu.modes.circuitpython." "MicroPythonMode.workspace_dir"
            ) as mpm:
                mpm.return_value = "foo"
                assert am.workspace_dir() == "foo"


def test_workspace_dir_posix_chromeos_exists():
    """
    Simulate being on os.name == 'posix' and a check in /mnt/chromeos/removable returns
    a record associated with a CIRCUITPY device.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open("tests/modes/chromeos_devpath_exists.txt", "rb") as fixture_file:
        fixture = fixture_file.read()
        with mock.patch("os.name", "posix"):
            with mock.patch(
                "mu.modes.circuitpython.check_output", return_value=fixture
            ):
                with mock.patch("os.path.exists", return_value=True):
                    assert (
                        am.workspace_dir()
                        == "/mnt/chromeos/removable/CIRCUITPY/"
                    )


def test_workspace_dir_posix_chromeos_missing():
    """
    Simulate being on os.name == 'posix' and a check in /mnt/chromeos/removable returns
    no records associated with a CIRCUITPY device.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with open(
        "tests/modes/chromeos_devpath_missing.txt", "rb"
    ) as fixture_file:
        fixture = fixture_file.read()
        with mock.patch("os.name", "posix"):
            with mock.patch(
                "mu.modes.circuitpython.check_output", return_value=fixture
            ):
                with mock.patch("os.path.exists", return_value=False):
                    assert am.workspace_dir().endswith("mu_code")


@pytest.fixture
def windll():
    """
    Mocking the windll is tricky. It's not present on Posix platforms so
    we can't use standard patching. But it *is* present on Windows platforms
    so we need to unpatch once finished.
    """
    ctypes_has_windll = hasattr(ctypes, "windll")
    if ctypes_has_windll:
        mock_windll = mock.patch("ctypes.windll")
        mock_windll.start()
    else:
        mock_windll = mock.MagicMock()
        ctypes.windll = mock_windll

    yield mock_windll

    if ctypes_has_windll:
        mock_windll.stop()
    else:
        delattr(ctypes, "windll")


def test_workspace_dir_nt_exists(windll):
    """
    Simulate being on os.name == 'nt' and a disk with a volume name 'CIRCUITPY'
    exists indicating a connected device.

    """
    # ~ mock_windll = mock.MagicMock()
    # ~ mock_windll.kernel32 = mock.MagicMock()
    # ~ mock_windll.kernel32.GetVolumeInformationW = mock.MagicMock()
    # ~ mock_windll.kernel32.GetVolumeInformationW.return_value = None
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)

    with mock.patch("os.name", "nt"):
        with mock.patch("os.path.exists", return_value=True):
            return_value = ctypes.create_unicode_buffer("CIRCUITPY")
            with mock.patch(
                "ctypes.create_unicode_buffer", return_value=return_value
            ):
                assert am.workspace_dir() == "A:\\"


def test_workspace_dir_nt_missing(windll):
    """
    Simulate being on os.name == 'nt' and a disk with a volume name 'CIRCUITPY'
    does not exist for a device.
    """
    # ~ mock_windll = mock.MagicMock()
    # ~ mock_windll.kernel32 = mock.MagicMock()
    # ~ mock_windll.kernel32.GetVolumeInformationW = mock.MagicMock()
    # ~ mock_windll.kernel32.GetVolumeInformationW.return_value = None
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with mock.patch("os.name", "nt"):
        with mock.patch("os.path.exists", return_value=True):
            return_value = ctypes.create_unicode_buffer(1024)
            with mock.patch(
                "ctypes.create_unicode_buffer", return_value=return_value
            ), mock.patch(
                "mu.modes.circuitpython." "MicroPythonMode.workspace_dir"
            ) as mpm:
                mpm.return_value = "foo"
                assert am.workspace_dir() == "foo"


def test_workspace_dir_unknown_os():
    """
    Raises a NotImplementedError if the host OS is not supported.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = CircuitPythonMode(editor, view)
    with mock.patch("os.name", "foo"):
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
