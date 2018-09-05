# -*- coding: utf-8 -*-
"""
Tests for Pixel Kit mode.
"""
import esptool
from argparse import Namespace
from mu.modes.pixelkit import DeviceFlasher
from unittest import mock


TEST_ROOT = os.path.split(os.path.dirname(__file__))[0]

def test_DeviceFlasher_init():
    """
    Ensure the DeviceFlasher thread is set up correctly.
    """
    port = 'COM_PORT'
    firmware_type = 'micropython'
    df = DeviceFlasher(port, firmware_type)
    assert df.port == port
    assert df.firmware_type == firmware_type

def test_DeviceFlasher_init_defaults():
    """
    Ensure the DeviceFlasher defaults firmware_type to 'micropython'
    """
    port = 'COM_PORT'
    df = DeviceFlasher(port)
    assert df.firmware_type == 'micropython'

def test_DeviceFlasher_run():
    """
    Ensure DeviceFlasher will call the correct method to flash based on
    firmware_type
    """
    port = 'COM_PORT'
    with mock.patch.object(DeviceFlasher, 'flash_micropython'), \
        mock.patch.object(DeviceFlasher, 'flash_kanocode'):
        df_mp = DeviceFlasher(port, 'micropython')
        df_mp.run()
        df_mp.flash_micropython.assert_called_once()
        df_kc = DeviceFlasher(port, 'kanocode')
        df_kc.run()
        df_mp.flash_kanocode.assert_called_once()

def test_DeviceFlasher_run_fail():
    """
    Ensure the on_flash_fail signal is emitted if an exception is thrown when
    trying to run with an invalid firmware_type.
    """
    port = 'COM_PORT'
    df_unknown = DeviceFlasher(port, 'unknown_firmware_type')
    df_unknown.on_flash_fail = mock.MagicMock()
    df_unknown.run()
    df_unknown.on_flash_fail.emit.assert_called_once_with('Unknown firmware type: unknown_firmware_type')

def test_DeviceFlasher_get_addr_filename():
    # TODO
    pass

def test_DeviceFlasher_write_flash():
    """
    Ensure erase_flash will call esptool functions correctly
    """
    port = 'COM_PORT'
    addr_filename = [[int('0x1000', 0), '/tmp/filename']]
    args = Namespace()
    args.flash_freq = "40m"
    args.flash_mode = "dio"
    args.flash_size = "detect"
    args.no_progress = False
    args.compress = False
    args.no_stub = False
    args.trace = False
    args.verify = False
    args.addr_filename = addr_filename
    mock_esptool = mock.MagicMock()
    mock_ESP32ROM = mock.MagicMock()
    mock_stub = mock.MagicMock()
    mock_esp = mock_ESP32ROM()
    mock_esptool.ESPLoader.detect_chip.return_value = mock_esp
    mock_esp.run_stub.return_value = mock_stub
    df = DeviceFlasher(port)
    with mock.patch('mu.modes.pixelkit.esptool', mock_esptool):
        df.write_flash(addr_filename)
        mock_esptool.ESPLoader.detect_chip.assert_called_once_with(port, 115200, False)
        mock_esp.run_stub.assert_called_once()
        mock_stub.change_baud.assert_called_once_with(921600)
        mock_esptool.detect_flash_size.assert_called_once_with(mock_stub, args)
        mock_esptool.flash_size_bytes.assert_called_once_with(args.flash_size)
        flash_size_bytes = mock_esptool.flash_size_bytes(args.flash_size)
        mock_stub.flash_set_parameters.assert_called_once_with(flash_size_bytes)
        mock_esptool.erase_flash.assert_called_once_with(mock_stub, args)
        mock_esptool.write_flash.assert_called_once_with(mock_stub, args)
        mock_stub.hard_reset.assert_called_once()

def test_DeviceFlasher_write_flash_fail():
    """
    Ensure the on_flash_fail signal is emitted if an exception is thrown when
    something goes wrong on write_flash function
    """
    port = 'COM_PORT'
    addr_filename = [[int('0x1000', 0), '/tmp/filename']]
    mock_esptool = mock.MagicMock()
    mock_esptool.ESPLoader.detect_chip.side_effect = Exception('Problem')
    df = DeviceFlasher(port)
    df.on_flash_fail = mock.MagicMock()
    with mock.patch('mu.modes.pixelkit.esptool', mock_esptool):
        df.write_flash(addr_filename)
        df.on_flash_fail.emit.assert_called_once_with("Could not write to flash memory")

def test_DeviceFlasher_download_micropython():
    """
    Ensure download_micropython returns a filename
    """
    port = 'COM_PORT'
    df = DeviceFlasher(port)
    mock_request = mock.MagicMock()
    with mock.patch('mu.modes.pixelkit.urllib.request', mock_request):
        fname = df.download_micropython()
        assert fname

def test_DeviceFlasher_download_micropython_fail():
    """
    Ensure download_micropython returns a filename
    """
    port = 'COM_PORT'
    df = DeviceFlasher(port)
    df.on_flash_fail = mock.MagicMock()
    mock_request = mock.MagicMock()
    mock_request.urlretrieve.side_effect = Exception('Problem')
    with mock.patch('mu.modes.pixelkit.urllib.request', mock_request):
        fname = df.download_micropython()
        assert fname == None
        df.on_flash_fail.emit.assert_called_once_with('Could not download MicroPython firmware')

def test_DeviceFlasher_flash_micropython():
    """
    Ensure flash_micropython function will call download_micropython,
    get_addr_filename and write_flash correctly
    """
    port = 'COM_PORT'
    filename = 'micropython.bin'
    addr_filename = [[int('0x1000', 0), '/tmp/filename']]
    df = DeviceFlasher(port, 'micropython')
    with mock.patch.object(df, 'get_addr_filename', return_value=addr_filename), \
        mock.patch.object(df, 'download_micropython', return_value=filename), \
        mock.patch.object(df, 'write_flash'):
        df.flash_micropython()
        df.download_micropython.assert_called_once()
        df.get_addr_filename.assert_called_once_with(["0x1000", filename])
        df.write_flash.assert_called_once_with(addr_filename)
