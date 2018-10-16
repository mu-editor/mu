# -*- coding: utf-8 -*-
import pytest
from unittest import mock
from mu.modes.esp import DeviceFlasher, FileManager, ESPMode, PyboardError
from mu.modes.api import ESP_APIS, SHARED_APIS


@pytest.fixture
def device_flasher():
    pyboard = mock.Mock()
    df = DeviceFlasher(pyboard, 'thepath', 'thescript')
    df.on_flash_fail = mock.Mock()
    return df


@pytest.fixture
def file_manager():
    pyboard = mock.Mock()
    files = mock.Mock()
    fm = FileManager(pyboard, files)
    fm.on_list_files = mock.Mock()
    fm.on_get_file = mock.Mock()
    fm.on_put_file = mock.Mock()
    fm.on_delete_file = mock.Mock()
    fm.on_list_fail = mock.Mock()
    fm.on_get_fail = mock.Mock()
    fm.on_put_fail = mock.Mock()
    fm.on_delete_fail = mock.Mock()
    return fm


@pytest.fixture
def esp_mode():
    editor = mock.MagicMock()
    view = mock.MagicMock()
    esp_mode = ESPMode(editor, view)
    return esp_mode


# Test DeviceFlasher
def test_DeviceFlasher_init():
    """
    Ensure the DeviceFlasher thread is set up correctly.
    """
    pyboard = mock.Mock()
    df = DeviceFlasher(pyboard, 'thepath', 'thescript')
    assert df.pyboard is pyboard
    assert df.filename == 'thepath'
    assert df.python_script == 'thescript'


@mock.patch("mu.contrib.files.Files")
def test_DeviceFlasher_run(files, device_flasher):
    """
    Ensure the Files.put function is called as expected.
    """
    files_instance = files.return_value
    device_flasher.run()
    files_instance.put.assert_called_once_with('thepath', 'thescript')


@mock.patch("mu.contrib.files.Files")
def test_DeviceFlasher_run_fail(files, device_flasher):
    """
    Ensure the on_flash_fail signal is emitted if an exception is thrown.
    """
    ex = Exception('Boom')
    files_instance = files.return_value
    files_instance.put.side_effect = ex
    device_flasher.run()
    device_flasher.on_flash_fail.emit.assert_called_once_with(str(ex))


# Test FileManager
def test_FileManager_init(file_manager):
    """
    Ensure the FileManager is setup up correctly.
    """
    pyboard = mock.Mock()
    files = mock.Mock()
    fm = FileManager(pyboard, files)
    assert fm.pyboard is pyboard
    assert fm.fs is files


def test_FileManager_on_start(file_manager):
    """
    When a thread signals it has started, list the files.
    """
    file_manager.ls = mock.MagicMock()
    file_manager.on_start()
    file_manager.ls.assert_called_once_with()


def test_FileManager_ls(file_manager):
    """
    Ensure the on_list_files signal is emitted, when successfully
    obtaining a file list.
    """
    fs = file_manager.fs
    fs.ls = mock.MagicMock(return_value=["file1.py", "file2.txt"])
    file_manager.ls()
    fs.ls.assert_called_once_with(long_format=False)
    file_manager.on_list_files.emit.assert_called_once_with(("file1.py",
                                                             "file2.txt"))


def test_FileManager_ls_fail(file_manager):
    """
    Ensure the on_list_fail signal is emitted, when an error
    occurs during file listing.
    """
    ex = Exception('Boom')
    fs = file_manager.fs
    fs.ls = mock.MagicMock()
    fs.ls.side_effect = ex
    file_manager.ls()
    fs.ls.assert_called_once_with(long_format=False)
    file_manager.on_list_fail.emit.assert_called_once_with(str(ex))


def test_FileManger_get(file_manager):
    """
    Ensure the on_get_file signal is emitted when successfully retrieved
    a file from the device.
    """
    fs = file_manager.fs
    m = mock.mock_open()
    with mock.patch("builtins.open", m):
        file_manager.get("device_filename.py", "local_filename.py")
    fs.get.assert_called_once_with("device_filename.py")
    m.assert_called_once_with("local_filename.py", "wb")
    file_manager.on_get_file.emit.assert_called_once_with("device_filename.py")


