"""
Contains definitions for the Neopia related APIs so they can be
used in the editor for autocomplete and call tips.

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


NEOPIA_APIS = [
    _(
        "get_value(port) \nport: 'in1' ~ 'in3', 'remo', 'bat' \nGet a value from input port."
    ),
    _(
        "set_value(port, value) \nport: 'out1' ~ 'out3', 'all' \value to set: 0 ~ 255 \nSet a value to output port."
    ),
    _(
        "convert_scale(port, 0, 255, 0, 100) \nport: 'in1' ~ 'in3' \nparam2, param3 - min and max value of original scale: 0 ~ 255 \nparam3, param4 - min and max value of scale to be converted \nConvert a range of values from input port to another."
    ),
    _(

    ),
]
