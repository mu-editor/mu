"""
Contains definitions for the MicroPython Studuino:bit related APIs so they can be
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

STUDUINOBIT_APIS = [
    # Pushbutton
    _("pystubit.board.button_a.is_pressed() \nIf button A is pressed down, is_pressed() is True, else False."),
    _("pystubit.board.button_a.was_pressed() \nUse was_pressed() to learn if button A was pressed since the last time\nwas_pressed() was called. Returns True or False, then resets the record."),
    _("pystubit.board.button_a.get_presses() \nUse get_presses() to get the running total of button presses, and also\nreset this counter to zero."),
    _("pystubit.board.button_a.get_value() \nIf button A is pressed down, get_value() is 0, else 1."),
    _("pystubit.board.button_b.is_pressed() \nIf button B is pressed down, is_pressed() is True, else False."),
    _("pystubit.board.button_b.was_pressed() \nUse was_pressed() to learn if button B was pressed since the last time\nwas_pressed() was called. Returns True or False, then resets the record."),
    _("pystubit.board.button_b.get_presses() \nUse get_presses() to get the running total of button presses, and also\nreset this counter to zero."),
    _("pystubit.board.button_b.get_value() \nIf button B is pressed down, get_value() is 0, else 1."),
    # Display 5x5 LED grid
    _("pystubit.board.display.get_pixel(x, y)\nUse get_pixel(x, y) to return the display's color at LED pixel (x,y) in an (R, G, B) tuple.\nReturns values from (0, 0, 0) to (31, 31, 31)."),
    _("pystubit.board.display.set_pixel(x, y, color)\nUse set_pixel(x, y, color) to set the display color at LED pixel (x,y).\nUse a tuple (R,G,B), list [R,G,B] or integer #RGB in 'color' to set the LED's color. "),
    _("pystubit.board.display.clear()\nUse clear() to clear the display."),
    _("pystubit.board.display.show(x, delay=400, wait=True, loop=False, clear=False, color=None)\nUse show(x) to print a string or image to the display. If 'x' is a list\nof images they will be animated together.\nUse 'delay' to specify the speed of frame changes in milliseconds.\nIf wait is False animation will happen in the background while the program continues.\nIf loop is True the animation will repeat forever.\nIf clear is True the display will clear at the end of the animation.\nUse a tuple (R,G,B), list [R,G,B] or integer #RGB in 'color' to set the image's color. "),
    _("pystubit.board.display.scroll(string, delay=150, wait=True, loop=False, color=None)\nUse scroll(string) to scroll the string across the display.\nUse delay to control how fast the text scrolls.\nIf wait is False the text will scroll in the background while the program continues.\nIf loop is True the text will repeat forever.\nUse a tuple (R,G,B), list [R,G,B] or integer #RGB in 'color' to set the image's color. "),
    _("pystubit.board.display.on()\nTurn on the display."),
    _("pystubit.board.display.off()\nTurn off the display. (This allows GPIO used by the display to be used for other purposes.)"),
    _("pystubit.board.display.is_on()\nQuery if the display is on (True) or off (False)."),
    _("pystubit.board.display.BLACK"),
    _("pystubit.board.display.WHITE"),
    _("pystubit.board.display.RED"),
    _("pystubit.board.display.LIME"),
    _("pystubit.board.display.BLUE"),
    _("pystubit.board.display.YELLOW"),
    _("pystubit.board.display.CYAN"),
    _("pystubit.board.display.MAGENTA"),
    _("pystubit.board.display.SILVER"),
    _("pystubit.board.display.GRAY"),
    _("pystubit.board.display.MAROON"),
    _("pystubit.board.display.OLIVE"),
    _("pystubit.board.display.GREEN"),
    _("pystubit.board.display.PURPLE"),
    _("pystubit.board.display.TEAL"),
    _("pystubit.board.display.NAVY"),
    # Image
    _("pystubit.board.Image(string, color)\nCreate and use built-in IMAGES to show on the display. Use:\n Image(\n    '01100:'\n    '10010:'\n    '11110:'\n    '10010:'\n    '10010:',\n    color=(0,10,0))\n...to make a new green heart image.\nUse 1s (ON) and 0s (OFF) in 'string' to set a pattern.\nUse a tuple (R,G,B), list [R,G,B] or integer #RGB in 'color' to set the image's color. "),
    _("pystubit.board.Image.width()\nReturn the width of the image in pixels."),
    _("pystubit.board.Image.height()\nReturn the height of the image in pixels."),
    _("pystubit.board.Image.set_pixel(x, y, value)\nUse set_pixel(x, y, value) to set the value of an LED pixel (x,y) in the image.\nIt can be set to 0 (off) or 1 (on)."),
    _("pystubit.board.Image.set_pixel_color(x, y, color)\nUse set_pixel_color(x, y, color) to set the LED pixel (x,y) \nin the image to a color which can be set\nusing a tuple (R,G,B), list [R,G,B] or integer #RGB. "),
    _("pystubit.board.Image.get_pixel(x, y)\nReturn 1 (on) or 0 (off) according to\nthe state of the LED pixel (x,y) in the image."),
    _("pystubit.board.Image.get_pixel_color(x, y, hex=False)\nUse get_pixel_color(x, y, hex=False) to find the color of the LED pixel (x,y) in the image.\nReturns a color as a tuple (R,G,B) if hex is False,\nand as an integer #RGB if hex is True."),
    _("pystubit.board.Image.set_base_color(color)\nUse set_base_color(color) to set all LED pixels in the image\nto a color which can be set using a tuple (R,G,B), list [R,G,B] or integer #RGB."),
    _("pystubit.board.Image.shift_left(n)\nUse shift_left(n) to make a copy of the image\nbut moved 'n' pixels to the left."),
    _("pystubit.board.Image.shift_right(n)\nUse shift_right(n) to make a copy of the image\nbut moved 'n' pixels to the right."),
    _("pystubit.board.Image.shift_up(n)\nUse shift_up(n) to make a copy of the image\nbut moved 'n' pixels up."),
    _("pystubit.board.Image.shift_down(n)\nUse shift_down(n) to make a copy of the\nimage but moved 'n' pixels down."),
    _("pystubit.board.Image.copy()\nUse copy() to make a new exact copy of the image."),
    _("pystubit.board.Image.HEART"),
    _("pystubit.board.Image.HEART_SMALL"),
    _("pystubit.board.Image.HAPPY"),
    _("pystubit.board.Image.SMILE"),
    _("pystubit.board.Image.SAD"),
    _("pystubit.board.Image.CONFUSED"),
    _("pystubit.board.Image.ANGRY"),
    _("pystubit.board.Image.ASLEEP"),
    _("pystubit.board.Image.SURPRISED"),
    _("pystubit.board.Image.SILLY"),
    _("pystubit.board.Image.FABULOUS"),
    _("pystubit.board.Image.MEH"),
    _("pystubit.board.Image.YES"),
    _("pystubit.board.Image.NO"),
    _("pystubit.board.Image.CLOCK12"),
    _("pystubit.board.Image.CLOCK11"),
    _("pystubit.board.Image.CLOCK10"),
    _("pystubit.board.Image.CLOCK9"),
    _("pystubit.board.Image.CLOCK8"),
    _("pystubit.board.Image.CLOCK7"),
    _("pystubit.board.Image.CLOCK6"),
    _("pystubit.board.Image.CLOCK5"),
    _("pystubit.board.Image.CLOCK4"),
    _("pystubit.board.Image.CLOCK3"),
    _("pystubit.board.Image.CLOCK2"),
    _("pystubit.board.Image.CLOCK1"),
    _("pystubit.board.Image.ARROW_N"),
    _("pystubit.board.Image.ARROW_NE"),
    _("pystubit.board.Image.ARROW_E"),
    _("pystubit.board.Image.ARROW_SE"),
    _("pystubit.board.Image.ARROW_S"),
    _("pystubit.board.Image.ARROW_SW"),
    _("pystubit.board.Image.ARROW_W"),
    _("pystubit.board.Image.ARROW_NW"),
    _("pystubit.board.Image.TRIANGLE"),
    _("pystubit.board.Image.TRIANGLE_LEFT"),
    _("pystubit.board.Image.CHESSBOARD"),
    _("pystubit.board.Image.DIAMOND"),
    _("pystubit.board.Image.DIAMOND_SMALL"),
    _("pystubit.board.Image.SQUARE"),
    _("pystubit.board.Image.SQUARE_SMALL"),
    _("pystubit.board.Image.RABBIT"),
    _("pystubit.board.Image.COW"),
    _("pystubit.board.Image.MUSIC_CROTCHET"),
    _("pystubit.board.Image.MUSIC_QUAVER"),
    _("pystubit.board.Image.MUSIC_QUAVERS"),
    _("pystubit.board.Image.PITCHFORK"),
    _("pystubit.board.Image.XMAS"),
    _("pystubit.board.Image.PACMAN"),
    _("pystubit.board.Image.TARGET"),
    _("pystubit.board.Image.TSHIRT"),
    _("pystubit.board.Image.ROLLERSKATE"),
    _("pystubit.board.Image.DUCK"),
    _("pystubit.board.Image.HOUSE"),
    _("pystubit.board.Image.TORTOISE"),
    _("pystubit.board.Image.BUTTERFLY"),
    _("pystubit.board.Image.STICKFIGURE"),
    _("pystubit.board.Image.GHOST"),
    _("pystubit.board.Image.SWORD"),
    _("pystubit.board.Image.GIRAFFE"),
    _("pystubit.board.Image.SKULL"),
    _("pystubit.board.Image.UMBRELLA"),
    _("pystubit.board.Image.SNAKE"),
    _("pystubit.board.Image.ALL_CLOCKS"),
    _("pystubit.board.Image.ALL_ARROWS"),
    _("pystubit.board.Image.BLACK"),
    _("pystubit.board.Image.WHITE"),
    _("pystubit.board.Image.RED"),
    _("pystubit.board.Image.LIME"),
    _("pystubit.board.Image.BLUE"),
    _("pystubit.board.Image.YELLOW"),
    _("pystubit.board.Image.CYAN"),
    _("pystubit.board.Image.MAGENTA"),
    _("pystubit.board.Image.SILVER"),
    _("pystubit.board.Image.GRAY"),
    _("pystubit.board.Image.MAROON"),
    _("pystubit.board.Image.OLIVE"),
    _("pystubit.board.Image.GREEN"),
    _("pystubit.board.Image.PURPLE"),
    _("pystubit.board.Image.TEAL"),
    _("pystubit.board.Image.NAVY"),
    # buzzer
    _("pystubit.board.buzzer.on(sound, duration=-1)\nPlay sound from the Buzzer at a pitch specified in 'sound'.\n'sound' can be set using strings ('C3'-'G9'), \nMIDI note numbers ('48'-'127') or frequencies (in integers).\nUse 'duration' to set the duration of the sound in milliseconds."),
    _("pystubit.board.buzzer.off()\nStop any current sound output."),
    # temperature
    _("pystubit.board.temperature.get_value()\nReturn Studuino:bit's temperature value(0-4095) in degrees Linear."),
    _("pystubit.board.temperature.get_celsius()\nReturn Studuino:bit's temperature in degrees Celcius."),
    # lightsensor
    _("pystubit.board.lightsensor.get_value()\nReturn Studuino:bit's light sensor's  value(0-4095) in linear."),
    # accelerometer
    _("pystubit.board.accelerometer.get_x()\nReturn Studuino:bit's tilt (X acceleration) in m/s/s's."),
    _("pystubit.board.accelerometer.get_y()\nReturn Studuino:bit's tilt (Y acceleration) in m/s/s's."),
    _("pystubit.board.accelerometer.get_z()\nReturn Studuino:bit's tilt (Z acceleration) in m/s/s's."),
    _("pystubit.board.accelerometer.get_values()\nGet the acceleration measurements in all axes at once, \nas a three-element tuple of integers (ordered as X, Y, Z)."),
    _("pystubit.board.accelerometer.set_fs(value)\nSet the sensor's maximum measurement.\nUse the string '2g', '4g', '8g', or '16g' to set the maximum\nvalue between 2G and 16G."),
    _("pystubit.board.accelerometer.set_sf(value)\nSet the sensor's units of measurement.\nIt can be set to 'mg' (mg units) or 'ms2' (m/s/s units)."),
    # gyro
    _("pystubit.board.gyro.get_x()\nReturn Studuino:bit's angular velocity on the X-axis in m/s/s's."),
    _("pystubit.board.gyro.get_y()\nReturn Studuino:bit's angular velocity on the Y-axis in m/s/s's."),
    _("pystubit.board.gyro.get_z()\nReturn Studuino:bit's angular velocity on the Z-axis in m/s/s's."),
    _("pystubit.board.gyro.get_values()\nGet the angular velocity in all axes at once,\nas a three-element tuple of integers (ordered as X, Y, Z)."),
    _("pystubit.board.gyro.set_fs(value)\nSet the sensor's maximum measurement.\nUse the string '250dps', '500dps', '1000dps', or '2000dps'\nto set the maximum value between 250 and 2000 degrees per second."),
    _("pystubit.board.gyro.set_sf(value)\nSet the sensor's units of measurement.\nIt can be set to 'dps' (degrees per second) or 'rps' (radians per second). "),
    # compass
    _("pystubit.board.compass.get_x()\nReturn magnetic field detected along Studuino:bit's X axis.\nThe compass returns the earth's magnetic field in micro-Tesla units.\nThe value will be higher facing magnetic north,\nand lower facing magnetic south."),
    _("pystubit.board.compass.get_y()\nReturn magnetic field detected along Studuino:bit's Y axis.\nThe compass returns the earth's magnetic field in micro-Tesla units.\nThe value will be higher facing magnetic north,\nand lower facing magnetic south."),
    _("pystubit.board.compass.get_z()\nReturn magnetic field detected along Studuino:bit's Z axis.\nThe compass returns the earth's magnetic field in micro-Tesla units.\nThe value will be higher facing magnetic north,\nand lower facing magnetic south."),
    _("pystubit.board.compass.get_values()\nGet the magnetic field measurements from all axes at once,\nas a three-element tuple of integers (ordered as X, Y, Z)."),
    _("pystubit.board.compass.calibrate()\nIf Studuino:bit's compass is confused, calibrate() it to adjust the its accuracy.\nCalibration will ask you to rotate the device to draw a circle on the display.\nAfterwards, Studuino:bit will know which way is north."),
    _("pystubit.board.compass.is_calibrated()\nIf Studuino:bit's compass is_calibrated() and adjusted for accuracy, return True.\nIf the compass hasn't been adjusted for accuracy, return False."),
    _("pystubit.board.compass.clear_calibration()\nReset Studuino:bit's compass using clear_calibration() command."),
    _("pystubit.board.compass.heading()\nReturn a number between 0-360 indicating the device's heading. 180 is north."),
    # p0
    _("pystubit.board.p0.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p0.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p0.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p0.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p0.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p0.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p0.status()\nDisplay current PWM usage on REPL."),
    _("pystubit.board.p0.read_analog(mv=False)\nRead the voltage applied to pin. If mv=False, return the reading\nas a number between 0 (meaning 0v) and 4095. \nIf mv=True, return the reading in millivolts."),
    # p1
    _("pystubit.board.p1.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p1.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p1.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p1.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p1.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p1.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p1.status()\nDisplay current PWM usage on REPL."),
    _("pystubit.board.p1.read_analog(mv=False)\nRead the voltage applied to pin. If mv=False, return the reading\nas a number between 0 (meaning 0v) and 4095. \nIf mv=True, return the reading in millivolts."),
    # p2
    _("pystubit.board.p2.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p2.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p2.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p2.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p2.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p2.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p2.status()\nDisplay current PWM usage on REPL."),
    _("pystubit.board.p2.read_analog(mv=False)\nRead the voltage applied to pin. If mv=False, return the reading\nas a number between 0 (meaning 0v) and 4095. \nIf mv=True, return the reading in millivolts."),
    # p3
    _("pystubit.board.p3.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p3.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p3.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p3.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p3.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p3.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p3.status()\nDisplay current PWM usage on REPL."),
    _("pystubit.board.p3.read_analog(mv=False)\nRead the voltage applied to pin. If mv=False, return the reading\nas a number between 0 (meaning 0v) and 4095. \nIf mv=True, return the reading in millivolts."),
    # p4
    _("pystubit.board.p4.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p4.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p4.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p4.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p4.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p4.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p4.status()\nDisplay current PWM usage on REPL."),
    # p5
    _("pystubit.board.p5.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p5.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p5.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p5.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p5.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p5.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p5.status()\nDisplay current PWM usage on REPL."),
    _("pystubit.board.p5.read_analog(mv=False)\nRead the voltage applied to pin. If mv=False, return the reading\nas a number between 0 (meaning 0v) and 4095. \nIf mv=True, return the reading in millivolts."),
    # p6
    _("pystubit.board.p6.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p6.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p6.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p6.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p6.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p6.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p6.status()\nDisplay current PWM usage on REPL."),
    # p7
    _("pystubit.board.p7.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p7.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p7.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p7.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p7.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p7.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p7.status()\nDisplay current PWM usage on REPL."),
    # p8
    _("pystubit.board.p8.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p8.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p8.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p8.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p8.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p8.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p8.status()\nDisplay current PWM usage on REPL."),
    _("pystubit.board.p8.read_analog(mv=False)\nRead the voltage applied to pin. If mv=False, return the reading\nas a number between 0 (meaning 0v) and 4095. \nIf mv=True, return the reading in millivolts."),
    # p9
    _("pystubit.board.p9.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p9.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p9.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p9.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p9.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p9.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p9.status()\nDisplay current PWM usage on REPL."),
    _("pystubit.board.p9.read_analog(mv=False)\nRead the voltage applied to pin. If mv=False, return the reading\nas a number between 0 (meaning 0v) and 4095. \nIf mv=True, return the reading in millivolts."),
    # p10
    _("pystubit.board.p10.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p10.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p10.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p10.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p10.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p10.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p10.status()\nDisplay current PWM usage on REPL."),
    # p11
    _("pystubit.board.p11.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p11.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p11.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p11.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p11.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p11.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p11.status()\nDisplay current PWM usage on REPL."),
    # p12
    _("pystubit.board.p12.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p12.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p12.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p12.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p12.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p12.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p12.status()\nDisplay current PWM usage on REPL."),
    # p13
    _("pystubit.board.p13.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p13.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p13.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p13.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p13.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p13.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p13.status()\nDisplay current PWM usage on REPL."),
    # p14
    _("pystubit.board.p14.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p14.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p14.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p14.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p14.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p14.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p14.status()\nDisplay current PWM usage on REPL."),
    # p15
    _("pystubit.board.p15.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p15.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p15.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p15.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p15.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p15.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p15.status()\nDisplay current PWM usage on REPL."),
    # p16
    _("pystubit.board.p16.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p16.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p16.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p16.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p16.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p16.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p16.status()\nDisplay current PWM usage on REPL."),
    _("pystubit.board.p16.read_analog(mv=False)\nRead the voltage applied to pin. If mv=False, return the reading\nas a number between 0 (meaning 0v) and 4095. \nIf mv=True, return the reading in millivolts."),
    # p19
    _("pystubit.board.p19.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p19.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p19.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p19.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p19.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p19.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p19.status()\nDisplay current PWM usage on REPL."),
    # p20
    _("pystubit.board.p20.write_digital(value)\nWrite digital output to a pin. Set pin to output high if value is 1, or to low, if it is 0."),
    _("pystubit.board.p20.read_digital()\nRead digital value from pin. The reading will be either 0 (low) or 1 (high)."),
    _("pystubit.board.p20.write_analog(value)\nOutput PWM signal. Set the output from 0 (0%) to 100 (100%)."),
    _("pystubit.board.p20.set_analog_period(period, timer=-1)\nSet the period of the PWM signal output to period milliseconds.\nThe minimum period is 1ms.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p20.set_analog_period_microseconds(period, timer=-1)\nSet the period of the PWM signal output to period microseconds.\nThe minimum period is 256us.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p20.set_analog_hz(hz, timer=-1)\nSet the period of the PWM signal output to period frequency.\nYou can set the PWM's timer by picking a timer ID 0-3."),
    _("pystubit.board.p20.status()\nDisplay current PWM usage on REPL."),

    # DCMotor
    _("pyatcrobo2.parts.DCMotor(pin)\nCreate a DC Motor instance. The pin parameter can be set\nto either 'M1' or 'M2' to specify a pin with a DC Motor connected to it."),
    _("pyatcrobo2.parts.DCMotor.cw()\nSpin a DC Motor clockwise."),
    _("pyatcrobo2.parts.DCMotor.ccw()\nSpin a DC Motor counter-clockwise."),
    _("pyatcrobo2.parts.DCMotor.stop()\nStop powering a DC Motor, allowing it to coast to a stop."),
    _("pyatcrobo2.parts.DCMotor.brake()\nStop a DC Motor's rotation."),
    _("pyatcrobo2.parts.DCMotor.power(power)\nSet a DC Motor's speed.\nThe speed can be set from 0 (slowest) to 255 (fastest)."),
    # Servomotor
    _("pyatcrobo2.parts.Servomotor(pin)\nCreate a Servomotor instance.\nThe pin parameter can be set to 'P13', 'P14', 'P15', or 'P16'\nto specify a pin with a Servomotor connected to it. "),
    _("pyatcrobo2.parts.Servomotor.set_angle(degree)\nSet a Servomotor's angle.\nThe angle can be sety in degrees 0-180."),
    # Buzzer
    _("pyatcrobo2.parts.Buzzer(pin)\nCreate a Buzzer instance.\nThe pin parameter can be set to 'P13', 'P14', 'P15', or 'P16'\nto specify a pin with a Buzzer connected to it. "),
    _("pyatcrobo2.parts.Buzzer.on(sound, volume=-1, duration=-1)\nSet a specific note for the Buzzer to play.\nThe note can be set using strings ('C3'-'G9'),\nMIDI note numbers ('48'-'127') or frequencies (in integers).\nThe volume can be set by percentage (0-99).\nDuration can be set in milliseconds to make the sound\nplay for a pre-set length of time."),
    _("pyatcrobo2.parts.Buzzer.off()\nStop any current sound output."),
    # LED
    _("pyatcrobo2.parts.LED(pin)\nCreate an LED instance.\nThe pin parameter can be set to 'P13', 'P14', 'P15', or 'P16'\nto specify a pin with an LED connected to it. "),
    _("pyatcrobo2.parts.LED.on()\nTurn on an LED."),
    _("pyatcrobo2.parts.LED.off()\nTurn off an LED."),
    # IRPhotoReflector
    _("pyatcrobo2.parts.IRPhotoReflector(pin)\nCreate an IR Photoreflector instance.\nThe pin parameter can be set to 'P0', 'P1', or 'P2'\nto specify a pin with an IR Photoreflector connected to it. "),
    _("pyatcrobo2.parts.IRPhotoReflector.get_value()\nRetrieve current sensor value (0-4095)."),
    # LightSensor
    _("pyatcrobo2.parts.LightSensor(pin)\nCreate a Light Sensor instance.\nThe pin parameter can be set to 'P0', 'P1', or 'P2'\nto specify a pin with a Light Sensor connected to it. "),
    _("pyatcrobo2.parts.LightSensor.get_value()\nRetrieve current sensor value (0-4095)."),
    # Temperature
    _("pyatcrobo2.parts.Temperature(pin)\nCreate a Temperature Sensor instance.\nThe pin parameter can be set to 'P0', 'P1', or 'P2'\nto specify a pin with a Temperature Sensor connected to it. "),
    _("pyatcrobo2.parts.Temperature.get_value()\nRetrieve current sensor value (0-4095)."),
    _("pyatcrobo2.parts.Temperature.get_celsius()\nRetrieve current sensor value in degrees Celsius."),
    # SoundSensor
    _("pyatcrobo2.parts.SoundSensor(pin)\nCreate a Sound Sensor instance.\nThe pin parameter can be set to 'P0', 'P1', or 'P2'\nto specify a pin with a Sound Sensor connected to it. "),
    _("pyatcrobo2.parts.SoundSensor.get_value()\nRetrieve current sensor value (0-4095)."),
    # TouchSensor
    _("pyatcrobo2.parts.TouchSensor(pin)\nCreate a Touch Sensor instance.\nThe pin parameter can be set to 'P0', 'P1', or 'P2'\nto specify a pin with a Touch Sensor connected to it. "),
    _("pyatcrobo2.parts.TouchSensor.get_value()\nRetrieve current sensor value (0/1)."),
    # Accelerometer
    _("pyatcrobo2.parts.Accelerometer(pin)\nCreate an Accelerometer instance.\nUse 'I2C' to set the Accelerometer's pin."),
    _("pyatcrobo2.parts.Accelerometer.configuration(highres, scale)\nChange the Accelerometer's settings.\nHigh res can be set to True (16-bit resolution) or False (8-bit resolution).\nThe Accelerometer's maximum measurable acceleration\ncan be set to 2, 4, or 8 (from 2G to 8G)."),
    _("pyatcrobo2.parts.Accelerometer.get_x()\nReturn tilt (X acceleration) in m/s/s's."),
    _("pyatcrobo2.parts.Accelerometer.get_y()\nReturn tilt (Y acceleration) in m/s/s's."),
    _("pyatcrobo2.parts.Accelerometer.get_z()\nReturn tilt (Z acceleration) in m/s/s's."),
    _("pyatcrobo2.parts.Accelerometer.get_values()\nGet the acceleration measurements in all axes at once, \nas a three-element tuple of integers (ordered as X, Y, Z)."),





    # RNG
    _("random.getrandbits(n) \nReturn an integer with n random bits."),
    _("random.seed(n) \nInitialise the random number generator with a known integer 'n'."),
    _("random.randint(a, b) \nReturn a random whole number between a and b (inclusive)."),
    _("random.randrange(stop) \nReturn a random whole number between 0 and up to (but not including) stop."),
    _("random.choice(seq) \nReturn a randomly selected element from a sequence of objects (such as a list)."),
    _("random.random() \nReturn a random floating point number between 0.0 and 1.0."),
    _("random.uniform(a, b) \nReturn a random floating point number between a and b (inclusive)."),
    # OS
    _("os.listdir() \nReturn a list of the names of all the files contained within the local\non-device file system."),
    _("os.remove(filename) \nRemove (delete) the file named filename."),
    _("os.size(filename) \nReturn the size, in bytes, of the file named filename."),
    _("os.uname() \nReturn information about MicroPython and the device."),
    _("os.getcwd() \nReturn current working directory"),
    _("os.chdir(path) \nChange current working directory"),
    _("os.mkdir(path) \nMake new directory"),
    _("os.rmdir(path) \nRemove directory"),
    _("os.listdir(path='.') \nReturn list of directory. Defaults to current working directory."),
    # SYS
    _("sys.version \nReturn Python version as a string "),
    _("sys.version_info \nReturn Python version as a tuple"),
    _("sys.implementation \nReturn MicroPython version"),
    _("sys.platform \nReturn hardware platform as string, e.g. 'esp8266' or 'esp32'"),
    _("sys.byteorder \nReturn platform endianness. 'little' for least-significant byte first or 'big' for most-significant byte first." ),
    _("sys.print_exception(ex) \nPrint to the REPL information about the exception 'ex'."),
    # Machine module
    _("machine.reset() \nResets the device in a manner similar to pushing the external RESET button"),
    _("machine.freq() \nReturns CPU frequency in hertz."),

    _("""machine.Pin(id [, mode, pull])\nCreate a Pin-object. Only id is mandatory.