def test_FileManger_get_fail(file_manager):
    """
    Ensure the on_get_fail signal is emitted when an error occurs during
    file retrieval from the device.
    """
    fs = file_manager.fs
    m = mock.mock_open()
    with mock.patch("builtins.open", m):
        m.side_effect = Exception("Boom")
        file_manager.get("device_filename.py", "local_filename.py")
    fs.get.assert_called_once_with("device_filename.py")
    m.assert_called_once_with("local_filename.py", "wb")
    file_manager.on_get_fail.emit.assert_called_once_with("device_filename.py")


@mock.patch("os.path.isfile")
def test_FileManager_put(mock_isfile, file_manager):
    """
    Ensure the on_put_file signal is emitted, when a file has successfully
    been transferred to the device.
    """
    mock_isfile.return_value = True
    m = mock.mock_open(read_data="file contents")
    with mock.patch("builtins.open", m):
        file_manager.put("path/to/file.py")
    m.assert_called_once_with("path/to/file.py", "rb")
    file_manager.fs.put.assert_called_once_with("file.py", "file contents")
    file_manager.on_put_file.emit.assert_called_once_with("file.py")


@mock.patch("os.path.isfile")
def test_FileManager_put_doesnt_exist(mock_isfile, file_manager):
    """
    Ensure on_put_fail signal is emitted when an the file to transfer is not
    found on the local system.
    """
    mock_isfile.return_value = False
    m = mock.mock_open(read_data="file contents")
    with mock.patch("builtins.open", m):
        file_manager.put("path/to/file.py")
    m.assert_not_called()
    file_manager.fs.put.assert_not_called()
    file_manager.on_put_file.emit.assert_not_called()
    file_manager.on_put_fail.emit.assert_called_once_with("path/to/file.py")


@mock.patch("os.path.isfile")
def test_FileManager_put_fail(mock_isfile, file_manager):
    """
    Ensure on_put_fail signal is emitted when an error occurs during
    file transfer to the device.
    """
    fs = file_manager.fs
    mock_isfile.return_value = True
    m = mock.mock_open(read_data="file contents")
    fs.put = mock.MagicMock()
    fs.put.side_effect = Exception("Boom")
    with mock.patch("builtins.open", m):
        file_manager.put("path/to/file.py")
    m.assert_called_once_with("path/to/file.py", "rb")
    fs.put.assert_called_once_with("file.py", "file contents")
    file_manager.on_put_fail.emit.assert_called_once_with("path/to/file.py")


def test_FileManager_delete(file_manager):
    """
    Ensure the signal on_delete_file is emitted when a file has
    successfully been removed from the device.
    """
    fs = file_manager.fs
    fs.rm = mock.MagicMock()
    file_manager.delete("filename.py")
    fs.rm.assert_called_once_with("filename.py")
    file_manager.on_delete_file.emit.assert_called_once_with("filename.py")


def test_FileManager_delete_fail(file_manager):
    """
    Ensure the signal on_delete_fail is emitted when an error occurs
    during deletion of a device-file.
    """
    fs = file_manager.fs
    fs.rm = mock.MagicMock()
    fs.rm.side_effect = Exception('Boom')
    file_manager.delete("filename.py")
    fs.rm.assert_called_once_with("filename.py")
    file_manager.on_delete_fail.emit.assert_called_once_with("filename.py")


# Test ESPMode
def test_ESPMode_init():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    esp_mode = ESPMode(editor, view)
    assert esp_mode.name == 'ESP8266/ESP32 MicroPython'
    assert esp_mode.description is not None
    assert esp_mode.icon == 'esp8266'


def test_ESPMode_actions(esp_mode):
    """
    Sanity check for mode actions.
    """
    actions = esp_mode.actions()
    assert len(actions) == 3
    assert actions[0]['name'] == 'flash'
    assert actions[0]['handler'] == esp_mode.flash
    assert actions[1]['name'] == 'files'
    assert actions[1]['handler'] == esp_mode.toggle_files
    assert actions[2]['name'] == 'repl'
    assert actions[2]['handler'] == esp_mode.toggle_repl


def test_api(esp_mode):
    """
    Ensure the right thing comes back from the API.
    """
    api = esp_mode.api()
    assert api == SHARED_APIS + ESP_APIS


