# -*- coding: utf-8 -*-
"""
Tests for the micro:bit mode.
"""
import os
import os.path
import pytest
from mu.config import HOME_DIRECTORY
from mu.logic import Device
from mu.modes.microbit import MicrobitMode, DeviceFlasher, can_minify
from mu.modes.api import MICROBIT_APIS, SHARED_APIS
from mu.contrib import uflash
from unittest import mock
from tokenize import TokenError


TEST_ROOT = os.path.split(os.path.dirname(__file__))[0]


@pytest.fixture()
def microbit():
    # Board ID in Serial Number for micro:bit v1.3 and v1.3B
    return Device(
        0x0D28, 0x0204, "COM0", "9900ABCD", "ARM", "BBC micro:bit", "microbit"
    )


@pytest.fixture()
def microbit_v1_5():
    # Board ID in Serial Number for micro:bit v1.5
    return Device(
        0x0D28, 0x0204, "COM10", "9901ABCD", "ARM", "BBC micro:bit", "microbit"
    )


@pytest.fixture()
def microbit_incompatible():
    # Board ID not valid for a micro:bit board
    return Device(
        0x0D28, 0x0204, "COM0", "99AA1234", "ARM", "BBC micro:bit", "microbit"
    )


def test_DeviceFlasher_init():
    """
    Ensure the DeviceFlasher thread is set up correctly.
    """
    df = DeviceFlasher("path", "script", None)
    assert df.path_to_microbit == "path"
    assert df.python_script == "script"


def test_DeviceFlasher_run():
    """
    Ensure the uflash.flash function is called as expected.
    """
    df = DeviceFlasher("path", "script", None)
    mock_flash = mock.MagicMock()
    with mock.patch("mu.modes.microbit.uflash", mock_flash):
        df.run()
    mock_flash.flash.assert_called_once_with(
        paths_to_microbits=["path"], python_script="script"
    )


def test_DeviceFlasher_run_fail():
    """
    Ensure the on_flash_fail signal is emitted if an exception is thrown.
    """
    df = DeviceFlasher(["path"], "script", None)
    df.on_flash_fail = mock.MagicMock()
    mock_flash = mock.MagicMock()
    mock_flash.flash.side_effect = Exception("Boom")
    with mock.patch("mu.modes.microbit.uflash", mock_flash):
        df.run()
    df.on_flash_fail.emit.assert_called_once_with(str(Exception("Boom")))


def test_microbit_mode():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    assert mm.name == "BBC micro:bit"
    assert mm.description is not None
    assert mm.icon == "microbit"
    assert mm.editor == editor
    assert mm.view == view

    with mock.patch("mu.modes.microbit.CHARTS", True):
        actions = mm.actions()
    assert len(actions) == 4
    assert actions[0]["name"] == "flash"
    assert actions[0]["handler"] == mm.flash
    assert actions[1]["name"] == "files"
    assert actions[1]["handler"] == mm.toggle_files
    assert actions[2]["name"] == "repl"
    assert actions[2]["handler"] == mm.toggle_repl
    assert actions[3]["name"] == "plotter"
    assert actions[3]["handler"] == mm.toggle_plotter


def test_microbit_mode_no_charts():
    """
    If QCharts is not available, ensure plotter is not displayed.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch("mu.modes.microbit.CHARTS", False):
        actions = mm.actions()
        assert len(actions) == 3
        assert actions[0]["name"] == "flash"
        assert actions[0]["handler"] == mm.flash
        assert actions[1]["name"] == "files"
        assert actions[1]["handler"] == mm.toggle_files
        assert actions[2]["name"] == "repl"
        assert actions[2]["handler"] == mm.toggle_repl


def test_flash_no_tab():
    """
    If there are no active tabs simply return.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    mm = MicrobitMode(editor, view)
    assert mm.flash() is None


