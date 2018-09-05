# -*- coding: utf-8 -*-
"""
Tests for Pixel Kit mode.
"""
import os
import esptool
from argparse import Namespace
from mu.modes.pixelkit import DeviceFlasher, FileManager
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

def test_FileManager_on_start():
    """
    When a thread signals it has started, list the files.
    """
    fm = FileManager()
    fm.ls = mock.MagicMock()
    fm.on_start()
    fm.ls.assert_called_once_with()


def test_FileManager_ls():
    """
    The on_list_files signal is emitted with a tuple of files when pixelfs.ls
    completes successfully.
    """
    fm = FileManager()
    fm.on_list_files = mock.MagicMock()
    mock_ls = mock.MagicMock(return_value=['foo.py', 'bar.py', ])
    with mock.patch('mu.modes.pixelkit.pixelfs.ls', mock_ls):
        fm.ls()
    fm.on_list_files.emit.assert_called_once_with(('foo.py', 'bar.py'))


def test_FileManager_ls_fail():
    """
    The on_list_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager()
    fm.on_list_fail = mock.MagicMock()
    with mock.patch('mu.modes.pixelkit.pixelfs.ls',
                    side_effect=Exception('boom')):
        fm.ls()
    fm.on_list_fail.emit.assert_called_once_with()


def test_fileManager_get():
    """
    The on_get_file signal is emitted with the name of the effected file when
    pixelfs.get completes successfully.
    """
    fm = FileManager()
    fm.on_get_file = mock.MagicMock()
    mock_get = mock.MagicMock()
    with mock.patch('mu.modes.pixelkit.pixelfs.get', mock_get):
        fm.get('foo.py', 'bar.py')
    mock_get.assert_called_once_with('foo.py', 'bar.py')
    fm.on_get_file.emit.assert_called_once_with('foo.py')


def test_FileManager_get_fail():
    """
    The on_get_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager()
    fm.on_get_fail = mock.MagicMock()
    with mock.patch('mu.modes.pixelkit.pixelfs.get',
                    side_effect=Exception('boom')):
        fm.get('foo.py', 'bar.py')
    fm.on_get_fail.emit.assert_called_once_with('foo.py')


def test_FileManager_put():
    """
    The on_put_file signal is emitted with the name of the effected file when
    pixelfs.put completes successfully.
    """
    fm = FileManager()
    fm.on_put_file = mock.MagicMock()
    mock_put = mock.MagicMock()
    path = os.path.join('directory', 'foo.py')
    with mock.patch('mu.modes.pixelkit.pixelfs.put', mock_put):
        fm.put(path)
    mock_put.assert_called_once_with(path, target=None)
    fm.on_put_file.emit.assert_called_once_with('foo.py')


def test_FileManager_put_fail():
    """
    The on_put_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager()
    fm.on_put_fail = mock.MagicMock()
    with mock.patch('mu.modes.pixelkit.pixelfs.put',
                    side_effect=Exception('boom')):
        fm.put('foo.py')
    fm.on_put_fail.emit.assert_called_once_with('foo.py')


def test_FileManager_delete():
    """
    The on_delete_file signal is emitted with the name of the effected file
    when pixelfs.rm completes successfully.
    """
    fm = FileManager()
    fm.on_delete_file = mock.MagicMock()
    mock_rm = mock.MagicMock()
    with mock.patch('mu.modes.pixelkit.pixelfs.rm', mock_rm):
        fm.delete('foo.py')
    mock_rm.assert_called_once_with('foo.py')
    fm.on_delete_file.emit.assert_called_once_with('foo.py')


def test_FileManager_delete_fail():
    """
    The on_delete_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager()
    fm.on_delete_fail = mock.MagicMock()
    with mock.patch('mu.modes.pixelkit.pixelfs.rm',
                    side_effect=Exception('boom')):
        fm.delete('foo.py')
    fm.on_delete_fail.emit.assert_called_once_with('foo.py')