@mock.patch("mu.modes.esp.Pyboard")
@mock.patch("mu.modes.esp.QThread")
@mock.patch("mu.modes.esp.FileManager")
def test_add_fs(fm, qthread, pyboard, esp_mode):
    """
    It's possible to add the file system pane if the REPL is inactive.
    """
    esp_mode.find_device = mock.MagicMock(return_value=('COM0', '12345'))
    esp_mode.add_fs()
    pyboard.assert_called_once_with("COM0", rawdelay=2)
    workspace = esp_mode.workspace_dir()
    esp_mode.view.add_filesystem.assert_called_once_with(workspace,
                                                         esp_mode.file_manager)
    assert esp_mode.fs


def test_add_fs_no_device(esp_mode):
    """
    If there's no device attached then ensure a helpful message is displayed.
    """
    esp_mode.find_device = mock.MagicMock(return_value=(None, None))
    esp_mode.add_fs()
    esp_mode.view.show_message.assert_called_once()


@mock.patch("mu.modes.esp.Pyboard")
@mock.patch("mu.modes.esp.QThread")
@mock.patch("mu.modes.esp.FileManager")
def test_add_fs_pyboard_error(fm, qthread, pyboard, esp_mode):
    """
    If a PyboardError is raised, an error message should be displayed."
    """
    pyboard.side_effect = PyboardError("Error")
    esp_mode.find_device = mock.MagicMock(return_value=('COM0', '12345'))
    esp_mode.add_fs()
    esp_mode.view.show_message.assert_called_once()


def test_remove_fs(esp_mode):
    """
    Removing the file system results in the expected state.
    """
    esp_mode.fs = True
    esp_mode.remove_fs()
    esp_mode.view.remove_filesystem.assert_called_once()
    assert esp_mode.fs is None


@mock.patch("mu.contrib.files.Files")
def test_toggle_repl_on(files, esp_mode):
    """
    Ensure the REPL is able to toggle on if there's no file system pane.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.fs = None
    esp_mode.repl = None
    event = mock.Mock()

    def side_effect(*args, **kwargs):
        esp_mode.repl = True

    with mock.patch('mu.modes.esp.MicroPythonMode.toggle_repl',
                    side_effect=side_effect) as super_toggle_repl:
        esp_mode.toggle_repl(event)
    super_toggle_repl.assert_called_once_with(event)
    esp_mode.set_buttons.assert_called_once_with(flash=False, files=False)
    files._lock.acquire.assert_called_once()
    assert esp_mode.repl


@mock.patch("mu.contrib.files.Files")
@mock.patch('mu.modes.esp.MicroPythonMode.toggle_repl')
def test_toggle_repl_fail(super_toggle_repl, files, esp_mode):
    """
    Ensure buttons are not disabled if enabling the REPL fails,
    and that the thread lock on file access is released.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.fs = None
    esp_mode.repl = None
    event = mock.Mock()

    esp_mode.toggle_repl(event)
    files._lock.acquire.assert_called_once()
    super_toggle_repl.assert_called_once_with(event)
    esp_mode.set_buttons.assert_not_called()
    files._lock.release.assert_called_once()
    assert not esp_mode.repl