def test_flash_with_attached_device_has_latest_firmware_v1(microbit):
    """
    There's NO need to use the DeviceFlasher if the board already has the
    latest firmware. In which case, just call copy_main.
    """
    version_info = {
        "sysname": "microbit",
        "nodename": "microbit",
        "release": uflash.MICROPYTHON_V1_VERSION,
        "version": (
            "micro:bit v0.1.0-b'e10a5ff' on 2018-6-8; MicroPython "
            "v1.9.2-34-gd64154c73 on 2017-09-01"
        ),
        "machine": "micro:bit with nRF51822",
    }
    with mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="/path/microbit"
    ), mock.patch(
        "mu.modes.microbit.microfs.version", return_value=version_info
    ), mock.patch(
        "mu.modes.microbit.os.path.exists", return_value=True
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = ""
        editor.current_device = microbit
        mm = MicrobitMode(editor, view)
        mm.copy_main = mock.MagicMock()
        mm.set_buttons = mock.MagicMock()
        mm.flash_start = mock.MagicMock()
        mm.flash()
        assert mm.flash_start.call_count == 0
        mm.copy_main.assert_called_once_with(b"foo")


def test_flash_with_attached_device_has_latest_firmware_v2(microbit):
    """
    There's NO need to use the DeviceFlasher if the board already has the
    latest firmware. In which case, just call copy_main.
    """
    version_info = {
        "sysname": "microbit",
        "nodename": "microbit",
        "release": uflash.MICROPYTHON_V2_VERSION,
        "version": (
            "micro:bit v2.0.0-beta.3+d6c01d0 on 2020-12-21; "
            "MicroPython v1.13 on 2020-12-21"
        ),
        "machine": "micro:bit with nRF52833",
    }
    with mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="/path/microbit"
    ), mock.patch(
        "mu.modes.microbit.microfs.version", return_value=version_info
    ), mock.patch(
        "mu.modes.microbit.os.path.exists", return_value=True
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = ""
        editor.current_device = microbit
        mm = MicrobitMode(editor, view)
        mm.copy_main = mock.MagicMock()
        mm.set_buttons = mock.MagicMock()
        mm.flash_start = mock.MagicMock()
        mm.flash()
        assert mm.flash_start.call_count == 0
        mm.copy_main.assert_called_once_with(b"foo")


def test_flash_device_has_latest_firmware_encounters_serial_problem(
    microbit,
):
    """
    If copy_main encounters an IOError (likely on Windows), revert to
    old-school flashing.
    """
    version_info = {
        "sysname": "microbit",
        "nodename": "microbit",
        "release": uflash.MICROPYTHON_V1_VERSION,
        "version": (
            "micro:bit v0.1.0-b'e10a5ff' on 2018-6-8; MicroPython "
            "v1.9.2-34-gd64154c73 on 2017-09-01"
        ),
        "machine": "micro:bit with nRF51822",
    }
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="/path/microbit"
    ), mock.patch(
        "mu.modes.microbit.microfs.version", return_value=version_info
    ), mock.patch(
        "mu.modes.microbit.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = ""
        editor.current_device = microbit
        mm = MicrobitMode(editor, view)
        mm.flash_failed = mock.MagicMock()
        error = IOError("bang")
        mm.copy_main = mock.MagicMock(side_effect=error)
        mm.set_buttons = mock.MagicMock()
        mm.flash_attached = mock.MagicMock(side_effect=mm.flash_attached)
        mm.flash()
        mm.copy_main.assert_called_once_with(b"foo")
        mm.flash_attached.assert_called_once_with(b"foo", "/path/microbit")
        mock_flasher_class.assert_called_once_with("/path/microbit", b"foo")
        mock_flasher.finished.connect.assert_called_once_with(
            mm.flash_finished
        )
        mock_flasher.on_flash_fail.connect.assert_called_once_with(
            mm.flash_failed
        )
        mock_flasher.start.assert_called_once_with()


def test_flash_with_attached_device_has_latest_firmware_encounters_problem(
    microbit,
):
    """
    If copy_main encounters a non-IOError, handle in a helpful manner.
    """
    version_info = {
        "sysname": "microbit",
        "nodename": "microbit",
        "release": uflash.MICROPYTHON_V1_VERSION,
        "version": (
            "micro:bit v0.1.0-b'e10a5ff' on 2018-6-8; MicroPython "
            "v1.9.2-34-gd64154c73 on 2017-09-01"
        ),
        "machine": "micro:bit with nRF51822",
    }
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="/path/microbit"
    ), mock.patch(
        "mu.modes.microbit.microfs.version", return_value=version_info
    ), mock.patch(
        "mu.modes.microbit.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = ""
        editor.current_device = microbit
        mm = MicrobitMode(editor, view)
        mm.flash_failed = mock.MagicMock()
        error = ValueError("bang")
        mm.copy_main = mock.MagicMock(side_effect=error)
        mm.set_buttons = mock.MagicMock()
        mm.flash()
        assert mock_flasher_class.call_count == 0
        mm.copy_main.assert_called_once_with(b"foo")
        mm.flash_failed.assert_called_once_with(error)


def test_flash_with_attached_device_has_old_firmware(microbit):
    """
    If the device has some unknown old firmware, force flash it.
    """
    version_info = {
        "sysname": "microbit",
        "nodename": "microbit",
        "release": "1.0",
        "version": ("v1.9.2-34-gd64154c73 on 2017-09-01"),
        "machine": "micro:bit with nRF51822",
    }
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="/path/microbit"
    ), mock.patch(
        "mu.modes.microbit.microfs.version", return_value=version_info
    ), mock.patch(
        "mu.modes.microbit.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = ""
        editor.current_device = microbit
        mm = MicrobitMode(editor, view)
        mm.copy_main = mock.MagicMock()
        mm.set_buttons = mock.MagicMock()
        mm.flash_and_send = mock.MagicMock(side_effect=mm.flash_and_send)
        mm.flash()
        assert mm.flash_thread == mock_flasher
        assert editor.show_status_message.call_count == 1
        mm.set_buttons.assert_called_once_with(
            flash=False, repl=False, files=False, plotter=False
        )
        mm.flash_and_send.assert_called_once_with(b"foo", "/path/microbit")
        mock_flasher_class.assert_called_once_with(
            "/path/microbit", path_to_runtime=None, python_script=None
        )
        mock_flasher.finished.connect.assert_called_once_with(
            mm.flash_finished
        )
        mock_flasher.on_flash_fail.connect.assert_called_once_with(
            mm.flash_failed
        )
        mock_flasher.start.assert_called_once_with()


def test_flash_force_with_no_micropython(microbit):
    """
    Ensure the expected calls are made to DeviceFlasher and a helpful status
    message is enacted if there is no MicroPython firmware on the device.
    """
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="bar"
    ), mock.patch(
        "mu.modes.microbit.microfs.version", side_effect=ValueError("bang")
    ), mock.patch(
        "mu.modes.microbit.os.path.isfile", return_value=True
    ), mock.patch(
        "mu.modes.microbit.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = "/foo/bar"
        editor.current_device = microbit
        mm = MicrobitMode(editor, view)
        mm.set_buttons = mock.MagicMock()
        mm.flash_and_send = mock.MagicMock(side_effect=mm.flash_and_send)
        mm.flash()
        assert mm.flash_thread == mock_flasher
        assert editor.show_status_message.call_count == 1
        mm.set_buttons.assert_called_once_with(
            flash=False, repl=False, files=False, plotter=False
        )
        mm.flash_and_send.assert_called_once_with(b"foo", "bar", "/foo/bar")
        mock_flasher_class.assert_called_once_with(
            "bar", python_script=None, path_to_runtime="/foo/bar"
        )
        mock_flasher.finished.connect.assert_called_once_with(
            mm.flash_finished
        )
        mock_flasher.on_flash_fail.connect.assert_called_once_with(
            mm.flash_failed
        )
        mock_flasher.start.assert_called_once_with()


def test_flash_force_with_unsupported_microbit(microbit_incompatible):
    """
    If Mu is supposed to flash the device, but the device is, in fact, not
    one that's supported by the version of MicroPython built into Mu, then
    display a warning message to the user.
    """
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="bar"
    ), mock.patch(
        "mu.modes.microbit.microfs.version", side_effect=ValueError("bang")
    ), mock.patch(
        "mu.modes.microbit.os.path.isfile", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        # Empty file to force flashing.
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.microbit_runtime = ""
        editor.minify = False
        editor.current_device = microbit_incompatible
        mm = MicrobitMode(editor, view)
        mm.set_buttons = mock.MagicMock()
        mm.flash()
        assert view.show_message.call_count == 1


def test_flash_force_with_attached_device(microbit):
    """
    Ensure the expected calls are made to DeviceFlasher and a helpful status
    message is enacted.
    """
    version_info = {
        "sysname": "microbit",
        "nodename": "microbit",
        "release": "1.0",
        "version": (
            "micro:bit v0.0.9-b'e10a5ff' on 2018-6-8; MicroPython "
            "v1.9.2-34-gd64154c73 on 2017-09-01"
        ),
        "machine": "micro:bit with nRF51822",
    }
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="/foo/microbit/"
    ), mock.patch(
        "mu.modes.microbit.microfs.version", return_value=version_info
    ), mock.patch(
        "mu.modes.microbit.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.os.path.isfile", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = "/foo/bar.hex"
        editor.current_device = microbit
        mm = MicrobitMode(editor, view)
        mm.set_buttons = mock.MagicMock()
        mm.flash_and_send = mock.MagicMock(side_effect=mm.flash_and_send)
        mm.flash()
        assert mm.flash_thread == mock_flasher
        assert editor.show_status_message.call_count == 1
        mm.set_buttons.assert_called_once_with(
            flash=False, repl=False, files=False, plotter=False
        )
        mm.flash_and_send.assert_called_once_with(
            b"foo", "/foo/microbit/", "/foo/bar.hex"
        )
        mock_flasher_class.assert_called_once_with(
            "/foo/microbit/",
            python_script=None,
            path_to_runtime="/foo/bar.hex",
        )
        mock_flasher.finished.connect.assert_called_once_with(
            mm.flash_finished
        )
        mock_flasher.on_flash_fail.connect.assert_called_once_with(
            mm.flash_failed
        )
        mock_flasher.start.assert_called_once_with()


def test_flash_with_attached_device_and_custom_runtime(microbit_v1_5):
    """
    Ensure the custom runtime is passed into the DeviceFlasher thread.
    """
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.modes.base.BaseMode.workspace_dir", return_value=TEST_ROOT
    ), mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="/foo/microbit/"
    ), mock.patch(
        "mu.modes.microbit.os.path.isfile", return_value=True
    ), mock.patch(
        "mu.modes.microbit.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = True
        editor.current_device = microbit_v1_5
        editor.microbit_runtime = os.path.join("tests", "customhextest.hex")
        mm = MicrobitMode(editor, view)
        mm.flash_and_send = mock.MagicMock(side_effect=mm.flash_and_send)
        mm.flash()
        assert editor.show_status_message.call_count == 1
        assert (
            os.path.join("tests", "customhextest.hex")
            in editor.show_status_message.call_args[0][0]
        )
        assert mock_flasher_class.call_count == 1
        mm.flash_and_send.assert_called_once_with(
            b"foo",
            "/foo/microbit/",
            os.path.join("tests", "customhextest.hex"),
        )
        mock_flasher_class.assert_called_once_with(
            "/foo/microbit/",
            python_script=None,
            path_to_runtime=os.path.join("tests", "customhextest.hex"),
        )
        mock_flasher.finished.connect.assert_called_once_with(
            mm.flash_finished
        )
        mock_flasher.on_flash_fail.connect.assert_called_once_with(
            mm.flash_failed
        )
        mock_flasher.start.assert_called_once_with()


def test_flash_with_attached_known_device_and_forced(microbit_v1_5):
    """
    If the runtime must be flashed, and the serial number for the device is
    supported, then flash the built-in MicroPython runtime.
    """
    version_info = {
        "sysname": "microbit",
        "nodename": "microbit",
        "release": "1.0.0",
        "version": (
            "micro:bit v0.0.9-b'e10a5ff' on 2018-6-8; MicroPython "
            "v1.9.2-34-gd64154c73 on 2017-09-01"
        ),
        "machine": "micro:bit with nRF51822",
    }
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.modes.microbit.uflash.find_microbit", return_value="/bar/microbit"
    ), mock.patch(
        "mu.modes.microbit.microfs.version", return_value=version_info
    ), mock.patch(
        "mu.modes.microbit.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        # Trigger force flash with an empty file.
        view.current_tab.text = mock.MagicMock(return_value="")
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = ""
        editor.current_device = microbit_v1_5
        mm = MicrobitMode(editor, view)
        mm.flash_and_send = mock.MagicMock(side_effect=mm.flash_and_send)
        mm.flash()
        assert mock_flasher_class.call_count == 1
        mm.flash_and_send.assert_called_once_with(b"", "/bar/microbit")
        mock_flasher_class.assert_called_once_with(
            "/bar/microbit", python_script=None, path_to_runtime=None
        )


def test_force_flash_no_serial_connection():
    """
    If Mu cannot establish a serial connection to the micro:bit, BUT the path
    to the micro:bit on the filesystem is known, then fall back to old-school
    flashing of hex with script appended to the end.
    """
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.contrib.uflash.find_microbit", return_value="/path/microbit"
    ), mock.patch("mu.contrib.microfs.get_serial"), mock.patch(
        "mu.contrib.microfs.version", side_effect=IOError("bang")
    ), mock.patch(
        "mu.logic.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = ""
        editor.current_device = None
        mm = MicrobitMode(editor, view)
        mm.flash_attached = mock.MagicMock(side_effect=mm.flash_attached)
        mm.flash()
        mm.flash_attached.assert_called_once_with(b"foo", "/path/microbit")
        mock_flasher_class.assert_called_once_with("/path/microbit", b"foo")
        mock_flasher.finished.connect.assert_called_once_with(
            mm.flash_finished
        )


def test_force_flash_empty_script(microbit_v1_5):
    """
    If the script to be flashed onto the device is empty, this is a signal to
    force a full flash of the "vanilla" / empty MicroPython runtime onto the
    device.
    """
    version_info = {
        "sysname": "microbit",
        "nodename": "microbit",
        "release": uflash.MICROPYTHON_V1_VERSION,
        "version": (
            "micro:bit v0.1.0-b'e10a5ff' on 2018-6-8; MicroPython "
            "v1.9.2-34-gd64154c73 on 2017-09-01"
        ),
        "machine": "micro:bit with nRF51822",
    }
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.contrib.uflash.find_microbit", return_value="/path/microbit"
    ), mock.patch("mu.contrib.microfs.get_serial"), mock.patch(
        "mu.contrib.microfs.version", return_value=version_info
    ), mock.patch(
        "mu.logic.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="   ")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = ""
        editor.current_device = microbit_v1_5
        mm = MicrobitMode(editor, view)
        mm.flash_and_send = mock.MagicMock(side_effect=mm.flash_and_send)
        mm.flash()
        mm.flash_and_send.assert_called_once_with(b"   ", "/path/microbit")
        mock_flasher_class.assert_called_once_with(
            "/path/microbit", path_to_runtime=None, python_script=None
        )
        mock_flasher.finished.connect.assert_called_once_with(
            mm.flash_finished
        )


def test_force_flash_user_specified_device_path():
    """
    Ensure that if a micro:bit is not automatically found by uflash then it
    prompts the user to locate the device and, assuming a path was given,
    saves the hex in the expected location.
    """
    version_info = {
        "sysname": "microbit",
        "nodename": "microbit",
        "release": uflash.MICROPYTHON_V1_VERSION,
        "version": (
            "micro:bit v0.1.0-b'e10a5ff' on 2018-6-8; MicroPython "
            "v1.9.2-34-gd64154c73 on 2017-09-01"
        ),
        "machine": "micro:bit with nRF51822",
    }
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch(
        "mu.contrib.uflash.find_microbit", return_value=None
    ), mock.patch("mu.contrib.microfs.get_serial"), mock.patch(
        "mu.contrib.microfs.version", return_value=version_info
    ), mock.patch(
        "mu.logic.os.path.exists", return_value=True
    ), mock.patch(
        "mu.modes.microbit.DeviceFlasher", mock_flasher_class
    ):
        view = mock.MagicMock()
        view.get_microbit_path = mock.MagicMock(return_value="/path/microbit")
        view.current_tab.text = mock.MagicMock(return_value="foo")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.minify = False
        editor.microbit_runtime = ""
        editor.current_device = None
        mm = MicrobitMode(editor, view)
        mm.flash_attached = mock.MagicMock(side_effect=mm.flash_attached)
        mm.flash()
        home = HOME_DIRECTORY
        view.get_microbit_path.assert_called_once_with(home)
        mm.flash_attached.assert_called_once_with(b"foo", "/path/microbit")
        mock_flasher_class.assert_called_once_with("/path/microbit", b"foo")
        mock_flasher.finished.connect.assert_called_once_with(
            mm.flash_finished
        )


def test_flash_path_specified_does_not_exist(microbit):
    """
    Ensure that if a micro:bit is not automatically found by uflash and the
    user has previously specified a path to the device, then the hex is saved
    in the specified location.
    """
    with mock.patch(
        "mu.contrib.uflash.find_microbit", return_value=None
    ), mock.patch("mu.logic.os.path.exists", return_value=False), mock.patch(
        "mu.logic.os.makedirs", return_value=None
    ), mock.patch(
        "mu.contrib.uflash.save_hex", return_value=None
    ) as s:
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value="")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.current_device = microbit
        mm = MicrobitMode(editor, view)
        mm.user_defined_microbit_path = "baz"
        mm.flash()
        message = "Could not find an attached BBC micro:bit."
        information = (
            "Please ensure you leave enough time for the BBC"
            " micro:bit to be attached and configured correctly"
            " by your computer. This may take several seconds."
            " Alternatively, try removing and re-attaching the"
            " device or saving your work and restarting Mu if"
            " the device remains unfound."
        )
        view.show_message.assert_called_once_with(message, information)
        assert s.call_count == 0


def test_flash_without_device():
    """
    If no device is found and the user doesn't provide a path then ensure a
    helpful status message is enacted.
    """
    with mock.patch(
        "mu.contrib.uflash.find_microbit", return_value=None
    ), mock.patch("mu.contrib.uflash.save_hex", return_value=None) as s:
        view = mock.MagicMock()
        view.get_microbit_path = mock.MagicMock(return_value=None)
        view.current_tab.text = mock.MagicMock(return_value="")
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        editor.current_device = None
        mm = MicrobitMode(editor, view)
        mm.flash()
        message = "Could not find an attached BBC micro:bit."
        information = (
            "Please ensure you leave enough time for the BBC"
            " micro:bit to be attached and configured correctly"
            " by your computer. This may take several seconds."
            " Alternatively, try removing and re-attaching the"
            " device or saving your work and restarting Mu if"
            " the device remains unfound."
        )
        view.show_message.assert_called_once_with(message, information)
        home = HOME_DIRECTORY
        view.get_microbit_path.assert_called_once_with(home)
        assert s.call_count == 0


@pytest.mark.skipif(not can_minify, reason="No minifier available to test")
def test_flash_script_too_big():
    """
    If the script in the current tab is too big, abort in the expected way.
    """
    view = mock.MagicMock()
    view.current_tab.text = mock.MagicMock(return_value="x" * 8193)
    view.current_tab.label = "foo"
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    editor.minify = True
    mm = MicrobitMode(editor, view)
    with mock.patch("mu.contrib.uflash._MAX_SIZE", 8188):
        mm.flash()
    view.show_message.assert_called_once_with(
        'Unable to flash "foo"',
        "Our minifier tried but your " "script is too long!",
        "Warning",
    )


def test_flash_script_too_big_no_minify():
    """
    If the script in the current tab is too big, abort in the expected way.
    """
    view = mock.MagicMock()
    view.current_tab.text = mock.MagicMock(return_value="x" * 8193)
    view.current_tab.label = "foo"
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    editor.minify = False
    mm = MicrobitMode(editor, view)
    with mock.patch("mu.modes.microbit.can_minify", False), mock.patch(
        "mu.contrib.uflash._MAX_SIZE", 8188
    ):
        mm.flash()
    view.show_message.assert_called_once_with(
        'Unable to flash "foo"',
        "Your script is too long and code minification is disabled",
        "Warning",
    )


def test_flash_finished_copy_main():
    """
    Ensure state is set back as expected when the flashing thread is finished.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.python_script = b"foo"
    mm.copy_main = mock.MagicMock()
    mm.set_buttons = mock.MagicMock()
    mm.flash_thread = mock.MagicMock()
    mm.flash_finished()
    mm.set_buttons.assert_called_once_with(
        flash=True, repl=True, files=True, plotter=True
    )
    editor.show_status_message.assert_called_once_with("Finished flashing.")
    assert mm.flash_thread is None
    mm.copy_main.assert_called_once_with(b"foo")


def test_flash_finished_copy_main_encounters_error():
    """
    If copy_main encounters an error, flash_failed is called.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.flash_failed = mock.MagicMock()
    mm.python_script = b"foo"
    error = IOError("boom")
    mm.copy_main = mock.MagicMock(side_effect=error)
    mm.set_buttons = mock.MagicMock()
    mm.flash_thread = mock.MagicMock()
    mm.flash_finished()
    mm.set_buttons.assert_called_once_with(
        flash=True, repl=True, files=True, plotter=True
    )
    editor.show_status_message.assert_called_once_with("Finished flashing.")
    assert mm.flash_thread is None
    mm.copy_main.assert_called_once_with(b"foo")
    mm.flash_failed.assert_called_once_with(error)


