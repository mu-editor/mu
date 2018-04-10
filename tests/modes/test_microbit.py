# -*- coding: utf-8 -*-
"""
Tests for the micro:bit mode.
"""
import os
import pytest
import os.path
from mu.logic import HOME_DIRECTORY
from mu.modes.microbit import MicrobitMode, FileManager, DeviceFlasher
from mu.modes.api import MICROBIT_APIS, SHARED_APIS
from unittest import mock


TEST_ROOT = os.path.split(os.path.dirname(__file__))[0]


def test_DeviceFlasher_init():
    """
    Ensure the DeviceFlasher thread is set up correctly.
    """
    df = DeviceFlasher(['path', ], 'script', None)
    assert df.paths_to_microbits == ['path', ]
    assert df.python_script == 'script'
    assert df.path_to_runtime is None


def test_DeviceFlasher_run():
    """
    Ensure the uflash.flash function is called as expected.
    """
    df = DeviceFlasher(['path', ], 'script', None)
    mock_flash = mock.MagicMock()
    with mock.patch('mu.modes.microbit.uflash', mock_flash):
        df.run()
    mock_flash.flash.assert_called_once_with(paths_to_microbits=['path', ],
                                             python_script='script',
                                             path_to_runtime=None)


def test_DeviceFlasher_run_fail():
    """
    Ensure the on_flash_fail signal is emitted if an exception is thrown.
    """
    df = DeviceFlasher(['path', ], 'script', None)
    df.on_flash_fail = mock.MagicMock()
    mock_flash = mock.MagicMock()
    mock_flash.flash.side_effect = Exception('Boom')
    with mock.patch('mu.modes.microbit.uflash', mock_flash):
        df.run()
    df.on_flash_fail.emit.assert_called_once_with(str(Exception('Boom')))


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
    The on_list_files signal is emitted with a tuple of files when microfs.ls
    completes successfully.
    """
    fm = FileManager()
    fm.on_list_files = mock.MagicMock()
    mock_ls = mock.MagicMock(return_value=['foo.py', 'bar.py', ])
    with mock.patch('mu.modes.microbit.microfs.ls', mock_ls),\
            mock.patch('mu.modes.microbit.microfs.get_serial'):
        fm.ls()
    fm.on_list_files.emit.assert_called_once_with(('foo.py', 'bar.py'))


def test_FileManager_ls_fail():
    """
    The on_list_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager()
    fm.on_list_fail = mock.MagicMock()
    with mock.patch('mu.modes.microbit.microfs.ls',
                    side_effect=Exception('boom')):
        fm.ls()
    fm.on_list_fail.emit.assert_called_once_with()


def test_fileManager_get():
    """
    The on_get_file signal is emitted with the name of the effected file when
    microfs.get completes successfully.
    """
    fm = FileManager()
    fm.on_get_file = mock.MagicMock()
    mock_get = mock.MagicMock()
    mock_serial = mock.MagicMock()
    with mock.patch('mu.modes.microbit.microfs.get', mock_get),\
            mock.patch('mu.modes.microbit.microfs.get_serial', mock_serial):
        fm.get('foo.py', 'bar.py')
    mock_get.assert_called_once_with('foo.py', 'bar.py',
                                     mock_serial().__enter__())
    fm.on_get_file.emit.assert_called_once_with('foo.py')


def test_FileManager_get_fail():
    """
    The on_get_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager()
    fm.on_get_fail = mock.MagicMock()
    with mock.patch('mu.modes.microbit.microfs.get_serial',
                    side_effect=Exception('boom')):
        fm.get('foo.py', 'bar.py')
    fm.on_get_fail.emit.assert_called_once_with('foo.py')


def test_FileManager_put():
    """
    The on_put_file signal is emitted with the name of the effected file when
    microfs.put completes successfully.
    """
    fm = FileManager()
    fm.on_put_file = mock.MagicMock()
    mock_put = mock.MagicMock()
    mock_serial = mock.MagicMock()
    path = os.path.join('directory', 'foo.py')
    with mock.patch('mu.modes.microbit.microfs.put', mock_put),\
            mock.patch('mu.modes.microbit.microfs.get_serial', mock_serial):
        fm.put(path)
    mock_put.assert_called_once_with(path, mock_serial().__enter__())
    fm.on_put_file.emit.assert_called_once_with('foo.py')


def test_FileManager_put_fail():
    """
    The on_put_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager()
    fm.on_put_fail = mock.MagicMock()
    with mock.patch('mu.modes.microbit.microfs.get_serial',
                    side_effect=Exception('boom')):
        fm.put('foo.py')
    fm.on_put_fail.emit.assert_called_once_with('foo.py')


