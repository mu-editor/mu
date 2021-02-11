"""
A mode for working with Lego Spike boards running MicroPython.

Copyright (c) 2015-2019 Nicholas H.Tollervey and others (see the AUTHORS file).

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
from mu.modes.api import LEGO_APIS, SHARED_APIS


logger = logging.getLogger(__name__)


class LegoMode(ESPMode):
    """
    Represents the functionality required for running MicroPython on Lego Spike
    boards. This is simply a modified version of the ESP mode.
    """

    name = _("Lego MicroPython")
    short_name = "lego"
    board_name = "Lego Spike"
    description = _("Write MicroPython directly on Lego Spike devices.")
    icon = "lego"
    fs = None

    valid_boards = [
        # VID  , PID,    Manufacturer string, Device name
        (0x0694, 0x0009, None, "Lego Spike"),  # Lego Spike board only.
    ]

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS + LEGO_APIS