def test_flash_finished_no_copy():
    """
    Ensure state is set back as expected when the flashing thread is finished.

    If no python_script is set, then copy_main is NOT called.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.copy_main = mock.MagicMock()
    mm.set_buttons = mock.MagicMock()
    mm.flash_thread = mock.MagicMock()
    mm.flash_finished()
    mm.set_buttons.assert_called_once_with(
        flash=True, repl=True, files=True, plotter=True
    )
    editor.show_status_message.assert_called_once_with("Finished flashing.")
    assert mm.flash_thread is None
    assert mm.copy_main.call_count == 0


def test_copy_main_no_python_script():
    """
    If copy_main is called and there's nothing in provided script, then
    don't do anything.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch("mu.modes.microbit.microfs") as mock_microfs:
        mm.copy_main("")
        assert mock_microfs.execute.call_count == 0


def test_copy_main_with_python_script():
    """
    If copy_main is called and there's something in provided script, then
    use microfs to write it to the device's on-board filesystem, followed by
    a soft-reboot.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch("mu.modes.microbit.microfs") as mock_microfs:
        mock_microfs.execute.return_value = ("", "")
        mm.copy_main("import love")
        serial = mock_microfs.get_serial()
        expected = [
            "fd = open('main.py', 'wb')",
            "f = fd.write",
            "f('import love')",
            "fd.close()",
        ]
        mock_microfs.execute.assert_called_once_with(expected, serial)
        assert serial.write.call_args_list[0][0][0] == b"import microbit\r\n"
        assert serial.write.call_args_list[1][0][0] == b"microbit.reset()\r\n"
        # The script is re-set to empty.
        assert mm.python_script == ""


def test_copy_main_with_python_script_encounters_device_error():
    """
    If the device returns an error, then copy_main should raise an IOError.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch("mu.modes.microbit.microfs") as mock_microfs:
        mock_microfs.execute.return_value = ("", "BANG!")
        with pytest.raises(IOError):
            mm.copy_main("import love")