def test_FileManager_delete():
    """
    The on_delete_file signal is emitted with the name of the effected file
    when microfs.rm completes successfully.
    """
    fm = FileManager()
    fm.on_delete_file = mock.MagicMock()
    mock_rm = mock.MagicMock()
    mock_serial = mock.MagicMock()
    with mock.patch('mu.modes.microbit.microfs.rm', mock_rm),\
            mock.patch('mu.modes.microbit.microfs.get_serial', mock_serial):
        fm.delete('foo.py')
    mock_rm.assert_called_once_with('foo.py', mock_serial().__enter__())
    fm.on_delete_file.emit.assert_called_once_with('foo.py')


def test_FileManager_delete_fail():
    """
    The on_delete_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager()
    fm.on_delete_fail = mock.MagicMock()
    with mock.patch('mu.modes.microbit.microfs.get_serial',
                    side_effect=Exception('boom')):
        fm.delete('foo.py')
    fm.on_delete_fail.emit.assert_called_once_with('foo.py')


def test_microbit_mode():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    assert mm.name == 'BBC micro:bit'
    assert mm.description is not None
    assert mm.icon == 'microbit'
    assert mm.editor == editor
    assert mm.view == view

    actions = mm.actions()
    assert len(actions) == 4
    assert actions[0]['name'] == 'flash'
    assert actions[0]['handler'] == mm.flash
    assert actions[1]['name'] == 'files'
    assert actions[1]['handler'] == mm.toggle_files
    assert actions[2]['name'] == 'repl'
    assert actions[2]['handler'] == mm.toggle_repl
    assert actions[3]['name'] == 'plotter'
    assert actions[3]['handler'] == mm.toggle_plotter


def test_microbit_mode_no_charts():
    """
    If QCharts is not available, ensure plotter is not displayed.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch('mu.modes.microbit.CHARTS', False):
        actions = mm.actions()
        assert len(actions) == 3
        assert actions[0]['name'] == 'flash'
        assert actions[0]['handler'] == mm.flash
        assert actions[1]['name'] == 'files'
        assert actions[1]['handler'] == mm.toggle_files
        assert actions[2]['name'] == 'repl'
        assert actions[2]['handler'] == mm.toggle_repl


def test_custom_hex_read():
    """
    Test that a custom hex file path can be read
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch('mu.modes.microbit.get_settings_path',
                    return_value='tests/settingswithcustomhex.json'), \
            mock.patch('mu.modes.microbit.os.path.exists', return_value=True),\
            mock.patch('mu.modes.base.BaseMode.workspace_dir',
                       return_value=TEST_ROOT):
        assert "customhextest.hex" in mm.get_hex_path()
    """
    Test that a corrupt settings file returns None for the
    runtime hex path
    """
    with mock.patch('mu.modes.microbit.get_settings_path',
                    return_value='tests/settingscorrupt.json'), \
            mock.patch('mu.modes.base.BaseMode.workspace_dir',
                       return_value=TEST_ROOT):
        assert mm.get_hex_path() is None
    """
    Test that a missing settings file returns None for the
    runtime hex path
    """
    with mock.patch('mu.modes.microbit.get_settings_path',
                    return_value='tests/settingswithmissingcustomhex.json'), \
            mock.patch('mu.modes.base.BaseMode.workspace_dir',
                       return_value=TEST_ROOT):
        assert mm.get_hex_path() is None


def test_flash_no_tab():
    """
    If there are no active tabs simply return.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    mm = MicrobitMode(editor, view)
    assert mm.flash() is None

def test_prepare_script():
    """
    Check that prepare_script returns the expected output
    and without showing a message
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    script = ''
    real_mangled = b''
    with open('tests/bigscript.py') as f:
        script = f.read()
    assert len(script) > 0
    with open('tests/bigscript_mangled.py') as f:
        real_mangled = f.read().encode('utf-8')
    assert len(real_mangled) > 0
    mangled = mm.prepare_script(script)
    assert view.show_message.call_count == 0
    assert mangled == real_mangled

def test_prepare_script_with_bad_syntax():
    """
    Check that prepare_script shows a message and returns
    and exception for a badly formatted script
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    script = ''
    with open('tests/bigscript_bad.py') as f:
        script = f.read()
    assert len(script) > 0
    mm = MicrobitMode(editor, view)
    mangled = mm.prepare_script(script)
    assert isinstance(mangled, Exception)
    assert view.show_message.call_count == 1

