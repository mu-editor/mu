"""
A mode for working with Vekatech's boards running MicroPython.

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
from mu.modes.api import SHARED_APIS


logger = logging.getLogger(__name__)


class VkMode(ESPMode):
    """
    Represents the functionality required for running MicroPython on VK boards.
    This is simply a modified version of the ESP mode.
    """

    name = _("VK board")
    short_name = "vk"
    board_name = "VK-RAxxx"
    description = _("Write MicroPython directly on a VK uPy enabled boards.")
    icon = "vk"
    fs = None

    valid_boards = [
        # VID  , PID,    Manufacturer string, Device name
        (0x045B, 0x5310, None, "CDC"),
        (0x1366, 0x0105, "SEGGER", "SWD"),
    ]

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS
