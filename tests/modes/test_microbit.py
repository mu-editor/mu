# -*- coding: utf-8 -*-
"""
Tests for the micro:bit mode.
"""
import os
import pytest
from mu.logic import HOME_DIRECTORY
from mu.modes.microbit import MicrobitMode
from unittest import mock


TEST_ROOT = os.path.split(os.path.dirname(__file__))[0]


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


def test_flash_with_attached_device():
    """
    Ensure the expected calls are made to uFlash and a helpful status message
    is enacted.
    """
    with mock.patch('mu.modes.microbit.uflash.hexlify', return_value=''), \
            mock.patch('mu.modes.microbit.uflash.embed_hex',
                       return_value='foo'), \
            mock.patch('mu.modes.microbit.uflash.find_microbit',
                       return_value='bar'),\
            mock.patch('mu.modes.microbit.os.path.exists', return_value=True),\
            mock.patch('mu.modes.microbit.uflash.save_hex',
                       return_value=None) as s:
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value='')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.flash()
        assert view.show_message.call_count == 1
        hex_file_path = os.path.join('bar', 'micropython.hex')
        s.assert_called_once_with('foo', hex_file_path)


def test_flash_with_attached_device_and_custom_runtime():
    """
    Ensure the expected calls are made to uFlash and a helpful status message
    is enacted.
    """
    with mock.patch('mu.modes.microbit.get_settings_path',
                    return_value='tests/settingswithcustomhex.json'), \
            mock.patch('mu.modes.base.BaseMode.workspace_dir',
                       return_value=TEST_ROOT), \
            mock.patch('mu.modes.microbit.uflash.flash') as fl:
        view = mock.MagicMock()
        view.current_tab.text = mock.MagicMock(return_value='')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.flash()
        assert view.show_message.call_count == 1
        assert 'tests/customhextest.hex' in view.show_message.call_args[0][0]
        assert fl.call_count == 1


def test_flash_user_specified_device_path():
    """
    Ensure that if a micro:bit is not automatically found by uflash then it
    prompts the user to locate the device and, assuming a path was given,
    saves the hex in the expected location.
    """
    with mock.patch('mu.logic.uflash.hexlify', return_value=''), \
            mock.patch('mu.logic.uflash.embed_hex', return_value='foo'), \
            mock.patch('mu.logic.uflash.find_microbit', return_value=None),\
            mock.patch('mu.logic.os.path.exists', return_value=True),\
            mock.patch('mu.logic.uflash.save_hex', return_value=None) as s:
        view = mock.MagicMock()
        view.get_microbit_path = mock.MagicMock(return_value='bar')
        view.current_tab.text = mock.MagicMock(return_value='')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.flash()
        home = HOME_DIRECTORY
        view.get_microbit_path.assert_called_once_with(home)
        assert view.show_message.call_count == 1
        assert mm.user_defined_microbit_path == 'bar'
        hex_file_path = os.path.join('bar', 'micropython.hex')
        s.assert_called_once_with('foo', hex_file_path)


def test_flash_existing_user_specified_device_path():
    """
    Ensure that if a micro:bit is not automatically found by uflash and the
    user has previously specified a path to the device, then the hex is saved
    in the specified location.
    """
    with mock.patch('mu.logic.uflash.hexlify', return_value=''), \
            mock.patch('mu.logic.uflash.embed_hex', return_value='foo'), \
            mock.patch('mu.logic.uflash.find_microbit', return_value=None),\
            mock.patch('mu.logic.os.path.exists', return_value=True),\
            mock.patch('mu.logic.uflash.save_hex', return_value=None) as s:
        view = mock.MagicMock()
        view.get_microbit_path = mock.MagicMock(return_value='bar')
        view.current_tab.text = mock.MagicMock(return_value='')
        view.show_message = mock.MagicMock()
        editor = mock.MagicMock()
        mm = MicrobitMode(editor, view)
        mm.user_defined_microbit_path = 'baz'
        mm.flash()
        assert view.get_microbit_path.call_count == 0
        assert view.show_message.call_count == 1
        hex_file_path = os.path.join('baz', 'micropython.hex')
        s.assert_called_once_with('foo', hex_file_path)


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


def test_add_fs_no_repl():
    """
    It's possible to add the file system pane if the REPL is inactive.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch('mu.modes.microbit.microfs.get_serial', return_value=True):
        mm.add_fs()
    workspace = mm.workspace_dir()
    view.add_filesystem.assert_called_once_with(home=workspace)
    assert mm.fs


def test_add_fs_with_repl():
    """
    If the REPL is active, you can't add the file system pane.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.repl = True
    with mock.patch('mu.modes.microbit.microfs.get_serial', return_value=True):
        mm.add_fs()
    assert view.add_filesystem.call_count == 0


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
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    mm.add_fs = mock.MagicMock()
    mm.repl = None
    mm.fs = None
    mm.toggle_files(None)
    assert mm.add_fs.call_count == 1


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


def test_toggle_repl():
    """
    If the file system is active, show a helpful message instead.
    """
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    with mock.patch('mu.modes.microbit.MicroPythonMode.toggle_repl') as tr:
        mm.repl = None
        mm.toggle_repl(None)
        tr.assert_called_once_with(None)


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


def test_api():
    """
    Ensure the right thing comes back from the API.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    api = mm.api()
    assert isinstance(api, list)
    assert api
