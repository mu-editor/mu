# -*- coding: utf-8 -*-
# import os
import pytest
from unittest import mock
from mu.modes.studuinobit import StuduinoBitMode, RegisterWindow
from mu.modes.api import STUDUINOBIT_APIS, SHARED_APIS
from PyQt5.QtWidgets import QApplication


# Required so the QWidget tests don't abort with the message:
# "QWidget: Must construct a QApplication before a QWidget"
# The QApplication need only be instantiated once.
app = QApplication([])


@pytest.fixture
def studuinobit_mode():
    editor = mock.MagicMock()
    view = mock.MagicMock()
    studuinobit_mode = StuduinoBitMode(editor, view)
    return studuinobit_mode


def test_StuduinoBitMode_init():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    studuinobit_mode = StuduinoBitMode(editor, view)
    assert studuinobit_mode.name == _('Artec Studuino:Bit MicroPython')
    assert studuinobit_mode.description is not None
    assert studuinobit_mode.icon == 'studuinobit'


def test_StuduinoBitMode_actions(studuinobit_mode):
    """
    Sanity check for mode actions.
    """
    actions = studuinobit_mode.actions()
    assert len(actions) == 5
    assert actions[0]['name'] == 'run'
    assert actions[0]['handler'] == studuinobit_mode.run
    assert actions[1]['name'] == 'flash_sb'
    assert actions[1]['handler'] == studuinobit_mode.toggle_flash
    assert actions[2]['name'] == 'files_sb'
    assert actions[2]['handler'] == studuinobit_mode.toggle_files
    assert actions[3]['name'] == 'repl'
    assert actions[3]['handler'] == studuinobit_mode.toggle_repl
    assert actions[4]['name'] == 'plotter'
    assert actions[4]['handler'] == studuinobit_mode.toggle_plotter


def test_api(studuinobit_mode):
    """
    Ensure the right thing comes back from the API.
    """
    api = studuinobit_mode.api()
    assert api == SHARED_APIS + STUDUINOBIT_APIS


@mock.patch("mu.modes.studuinobit.QThread")
@mock.patch("mu.modes.studuinobit.StuduinoBitFileManager")
def test_add_fs(fm, qthread, studuinobit_mode):
    """
    It's possible to add the file system pane if the REPL is inactive.
    """
    studuinobit_mode.view.current_tab = None
    studuinobit_mode.find_device = \
        mock.MagicMock(return_value=('COM0', '12345'))
    studuinobit_mode.add_fs()
    workspace = studuinobit_mode.workspace_dir()
    studuinobit_mode.view.add_studuinobit_filesystem.\
        assert_called_once_with(workspace, studuinobit_mode.file_manager)
    assert studuinobit_mode.fs


'''
@mock.patch("mu.modes.studuinobit.QThread")
@mock.patch("mu.modes.studuinobit.StuduinoBitFileManager")
def test_add_fs_project_path(fm, qthread, studuinobit_mode):
    """
    It's possible to add the file system pane if the REPL is inactive.
    """
    studuinobit_mode.view.current_tab.path = "foo"
    studuinobit_mode.find_device =\
        mock.MagicMock(return_value=('COM0', '12345'))
    studuinobit_mode.add_fs()
    workspace = os.path.dirname(os.path.abspath("foo"))
    studuinobit_mode.view.add_studuinobit_filesystem.\
        assert_called_once_with(workspace, studuinobit_mode.file_manager)
    assert studuinobit_mode.fs
'''


def test_add_fs_no_device(studuinobit_mode):
    """
    If there's no device attached then ensure a helpful message is displayed.
    """
    studuinobit_mode.find_device = mock.MagicMock(return_value=(None, None))
    studuinobit_mode.add_fs()
    assert studuinobit_mode.view.show_message.call_count == 1


def test_remove_fs(studuinobit_mode):
    """
    Removing the file system results in the expected state.
    """
    studuinobit_mode.fs = True
    studuinobit_mode.remove_fs()
    assert studuinobit_mode.view.remove_filesystem.call_count == 1
    assert studuinobit_mode.fs is None


