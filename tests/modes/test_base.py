# -*- coding: utf-8 -*-
"""
Tests for the BaseMode class.
"""
import os
import mu
import pytest
from mu.modes.base import BaseMode, MicroPythonMode, get_code_mode_hints
from unittest import mock


def test_get_code_mode_hints():
    import_list = [
        'import include',
        'import include as exclude',
        'import include.exclude',
        'import include.exclude as exclude_too',
        'from include import *',
        'from include import exclude',
        'from include import exclude, exclude_too',
        'from include import (exclude,\nexclude_too)',
        'from include import exclude,\\\nexclude_too',
        'from include\\\nimport exclude',
        'from include import exclude as exclude_too',
        'from include.exclude import exclude_too',
        'from include.exclude import exclude_too as exclude_again'
    ]
    function_code = [
        'exclude = None',
        'def detect():',
        '    def exclude_too():',
        '        pass',
        'if True:',
        '    def exclude_again():',
        '        pass',
        'class exclude_as_well():',
        '    pass'
    ]

    for import_code in import_list:
        found_imports = get_code_mode_hints(import_code)
        assert len(found_imports['modules']) == 1
        assert 'include' in found_imports['modules']

    found_imports = get_code_mode_hints('\n'.join(import_list + function_code))
    assert len(found_imports['modules']) == 1
    assert len(found_imports['functions']) == 1
    assert 'include' in found_imports['modules']
    assert 'detect' in found_imports['functions']

    import_list.append('import include, include_too, include_as_well.exclude')
    function_code.append('def detect_too():\n    pass')
    found_imports = get_code_mode_hints('\n'.join(import_list + function_code))
    assert len(found_imports['modules']) == 3
    assert len(found_imports['functions']) == 2
    assert 'include' in found_imports['modules']
    assert 'include_too' in found_imports['modules']
    assert 'include_as_well' in found_imports['modules']
    assert 'detect' in found_imports['functions']
    assert 'detect_too' in found_imports['functions']
    for module in found_imports['modules']:
        assert 'exclude' not in module
    for func in found_imports['functions']:
        assert 'exclude' not in func


def test_get_code_mode_hints_invalid_code():
    broken_code = [
        'import include',
        'import include_too',
        'def detect():',
        '    pass',
        'if True:    # If parsed until this line it will raise a syntax error',
        '    the text right here is not valid'
    ]
    found_imports = get_code_mode_hints('\n'.join(broken_code))
    assert len(found_imports['modules']) == 2
    assert len(found_imports['functions']) == 1
    assert 'include' in found_imports['modules']
    assert 'include_too' in found_imports['modules']
    assert 'detect' in found_imports['functions']

    found_imports = get_code_mode_hints('\n'.join(broken_code[4:]))
    assert len(found_imports['modules']) == 0
    assert len(found_imports['functions']) == 0


def test_get_code_mode_hints_with_exception():
    mock_ast_parse = mock.MagicMock(side_effect=Exception(':('))
    mock_log_warning = mock.MagicMock()
    with mock.patch('ast.parse', mock_ast_parse), \
            mock.patch('mu.modes.base.logger.warning', mock_log_warning):
        found_imports = get_code_mode_hints('some code')
    assert mock_ast_parse.call_count == 1
    assert mock_log_warning.call_count == 1
    assert len(found_imports['modules']) == 0
    assert len(found_imports['functions']) == 0


def test_base_mode():
    """
    Sanity check for the parent class of all modes.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    bm = BaseMode(editor, view)
    assert bm.name == 'UNNAMED MODE'
    assert bm.description == 'DESCRIPTION NOT AVAILABLE.'
    assert bm.icon == 'help'
    assert bm.is_debugger is False
    assert bm.editor == editor
    assert bm.view == view
    assert bm.actions() == NotImplemented
    assert bm.workspace_dir()
    assert bm.api() == NotImplemented
    assert bm.builtins is None


def test_base_mode_workspace_dir():
    """
    Return settings file workspace value.
    """
    # read from our demo settings.json
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='tests/settings.json'), \
            mock.patch('os.path.isdir', return_value=True):
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == '/home/foo/mycode'


def test_base_mode_workspace_not_present():
    """
    No workspace key in settings file, return default folder.
    """
    default_workspace = os.path.join(mu.logic.HOME_DIRECTORY,
                                     mu.logic.WORKSPACE_NAME)
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='tests/settingswithoutworkspace.json'):
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace


def test_base_mode_workspace_invalid_value():
    """
    Invalid workspace key in settings file, return default folder.
    """
    default_workspace = os.path.join(mu.logic.HOME_DIRECTORY,
                                     mu.logic.WORKSPACE_NAME)
    # read from our demo settings.json
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='tests/settings.json'), \
            mock.patch('os.path.isdir', return_value=False), \
            mock.patch('mu.modes.base.logger', return_value=None) as logger:
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace
        assert logger.error.call_count == 1


def test_base_mode_workspace_invalid_json():
    """
    Invalid workspace key in settings file, return default folder.
    """
    default_workspace = os.path.join(mu.logic.HOME_DIRECTORY,
                                     mu.logic.WORKSPACE_NAME)
    mock_open = mock.mock_open(read_data='{"workspace": invalid}')
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='a.json'), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('mu.modes.base.logger', return_value=None) as logger:
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace
        assert logger.error.call_count == 1


def test_base_mode_workspace_no_settings_file():
    """
    Invalid settings file, return default folder.
    """
    default_workspace = os.path.join(mu.logic.HOME_DIRECTORY,
                                     mu.logic.WORKSPACE_NAME)
    mock_open = mock.MagicMock(side_effect=FileNotFoundError())
    with mock.patch('mu.modes.base.get_settings_path',
                    return_value='tests/settings.json'), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('mu.modes.base.logger', return_value=None) as logger:
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace
        assert logger.error.call_count == 1


def test_base_mode_set_buttons():
    """
    Ensure only buttons for existing actions have their "Enabled" states
    updates.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.button_bar.slots = {
        'foo': mock.MagicMock(),
        'bar': mock.MagicMock()
    }
    bm = BaseMode(editor, view)
    bm.set_buttons(foo=True, bar=False, baz=True)
    view.button_bar.slots['foo'].setEnabled.assert_called_once_with(True)
    view.button_bar.slots['bar'].setEnabled.assert_called_once_with(False)
    assert 'baz' not in view.button_bar.slots


def test_base_mode_add_plotter():
    """
    Ensure the child classes need to implement this.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    bm = BaseMode(editor, view)
    assert bm.add_plotter() == NotImplemented


def test_base_mode_remove_plotter():
    """
    Ensure the plotter is removed and data is saved as a CSV file in the
    expected directory.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.plotter_pane.raw_data = [1, 2, 3]
    bm = BaseMode(editor, view)
    bm.plotter = mock.MagicMock()
    mock_mkdir = mock.MagicMock()
    mock_open = mock.mock_open()
    mock_csv_writer = mock.MagicMock()
    mock_csv = mock.MagicMock()
    mock_csv.writer.return_value = mock_csv_writer
    with mock.patch('mu.modes.base.os.path.exists', return_value=False), \
            mock.patch('mu.modes.base.os.makedirs', mock_mkdir), \
            mock.patch('builtins.open', mock_open), \
            mock.patch('mu.modes.base.csv', mock_csv):
        bm.remove_plotter()
    assert bm.plotter is None
    view.remove_plotter.assert_called_once_with()
    dd = os.path.join(bm.workspace_dir(), 'data_capture')
    mock_mkdir.assert_called_once_with(dd)
    mock_csv_writer.writerows.\
        assert_called_once_with(view.plotter_pane.raw_data)