def test_flash_with_bad_syntax():
    """
    Check that flash calls prepare_script which shows a
    message when working on a badly formatted script
    """
    view = mock.MagicMock()
    script = ''
    with open('tests/bigscript_bad.py') as f:
        script = f.read()
    assert len(script) > 0
    view.current_tab.text = mock.MagicMock(return_value=script)
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.flash()
    assert view.show_message.call_count == 1

def test_flash_with_attached_device_as_windows():
    """
    Ensure the expected calls are made to DeviceFlasher and a helpful status
    message is enacted as if on Windows.
    """
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch('mu.modes.microbit.uflash.find_microbit',
                    return_value='bar'),\
            mock.patch('mu.modes.microbit.os.path.exists', return_value=True),\
            mock.patch('mu.modes.microbit.DeviceFlasher',
                       mock_flasher_class), \
            mock.patch('mu.modes.microbit.sys.platform', 'win32'):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value='foo')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.flash()
        assert mm.flash_thread == mock_flasher
        assert editor.show_status_message.call_count == 1
        view.button_bar.slots['flash'].setEnabled.\
            assert_called_once_with(False)
        mock_flasher_class.assert_called_once_with(['bar', ], b'foo', None)
        mock_flasher.finished.connect.\
            assert_called_once_with(mm.flash_finished)
        mock_flasher.on_flash_fail.connect.\
            assert_called_once_with(mm.flash_failed)
        mock_flasher.start.assert_called_once_with()


def test_flash_with_attached_device_as_not_windows():
    """
    Ensure the expected calls are made to DeviceFlasher and a helpful status
    message is enacted as if not on Windows.
    """
    mock_timer = mock.MagicMock()
    mock_timer_class = mock.MagicMock(return_value=mock_timer)
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch('mu.modes.microbit.uflash.find_microbit',
                    return_value='bar'),\
            mock.patch('mu.modes.microbit.os.path.exists', return_value=True),\
            mock.patch('mu.modes.microbit.DeviceFlasher',
                       mock_flasher_class), \
            mock.patch('mu.modes.microbit.sys.platform', 'linux'), \
            mock.patch('mu.modes.microbit.QTimer', mock_timer_class):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value='foo')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.flash()
        assert mm.flash_timer == mock_timer
        assert editor.show_status_message.call_count == 1
        view.button_bar.slots['flash'].setEnabled.\
            assert_called_once_with(False)
        mock_flasher_class.assert_called_once_with(['bar', ], b'foo', None)
        assert mock_flasher.finished.connect.call_count == 0
        mock_timer.timeout.connect.assert_called_once_with(mm.flash_finished)
        mock_timer.setSingleShot.assert_called_once_with(True)
        mock_timer.start.assert_called_once_with(10000)
        mock_flasher.on_flash_fail.connect.\
            assert_called_once_with(mm.flash_failed)
        mock_flasher.start.assert_called_once_with()


def test_flash_with_attached_device_and_custom_runtime():
    """
    Ensure the custom runtime is passed into the DeviceFlasher thread.
    """
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch('mu.modes.microbit.get_settings_path',
                    return_value='tests/settingswithcustomhex.json'), \
            mock.patch('mu.modes.base.BaseMode.workspace_dir',
                       return_value=TEST_ROOT), \
            mock.patch('mu.modes.microbit.DeviceFlasher',
                       mock_flasher_class), \
            mock.patch('mu.modes.microbit.sys.platform', 'win32'):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value='foo')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.flash()
        assert editor.show_status_message.call_count == 1
        assert os.path.join('tests', 'customhextest.hex') in \
            editor.show_status_message.call_args[0][0]
        assert mock_flasher_class.call_count == 1


