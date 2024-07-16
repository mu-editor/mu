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

NEOPIA_APIS = {
    'en_US': [
        _(
            "get_value(port) \n\nport: 'in1' ~ 'in3', 'remo', 'bat' \nGet a value from input port."
        ),
        _(
            "set_value(port, value) \n\nport: 'out1' ~ 'out3', 'all' \value to set: 0 ~ 255 \nSet a value to output port."
        ),
        _(
            "convert_scale(port, 0, 255, 0, 100) \n\nport: 'in1' ~ 'in3' \nparam2, param3 - min and max value of original scale: 0 ~ 255 \nparam3, param4 - min and max value of scale to be converted \nConvert a range of values from input port to another."
        ),
        _(
            "color_check(port, color) \n\nport: 'in1' ~ 'in3' \ncolor: 'white', 'green', etc \nDetect color from input port."
        ),
        _(
            "led_on(port, brightness) \n\nport: 'out1' ~ 'out3', 'all' \npercentage of brightness: '0', '10' ~ '100' \nTurn on LED with brightness adjustment."
        ),
        _(
            "led_off(port) \n\nport: 'out1' ~ 'out3', 'all' \nTurn off LED."
        ),
        _(
            "color_led_on(port, 255, 0, 0) \n\nport: 'out1' ~ 'out3', 'all' \nparam1 - Red: 0 ~ 255 \nparam2 - Green: 0 ~ 255 \nparam3 - Blue: 0 ~ 255 \nTurn on color LED with color."
        ),
        _(
            "motor_move(direction) \n\ndirection: 'forward', 'backward', 'left', 'right', 'stop' \nMove forward by motor."
        ),
        _(
            "motor_rotate(motor, direction, speed) \n\nmotor: 'both', 'left', 'right' \ndirection: 'forward', 'backward', 'left', 'right', 'stop' \nspeed percentage or input port: '0', '10' ~ '100', 'in1' ~ 'in3' \nRotate DC motor by a count of motor, direction and speed."
        ),
        _(
            "motor_stop('right') \n\nposition of motor: 'both', 'left', 'right' \nStop motor."
        ),
        _(
            "buzzer(pitch, note, length) \n\npitch: '1' ~ '6' \nnote: 'c ', 'c#', 'db', 'd' ~ 'b' \nlength of note: '2', '4', '8', '16' \nPlay a sound by pitch, note with sharp and flat, and a length of note."
        ),
        _(
            "buzzer_by_port(param) \n\nparam - port: 'in1' ~ 'in3' \nPlay a sound by value from input port."
        ),
        _(
            "buzzer_stop() \n\nStop buzzer."
        ),
        _(
            "get_angle(port) \n\nport: 'in1' ~ 'in3' \nGet a degree of an angle sensor."
        ),
        _(
            "servo_rotate(port, direction, speed) \n\noutput port: 'out1', 'out2', 'out3' \ndirection: 'forward', 'backward' \nspeed percentage or input port: '0', '10' ~ '100', 'in1' ~ 'in3' \nRotate servo motor by direction and speed."
        ),
        _(
            "servo_reset_degree(port) \noutput port: 'out1' ~ 'out3', 'all' \n\nMake 0 degree where servo motor is currently."
        ),
        _(
            "servo_rotate_by_degree(port, direction, speed, angle) \n\noutput port: 'out1', 'out2', 'out3' \ndirection: 'forward', 'backward' \nspeed percentage or input port: '0', '10' ~ '100', 'in1' ~ 'in3' \ndegree of angle: '0', '5' ~ '180', 'in1' ~ 'in3' \nRotate servo motor by direction, speed and degree of angle."
        ),
        _(
            "servo_stop(port) \n\noutput port: 'out1' ~ 'out3', 'all' \nStop servo motor."
        ),
        _(
            "remote_button(button) \n\nbutton of RC: '1', '2', '3', 'up', 'left', 'right', 'down' \nCheck if the button of remote controller is pressed."
        )
    ],
    'uz_UZ': [
        _(
            "get_value(port) \n\nport: 'in1' ~ 'in3', 'remo', 'bat' \nGet a value from input port."
        ),
        _(
            "set_value(port, value) \n\nport: 'out1' ~ 'out3', 'all' \value to set: 0 ~ 255 \nSet a value to output port."
        ),
        _(
            "convert_scale(port, 0, 255, 0, 100) \n\nport: 'in1' ~ 'in3' \nparam2, param3 - min and max value of original scale: 0 ~ 255 \nparam3, param4 - min and max value of scale to be converted \nConvert a range of values from input port to another."
        ),
        _(
            "color_check(port, color) \n\nport: 'in1' ~ 'in3' \ncolor: 'white', 'green', etc \nDetect color from input port."
        ),
        _(
            "led_on(port, brightness) \n\nport: 'out1' ~ 'out3', 'all' \npercentage of brightness: '0', '10' ~ '100' \nTurn on LED with brightness adjustment."
        ),
        _(
            "led_off(port) \n\nport: 'out1' ~ 'out3', 'all' \nTurn off LED."
        ),
        _(
            "color_led_on(port, 255, 0, 0) \n\nport: 'out1' ~ 'out3', 'all' \nparam1 - Red: 0 ~ 255 \nparam2 - Green: 0 ~ 255 \nparam3 - Blue: 0 ~ 255 \nTurn on color LED with color."
        ),
        _(
            "motor_move(direction) \n\ndirection: 'forward', 'backward', 'left', 'right', 'stop' \nMove forward by motor."
        ),
        _(
            "motor_rotate(motor, direction, speed) \n\nmotor: 'both', 'left', 'right' \ndirection: 'forward', 'backward', 'left', 'right', 'stop' \nspeed percentage or input port: '0', '10' ~ '100', 'in1' ~ 'in3' \nRotate DC motor by a count of motor, direction and speed."
        ),
        _(
            "motor_stop('right') \n\nposition of motor: 'both', 'left', 'right' \nStop motor."
        ),
        _(
            "buzzer(pitch, note, length) \n\npitch: '1' ~ '6' \nnote: 'c ', 'c#', 'db', 'd' ~ 'b' \nlength of note: '2', '4', '8', '16' \nPlay a sound by pitch, note with sharp and flat, and a length of note."
        ),
        _(
            "buzzer_by_port(param) \n\nparam - port: 'in1' ~ 'in3' \nPlay a sound by value from input port."
        ),
        _(
            "buzzer_stop() \n\nStop buzzer."
        ),
        _(
            "get_angle(port) \n\nport: 'in1' ~ 'in3' \nGet a degree of an angle sensor."
        ),
        _(
            "servo_rotate(port, direction, speed) \n\noutput port: 'out1', 'out2', 'out3' \ndirection: 'forward', 'backward' \nspeed percentage or input port: '0', '10' ~ '100', 'in1' ~ 'in3' \nRotate servo motor by direction and speed."
        ),
        _(
            "servo_reset_degree(port) \noutput port: 'out1' ~ 'out3', 'all' \n\nMake 0 degree where servo motor is currently."
        ),
        _(
            "servo_rotate_by_degree(port, direction, speed, angle) \n\noutput port: 'out1', 'out2', 'out3' \ndirection: 'forward', 'backward' \nspeed percentage or input port: '0', '10' ~ '100', 'in1' ~ 'in3' \ndegree of angle: '0', '5' ~ '180', 'in1' ~ 'in3' \nRotate servo motor by direction, speed and degree of angle."
        ),
        _(
            "servo_stop(port) \n\noutput port: 'out1' ~ 'out3', 'all' \nStop servo motor."
        ),
        _(
            "remote_button(button) \n\nbutton of RC: '1', '2', '3', 'up', 'left', 'right', 'down' \nCheck if the button of remote controller is pressed."
        )
    ],
}