# -*- coding: utf-8 -*-
"""
This module contains functions for serial communication with ESP32 MicroPython.
relating to file system based operations.

You may:

* ls - list files on the device. Based on the equivalent Unix command.
* rm - remove a named file on the device. Based on the Unix command.
* put - copy a named local file onto the device a la equivalent FTP command.
* get - copy a named file from the device to the local file system a la FTP.
* tree - get the device folder structure.
"""
from __future__ import print_function
import ast
import argparse
import sys
import os
import time
import os.path
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtCore import QIODevice

PY2 = sys.version_info < (3,)


__all__ = ["ls", "rm", "put", "get", "get_serial", "tree"]

SERIAL_BAUD_RATE = 115200


def open_serial(port):
    """
    Creates a new serial link instance.
    """
    serial = QSerialPort()
    serial.setPortName(port)
    if serial.open(QIODevice.ReadWrite):
        serial.setDataTerminalReady(True)
        if not serial.isDataTerminalReady():
            # Using pyserial as a 'hack' to open the port and set DTR
            # as QtSerial does not seem to work on some Windows :(
            # See issues #281 and #302 for details.
            serial.close()
            pyser = serial.Serial(port)  # open serial port w/pyserial
            pyser.dtr = True
            pyser.close()
            serial.open(QIODevice.ReadWrite)
        serial.setBaudRate(115200)
    else:
        msg = _("Cannot connect to device on port {}").format(port)
        raise IOError(msg)

    return serial

def close_serial(serial):
    """
    Close and clean up the currently open serial link.
    """
    if serial:
        serial.close()

def read_until(serial, token, timeout=5000):
    buff = bytearray()
    while True:
        if not (serial.waitForReadyRead(timeout)):
            raise TimeoutError(_('Transfer synchronization processing failed'))
        data = bytes(serial.readAll())  # get all the available bytes.
        buff.extend(data)
        if token in buff:
            break
    return buff

def flush_to_msg(serial, token):
    read_until(serial, token)

def raw_on(serial):
    """
    Puts the device into raw mode.
    """
    raw_repl_msg = b"raw REPL; CTRL-B to exit\r\n>"
    # Send CTRL-B to end raw mode if required.
    serial.write(b"\x02")

    # Send CTRL-C three times between pauses to break out of loop.
    for i in range(3):
        serial.write(b"\r\x03")
        time.sleep(0.01)
    serial.flush()

    # Go into raw mode with CTRL-A.
    serial.write(b"\r\x01")
    flush_to_msg(serial, raw_repl_msg)

    # Soft Reset with CTRL-D
    serial.write(b"\x04")
    flush_to_msg(serial, b"soft reboot\r\n")

    # Some MicroPython versions/ports/forks provide a different message after
    # a Soft Reset, check if we are in raw REPL, if not send a CTRL-A again
    data = read_until(serial, raw_repl_msg)
    if not data.endswith(raw_repl_msg):
        serial.write(b"\r\x01")
        flush_to_msg(serial, raw_repl_msg)
    serial.flush()


def raw_off(serial):
    """
    Takes the device out of raw mode.
    """
    serial.write(b"\x02")  # Send CTRL-B to get out of raw mode.

def execute(commands, serial=None):
    """
    Sends the command to the connected micro:bit via serial and returns the
    result. If no serial connection is provided, attempts to autodetect the
    device.

    For this to work correctly, a particular sequence of commands needs to be
    sent to put the device into a good state to process the incoming command.

    Returns the stdout and stderr output from the micro:bit.
    """
    close_serial = False
    if serial is None:
        serial = get_serial()
        close_serial = True
        time.sleep(0.1)
    result = b""
    raw_on(serial)
    time.sleep(0.1)
    # Write the actual command and send CTRL-D to evaluate.
    for command in commands:
        command_bytes = command.encode("utf-8")
        for i in range(0, len(command_bytes), 32):
            serial.write(command_bytes[i : min(i + 32, len(command_bytes))])
            time.sleep(0.01)
        serial.write(b"\x04")
        response = read_until(serial, b"\x04>")  # Read until prompt.
        out, err = response[2:-2].split(b"\x04", 1)  # Split stdout, stderr
        result += out
        if err:
            return b"", err
    time.sleep(0.1)
    raw_off(serial)
    if close_serial:
        serial.close()
        time.sleep(0.1)
    return result, err

def send_cmd_blocking(serial, commands):
    """
    Separated RAW REPL ON / OFF processing from execute function to trace device
    directory hierarchy.   
    """
    result = b""
    for command in commands:
        command_bytes = command.encode("utf-8")
        for i in range(0, len(command_bytes), 32):
            serial.write(command_bytes[i : min(i + 32, len(command_bytes))])
            time.sleep(0.01)
        serial.write(b"\x04")
        response = read_until(serial, b"\x04>")  # Read until prompt.
        out, err = response[2:-2].split(b"\x04", 1)  # Split stdout, stderr
        result += out
        if err:
            return b"", err

    return result, err