def test_flash_user_specified_device_path():
    """
    Ensure that if a micro:bit is not automatically found by uflash then it
    prompts the user to locate the device and, assuming a path was given,
    saves the hex in the expected location.
    """
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch('mu.logic.uflash.find_microbit', return_value=None),\
            mock.patch('mu.logic.os.path.exists', return_value=True),\
            mock.patch('mu.modes.microbit.DeviceFlasher',
                       mock_flasher_class), \
            mock.patch('mu.modes.microbit.sys.platform', 'win32'):
        view = mock.MagicMock()
        view.get_microbit_path = mock.MagicMock(return_value='bar')
        view.current_tab.text = mock.MagicMock(return_value='foo')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.flash()
        home = HOME_DIRECTORY
        view.get_microbit_path.assert_called_once_with(home)
        assert editor.show_status_message.call_count == 1
        assert mm.user_defined_microbit_path == 'bar'
        mock_flasher_class.assert_called_once_with(['bar', ], b'foo', None)


def test_flash_existing_user_specified_device_path():
    """
    Ensure that if a micro:bit is not automatically found by uflash and the
    user has previously specified a path to the device, then the hex is saved
    in the specified location.
    """
    mock_flasher = mock.MagicMock()
    mock_flasher_class = mock.MagicMock(return_value=mock_flasher)
    with mock.patch('mu.logic.uflash.find_microbit', return_value=None),\
            mock.patch('mu.logic.os.path.exists', return_value=True),\
            mock.patch('mu.modes.microbit.DeviceFlasher',
                       mock_flasher_class), \
            mock.patch('mu.modes.microbit.sys.platform', 'win32'):
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value='foo')
        view.get_microbit_path = mock.MagicMock(return_value='bar')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.user_defined_microbit_path = 'baz'
        mm.flash()
        assert view.get_microbit_path.call_count == 0
        assert editor.show_status_message.call_count == 1
        mock_flasher_class.assert_called_once_with(['baz', ], b'foo', None)


def test_flash_path_specified_does_not_exist():
    """
    Ensure that if a micro:bit is not automatically found by uflash and the
    user has previously specified a path to the device, then the hex is saved
    in the specified location.
    """
    with mock.patch('mu.logic.uflash.hexlify', return_value=''), \
            mock.patch('mu.logic.uflash.embed_hex', return_value='foo'), \
            mock.patch('mu.logic.uflash.find_microbit', return_value=None),\
            mock.patch('mu.logic.os.path.exists', return_value=False),\
            mock.patch('mu.logic.os.makedirs', return_value=None), \
            mock.patch('mu.logic.uflash.save_hex', return_value=None) as s:
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value='')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.user_defined_microbit_path = 'baz'
        mm.flash()
        message = 'Could not find an attached BBC micro:bit.'
        information = ("Please ensure you leave enough time for the BBC"
                       " micro:bit to be attached and configured correctly"
                       " by your computer. This may take several seconds."
                       " Alternatively, try removing and re-attaching the"
                       " device or saving your work and restarting Mu if"
                       " the device remains unfound.")
        view.show_message.assert_called_once_with(message, information)
        assert s.call_count == 0
        assert mm.user_defined_microbit_path is None


def test_flash_without_device():
    """
    If no device is found and the user doesn't provide a path then ensure a
    helpful status message is enacted.
    """
    with mock.patch('mu.logic.uflash.hexlify', return_value=''), \
            mock.patch('mu.logic.uflash.embed_hex', return_value='foo'), \
            mock.patch('mu.logic.uflash.find_microbit', return_value=None), \
            mock.patch('mu.logic.uflash.save_hex', return_value=None) as s:
        view = mock.MagicMock()
        view.get_microbit_path = mock.MagicMock(return_value=None)
        view.current_tab.text = mock.MagicMock(return_value='')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.flash()
        message = 'Could not find an attached BBC micro:bit.'
        information = ("Please ensure you leave enough time for the BBC"
                       " micro:bit to be attached and configured correctly"
                       " by your computer. This may take several seconds."
                       " Alternatively, try removing and re-attaching the"
                       " device or saving your work and restarting Mu if"
                       " the device remains unfound.")
        view.show_message.assert_called_once_with(message, information)
        home = HOME_DIRECTORY
        view.get_microbit_path.assert_called_once_with(home)
        assert s.call_count == 0


def test_flash_script_too_big():
    """
    If the script in the current tab is too big, abort in the expected way.
    """
    view = mock.MagicMock()
    view.current_tab.text = mock.MagicMock(return_value='x' * 8193)
    view.current_tab.label = 'foo'
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.flash()
    view.show_message.assert_called_once_with('Unable to flash "foo"',
                                              'Your script is too long!',
                                              'Warning')


