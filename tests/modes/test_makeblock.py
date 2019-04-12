# -*- coding: utf-8 -*-
"""
Tests for the Makeblock mode.
"""
import serial
import mu.modes.makeblock as makeblock
from mu.modes.makeblock import MakeblockMode, FileTransferFSM, \
    bytes_to_hex_str, calc_add_checksum, calc_32bit_xor, \
    send_file, send_file_content
from mu.modes.api import MAKEBLOCK_APIS, SHARED_APIS
from unittest import mock
from unittest.mock import patch, mock_open


def test_makeblock_mode():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = MakeblockMode(editor, view)
    assert am.name == 'Makeblock MicroPython'
    assert am.description is not None
    assert am.icon == 'makeblock'
    assert am.editor == editor
    assert am.view == view

    actions = am.actions()
    assert len(actions) == 1
    assert actions[0]['name'] == 'flash_py'
    assert actions[0]['handler'] == am.flash
    assert 'code' not in am.module_names


@patch('serial.tools.list_ports', comports=lambda: [
       mock.Mock(vid=6790, pid=29987, device='test')])
def test_find_port(mock_list_ports):
    """
    Ensure correct Makeblock port (ch340) could be found.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MakeblockMode(editor, view)
    assert mm.find_port() == 'test'


@patch('serial.tools.list_ports', comports=lambda: [])
def test_find_port_not_found(mock_list_ports):
    """
    Ensure None is returned when Makeblock port (ch340) could not be found.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MakeblockMode(editor, view)
    assert mm.find_port() is None


@patch('mu.modes.makeblock.MakeblockMode.find_port', return_value=None)
def test_flash_port_not_found(mock_find_port):
    """
    Ensure Message is shown when no device found in flashing.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MakeblockMode(editor, view)
    mm.flash()
    assert view.show_message.call_count == 1


@patch('mu.modes.makeblock.flash_task')
@patch('mu.modes.makeblock.MakeblockMode.find_port', return_value='port')
def test_flash_no_code(mock_find_port, mock_flash_task):
    """
    Ensure flashing stops when no text in the current tab.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock(current_tab=None)
    mm = MakeblockMode(editor, view)
    mm.flash()
    assert view.show_message.call_count == 0
    assert mock_flash_task.call_count == 0


@patch('mu.modes.makeblock.flash_task')
@patch('mu.modes.makeblock.MakeblockMode.find_port', return_value='port')
def test_flash(mock_find_port, mock_flash_task):
    """
    Ensure flash() is called when all arguments are proper.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MakeblockMode(editor, view)
    mm.flash()
    assert view.show_message.call_count == 0
    assert mock_flash_task.call_count == 1


def test_api():
    """
    Ensure the correct API definitions are returned.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MakeblockMode(editor, view)
    assert mm.api() == SHARED_APIS + MAKEBLOCK_APIS


frame_header_str = "F3"
frame_end_str = "F4"
FRAME_HEAD = int(frame_header_str, 16)
FRAME_END = int(frame_end_str, 16)

FTP_FSM_HEAD_S = 0
FTP_FSM_HEAD_CHECK_S = 1
FTP_FSM_DATA_S = 4
FTP_FSM_CHECK_S = 5
FTP_FSM_END_S = 6


def test_fsm():
    """
    Ensure the FSM works correctly.
    """
    fsm = FileTransferFSM()
    # 1. failed head checksum
    fsm.push_char(FRAME_HEAD)
    assert fsm.get_state() == FTP_FSM_HEAD_CHECK_S
    fsm.push_char(243)  # checksum
    fsm.push_char(1)  # len low
    fsm.push_char(0)  # len high
    assert fsm.get_state() == FTP_FSM_HEAD_S

    # 2. correct head checksum
    fsm.push_char(FRAME_HEAD)
    fsm.push_char(244)  # checksum
    fsm.push_char(1)  # len low
    fsm.push_char(0)  # len high
    assert fsm.get_state() == FTP_FSM_DATA_S
    fsm.push_char(1)  # data

    # 2.1 incorrect data checksum
    fsm.push_char(0)  # incorrect data checksum
    assert fsm.get_state() == FTP_FSM_HEAD_S

    # 2.2 correct data checksum
    fsm.set_state(FTP_FSM_CHECK_S)
    fsm.push_char(1)  # data checksum
    assert fsm.get_state() == FTP_FSM_END_S

    assert fsm.push_char(0) is None
    fsm.set_state(FTP_FSM_END_S)
    assert fsm.push_char(FRAME_END) == [1]

    fsm.clear_buf()
    assert fsm.get_buf() == []


def test_bit_operators():
    """
    Ensure bit operators for uploading program works properly
    """
    assert bytes_to_hex_str([0, 1, 2, 3]) == '00 01 02 03'
    assert calc_add_checksum([0, 1, 2, 3]) == 6
    assert calc_32bit_xor([1, 2, 3, 4, 5]) == bytearray(b'\x04\x02\x03\x04')


