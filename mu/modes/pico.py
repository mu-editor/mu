"""
A mode for working with Raspberry Pi Pico running MicroPython.

Copyright (c) 2020 Nicholas H.Tollervey and others (see the AUTHORS file).

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
import logging
from mu.modes.esp import ESPMode
from mu.modes.api import SHARED_APIS  # TODO: Work out Pico APIs


logger = logging.getLogger(__name__)


class PicoMode(ESPMode):
    """
    Represents the functionality required for running MicroPython on a
    Raspberry Pi Pico board. This is simply a modified version of the ESP mode.
    """

    name = _("RP2040")
    short_name = "pico"
    board_name = "Raspberry Pi Pico"
    description = _("Write MicroPython directly on a Raspberry Pi Pico.")
    icon = "pico"
    fs = None

    valid_boards = [
        # VID  , PID,    Manufacturer string, Device name
        (0x2E8A, 0x0005, None, "Raspberry Pi Pico"),
    ]

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS
