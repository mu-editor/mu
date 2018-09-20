# -*- coding: utf-8 -*-
"""
Tests for Pixel Kit mode.
"""
import os
from argparse import Namespace
from mu.modes.pixelkit import DeviceFlasher, FileManager, PixelKitMode
from mu.modes.api import SHARED_APIS
from unittest import mock
from PyQt5.QtWidgets import QMessageBox


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
    df_unknown.on_flash_fail.emit.assert_called_once_with(
        'Unknown firmware type: unknown_firmware_type'
    )


def test_DeviceFlasher_get_addr_filename():
    """
    Get a list of tuples from get_addr_filename containing the address and
    file object
    """
    port = 'COM_PORT'
    mock_open = mock.mock_open()
    df = DeviceFlasher(port)
    addr_filename = [('0x1000', '/tmp/filename')]
    with mock.patch('mu.modes.pixelkit.open', mock_open, create=True):
        result = df.get_addr_filename(addr_filename)
        assert isinstance(result, list)
        assert len(result) == len(addr_filename)
        assert isinstance(result, list)
        assert isinstance(result[0], tuple)
        assert result[0][0] == int(addr_filename[0][0], 0)
        assert isinstance(result[0][1], mock.MagicMock)


def test_DeviceFlasher_get_addr_filename_fail():
    """
    nsure the on_flash_fail signal is emitted if an exception is thrown when
    something goes wrong on get_addr_filename function
    """
    port = 'COM_PORT'
    mock_open = mock.mock_open()
    arg_string = '/tmp/filename'
    arg_tuple = ('0x1000', '/tmp/filename')
    arg_list_string = ['0x1000', '/tmp/filename']
    with mock.patch('mu.modes.pixelkit.open', mock_open, create=True):
        df = DeviceFlasher(port)
        df.on_flash_fail = mock.MagicMock()
        df.get_addr_filename(arg_string)
        df.on_flash_fail.emit.assert_called_once_with(
            'Values must be a list'
        )
        df.on_flash_fail = mock.MagicMock()
        df.get_addr_filename(arg_tuple)
        df.on_flash_fail.emit.assert_called_once_with(
            'Values must be a list'
        )
        df.on_flash_fail = mock.MagicMock()
        df.get_addr_filename(arg_list_string)
        df.on_flash_fail.emit.assert_called_once_with(
            'Values items must be tuples'
        )


def test_DeviceFlasher_write_flash():
    """
    Ensure erase_flash will call esptool functions correctly
    """
    port = 'COM_PORT'
    addr_filename = [(int('0x1000', 0), '/tmp/filename')]
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
        mock_esptool.ESPLoader.detect_chip.assert_called_once_with(
            port, 115200, False
        )
        mock_esp.run_stub.assert_called_once()
        mock_stub.change_baud.assert_called_once_with(921600)
        mock_esptool.detect_flash_size.assert_called_once_with(mock_stub, args)
        mock_esptool.flash_size_bytes.assert_called_once_with(args.flash_size)
        size_bytes = mock_esptool.flash_size_bytes(args.flash_size)
        mock_stub.flash_set_parameters.assert_called_once_with(size_bytes)
        mock_esptool.erase_flash.assert_called_once_with(mock_stub, args)
        mock_esptool.write_flash.assert_called_once_with(mock_stub, args)
        mock_stub.hard_reset.assert_called_once()


def test_DeviceFlasher_write_flash_fail():
    """
    Ensure the on_flash_fail signal is emitted if an exception is thrown when
    something goes wrong on write_flash function
    """
    port = 'COM_PORT'
    addr_filename = [(int('0x1000', 0), '/tmp/filename')]
    mock_esptool = mock.MagicMock()
    mock_esptool.ESPLoader.detect_chip.side_effect = Exception('Problem')
    df = DeviceFlasher(port)
    df.on_flash_fail = mock.MagicMock()
    with mock.patch('mu.modes.pixelkit.esptool', mock_esptool):
        df.write_flash(addr_filename)
        df.on_flash_fail.emit.assert_called_once_with(
            "Could not write to flash memory"
        )


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
        assert fname is None
        df.on_flash_fail.emit.assert_called_once_with(
            'Could not download MicroPython firmware'
        )


def test_DeviceFlasher_flash_micropython():
    """
    Ensure flash_micropython function will call download_micropython,
    get_addr_filename and write_flash correctly
    """
    port = 'COM_PORT'
    f = 'micropython.bin'
    addr = [[int('0x1000', 0), '/tmp/filename']]
    df = DeviceFlasher(port, 'micropython')
    with mock.patch.object(df, 'get_addr_filename', return_value=addr), \
            mock.patch.object(df, 'download_micropython', return_value=f), \
            mock.patch.object(df, 'write_flash'):
        df.flash_micropython()
        df.download_micropython.assert_called_once()
        df.get_addr_filename.assert_called_once_with([("0x1000", f)])
        df.write_flash.assert_called_once_with(addr)


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


def test_pixelkit_mode():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    assert pm.name == 'Kano Pixel Kit'
    assert pm.description is not 'Write MicroPython on the Kano Pixel Kit.'
    assert pm.icon == 'pixelkit'
    assert pm.editor == editor
    assert pm.view == view

    actions = pm.actions()
    assert len(actions) == 5
    assert actions[0]['name'] == 'run'
    assert actions[0]['handler'] == pm.run
    assert actions[1]['name'] == 'stop'
    assert actions[1]['handler'] == pm.stop
    assert actions[2]['name'] == 'mpfiles'
    assert actions[2]['handler'] == pm.toggle_files
    assert actions[3]['name'] == 'repl'
    assert actions[3]['handler'] == pm.toggle_repl
    assert actions[4]['name'] == 'mpflash'
    assert actions[4]['handler'] == pm.flash


def test_pixelkit_api():
    view = mock.MagicMock()
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    api = pm.api()
    assert api == SHARED_APIS


def test_pixel_kit_run():
    code = 'print("hello world")'
    serial = mock.MagicMock()
    view = mock.MagicMock()
    view.serial = serial
    view.current_tab.text.return_value = code
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch.object(pm, 'find_device', return_value=(True, True)), \
            mock.patch.object(pm, 'toggle_repl'), \
            mock.patch.object(pm, 'enter_raw_repl'), \
            mock.patch.object(pm, 'exit_raw_repl'):
        pm.run()
        pm.toggle_repl.assert_called_once()
        pm.enter_raw_repl.assert_called_once()
        serial.write.assert_called_once_with(bytes(code, 'ascii'))
        pm.exit_raw_repl.assert_called_once()


def test_pixel_kit_run_without_device():
    view = mock.MagicMock()
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch.object(pm, 'find_device', return_value=(None, None)):
        pm.run()
        message = _('Could not find an attached Pixel Kit.')
        information = _("Please make sure the device is plugged "
                        "into this computer and turned on.\n\n"
                        "If it's already on, try reseting it and waiting "
                        "a few seconds before trying again.")
        view.show_message.assert_called_once_with(message, information)


def test_pixel_kit_run_opened_repl():
    code = 'print("hello world")'
    serial = mock.MagicMock()
    view = mock.MagicMock()
    view.serial = serial
    view.current_tab.text.return_value = code
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch.object(pm, 'repl', new=True), \
            mock.patch.object(pm, 'toggle_repl'), \
            mock.patch.object(pm, 'enter_raw_repl'), \
            mock.patch.object(pm, 'exit_raw_repl'):
        pm.run()
        pm.toggle_repl.assert_not_called()


def test_pixel_kit_enter_raw_repl():
    view = mock.MagicMock()
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    pm.enter_raw_repl()
    view.serial.write.assert_called_once_with(b'\x01')


def test_pixel_kit_exit_raw_repl():
    view = mock.MagicMock()
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    pm.exit_raw_repl()
    view.serial.write.assert_has_calls([
        mock.call(b'\x04'), mock.call(b'\x02')]
    )


def test_pixel_kit_stop():
    view = mock.MagicMock()
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch.object(pm, 'find_device', return_value=(True, True)), \
            mock.patch.object(pm, 'toggle_repl'):
        pm.stop()
        pm.toggle_repl.assert_called_once()
        view.serial.write.assert_called_once_with(b'\x03')


def test_pixel_kit_stop_opened_repl():
    view = mock.MagicMock()
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch.object(pm, 'find_device', return_value=(True, True)), \
            mock.patch.object(pm, 'repl', new=True), \
            mock.patch.object(pm, 'toggle_repl'):
        pm.stop()
        pm.toggle_repl.assert_not_called()


def test_pixel_kit_stop_without_device():
    view = mock.MagicMock()
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch.object(pm, 'find_device', return_value=(None, None)), \
            mock.patch.object(pm, 'toggle_repl'):
        pm.stop()
        message = _('Could not find an attached Pixel Kit.')
        information = _("Please make sure the device is plugged "
                        "into this computer and turned on.\n\n"
                        "If it's already on, try reseting it and waiting "
                        "a few seconds before trying again.")
        view.show_message.assert_called_once_with(message, information)


def test_flash_no_tab():
    """
    If there are no active tabs simply return.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    mp = PixelKitMode(editor, view)
    assert mp.flash() is None


def test_flash_without_device():
    """
    If no device is found and the user doesn't provide a path then ensure a
    helpful status message is enacted.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch.object(pm, 'find_device', return_value=(None, None)):
        pm.flash()
        message = _('Could not find an attached Pixel Kit.')
        information = _("Please make sure the device is plugged "
                        "into this computer and turned on.\n\n"
                        "If it's already on, try reseting it and waiting "
                        "a few seconds before trying again.")
        view.show_message.assert_called_once_with(message, information)


def test_flash_prompt():
    """
    When pressing the button to flash, a prompt will ask if you really want to
    flash your Pixel Kit with MicroPython. It shouldn't do anything if user
    clicks on cancel
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch('mu.modes.pixelkit.DeviceFlasher'), \
            mock.patch.object(pm, 'find_device', return_value=(True, True)), \
            mock.patch.object(pm, 'set_buttons'), \
            mock.patch.object(pm, 'flash_thread'):
        pm.flash()
        message = _("Flash your Pixel Kit with MicroPython.")
        information = _("Make sure you have internet connection and don't "
                        "disconnect your device during the process. It "
                        "might take a minute or two but you will only need"
                        "to do it once.")
        view.show_confirmation.assert_called_once_with(message, information)


def test_flash_prompt_cancel():
    """
    When pressing the button to flash, a prompt will ask if you really want to
    flash your Pixel Kit with MicroPython. It shouldn't do anything if user
    clicks on cancel
    """
    view = mock.MagicMock()
    view.show_confirmation.return_value = QMessageBox.Cancel
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch('mu.modes.pixelkit.DeviceFlasher'), \
            mock.patch.object(pm, 'find_device', return_value=(True, True)), \
            mock.patch.object(pm, 'set_buttons'), \
            mock.patch.object(pm, 'flash_thread'):
        pm.flash()
        pm.set_buttons.assert_not_called()
        pm.flash_thread.finished.connect.assert_not_called()
        pm.flash_thread.on_flash_fail.connect.assert_not_called()
        pm.flash_thread.on_data.connect.assert_not_called()
        pm.flash_thread.start.assert_not_called()


def test_flash_prompt_ok():
    """
    When pressing the button to flash, a prompt will ask if you really want to
    flash your Pixel Kit with MicroPython. It should start flash thread if user
    clicks on ok
    """
    view = mock.MagicMock()
    view.show_confirmation.return_value = QMessageBox.Ok
    editor = mock.MagicMock()
    pm = PixelKitMode(editor, view)
    with mock.patch('mu.modes.pixelkit.DeviceFlasher'), \
            mock.patch.object(pm, 'find_device', return_value=(True, True)), \
            mock.patch.object(pm, 'set_buttons'), \
            mock.patch.object(pm, 'flash_thread'):
        pm.flash()
        pm.set_buttons.assert_called_once_with(
            mpflash=False, mpfiles=False, run=False, stop=False, repl=False
        )
        pm.flash_thread.finished.connect.assert_called_once()
        pm.flash_thread.on_flash_fail.connect.assert_called_once()
        pm.flash_thread.on_data.connect.assert_called_once()
        pm.flash_thread.start.assert_called_once()


def test_pixel_flash_thread_finished():
    # TODO:
    pass


def test_pixel_flash_thread_fail():
    # TODO:
    pass


def test_pixel_flash_thread_on_data():
    # TODO:
    pass


def test_pixel_flash_finished():
    # TODO:
    pass


def test_pixel_flash_failed():
    # TODO:
    pass


def test_pixel_on_flash_data():
    # TODO:
    pass


def test_pixel_on_toggle_repl():
    # TODO:
    pass


def test_pixel_on_toggle_repl_fail():
    # TODO:
    pass


def test_pixel_on_toggle_files():
    # TODO:
    pass


def test_pixel_on_toggle_files_fail():
    # TODO:
    pass


def test_pixel_add_fs():
    # TODO:
    pass


def test_pixel_add_fs_fail():
    # TODO:
    pass


def test_pixel_remove_fs():
    # TODO:
    pass


def test_pixel_remove_fs_fail():
    # TODO:
    pass


def test_pixel_data_flood():
    # TODO:
    pass
