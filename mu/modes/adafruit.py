"""
A mode for working with Adafuit's line of Circuit Python boards.

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
from shutil import copyfile
from subprocess import check_output
from mu.modes.base import MicroPythonMode
from mu.modes.api import ADAFRUIT_APIS, SHARED_APIS
from mu.interface.panes import CHARTS
from mu.logic import get_pathname


class AdafruitMode(MicroPythonMode):
    """
    Represents the functionality required by the Adafruit mode.
    """

    name = _('Adafruit CircuitPython')
    description = _("Use CircuitPython on Adafruit's line of boards.")
    icon = 'adafruit'
    save_timeout = 0  #: Don't autosave on Adafruit boards. Casues a restart.
    connected = True  #: is the Adafruit board connected.
    force_interrupt = False  #: NO keyboard interrupt on serial connection.
    valid_boards = [
        (0x239A, 0x8015),  # Adafruit Feather M0 CircuitPython
        (0x239A, 0x8023),  # Adafruit Feather M0 Express CircuitPython
        (0x239A, 0x801B),  # Adafruit Feather M0 Express CircuitPython
        (0x239A, 0x8014),  # Adafruit Metro M0 CircuitPython
        (0x239A, 0x8019),  # Adafruit CircuitPlayground Express CircuitPython
        (0x239A, 0x801D),  # Adafruit Gemma M0
        (0x239A, 0x801F),  # Adafruit Trinket M0
        (0x239A, 0x8012),  # Adafruit ItsyBitsy M0
        (0x239A, 0x8021),  # Adafruit Metro M4
        (0x239A, 0x8025),  # Adafruit Feather RadioFruit
        (0x239A, 0x8026),  # Adafruit Feather M4
        (0x239A, 0x8028),  # Adafruit pIRKey M0
        (0x239A, 0x802A),  # Adafruit Feather 52840
        (0x239A, 0x802C),  # Adafruit Itsy M4
        (0x239A, 0x802E),  # Adafruit CRICKit M0
        (0x239A, 0xD1ED),  # Adafruit HalloWing M0
    ]
    # Modules built into CircuitPython which mustn't be used as file names
    # for source code.
    module_names = {'storage', 'os', 'touchio', 'microcontroller', 'bitbangio',
                    'digitalio', 'audiobusio', 'multiterminal', 'nvm',
                    'pulseio', 'usb_hid', 'analogio', 'time', 'busio',
                    'random', 'audioio', 'sys', 'math', 'builtins'}

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
            {
                'name': 'run',
                'display_name': _('Run'),
                'description': _('Save and run your current file '
                                 'on CIRCUITPY'),
                'handler': self.run,
                'shortcut': 'CTRL+Shift+R',
            },
            {
                'name': 'serial',
                'display_name': _('Serial'),
                'description': _('Open a serial connection to your device.'),
                'handler': self.toggle_repl,
                'shortcut': 'CTRL+Shift+U',
            }, ]
        if CHARTS:
            buttons.append({
                'name': 'plotter',
                'display_name': _('Plotter'),
                'description': _('Plot incoming REPL data.'),
                'handler': self.toggle_plotter,
                'shortcut': 'CTRL+Shift+P',
            })
        return buttons

    def workspace_dir(self):
        """
        Return the default location on the filesystem for opening and closing
        files.
        """
        device_dir = None
        # Attempts to find the path on the filesystem that represents the
        # plugged in CIRCUITPY board.
        if os.name == 'posix':
            # We're on Linux or OSX
            for mount_command in ['mount', '/sbin/mount']:
                try:
                    mount_output = check_output(mount_command).splitlines()
                    mounted_volumes = [x.split()[2] for x in mount_output]
                    for volume in mounted_volumes:
                        if volume.endswith(b'CIRCUITPY'):
                            device_dir = volume.decode('utf-8')
                except FileNotFoundError:
                    next
        elif os.name == 'nt':
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
                    ctypes.c_wchar_p(disk_name), vol_name_buf,
                    ctypes.sizeof(vol_name_buf), None, None, None, None, 0)
                return vol_name_buf.value

            #
            # In certain circumstances, volumes are allocated to USB
            # storage devices which cause a Windows popup to raise if their
            # volume contains no media. Wrapping the check in SetErrorMode
            # with SEM_FAILCRITICALERRORS (1) prevents this popup.
            #
            old_mode = ctypes.windll.kernel32.SetErrorMode(1)
            try:
                for disk in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    path = '{}:\\'.format(disk)
                    if (os.path.exists(path) and
                            get_volume_name(path) == 'CIRCUITPY'):
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
                m = _('Could not find an attached Adafruit CircuitPython'
                      ' device.')
                info = _("Python files for Adafruit CircuitPython devices"
                         " are stored on the device. Therefore, to edit"
                         " these files you need to have the device plugged"
                         " in. Until you plug in a device, Mu will use the"
                         " directory found here to store new files:\n\n"
                         " {}\n\n...to store your code.")
                self.view.show_message(m, info.format(wd))
                self.connected = False
            return wd

    def workspace_dir_cp(self):
        """
        Is the file currently being edited located on CIRCUITPY.
        """
        return "CIRCUITPY" in str(get_pathname(self))

    def workspace_cp_avail(self):
        """
        Is CIRCUITPY available.
        """
        return "CIRCUITPY" in str(self.workspace_dir())

    def run(self, event):
        """
        Save the file and copy to CIRCUITPY if not already there and available.
        """
        self.editor.save()

        if not self.workspace_dir_cp() and self.workspace_cp_avail():
            pathname = get_pathname(self)
            if pathname:
                destination = self.workspace_dir() + "/code.py"
                copyfile(pathname, destination)

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS + ADAFRUIT_APIS
