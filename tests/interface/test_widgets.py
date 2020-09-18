# -*- coding: utf-8 -*-
"""
Tests for custom widgets made for Mu.
"""

from unittest import mock
import pytest
import mu.interface.main
import mu.interface.themes
import mu.interface.editor


@pytest.fixture
def microbit():
    """
    Fixture for easy setup of microbit device in tests
    """
    microbit = mu.logic.Device(
        0x0D28,
        0x0204,
        "COM1",
        123456,
        "ARM",
        "BBC micro:bit",
        "microbit",
        None,
    )
    return microbit


@pytest.fixture
def adafruit_feather():
    """
    Fixture for easy setup of adafruit feather device in tests
    """
    adafruit_feather = mu.logic.Device(
        0x239A,
        0x800B,
        "COM1",
        123456,
        "ARM",
        "CircuitPython",
        "circuitpython",
        "Adafruit Feather",
    )
    return adafruit_feather


def test_device_selector_device_changed_to_none(qtapp):
    """
    Check that when device changes to index out of range,
    the device selector emits None on the device_changed signal
    """
    device_selector = mu.interface.main.DeviceSelector()
    device_selector.device_changed = mock.MagicMock()
    device_selector._device_changed(-1)
    device_selector.device_changed.emit.assert_called_once_with(None)


def test_device_selector_selected_device_w_no_devices(qtapp):
    """
    Test that device_changed signals are emitted, when the user
    changes device.
    """
    device_selector = mu.interface.main.DeviceSelector()
    device_list = []
    device_selector.selector.model = mock.MagicMock(return_value=device_list)
    device = device_selector.selected_device()
    assert device is None


def test_device_selector_device_changed(qtapp, microbit, adafruit_feather):
    """
    Test that device_changed signals are emitted, when the user
    changes device.
    """
    device_selector = mu.interface.main.DeviceSelector()
    device_selector.device_changed = mock.MagicMock()
    device_list = [microbit, adafruit_feather]
    device_selector.selector.model = mock.MagicMock(return_value=device_list)
    device_selector._device_changed(0)
    device_selector.device_changed.emit.assert_called_once_with(microbit)
    device_selector._device_changed(1)
    device_selector.device_changed.emit.assert_called_with(adafruit_feather)


def test_DeviceSelector_device_connected(qtapp, microbit):
    """
    Test that _update_view is called when a device connects
    """
    device_selector = mu.interface.main.DeviceSelector()
    device_selector._update_view = mock.MagicMock()
    device_selector.device_connected(microbit)
    device_selector._update_view.assert_called_once_with()


def test_DeviceSelector_device_disconnected(qtapp, microbit):
    """
    Test that _update_view is called when a device disconnects
    """
    device_selector = mu.interface.main.DeviceSelector()
    device_selector._update_view = mock.MagicMock()
    device_selector.device_disconnected(microbit)
    device_selector._update_view.assert_called_once_with()


def test_DeviceSelector_update_view_selector_hidden_on_1_device(qtapp):
    """
    Test that _update_view hides the combobox selector when only
    one device connected
    """
    device_selector = mu.interface.main.DeviceSelector()
    model = mock.MagicMock()
    model.data = mock.MagicMock(return_value="Tooltip text")
    device_selector.selector.model = mock.MagicMock(return_value=model)
    device_selector.selector.count = mock.MagicMock(return_value=1)

    device_selector._update_view()
    assert device_selector.selector.isHidden()


def test_DeviceSelector_update_view_selector_shown_on_2_devices(qtapp):
    """
    Test that _update_view displays the combobox selector when two
    devices connected
    """
    device_selector = mu.interface.main.DeviceSelector(show_label=True)
    model = mock.MagicMock()
    model.data = mock.MagicMock(return_value="Tooltip text")
    device_selector.selector.model = mock.MagicMock(return_value=model)
    device_selector.selector.count = mock.MagicMock(return_value=2)

    device_selector._update_view()
    assert not device_selector.selector.isHidden()
    assert device_selector.status_label.isHidden()


def test_DeviceSelector_update_view_check_disconnected_icon(qtapp):
    """
    Test that _update_view displays the disconnected icon when
    no device connected
    """
    device_selector = mu.interface.main.DeviceSelector()
    device_selector.selector.count = mock.MagicMock(return_value=0)
    device_selector.connection_status.setPixmap = mock.MagicMock()

    device_selector._update_view()
    device_selector.connection_status.setPixmap.assert_called_once_with(
        device_selector.disconnected_icon
    )


def test_DeviceSelector_update_view_check_connected_icon(qtapp):
    """
    Test that _update_view displays the connected icon when
    one device connected
    """
    device_selector = mu.interface.main.DeviceSelector()
    model = mock.MagicMock()
    model.data = mock.MagicMock(return_value="Tooltip text")
    device_selector.selector.model = mock.MagicMock(return_value=model)
    device_selector.selector.count = mock.MagicMock(return_value=1)

    device_selector.connection_status.setPixmap = mock.MagicMock()
    device_selector._update_view()
    device_selector.connection_status.setPixmap.assert_called_once_with(
        device_selector.connected_icon
    )