mode (optional): specifies the pin mode (Pin.OUT or Pin.IN)
pull (optional): specifies if the pin has a pull resistor attached 
  pull can be one of: None, Pin.PULL_UP or Pin.PULL_DOWN."""),
    _("""machine.Pin.value([x])\n This method allows to set and get the
value of the pin, depending on whether the argument x is supplied or not.
If the argument is omitted, the method returns the actual input value (0 or 1) on the pin.
If the argument is supplied, the method sets the output to the given value."""),
    _("machine.Pin.OUT"),
    _("machine.Pin.IN"),
    _("machine.Pin.PULL_UP"),
    _("machine.Pin.PULL_DOWN"),
    _("""machine.ADC(pin)
Create an ADC object associated with the given pin. 
This allows you to then read analog values on that pin.
machine.ADC(machine.Pin(39))"""),
    _("machine.ADC.read() \nRead the analog pin value.\n\nadc = machine.ADC(machine.Pin(39))\nvalue = adc.read()"),
    # Time module
    _("time.sleep(seconds) \nSleep the given number of seconds."),
    _("time.sleep_ms(milliseconds) \nSleep the given number of milliseconds."),
    _("time.sleep_us(milliseconds) \nSleep the given number of microseconds."),
    _("time.ticks_ms() \nReturn number of milliseconds from an increasing counter. Wraps around after some value."),
    _("time.ticks_us() \nReturn number of microseconds from an increasing counter. Wraps around after some value."),
    _("time.ticks_diff() \nCompute difference between values ticks values obtained from time.ticks_ms() and time.ticks_us()."),
    _("""time.time() 
Returns the number of seconds, as an integer, since the Epoch, 
assuming that underlying RTC is set and maintained. If an
RTC is not set, this function returns number of seconds since a
port-specific reference point in time (usually since boot or reset)."""),
    # Network module
    _("""network.WLAN(interface_id) \n
Create a WLAN interface object. Supported interfaces are:
network.STA_IF (station aka client, connects to upstream WiFi access points) and 
network.AP_IF (access point mode, allows other WiFi clients to connect)."""),
    _("network.WLAN.STA_IF"),
    _("network.WLAN.AP_IF"),
    _("""network.WLAN.active([ is_active ])
Activates or deactivates the network interface when given boolean
argument. When argument is omitted the function returns the current state."""),
    _("""network.WLAN.connect(ssid, password)
Connect to the specified wireless network using the specified password."""),
    _("network.WLAN.disconnect() \nDisconnect from the currently connected wireless network."),
    _("""network.WLAN.scan()
Scan for the available wireless networks. Scanning is only possible on
STA interface. Returns list of tuples with the information about WiFi
access points:
   (ssid, bssid, channel, RSSI, authmode, hidden)"""),
    _("""network.WLAN.status()
Return the current status of the wireless connection. Possible values:
 - STAT_IDLE (no connection and no activity)
 - STAT_CONNECTING (connecting in progress)
 - STAT_WRONG_PASSWORD (failed due to incorrect password),
 - STAT_NO_AP_FOUND (failed because no access point replied),
 - STAT_CONNECT_FAIL (failed due to other problems),
 - STAT_GOT_IP (connection successful)"""),
    _("""network.WLAN.isconnected()