@mock.patch("mu.contrib.files.Files")
def test_toggle_repl_off(files, esp_mode):
    """
    Ensure the file system button is enabled if the repl toggles off.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.fs = None
    esp_mode.repl = True
    event = mock.Mock()

    def side_effect(*args, **kwargs):
        esp_mode.repl = False

    with mock.patch('mu.modes.esp.MicroPythonMode.toggle_repl',
                    side_effect=side_effect) as super_toggle_repl:
        esp_mode.toggle_repl(event)
    super_toggle_repl.assert_called_once_with(event)
    esp_mode.set_buttons.assert_called_once_with(flash=True, files=True)
    files._lock.release.assert_called_once()


def test_toggle_repl_with_fs(esp_mode):
    """
    If the file system is active, show a helpful message instead.
    """
    esp_mode.remove_repl = mock.MagicMock()
    esp_mode.repl = None
    esp_mode.fs = True
    esp_mode.toggle_repl(None)
    esp_mode.view.show_message.assert_called_once()


def test_toggle_files_on(esp_mode):
    """
    If the fs is off, toggle it on.
    """
    def side_effect(*args, **kwargs):
        esp_mode.fs = True

    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.add_fs = mock.MagicMock(side_effect=side_effect)
    esp_mode.repl = None
    esp_mode.fs = None
    event = mock.Mock()
    esp_mode.toggle_files(event)
    esp_mode.add_fs.assert_called_once()
    esp_mode.set_buttons.assert_called_once_with(flash=False,
                                                 repl=False,
                                                 plotter=False)


def test_toggle_files_off(esp_mode):
    """
    If the fs is on, toggle if off.
    """
    esp_mode.remove_fs = mock.MagicMock()
    esp_mode.repl = None
    esp_mode.fs = True
    event = mock.Mock()
    esp_mode.toggle_files(event)
    esp_mode.remove_fs.assert_called_once()


def test_toggle_files_with_repl(esp_mode):
    """
    If the REPL is active, ensure a helpful message is displayed.
    """
    esp_mode.add_repl = mock.MagicMock()
    esp_mode.repl = True
    esp_mode.fs = None
    event = mock.Mock()
    esp_mode.toggle_files(event)
    esp_mode.view.show_message.assert_called_once()


def test_flash_repl_enabled(esp_mode):
    """
    Ensure an error message is displayed if attempting to flash
    while the repl is open. (this should not be possible as the
    button should be disabled)
    """
    esp_mode.repl = True
    esp_mode.flash()
    esp_mode.view.show_message.assert_called_once()


def test_flash_no_editor(esp_mode):
    """
    Ensure an error message is displayed if attempting to flash
    without any text editor tabs open.
    """
    esp_mode.view.current_tab = None
    esp_mode.flash()
    esp_mode.view.show_message.assert_called_once()


def test_flash_no_device(esp_mode):
    """
    Ensure an error message is displayed if attempting to flash,
    and no device is found.
    """
    esp_mode.find_device = mock.MagicMock(return_value=(None, None))
    esp_mode.flash()
    esp_mode.view.show_message.assert_called_once()


@mock.patch("mu.modes.esp.Pyboard")
@mock.patch("mu.modes.esp.DeviceFlasher")
@mock.patch("mu.modes.esp.QTimer")
def test_flash(qtimer, device_flasher, pyboard, esp_mode):
    """
    Ensure flash/repl/files buttons are disabled while flashing.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.find_device = mock.MagicMock(return_value=('COM0', '12345'))
    esp_mode.flash()
    esp_mode.set_buttons.assert_called_once_with(flash=False,
                                                 repl=False,
                                                 files=False)


@mock.patch("mu.modes.esp.Pyboard")
@mock.patch("mu.modes.esp.DeviceFlasher")
@mock.patch("mu.modes.esp.QTimer")
def test_flash_pyboard_error(qtimer, device_flasher, pyboard, esp_mode):
    """
    Ensure an error message is displayed if an error occurs while
    the flashing thread is initialized."
    """
    pyboard.side_effect = PyboardError("Error")
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.find_device = mock.MagicMock(return_value=('COM0', '12345'))
    esp_mode.flash()
    esp_mode.set_buttons.assert_called_with(flash=True,
                                            repl=True,
                                            files=True)
    esp_mode.view.show_message.assert_called_once()


def test_flash_finished(esp_mode):
    """
    Ensure state is set back as expected when the flashing thread is finished.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.flash_thread = mock.MagicMock()
    mock_timer = mock.MagicMock()
    esp_mode.flash_timer = mock_timer
    esp_mode.flash_finished()
    esp_mode.set_buttons.assert_called_once_with(flash=True,
                                                 repl=True,
                                                 files=True)
    assert esp_mode.flash_thread is None
    assert esp_mode.flash_timer is None
    mock_timer.stop.assert_called_once_with()


def test_flash_failed(esp_mode):
    """
    Ensure things are cleaned up if flashing failed.
    """
    esp_mode.set_buttons = mock.MagicMock()
    mock_timer = mock.MagicMock()
    esp_mode.flash_timer = mock_timer
    esp_mode.flash_thread = mock.MagicMock()
    esp_mode.flash_failed("Boom")
    esp_mode.view.show_message.assert_called_once()
    esp_mode.set_buttons.assert_called_once_with(flash=True,
                                                 repl=True,
                                                 files=True)
    assert esp_mode.flash_thread is None
    assert esp_mode.flash_timer is None
    mock_timer.stop.assert_called_once_with()


def test_on_data_flood(esp_mode):
    """
    Ensure the "Files" button is re-enabled before calling the base method.
    """
    esp_mode.set_buttons = mock.MagicMock()
    with mock.patch('builtins.super') as mock_super:
        esp_mode.on_data_flood()
        esp_mode.set_buttons.assert_called_once_with(files=True)
        mock_super().on_data_flood.assert_called_once_with()