def test_toggle_repl_on(studuinobit_mode):
    """
    Ensure the REPL is able to toggle on if there's no file system pane.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.fs = None
    studuinobit_mode.repl = None
    event = mock.Mock()

    def side_effect(*args, **kwargs):
        studuinobit_mode.repl = True

    with mock.patch('mu.modes.esp.MicroPythonMode.toggle_repl',
                    side_effect=side_effect) as super_toggle_repl:
        studuinobit_mode.toggle_repl(event)
    super_toggle_repl.assert_called_once_with(event)
    studuinobit_mode.set_buttons.\
        assert_called_once_with(files_sb=False, flash_sb=False)
    assert studuinobit_mode.repl


def test_toggle_repl_on_ioerror(studuinobit_mode):
    """
    Ensure the REPL is able to toggle on if there's no file system pane.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.fs = None
    studuinobit_mode.repl = None
    event = mock.Mock()

    studuinobit_mode.view.add_studuionbit_repl.side_effect = IOError()
    studuinobit_mode.toggle_repl(event)


def test_toggle_repl_on_exception(studuinobit_mode):
    """
    Ensure the REPL is able to toggle on if there's no file system pane.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.fs = None
    studuinobit_mode.repl = None
    event = mock.Mock()

    studuinobit_mode.view.add_studuionbit_repl.side_effect = Exception()
    studuinobit_mode.toggle_repl(event)


def test_toggle_repl_on_fail(studuinobit_mode):
    """
    Ensure the REPL is able to toggle on if there's no file system pane.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.fs = None
    studuinobit_mode.repl = None
    event = mock.Mock()

    studuinobit_mode.find_device = mock.MagicMock(return_value=(None, None))
    studuinobit_mode.toggle_repl(event)


@mock.patch('mu.modes.esp.MicroPythonMode.toggle_repl')
def test_toggle_repl_fail(super_toggle_repl, studuinobit_mode):
    """
    Ensure buttons are not disabled if enabling the REPL fails,
    and that the thread lock on file access is released.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.fs = None
    studuinobit_mode.repl = None
    event = mock.Mock()

    studuinobit_mode.toggle_repl(event)
    super_toggle_repl.assert_called_once_with(event)
    studuinobit_mode.set_buttons.assert_not_called()
    assert not studuinobit_mode.repl


def test_toggle_repl_off(studuinobit_mode):
    """
    Ensure the file system button is enabled if the repl toggles off.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.fs = None
    studuinobit_mode.repl = True
    event = mock.Mock()

    def side_effect(*args, **kwargs):
        studuinobit_mode.repl = False

    with mock.patch('mu.modes.esp.MicroPythonMode.toggle_repl',
                    side_effect=side_effect) as super_toggle_repl:
        studuinobit_mode.toggle_repl(event)
    super_toggle_repl.assert_called_once_with(event)
    studuinobit_mode.set_buttons.\
        assert_called_once_with(files_sb=True, flash_sb=True)


def test_toggle_repl_with_fs(studuinobit_mode):
    """
    If the file system is active, show a helpful message instead.
    """
    studuinobit_mode.remove_repl = mock.MagicMock()
    studuinobit_mode.repl = None
    studuinobit_mode.fs = True
    studuinobit_mode.toggle_repl(None)
    assert studuinobit_mode.view.show_message.call_count == 1


def test_toggle_files_on(studuinobit_mode):
    """
    If the fs is off, toggle it on.
    """
    def side_effect(*args, **kwargs):
        studuinobit_mode.fs = True

    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.add_fs = mock.MagicMock(side_effect=side_effect)
    studuinobit_mode.repl = None
    studuinobit_mode.fs = None
    event = mock.Mock()
    studuinobit_mode.toggle_files(event)
    assert studuinobit_mode.add_fs.call_count == 1
    studuinobit_mode.set_buttons.\
        assert_called_once_with(flash_sb=False, run=False,
                                repl=False, plotter=False)