In case of STA mode, returns True if connected to a WiFi access point
and has a valid IP address. In AP mode returns True when a station is
connected. Returns False otherwise."""),
    _("""network.WLAN.ifconfig([ (ip, subnet, gateway, dns) ]) 
Get/set IP-level network interface parameters: IP address, subnet
mask, gateway and DNS server. When called with no arguments, this
method returns a 4-tuple with the above information. To set the above
values, pass a 4-tuple with the required information. For example:

nic = network.WLAN(network.WLAN.AP_IF)
nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))"""),
    # urequests module
    _("""urequests.get(url, headers={})
Send HTTP GET request to the given URL. 
An optional dictionary of HTTP headers can be provided.
Returns a urequests.Response-object"""),
    _("""urequests.post(url, data=None, json=None, headers={}) 
Send HTTP POST request to the given URL. Returns a
urequests.Response-object.
 - data (optional): bytes to send in the body of the request.
 - json (optional): JSON data to send in the body of the Request.
 - headers (optional): An optional dictionary of HTTP headers."""),
    _("urequests.Response() \n Object returned by "),
    _("urequests.Response.text \n String representation of response "),
    _("urequests.Response.json() \n Convert Response from JSON to Python dictionary."),
    # NeoPixel module
    _("""neopixel.NeoPixel(pin, n) 

