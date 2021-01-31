"""
A mode for working with Circuit Python boards.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import ctypes
import logging
from subprocess import check_output
from mu.modes.base import MicroPythonMode
from mu.modes.api import ADAFRUIT_APIS, SHARED_APIS
from mu.interface.panes import CHARTS


logger = logging.getLogger(__name__)


class CircuitPythonMode(MicroPythonMode):
    """
    Represents the functionality required by the CircuitPython mode.
    """

    name = _("CircuitPython")
    short_name = "circuitpython"
    description = _("Write code for boards running CircuitPython.")
    icon = "circuitpython"
    save_timeout = 0  #: No auto-save on CP boards. Will restart.
    connected = True  #: is the board connected.
    force_interrupt = False  #: NO keyboard interrupt on serial connection.
    valid_boards = [
        (0x2B04, 0xC00C, None, "Particle Argon"),
        (0x2B04, 0xC00D, None, "Particle Boron"),
        (0x2B04, 0xC00E, None, "Particle Xenon"),
        (0x239A, None, None, "Adafruit CircuitPlayground"),
        # Non-Adafruit boards
        (0x1209, 0xBAB1, None, "Electronic Cats Meow Meow"),
        (0x1209, 0xBAB2, None, "Electronic Cats CatWAN USBStick"),
        (0x1209, 0xBAB3, None, "Electronic Cats Bast Pro Mini M0"),
        (0x1209, 0xBAB6, None, "Electronic Cats Escornabot Makech"),
        (0x1B4F, 0x8D22, None, "SparkFun SAMD21 Mini Breakout"),
        (0x1B4F, 0x8D23, None, "SparkFun SAMD21 Dev Breakout"),
        (0x1209, 0x2017, None, "Mini SAM M4"),
        (0x1209, 0x7102, None, "Mini SAM M0"),
        (0x04D8, 0xEC72, None, "XinaBox CC03"),
        (0x04D8, 0xEC75, None, "XinaBox CS11"),
        (0x04D8, 0xED5E, None, "XinaBox CW03"),
        (0x3171, 0x0101, None, "8086.net Commander"),
        (0x04D8, 0xED94, None, "PyCubed"),
        (0x04D8, 0xEDBE, None, "SAM32"),
        (0x1D50, 0x60E8, None, "PewPew Game Console"),
        (0x2886, 0x802D, None, "Seeed Wio Terminal"),
        (0x2886, 0x002F, None, "Seeed XIAO"),
        (0x1B4F, 0x0016, None, "Sparkfun Thing Plus - SAMD51"),
        (0x2341, 0x8057, None, "Arduino Nano 33 IoT board"),
        (0x04D8, 0xEAD1, None, "DynOSSAT-EDU-EPS"),
        (0x04D8, 0xEAD2, None, "DynOSSAT-EDU-OBC"),
        (0x1209, 0x4DDD, None, "ODT CP Sapling M0"),
        (0x1209, 0x4DDE, None, "ODT CP Sapling M0 w/ SPI Flash"),
        (0x239A, 0x80AC, None, "Unexpected Maker FeatherS2"),
        (0x303A, 0x8002, None, "Unexpected Maker TinyS2"),
        (0x054C, 0x0BC2, None, "Spresense"),
    ]
    # Modules built into CircuitPython which mustn't be used as file names
    # for source code.
    module_names = {
        "storage",
        "os",
        "touchio",
        "microcontroller",
        "bitbangio",
        "digitalio",
        "audiobusio",
        "multiterminal",
        "nvm",
        "pulseio",
        "usb_hid",
        "analogio",
        "time",
        "busio",
        "random",
        "audioio",
        "sys",
        "math",
        "builtins",
    }

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
            {
                "name": "serial",
                "display_name": _("Serial"),
                "description": _("Open a serial connection to your device."),
                "handler": self.toggle_repl,
                "shortcut": "CTRL+Shift+U",
            }
        ]
        if CHARTS:
            buttons.append(
                {
                    "name": "plotter",
                    "display_name": _("Plotter"),
                    "description": _("Plot incoming REPL data."),
                    "handler": self.toggle_plotter,
                    "shortcut": "CTRL+Shift+P",
                }
            )
        return buttons

    def workspace_dir(self):
        """
        Return the default location on the filesystem for opening and closing
        files.
        """
        device_dir = None
        # Attempts to find the path on the filesystem that represents the
        # plugged in CIRCUITPY board.
        if os.name == "posix":
            # We're on Linux or OSX
            for mount_command in ["mount", "/sbin/mount"]:
                try:
                    mount_output = check_output(mount_command).splitlines()
                    mounted_volumes = [x.split()[2] for x in mount_output]
                    for volume in mounted_volumes:
                        tail = os.path.split(volume)[-1]
                        if tail.startswith(b"CIRCUITPY") or tail.startswith(
                            b"PYBFLASH"
                        ):
                            device_dir = volume.decode("utf-8")
                            break
                except FileNotFoundError:
                    pass
                except PermissionError as e:
                    logger.error(
                        "Received '{}' running command: {}".format(
                            repr(e),
                            mount_command,
                        )
                    )
                    m = _("Permission error running mount command")
                    info = _(
                        'The mount command ("{}") returned an error: '
                        "{}. Mu will continue as if a device isn't "
                        "plugged in."
                    ).format(mount_command, repr(e))
                    self.view.show_message(m, info)
                # Avoid crashing Mu, the workspace dir will be set to default
                except Exception as e:
                    logger.error(
                        "Received '{}' running command: {}".format(
                            repr(e),
                            mount_command,
                        )
                    )

        elif os.name == "nt":
            # We're on Windows.

            def get_volume_name(disk_name):
                """
                Each disk or external device connected to windows has an
                attribute called "volume name". This function returns the
                volume name for the given disk/device.

                Code from http://stackoverflow.com/a/12056414
                """
                vol_name_buf = ctypes.create_unicode_buffer(1024)
                ctypes.windll.kernel32.GetVolumeInformationW(
                    ctypes.c_wchar_p(disk_name),
                    vol_name_buf,
                    ctypes.sizeof(vol_name_buf),
                    None,
                    None,
                    None,
                    None,
                    0,
                )
                return vol_name_buf.value

            #
            # In certain circumstances, volumes are allocated to USB
            # storage devices which cause a Windows popup to raise if their
            # volume contains no media. Wrapping the check in SetErrorMode
            # with SEM_FAILCRITICALERRORS (1) prevents this popup.
            #
            old_mode = ctypes.windll.kernel32.SetErrorMode(1)
            try:
                for disk in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    path = "{}:\\".format(disk)
                    if (
                        os.path.exists(path)
                        and get_volume_name(path) == "CIRCUITPY"
                    ):
                        return path
            finally:
                ctypes.windll.kernel32.SetErrorMode(old_mode)
        else:
            # No support for unknown operating systems.
            raise NotImplementedError('OS "{}" not supported.'.format(os.name))

        if device_dir:
            # Found it!
            self.connected = True
            return device_dir
        else:
            # Not plugged in? Just return Mu's regular workspace directory
            # after warning the user.
            wd = super().workspace_dir()
            if self.connected:
                m = _("Could not find an attached CircuitPython device.")
                info = _(
                    "Python files for CircuitPython devices"
                    " are stored on the device. Therefore, to edit"
                    " these files you need to have the device plugged in."
                    " Until you plug in a device, Mu will use the"
                    " directory found here:\n\n"
                    " {}\n\n...to store your code."
                )
                self.view.show_message(m, info.format(wd))
                self.connected = False
            return wd

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS + ADAFRUIT_APIS