def send_cmd(serial, commands, cb):
    """
    Separated RAW REPL ON / OFF processing from execute function to trace device
    directory hierarchy.   
    """

    serial.readyRead.connect(cb)

    result = b""
    for command in commands:
        command_bytes = command.encode("utf-8")
        for i in range(0, len(command_bytes), 32):
            serial.write(command_bytes[i : min(i + 32, len(command_bytes))])
            time.sleep(0.01)
        serial.write(b"\x04")


def ls(serial=None):
    """
    List the files on the micro:bit.

    If no serial object is supplied, microfs will attempt to detect the
    connection itself.

    Returns a list of the files on the connected device or raises an IOError if
    there's a problem.
    """
    out, err = execute(["import os", "print(os.listdir())"], serial)
    if err:
        raise IOError(clean_error(err))
    return ast.literal_eval(out.decode("utf-8"))


def rm(filename, serial=None):
    """
    Removes a referenced file on the micro:bit.

    If no serial object is supplied, microfs will attempt to detect the
    connection itself.

    Returns True for success or raises an IOError if there's a problem.
    """
    commands = ["import os", "os.remove('{}')".format(filename)]
    out, err = execute(commands, serial)
    if err:
        raise IOError(clean_error(err))
    return True


def put(filename, target=None, serial=None):
    """
    Puts a referenced file on the LOCAL file system onto the
    file system on the BBC micro:bit.

    If no serial object is supplied, microfs will attempt to detect the
    connection itself.

    Returns True for success or raises an IOError if there's a problem.
    """
    if not os.path.isfile(filename):
        raise IOError("No such file.")
    with open(filename, "rb") as local:
        content = local.read()
    filename = os.path.basename(filename)
    if target is None:
        target = filename
    commands = ["fd = open('{}', 'wb')".format(target), "f = fd.write"]
    while content:
        line = content[:64]
        if PY2:
            commands.append("f(b" + repr(line) + ")")
        else:
            commands.append("f(" + repr(line) + ")")
        content = content[64:]
    commands.append("fd.close()")
    out, err = execute(commands, serial)
    if err:
        raise IOError(clean_error(err))
    return True


def get(filename, target=None, serial=None):
    """
    Gets a referenced file on the device's file system and copies it to the
    target (or current working directory if unspecified).

    If no serial object is supplied, microfs will attempt to detect the
    connection itself.

    Returns True for success or raises an IOError if there's a problem.
    """
    if target is None:
        target = filename
    commands = [
        "\n".join(
            [
                "try:",
                " from microbit import uart as u",
                "except ImportError:",
                " try:",
                "  from machine import UART",
                "  u = UART(0, {})".format(SERIAL_BAUD_RATE),
                " except Exception:",
                "  try:",
                "   from sys import stdout as u",
                "  except Exception:",
                "   raise Exception('Could not find UART module in device.')",
            ]
        ),
        "f = open('{}', 'rb')".format(filename),
        "r = f.read",
        "result = True",
        "while result:\n result = r(32)\n if result:\n  u.write(result)\n",
        "f.close()",
    ]
    out, err = execute(commands, serial)
    if err:
        raise IOError(clean_error(err))
    # Recombine the bytes while removing "b'" from start and "'" from end.
    with open(target, "wb") as f:
        f.write(out)
    return True


def version(serial=None):
    """
    Returns version information for MicroPython running on the connected
    device.

    If such information is not available or the device is not running
    MicroPython, raise a ValueError.

    If any other exception is thrown, the device was running MicroPython but
    there was a problem parsing the output.
    """
    try:
        out, err = execute(["import os", "print(os.uname())"], serial)
        if err:
            raise ValueError(clean_error(err))
    except ValueError:
        # Re-raise any errors from stderr raised in the try block.
        raise
    except Exception:
        # Raise a value error to indicate unable to find something on the
        # microbit that will return parseable information about the version.
        # It doesn't matter what the error is, we just need to indicate a
        # failure with the expected ValueError exception.
        raise ValueError()
    raw = out.decode("utf-8").strip()
    raw = raw[1:-1]
    items = raw.split(", ")
    result = {}
    for item in items:
        key, value = item.split("=")
        result[key] = value[1:-1]
    return result

def seek(dirs, path, serial, flist):
    """
    Get device directory hierarchy.
    """
    dirs = ast.literal_eval(dirs.decode("utf-8"))
    for f in dirs:
        # kind = os.stat(path+'/'+f)[0]
        command = ["import os", "print(os.stat('" + path + "/" + f + "'))"]
        out, err = send_cmd_blocking(serial, command)
        out = ast.literal_eval(out.decode("utf-8"))
        kind = out[0]
        if kind == 0x4000:  # dir
            new_path = path + "/" + f

            # tree(os.listdir(new_path), new_path)
            command = ["import os", "print(os.listdir('" + new_path + "'))"]
            out, err = send_cmd_blocking(serial, command)
            if out == b'[]\r\n':
                flist.append(new_path + "/")
            else:
                seek(out, new_path, serial, flist)

        if kind == 0x8000:
            flist.append(path + "/" + f)

def tree(serial=None):
    """
    Get device directory tree hierarchy.
    """
    raw_on(serial)

    # Get root files
    flist = []
    commands = ["import os", "print(os.listdir('.'))"]
    out, err = send_cmd_blocking(serial, commands)
    seek(out, ".", serial, flist)
    raw_off(serial)
    return flist