def test_toggle_files_off(studuinobit_mode):
    """
    If the fs is on, toggle if off.
    """
    studuinobit_mode.remove_fs = mock.MagicMock()
    studuinobit_mode.repl = None
    studuinobit_mode.fs = True
    event = mock.Mock()
    studuinobit_mode.toggle_files(event)
    assert studuinobit_mode.remove_fs.call_count == 1


def test_toggle_files_with_repl(studuinobit_mode):
    """
    If the REPL is active, ensure a helpful message is displayed.
    """
    studuinobit_mode.add_repl = mock.MagicMock()
    studuinobit_mode.repl = True
    studuinobit_mode.fs = None
    event = mock.Mock()
    studuinobit_mode.toggle_files(event)
    assert studuinobit_mode.view.show_message.call_count == 1


def test_run_dtr_exception(studuinobit_mode):
    """
    Ensure an error message is displayed if attempting to run a script
    and no device is found.
    """
    studuinobit_mode.repl = False
    studuinobit_mode.find_device = mock.MagicMock(return_value=(None, None))
    studuinobit_mode.run()


def test_run_dtr_ioerror(studuinobit_mode):
    """
    Ensure an error message is displayed if attempting to run a script
    and no device is found.
    """
    studuinobit_mode.repl = False
    studuinobit_mode.run()


def test_run_dtr_editor_none(studuinobit_mode):
    """
    Ensure an error message is displayed if attempting to run a script
    and no device is found.
    """
    studuinobit_mode.repl = False
    with mock.patch('mu.modes.studuinobit.microfs') as mock_microfs:
        mock_microfs.execute.return_value = ('', '')
        studuinobit_mode.view.current_tab = None
        studuinobit_mode.run()


def test_run_dtr_editor(studuinobit_mode):
    """
    Ensure an error message is displayed if attempting to run a script
    and no device is found.
    """
    studuinobit_mode.repl = True
    studuinobit_mode.view.current_tab.text.return_value = "bar"
    studuinobit_mode.run()


def test_run_dtr_editor_toggle_repl(studuinobit_mode):
    """
    Ensure an error message is displayed if attempting to run a script
    and no device is found.
    """
    studuinobit_mode.repl = False
    with mock.patch('mu.modes.studuinobit.microfs') as mock_microfs:
        mock_microfs.execute.return_value = ('', '')
        studuinobit_mode.view.current_tab.text.return_value = "bar"
        studuinobit_mode.run()


def test_run(studuinobit_mode):
    """
    Ensure run/repl/files buttons are disabled while flashing.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.find_device =\
        mock.MagicMock(return_value=('COM0', '12345'))
    studuinobit_mode.run()
    # studuinobit_mode.set_buttons.assert_called_once_with(files_sb=False)


def test_on_data_flood(studuinobit_mode):
    """
    Ensure the "Files" button is re-enabled before calling the base method.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    with mock.patch('builtins.super') as mock_super:
        studuinobit_mode.on_data_flood()
        studuinobit_mode.set_buttons.assert_called_once_with(files_sb=True)
        mock_super().on_data_flood.assert_called_once_with()