def test_flash_failed():
    """
    Ensure things are cleaned up if flashing failed.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.set_buttons = mock.MagicMock()
    mm.flash_thread = mock.MagicMock()
    mm.flash_failed("Boom")
    assert view.show_message.call_count == 1
    mm.set_buttons.assert_called_once_with(
        flash=True, repl=True, files=True, plotter=True
    )
    assert mm.flash_thread is None


def test_flash_minify(microbit_v1_5):
    view = mock.MagicMock()
    script = "#" + ("x" * 8193) + "\n"
    view.current_tab.text = mock.MagicMock(return_value=script)
    view.current_tab.label = "foo"
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    editor.minify = True
    editor.current_device = microbit_v1_5
    mm = MicrobitMode(editor, view)
    mm.set_buttons = mock.MagicMock()
    with mock.patch("mu.modes.microbit.DeviceFlasher"), mock.patch(
        "mu.contrib.uflash._MAX_SIZE", 8188
    ), mock.patch("nudatus.mangle", return_value="") as m:
        mm.flash()
        m.assert_called_once_with(script)

    ex = TokenError("Bad", (1, 0))
    with mock.patch("nudatus.mangle", side_effect=ex) as m, mock.patch(
        "mu.contrib.uflash._MAX_SIZE", 8188
    ):
        mm.flash()
        view.show_message.assert_called_with(
            'Unable to flash "foo"',
            "Problem minifying script\nBad [1:0]",
            "Warning",
        )


def test_flash_minify_no_minify(microbit_v1_5):
    view = mock.MagicMock()
    view.current_tab.label = "foo"
    view.show_message = mock.MagicMock()
    script = "#" + ("x" * 8193) + "\n"
    view.current_tab.text = mock.MagicMock(return_value=script)
    editor = mock.MagicMock()
    editor.minify = True
    editor.current_device = microbit_v1_5
    mm = MicrobitMode(editor, view)
    mm.set_buttons = mock.MagicMock()
    with mock.patch("mu.modes.microbit.can_minify", False), mock.patch(
        "mu.contrib.uflash._MAX_SIZE", 8188
    ), mock.patch("nudatus.mangle", return_value="") as m:
        mm.flash()
        assert m.call_count == 0
        view.show_message.assert_called_once_with(
            'Unable to flash "foo"',
            "Your script is too long and the minifier isn't available",
            "Warning",
        )


def test_add_fs(microbit):
    """
    It's possible to add the file system pane if the REPL is inactive.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    editor.current_device = microbit
    mm = MicrobitMode(editor, view)
    with mock.patch("mu.modes.microbit.FileManager") as mock_fm, mock.patch(
        "mu.modes.microbit.QThread"
    ):
        mm.add_fs()
        workspace = mm.workspace_dir()
        view.add_filesystem.assert_called_once_with(
            workspace, mock_fm(), "micro:bit"
        )
        assert mm.fs