def test_base_on_data_flood():
    """
    Ensure the plotter is removed and a helpful message is displayed to the
    user.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    bm = BaseMode(editor, view)
    bm.on_data_flood()
    view.remove_plotter.assert_called_once_with()
    assert view.show_message.call_count == 1


def test_micropython_mode_find_device():
    """
    Ensure it's possible to detect a device and return the expected port.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mock_port = mock.MagicMock()
    for vid, pid in mm.valid_boards:
        mock_port.vid = vid
        mock_port.productIdentifier = mock.MagicMock()
        mock_port.productIdentifier.return_value = pid
        mock_port.vendorIdentifier = mock.MagicMock()
        mock_port.vendorIdentifier.return_value = vid
        mock_port.portName = mock.MagicMock(return_value='COM0')
        mock_os = mock.MagicMock()
        mock_os.name = 'nt'
        with mock.patch('mu.modes.base.QSerialPortInfo.availablePorts',
                        return_value=[mock_port, ]), \
                mock.patch('mu.modes.base.os', mock_os):
            assert mm.find_device() == 'COM0'


def test_micropython_mode_find_device_no_ports():
    """
    There are no connected devices so return None.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    with mock.patch('mu.modes.base.QSerialPortInfo.availablePorts',
                    return_value=[]):
        assert mm.find_device() is None


def test_micropython_mode_find_device_but_no_device():
    """
    None of the connected devices is a valid board so return None.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mock_port = mock.MagicMock()
    mock_port.productIdentifier = mock.MagicMock(return_value=666)
    mock_port.vendorIdentifier = mock.MagicMock(return_value=999)
    with mock.patch('mu.modes.base.QSerialPortInfo.availablePorts',
                    return_value=[mock_port, ]):
        assert mm.find_device() is None


def test_micropython_mode_port_path_posix():
    """
    Ensure the correct path for a port_name is returned if the platform is
    posix.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    with mock.patch('os.name', 'posix'):
        assert mm.port_path('tty1') == "/dev/tty1"


def test_micropython_mode_port_path_nt():
    """
    Ensure the correct path for a port_name is returned if the platform is
    nt.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    with mock.patch('os.name', 'nt'):
        assert mm.port_path('COM0') == "COM0"


def test_micropython_mode_port_path_unknown():
    """
    If the platform is unknown, raise NotImplementedError.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    with mock.patch('os.name', 'foo'):
        with pytest.raises(NotImplementedError):
            mm.port_path('bar')


def test_micropython_mode_add_repl_no_port():
    """
    If it's not possible to find a connected micro:bit then ensure a helpful
    message is enacted.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value=False)
    mm.add_repl()
    assert view.show_message.call_count == 1
    message = 'Could not find an attached device.'
    assert view.show_message.call_args[0][0] == message


def test_micropython_mode_add_repl_ioerror():
    """
    Sometimes when attempting to connect to the device there is an IOError
    because it's still booting up or connecting to the host computer. In this
    case, ensure a useful message is displayed.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    ex = IOError('BOOM')
    view.add_micropython_repl = mock.MagicMock(side_effect=ex)
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value='COM0')
    mm.add_repl()
    assert view.show_message.call_count == 1
    assert view.show_message.call_args[0][0] == str(ex)


def test_micropython_mode_add_repl_exception():
    """
    Ensure that any non-IOError based exceptions are logged.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    ex = Exception('BOOM')
    view.add_micropython_repl = mock.MagicMock(side_effect=ex)
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value='COM0')
    with mock.patch('mu.modes.base.logger', return_value=None) as logger:
        mm.add_repl()
        logger.error.assert_called_once_with(ex)