def test_toggle_plotter(studuinobit_mode):
    """
    Ensure the plotter is toggled on if the file system pane is absent.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.view.show_message = mock.MagicMock()

    def side_effect(*args, **kwargs):
        studuinobit_mode.plotter = True

    with mock.patch('mu.modes.studuinobit.MicroPythonMode.toggle_plotter',
                    side_effect=side_effect) as tp:
        studuinobit_mode.plotter = None
        studuinobit_mode.toggle_plotter(None)
        tp.assert_called_once_with(None)
        studuinobit_mode.set_buttons.\
            assert_called_once_with(files_sb=False, flash_sb=False)


def test_toggle_plotter_no_repl_or_plotter(studuinobit_mode):
    """
    Ensure the file system button is enabled if the plotter toggles off and the
    repl isn't active.
    """
    studuinobit_mode.set_buttons = mock.MagicMock()
    studuinobit_mode.view.show_message = mock.MagicMock()

    def side_effect(*args, **kwargs):
        studuinobit_mode.plotter = False
        studuinobit_mode.repl = False

    with mock.patch('mu.modes.studuinobit.MicroPythonMode.toggle_plotter',
                    side_effect=side_effect) as tp:
        studuinobit_mode.plotter = None
        studuinobit_mode.toggle_plotter(None)
        tp.assert_called_once_with(None)
        studuinobit_mode.set_buttons.\
            assert_called_once_with(files_sb=True, flash_sb=True)


def test_toggle_plotter_with_fs(studuinobit_mode):
    """
    If the file system is active, show a helpful message instead.
    """
    studuinobit_mode.remove_plotter = mock.MagicMock()
    studuinobit_mode.view.show_message = mock.MagicMock()
    studuinobit_mode.plotter = None
    studuinobit_mode.fs = True
    studuinobit_mode.toggle_plotter(None)
    assert studuinobit_mode.view.show_message.call_count == 1


def test_toggle_flash_on(studuinobit_mode):
    """
    If the fs is off, toggle it on.
    """
    studuinobit_mode.view.current_tab.path = "foo"
    studuinobit_mode.view.current_tab.text.return_value = "bar"
    studuinobit_mode.view.current_tab.newline = "\n"

    with mock.patch('mu.modes.studuinobit.RegisterWindow') as m,\
            mock.patch('mu.modes.studuinobit.microfs') as mock_microfs,\
            mock.patch('mu.modes.studuinobit.Serial') as mock_serial:

        mock_serial = mock.MagicMock(return_value=mock.MagicMock())
        mock_serial.write = mock.MagicMock(return_value=True)

        studuinobit_mode.regist_box = m.return_value
        studuinobit_mode.regist_box.exec.return_value = 1
        studuinobit_mode.regist_box.get_register_info.\
            return_value = ['1', ]

        mock_microfs.put.return_value = None
        mock_microfs.execute.return_value = ('', '')

        event = mock.Mock()
        studuinobit_mode.toggle_flash(event)

        assert mock_microfs.put.call_count == 1
        assert mock_microfs.execute.call_count == 1
        studuinobit_mode.editor.show_status_message.\
            assert_called_with(_("Finished transfer. \
                Press the reset button on the Studuino:bit"))


def test_toggle_flash_on_cancel(studuinobit_mode):
    """
    If the fs is off, toggle it on.
    """
    with mock.patch('mu.modes.studuinobit.RegisterWindow') as m:
        studuinobit_mode.regist_box = m.return_value
        studuinobit_mode.regist_box.exec.return_value = 0
        event = mock.Mock()
        result = studuinobit_mode.toggle_flash(event)
        studuinobit_mode.regist_box.exec.\
            assert_called_once_with()
        assert result is None


def test_toggle_flash_on_exception(studuinobit_mode):
    """
    If the fs is off, toggle it on.
    """
    studuinobit_mode.view.current_tab.path = "foo"
    studuinobit_mode.view.current_tab.text.return_value = "bar"
    studuinobit_mode.view.current_tab.newline = "\n"

    with mock.patch('mu.modes.studuinobit.RegisterWindow') as m:
        with mock.patch('mu.modes.studuinobit.microfs') as mock_microfs:
            with mock.patch("mu.modes.studuinobit.save_and_encode",
                            return_value=None) as mock_save:

                studuinobit_mode.regist_box = m.return_value
                studuinobit_mode.regist_box.exec.return_value = 1
                studuinobit_mode.regist_box.get_register_info.\
                    return_value = ['1', ]

                mock_microfs.put.return_value = None
                mock_microfs.execute.side_effect = Exception()
                mock_microfs.execute.return_value = ('', 'BANG!')

                event = mock.Mock()
                studuinobit_mode.toggle_flash(event)

                studuinobit_mode.editor.\
                    show_status_message(_("Updating..."))
                assert mock_save.call_count == 1
                studuinobit_mode.editor.\
                    show_status_message(_("Can't transfer."))


def test_studuinobit_mode_add_repl_no_port():
    """
    If it's not possible to find a connected Studuino:bit then ensure a helpful
    message is enacted.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    sbm = StuduinoBitMode(editor, view)
    sbm.find_device = mock.MagicMock(return_value=(None, None))
    sbm.add_repl()
    assert view.show_message.call_count == 1
    message = _('Could not find an attached device.')
    assert view.show_message.call_args[0][0] == message