def test_add_fs_no_device():
    """
    If there's no device attached then ensure a helpful message is displayed.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    editor.current_device = None
    mm = MicrobitMode(editor, view)
    mm.add_fs()
    assert view.show_message.call_count == 1


@mock.patch("mu.modes.microbit.FileManager")
def test_remove_fs(fm):
    """
    Removing the file system shuts down the file manager thread and
    results in the expected state.

    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)

    mock_qthread = mock.MagicMock()
    mock_qthread_class = mock.MagicMock(return_value=mock_qthread)

    with mock.patch("mu.modes.microbit.QThread", mock_qthread_class):
        mm.add_fs()
        mm.remove_fs()
        mock_qthread.quit.assert_called_once_with()
        assert mm.view.remove_filesystem.call_count == 1
        assert mm.fs is None
        assert mm.file_manager is None
        assert mm.file_manager_thread is None


@mock.patch("mu.modes.microbit.FileManager")
def test_remove_fs_terminates_thread(fm):
    """
    If the file manager thread doesn't quit by itself, we will terminate it
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)

    mock_qthread = mock.MagicMock()
    mock_qthread_class = mock.MagicMock(return_value=mock_qthread)
    mock_qthread.wait = mock.MagicMock(return_value=False)

    with mock.patch("mu.modes.microbit.QThread", mock_qthread_class):
        mm.add_fs()
        mm.remove_fs()
        mock_qthread.quit.assert_called_once_with()
        mock_qthread.terminate.assert_called_once_with()
        mock_qthread.wait.call_count == 2


def test_toggle_files_on():
    """
    If the fs is off, toggle it on.
    """
    view = mock.MagicMock()
    view.button_bar.slots = {
        "repl": mock.MagicMock(),
        "plotter": mock.MagicMock(),
    }
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)

    def side_effect(*args, **kwargs):
        mm.fs = True

    mm.add_fs = mock.MagicMock(side_effect=side_effect)
    mm.repl = None
    mm.fs = None
    mm.toggle_files(None)
    assert mm.add_fs.call_count == 1
    view.button_bar.slots["repl"].setEnabled.assert_called_once_with(False)
    view.button_bar.slots["plotter"].setEnabled.assert_called_once_with(False)


def test_toggle_files_off():
    """
    If the fs is on, toggle if off.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.remove_fs = mock.MagicMock()
    mm.repl = None
    mm.fs = True
    mm.toggle_files(None)
    assert mm.remove_fs.call_count == 1


def test_toggle_files_with_repl():
    """
    If the REPL is active, ensure a helpful message is displayed.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.add_repl = mock.MagicMock()
    mm.repl = True
    mm.fs = None
    mm.toggle_files(None)
    assert view.show_message.call_count == 1


def test_toggle_files_with_plotter():
    """
    If the plotter is active, ensure a helpful message is displayed.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.plotter = True
    mm.fs = None
    mm.toggle_files(None)
    assert view.show_message.call_count == 1


def test_toggle_repl():
    """
    Ensure the REPL is able to toggle on if there's no file system pane.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.set_buttons = mock.MagicMock()

    def side_effect(*args, **kwargs):
        mm.repl = True

    with mock.patch(
        "mu.modes.microbit.MicroPythonMode.toggle_repl",
        side_effect=side_effect,
    ) as tr:
        mm.repl = None
        mm.toggle_repl(None)
        tr.assert_called_once_with(None)
        mm.set_buttons.assert_called_once_with(flash=False, files=False)


def test_toggle_repl_no_repl_or_plotter():
    """
    Ensure the file system button is enabled if the repl toggles off and the
    plotter isn't active.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.set_buttons = mock.MagicMock()

    def side_effect(*args, **kwargs):
        mm.repl = False
        mm.plotter = False

    with mock.patch(
        "mu.modes.microbit.MicroPythonMode.toggle_repl",
        side_effect=side_effect,
    ) as tr:
        mm.repl = None
        mm.toggle_repl(None)
        tr.assert_called_once_with(None)
        mm.set_buttons.assert_called_once_with(flash=True, files=True)


def test_toggle_repl_with_fs():
    """
    If the file system is active, show a helpful message instead.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.remove_repl = mock.MagicMock()
    mm.repl = None
    mm.fs = True
    mm.toggle_repl(None)
    assert view.show_message.call_count == 1


def test_toggle_plotter():
    """
    Ensure the plotter is toggled on if the file system pane is absent.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.set_buttons = mock.MagicMock()

    def side_effect(*args, **kwargs):
        mm.plotter = True

    with mock.patch(
        "mu.modes.microbit.MicroPythonMode.toggle_plotter",
        side_effect=side_effect,
    ) as tp:
        mm.plotter = None
        mm.toggle_plotter(None)
        tp.assert_called_once_with(None)
        mm.set_buttons.assert_called_once_with(flash=False, files=False)