def test_micropython_mode_add_repl():
    """
    Nothing goes wrong so check the _view.add_micropython_repl gets the
    expected argument.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_micropython_repl = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value='COM0')
    with mock.patch('os.name', 'nt'):
        mm.add_repl()
    assert view.show_message.call_count == 0
    assert view.add_micropython_repl.call_args[0][0] == 'COM0'


def test_micropython_mode_add_repl_no_force_interrupt():
    """
    Nothing goes wrong so check the _view.add_micropython_repl gets the
    expected arguments (including the flag so no keyboard interrupt is called).
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_micropython_repl = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.force_interrupt = False
    mm.find_device = mock.MagicMock(return_value='COM0')
    with mock.patch('os.name', 'nt'):
        mm.add_repl()
    assert view.show_message.call_count == 0
    assert view.add_micropython_repl.call_args[0][0] == 'COM0'
    assert view.add_micropython_repl.call_args[0][2] is False


def test_micropython_mode_remove_repl():
    """
    If there is a repl, make sure it's removed as expected and the state is
    updated.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.remove_repl = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.repl = True
    mm.remove_repl()
    assert view.remove_repl.call_count == 1
    assert mm.repl is False


def test_micropython_mode_toggle_repl_on():
    """
    There is no repl, so toggle on.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.add_repl = mock.MagicMock()
    mm.repl = None
    mm.toggle_repl(None)
    assert mm.add_repl.call_count == 1


def test_micropython_mode_toggle_repl_off():
    """
    There is a repl, so toggle off.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.remove_repl = mock.MagicMock()
    mm.repl = True
    mm.toggle_repl(None)
    assert mm.remove_repl.call_count == 1


def test_micropython_mode_toggle_plotter_on():
    """
    There is no plotter, so toggle on.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.add_plotter = mock.MagicMock()
    mm.plotter = None
    mm.toggle_plotter(None)
    assert mm.add_plotter.call_count == 1


def test_micropython_mode_toggle_plotter_off():
    """
    There is a plotter, so toggle off.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.remove_plotter = mock.MagicMock()
    mm.plotter = True
    mm.toggle_plotter(None)
    assert mm.remove_plotter.call_count == 1


def test_micropython_mode_add_plotter_no_port():
    """
    If it's not possible to find a connected micro:bit then ensure a helpful
    message is enacted.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value=False)
    mm.add_plotter()
    assert view.show_message.call_count == 1
    message = 'Could not find an attached device.'
    assert view.show_message.call_args[0][0] == message


def test_micropython_mode_add_plotter_ioerror():
    """
    Sometimes when attempting to connect to the device there is an IOError
    because it's still booting up or connecting to the host computer. In this
    case, ensure a useful message is displayed.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    ex = IOError('BOOM')
    view.add_micropython_plotter = mock.MagicMock(side_effect=ex)
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value='COM0')
    mm.add_plotter()
    assert view.show_message.call_count == 1
    assert view.show_message.call_args[0][0] == str(ex)


def test_micropython_mode_add_plotter_exception():
    """
    Ensure that any non-IOError based exceptions are logged.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    ex = Exception('BOOM')
    view.add_micropython_plotter = mock.MagicMock(side_effect=ex)
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value='COM0')
    with mock.patch('mu.modes.base.logger', return_value=None) as logger:
        mm.add_plotter()
        logger.error.assert_called_once_with(ex)


def test_micropython_mode_add_plotter():
    """
    Nothing goes wrong so check the _view.add_micropython_plotter gets the
    expected argument.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_micropython_plotter = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.find_device = mock.MagicMock(return_value='COM0')
    with mock.patch('os.name', 'nt'):
        mm.add_plotter()
    assert view.show_message.call_count == 0
    assert view.add_micropython_plotter.call_args[0][0] == 'COM0'


def test_micropython_on_data_flood():
    """
    Ensure that the REPL is removed before calling the base on_data_flood
    method.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.remove_repl = mock.MagicMock()
    with mock.patch('builtins.super') as mock_super:
        mm.on_data_flood()
        mm.remove_repl.assert_called_once_with()
        mock_super().on_data_flood.assert_called_once_with()