Create a list representing a strip of 'n' neopixels controlled from
the specified pin (e.g. machine.Pin(0)). Use the resulting object to
change each pixel by position (starting from 0). Individual pixels
are given RGB (red, green, blue) values between 0-255 as a tupel. For
example, (255, 255, 255) is white:

np = neopixel.NeoPixel(machine.Pin(0), 8)\nnp[0] = (255, 0, 128)
np.write()"""),
    _("neopixel.NeoPixel.write() \nShow the pixels. Must be called for any updates to become visible."),
    # Math functions
    _("math.sqrt(x) \nReturn the square root of 'x'."),
    _("math.pow(x, y) \nReturn 'x' raised to the power 'y'."),
    _("math.exp(x) \nReturn math.e**'x'."),
    _("math.log(x, base=math.e) \nWith one argument, return the natural logarithm of 'x' (to base e).\nWith two arguments, return the logarithm of 'x' to the given 'base'."),
    _("math.cos(x) \nReturn the cosine of 'x' radians."),
    _("math.sin(x) \nReturn the sine of 'x' radians."),
    _("math.tan(x) \nReturn the tangent of 'x' radians."),
    _("math.acos(x) \nReturn the arc cosine of 'x', in radians."),
    _("math.asin(x) \nReturn the arc sine of 'x', in radians."),
    _("math.atan(x) \nReturn the arc tangent of 'x', in radians."),
    _("math.atan2(x, y) \nReturn atan(y / x), in radians."),
    _("math.ceil(x) \nReturn the ceiling of 'x', the smallest integer greater than or equal to 'x'."),
    _("math.copysign(x, y) \nReturn a float with the magnitude (absolute value) of 'x' but the sign of 'y'. "),
    _("math.fabs(x) \nReturn the absolute value of 'x'."),
    _("math.floor(x) \nReturn the floor of 'x', the largest integer less than or equal to 'x'."),
    _("math.fmod(x, y) \nReturn 'x' modulo 'y'."),
    _("math.frexp(x) \nReturn the mantissa and exponent of 'x' as the pair (m, e). "),
    _("math.ldexp(x, i) \nReturn 'x' * (2**'i')."),
    _("math.modf(x) \nReturn the fractional and integer parts of x.\nBoth results carry the sign of x and are floats."),
    _("math.isfinite(x) \nReturn True if 'x' is neither an infinity nor a NaN, and False otherwise."),
    _("math.isinf(x) \nReturn True if 'x' is a positive or negative infinity, and False otherwise."),
    _("math.isnan(x) \nReturn True if 'x' is a NaN (not a number), and False otherwise."),
    _("math.trunc(x) \nReturn the Real value 'x' truncated to an Integral (usually an integer)."),
    _("math.radians(x) \nConvert angle 'x' from degrees to radians."),
    _("math.degrees(x) \nConvert angle 'x' from radians to degrees."),
]