def test_toggle_plotter_no_repl_or_plotter():
    """
    Ensure the file system button is enabled if the plotter toggles off and the
    repl isn't active.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.set_buttons = mock.MagicMock()

    def side_effect(*args, **kwargs):
        mm.plotter = False
        mm.repl = False

    with mock.patch(
        "mu.modes.microbit.MicroPythonMode.toggle_plotter",
        side_effect=side_effect,
    ) as tp:
        mm.plotter = None
        mm.toggle_plotter(None)
        tp.assert_called_once_with(None)
        mm.set_buttons.assert_called_once_with(flash=True, files=True)


def test_toggle_plotter_with_fs():
    """
    If the file system is active, show a helpful message instead.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.remove_plotter = mock.MagicMock()
    mm.plotter = None
    mm.fs = True
    mm.toggle_plotter(None)
    assert view.show_message.call_count == 1


def test_api():
    """
    Ensure the right thing comes back from the API.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    api = mm.api()
    assert api == SHARED_APIS + MICROBIT_APIS


def test_on_data_flood():
    """
    Ensure the "Files" button is re-enabled before calling the base method.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.set_buttons = mock.MagicMock()
    with mock.patch("builtins.super") as mock_super:
        mm.on_data_flood()
        mm.set_buttons.assert_called_once_with(files=True)
        mock_super().on_data_flood.assert_called_once_with()


def test_open_hex():
    """
    Tries to open hex files with uFlash.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mock_open = mock.mock_open()
    hex_extracted = "RECOVERED"
    with mock.patch("builtins.open", mock_open), mock.patch(
        "mu.contrib.uflash.extract_script", return_value=hex_extracted
    ) as extract_script:
        text, newline = mm.open_file("path_to_file.hex")
    assert text == hex_extracted
    assert newline == os.linesep
    assert extract_script.call_count == 1
    assert mock_open.call_count == 1


def test_open_ignore_non_hex():
    """
    Ignores any other than hex file types.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mock_open = mock.mock_open()
    with mock.patch("builtins.open", mock_open), mock.patch(
        "mu.contrib.uflash.extract_script", return_value="Should not be called"
    ) as extract_script:
        text, newline = mm.open_file("path_to_file.py")
    assert text is None
    assert newline is None
    assert extract_script.call_count == 0
    assert mock_open.call_count == 0

    mock_open.reset_mock()
    with mock.patch("builtins.open", mock_open), mock.patch(
        "mu.contrib.uflash.extract_script", return_value="Should not be called"
    ) as extract_script:
        text, newline = mm.open_file("file_no_extension")
    assert text is None
    assert newline is None
    assert extract_script.call_count == 0
    assert mock_open.call_count == 0


def test_open_hex_with_exception():
    """
    If an exception is encountered when trying to open the hex file, make sure
    it is swallowed and return None.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mock_open = mock.mock_open()
    mock_extract = mock.MagicMock(side_effect=Exception(":("))
    with mock.patch("builtins.open", mock_open), mock.patch(
        "mu.contrib.uflash.extract_script", mock_extract
    ):
        text, newline = mm.open_file("path_to_file.hex")
    assert text is None
    assert newline is None
    assert mock_extract.call_count == 1
    assert mock_open.call_count == 1


def test_deactivate():
    """
    Ensure Filesystem pane is hidden, when MicroPython-mode is
    deactivated.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.remove_fs = mock.MagicMock()
    mm.activate()
    mm.fs = True
    mm.deactivate()
    mm.remove_fs.assert_called_once_with()


def test_device_changed(microbit):
    """
    Ensure Filesystem pane is reconnected, when the user changes
    device.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.add_fs = mock.MagicMock()
    mm.remove_fs = mock.MagicMock()
    mm.activate()
    mm.fs = True
    mm.device_changed(microbit)
    mm.remove_fs.assert_called_once_with()
    mm.add_fs.assert_called_once_with()


def test_stop(microbit):
    """
    Check that invoking stop remove the file system pane and thus
    shutsdown the file manager thread
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.remove_fs = mock.MagicMock()

    mock_flash_thread = mock.MagicMock()
    with mock.patch(
        "mu.modes.microbit.DeviceFlasher", return_value=mock_flash_thread
    ):
        mm.flash_attached("pass", "/path/to/microbit/mount/")
        mm.stop()
        mock_flash_thread.quit.assert_called_once_with()

    mm.remove_fs.assert_called_once_with()


def test_stop_terminates_thread(microbit):
    """
    Check that invoking stop remove the file system pane and thus
    shutsdown the file manager thread
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.remove_fs = mock.MagicMock()

    mock_flash_thread = mock.MagicMock()
    mock_flash_thread.wait = mock.MagicMock(return_value=False)
    with mock.patch(
        "mu.modes.microbit.DeviceFlasher", return_value=mock_flash_thread
    ):
        mm.flash_attached("pass", "/path/to/microbit/mount/")
        mm.stop()
        mock_flash_thread.quit.assert_called_once_with()
        mock_flash_thread.terminate.assert_called_once_with()
        mock_flash_thread.wait.call_count == 2