def test_studuinobit_mode_add_repl_ioerror():
    """
    Sometimes when attempting to connect to the device there is an IOError
    because it's still booting up or connecting to the host computer. In this
    case, ensure a useful message is displayed.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    ex = IOError('BOOM')
    view.add_studuionbit_repl = mock.MagicMock(side_effect=ex)
    sbm = StuduinoBitMode(editor, view)
    sbm.find_device = mock.MagicMock(return_value=('COM0', '12345'))
    sbm.add_repl()
    assert view.show_message.call_count == 1
    assert view.show_message.call_args[0][0] == str(ex)


def test_studuinobit_mode_add_repl_exception():
    """
    Ensure that any non-IOError based exceptions are logged.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    ex = Exception('BOOM')
    view.add_studuionbit_repl = mock.MagicMock(side_effect=ex)
    sbm = StuduinoBitMode(editor, view)
    sbm.find_device = mock.MagicMock(return_value=('COM0', '12345'))
    with mock.patch('mu.modes.studuinobit.logger',
                    return_value=None) as logger:
        sbm.add_repl()
        logger.error.assert_called_once_with(ex)


def test_studuinobit_mode_add_repl():
    """
    Nothing goes wrong so check the _view.add_studuionbit_repl gets the
    expected argument.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_studuionbit_repl = mock.MagicMock()
    sbm = StuduinoBitMode(editor, view)
    sbm.find_device = mock.MagicMock(return_value=('COM0', '12345'))
    with mock.patch('os.name', 'nt'):
        sbm.add_repl()
    assert view.show_message.call_count == 0
    assert view.add_studuionbit_repl.call_args[0][0] == 'COM0'


def test_studuinobit_mode_add_repl_no_force_interrupt():
    """
    Nothing goes wrong so check the _view.add_studuionbit_repl gets the
    expected arguments (including the flag so no keyboard interrupt is called).
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_studuionbit_repl = mock.MagicMock()
    sbm = StuduinoBitMode(editor, view)
    sbm.force_interrupt = False
    sbm.find_device = mock.MagicMock(return_value=('COM0', '12345'))
    with mock.patch('os.name', 'nt'):
        sbm.add_repl()
    assert view.show_message.call_count == 0
    assert view.add_studuionbit_repl.call_args[0][0] == 'COM0'
    assert view.add_studuionbit_repl.call_args[0][2] is False


def test_studuinobit_mode_toggle_repl_on():
    """
    There is no repl, so toggle on.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    sbm = StuduinoBitMode(editor, view)
    sbm.add_repl = mock.MagicMock()
    sbm.repl = None
    sbm.toggle_repl(None)
    assert sbm.add_repl.call_count == 1


def test_registerwindow_init():
    """
    Sanity check for setting up the mode.
    """
    rw = RegisterWindow()
    assert rw.register_info == []


def test_registerwindow_on_click():
    rw = RegisterWindow()

    rw.sender = mock.MagicMock(return_value=mock.MagicMock())
    rw.sender().parent = mock.MagicMock(return_value=mock.MagicMock())
    rw.sender().parent().title.return_value = '1'
    rw.accept = mock.MagicMock()
    rw.on_click()
    rw.accept.assert_called_once_with()

    info = rw.get_register_info()
    assert info == ['1']