def test_flash_finished():
    """
    Ensure state is set back as expected when the flashing thread is finished.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.flash_thread = mock.MagicMock()
    mm.flash_timer = mock.MagicMock()
    mm.flash_finished()
    view.button_bar.slots['flash'].setEnabled.assert_called_once_with(True)
    editor.show_status_message.assert_called_once_with("Finished flashing.")
    assert mm.flash_thread is None
    assert mm.flash_timer is None


def test_flash_failed():
    """
    Ensure things are cleaned up if flashing failed.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mock_timer = mock.MagicMock()
    mm.flash_timer = mock_timer
    mm.flash_thread = mock.MagicMock()
    mm.flash_failed('Boom')
    assert view.show_message.call_count == 1
    view.button_bar.slots['flash'].setEnabled.assert_called_once_with(True)
    assert mm.flash_thread is None
    assert mm.flash_timer is None
    mock_timer.stop.assert_called_once_with()


def test_add_fs():
    """
    It's possible to add the file system pane if the REPL is inactive.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch('mu.modes.microbit.FileManager') as mock_fm,\
            mock.patch('mu.modes.microbit.QThread'),\
            mock.patch('mu.modes.microbit.microfs.get_serial',
                       return_value=True):
        mm.add_fs()
        workspace = mm.workspace_dir()
        view.add_filesystem.assert_called_once_with(workspace, mock_fm())
        assert mm.fs


def test_add_fs_no_device():
    """
    If there's no device attached then ensure a helpful message is displayed.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    ex = IOError('BOOM')
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch('mu.modes.microbit.microfs.get_serial', side_effect=ex):
        mm.add_fs()
    assert view.show_message.call_count == 1


def test_remove_fs_no_fs():
    """
    Removing a non-existent file system raises a RuntimeError.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.fs = None
    with pytest.raises(RuntimeError):
        mm.remove_fs()


def test_remove_fs():
    """
    Removing the file system results in the expected state.
    """
    view = mock.MagicMock()
    view.remove_repl = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.fs = True
    mm.remove_fs()
    assert view.remove_filesystem.call_count == 1
    assert mm.fs is None


def test_toggle_files_on():
    """
    If the fs is off, toggle it on.
    """
    view = mock.MagicMock()
    view.button_bar.slots = {
        'repl': mock.MagicMock(),
        'plotter': mock.MagicMock(),
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
    view.button_bar.slots['repl'].setEnabled.assert_called_once_with(False)
    view.button_bar.slots['plotter'].setEnabled.assert_called_once_with(False)


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

    def side_effect(*args, **kwargs):
        mm.repl = True

    with mock.patch('mu.modes.microbit.MicroPythonMode.toggle_repl',
                    side_effect=side_effect) as tr:
        mm.repl = None
        mm.toggle_repl(None)
        tr.assert_called_once_with(None)
        view.button_bar.slots['files'].\
            setEnabled.assert_called_once_with(False)


def test_toggle_repl_no_repl_or_plotter():
    """
    Ensure the file system button is enabled if the repl toggles off and the
    plotter isn't active.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)

    def side_effect(*args, **kwargs):
        mm.repl = False
        mm.plotter = False

    with mock.patch('mu.modes.microbit.MicroPythonMode.toggle_repl',
                    side_effect=side_effect) as tr:
        mm.repl = None
        mm.toggle_repl(None)
        tr.assert_called_once_with(None)
        view.button_bar.slots['files'].\
            setEnabled.assert_called_once_with(True)


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

    def side_effect(*args, **kwargs):
        mm.plotter = True

    with mock.patch('mu.modes.microbit.MicroPythonMode.toggle_plotter',
                    side_effect=side_effect) as tp:
        mm.plotter = None
        mm.toggle_plotter(None)
        tp.assert_called_once_with(None)
        view.button_bar.slots['files'].\
            setEnabled.assert_called_once_with(False)


def test_toggle_plotter_no_repl_or_plotter():
    """
    Ensure the file system button is enabled if the plotter toggles off and the
    repl isn't active.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)

    def side_effect(*args, **kwargs):
        mm.plotter = False
        mm.repl = False

    with mock.patch('mu.modes.microbit.MicroPythonMode.toggle_plotter',
                    side_effect=side_effect) as tp:
        mm.plotter = None
        mm.toggle_plotter(None)
        tp.assert_called_once_with(None)
        view.button_bar.slots['files'].\
            setEnabled.assert_called_once_with(True)


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