def test_send_file():
    """
    Ensure MakeblockMode can open file and get its content for upload.
    """
    with patch('mu.modes.makeblock.send_file_content') as sfc:
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            send_file("ser", "input_file", "target_file")
            mock_file.assert_called_with("input_file", "rb")
            sfc.assert_called_with("ser", "data", "target_file")


def test_send_file_content_timeout():
    """
    Ensure timeout when no response is received when sending the header.
    """
    ser = mock.MagicMock()
    with patch('mu.modes.makeblock.COMMAND_MAX_TIME_OUT', 1):
        send_file_content(ser, [0, 1, 2, 3], '/dev/flash')
        assert makeblock.retransmission_count == 5


@patch('mu.modes.makeblock.show_status_message')
@patch('mu.modes.makeblock.serial_fd')
@patch('mu.modes.makeblock.COMMAND_MAX_TIME_OUT', 1)
def test_send_file_content_block_timeout(mock_object, mock_called):
    """
    Ensure timeout when no response is received when sending a file.
    """
    def serial_write_mock(bytes):
        if not serial_write_mock.has_been_true:
            makeblock.command_result = True
            serial_write_mock.has_been_true = True
    serial_write_mock.has_been_true = False
    ser = mock.Mock(write=serial_write_mock)
    send_file_content(ser, [0, 1, 2, 3], '/dev/flash')
    assert makeblock.retransmission_count == 3


@patch('mu.modes.makeblock.show_status_message')
@patch('mu.modes.makeblock.serial_fd')
@patch('mu.modes.makeblock.FILE_BLOCK_SIZE', 3)
def test_send_file_content(mock_object, mock_called):
    """
    Ensure MakeblockMode can send a file to the device
    """
    def serial_write_mock(bytes):
        if not hasattr(serial_write_mock, 'wrote'):
            serial_write_mock.wrote = []
        serial_write_mock.wrote.append(bytes)
        makeblock.command_result = True
    ser = mock.Mock(write=serial_write_mock)
    send_file_content(ser, [0, 1, 2, 3], '/dev/flash')
    assert len(serial_write_mock.wrote) == 3


@patch('mu.modes.makeblock.serial_fd', "fd")
@patch('mu.modes.makeblock.input_file_content', "input_file_content")
@patch('mu.modes.makeblock.target_file_path', "target_file_path")
def test_firmware_update_task():
    """
    Ensure firmware update process works properly.
    """
    with patch('mu.modes.makeblock.send_file_content') as sfc:
        makeblock.firmware_update_task()
        sfc.assert_called_with("fd", "input_file_content", "target_file_path")


@patch('mu.modes.makeblock.ftp_process', push_char=lambda x: x)
def test_receive_task_mismatch(patch1):
    """
    Ensure False is passed out when improper bytes are received.
    """
    class mock_serial_fd:
        open_flag = True

        def readable(self):
            return True

        def inWaiting(self):
            return True

        def read(self, param):
            return [[0, 1, 2]]

        @property
        def is_open(self):
            if self.open_flag:
                self.open_flag = False
                return True
            return False
    with patch('mu.modes.makeblock.serial_fd', mock_serial_fd()):
        makeblock.receive_task()
        assert makeblock.command_result is False


@patch('mu.modes.makeblock.ftp_process', push_char=lambda x: x)
def test_receive_task(patch1):
    """
    Ensure receive process works properly.
    """
    class mock_serial_fd:
        open_flag = True

        def readable(self):
            return True

        def inWaiting(self):
            return True

        def read(self, param):
            return [[1, 2, 3, 4, 5, 6, 0]]

        @property
        def is_open(self):
            if self.open_flag:
                self.open_flag = False
                return True
            return False
    with patch('mu.modes.makeblock.serial_fd', mock_serial_fd()):
        makeblock.receive_task()
        assert makeblock.command_result is True


@patch('mu.modes.makeblock.ftp_process', push_char=lambda x: x)
def test_receive_task_exception(patch1):
    """
    Ensure receive task can handle exception.
    """
    class mock_serial_fd:
        open_flag = True

        def readable(self):
            return True

        def inWaiting(self):
            return True

        def read(self, param):
            raise serial.SerialException('Test')

        @property
        def is_open(self):
            if self.open_flag:
                self.open_flag = False
                return True
            return False
    with patch('mu.modes.makeblock.serial_fd', mock_serial_fd()):
        makeblock.receive_task()
        patch1.assert_not_called()


@patch('mu.modes.makeblock.serial_fd', is_open=lambda _: True)
@patch('serial.Serial')
@patch('threading.Thread')
def test_flash_task(mock_threading, mock_serial, mock_serial_fd):
    """
    Ensure flash task can start 2 threads.
    """
    makeblock.flash_task('serial_name', 'file_content')
    assert mock_threading.call_count == 2
