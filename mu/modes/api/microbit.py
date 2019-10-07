"""
Contains definitions for the MicroPython micro:bit related APIs so they can be
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


MICROBIT_APIS = [
    # RNG
    _("random.getrandbits(n) \nReturn an integer with n random bits."),
    _(
        "random.seed(n) \nInitialise the random number generator with a known integer 'n'."
    ),
    _(
        "random.randint(a, b) \nReturn a random whole number between a and b (inclusive)."
    ),
    _(
        "random.randrange(stop) \nReturn a random whole number between 0 and up to (but not including) stop."
    ),
    _(
        "random.choice(seq) \nReturn a randomly selected element from a sequence of objects (such as a list)."
    ),
    _(
        "random.random() \nReturn a random floating point number between 0.0 and 1.0."
    ),
    _(
        "random.uniform(a, b) \nReturn a random floating point number between a and b (inclusive)."
    ),
    # OS
    _(
        "os.listdir() \nReturn a list of the names of all the files contained within the local\non-device file system."
    ),
    _("os.remove(filename) \nRemove (delete) the file named filename."),
    _(
        "os.size(filename) \nReturn the size, in bytes, of the file named filename."
    ),
    _("os.uname() \nReturn information about MicroPython and the device."),
    # SYS
    _("sys.version"),
    _("sys.version_info"),
    _("sys.implementation"),
    _("sys.platform"),
    _("sys.byteorder"),
    _(
        "sys.print_exception(ex) \nPrint to the REPL information about the exception 'ex'."
    ),
    # System state objects.
    _(
        "microbit.panic() \nPut micro:bit in panic() mode and display an unhappy face.\nPress the reset button to exit panic() mode."
    ),
    _(
        "microbit.sleep(time) \nPut micro:bit to sleep for some milliseconds (1 second = 1000 ms) of time.\nsleep(2000) gives micro:bit a 2 second nap.\nNB: If you use time.sleep(), times are in whole seconds not milliseconds,\nuse time.sleep(2) to nap for 2 seconds, in that case."
    ),
    _(
        "microbit.running_time() \nReturn running_time() in milliseconds since micro:bit's last reset."
    ),
    _(
        "microbit.temperature() \nReturn micro:bit's temperature in degrees Celcius."
    ),
    # Accelerometer 3D orientation
    _(
        "microbit.accelerometer.get_x() \nReturn micro:bit's tilt (X acceleration) in milli-g's."
    ),
    _(
        "microbit.accelerometer.get_y() \nReturn micro:bit's tilt (Y acceleration) in milli-g's."
    ),
    _(
        "microbit.accelerometer.get_z() \nReturn micro:bit's up-down motion (Z acceleration) in milli-g's.\nZ is a positive number when moving up. Moving down, Z is a negative number."
    ),
    _(
        "microbit.accelerometer.is_gesture(name) \nReturn True or False to indicate if the named gesture is currently active.\nMicroPython understands the following gestures: 'up', 'down', 'left', 'right',\n'face up', 'face down', 'freefall', '3g', '6g', '8g' and 'shake'."
    ),
    _(
        "microbit.accelerometer.was_gesture(name) \nReturn True or False to indicate if the named gesture was active since the\nlast call.\nMicroPython understands the following gestures: 'up', 'down', 'left', 'right',\n'face up', 'face down', 'freefall', '3g', '6g', '8g' and 'shake'."
    ),
    _(
        "microbit.accelerometer.get_gestures() \nReturn a list indicating the gesture history. The most recent gesture is last.\nCalling this method also clears the gesture history.\nMicroPython understands the following gestures: 'up', 'down', 'left', 'right',\n'face up', 'face down', 'freefall', '3g', '6g', '8g' and 'shake'."
    ),
    _(
        "microbit.accelerometer.get_values() \nGet the acceleration measurements in all axes at once, as a three-element tuple of integers ordered as X, Y, Z."
    ),
    # Pushbutton
    _(
        "microbit.button_a.is_pressed() \nIf button A is pressed down, is_pressed() is True, else False."
    ),
    _(
        "microbit.button_a.was_pressed() \nUse was_pressed() to learn if button A was pressed since the last time\nwas_pressed() was called. Returns True or False."
    ),
    _(
        "microbit.button_a.get_presses() \nUse get_presses() to get the running total of button presses, and also\nreset this counter to zero."
    ),
    _(
        "microbit.button_b.is_pressed() \nIf button B is pressed down, is_pressed() is True, else False."
    ),
    _(
        "microbit.button_b.was_pressed() \nUse was_pressed() to learn if button B was pressed since the last time\nwas_pressed() was called. Returns True or False."
    ),
    _(
        "microbit.button_b.get_presses() \nUse get_presses() to get the running total of button presses, and also\nreset this counter to zero."
    ),
    # Compass 3D direction heading
    _(
        "microbit.compass.is_calibrated() \nIf micro:bit's compass is_calibrated() and adjusted for accuracy, return True.\nIf compass hasn't been adjusted for accuracy, return False."
    ),
    _(
        "microbit.compass.calibrate() \nIf micro:bit is confused, calibrate() the compass to adjust the its accuracy.\nWill ask you to rotate the device to draw a circle on the display. Afterwards, micro:bit will know which way is north."
    ),
    _(
        "microbit.compass.clear_calibration() \nReset micro:bit's compass using clear_calibration() command.\nRun calibrate() to improve accuracy."
    ),
    _(
        "microbit.compass.get_x() \nReturn magnetic field detected along micro:bit's X axis.\nUsually, the compass returns the earth's magnetic field in micro-Tesla units.\nUnless...a strong magnet is nearby!"
    ),
    _(
        "microbit.compass.get_y() \nReturn magnetic field detected along micro:bit's Y axis.\nUsually, the compass returns the earth's magnetic field in micro-Tesla units.\nUnless...a strong magnet is nearby!"
    ),
    _(
        "microbit.compass.get_z() \nReturn magnetic field detected along micro:bit's Z axis.\nUsually, the compass returns the earth's magnetic field in micro-Tesla units.\nUnless...a strong magnet is nearby!"
    ),
    _(
        "microbit.compass.get_field_strength() \nReturn strength of magnetic field around micro:bit."
    ),
    _(
        "microbit.compass.heading() \nReturn a number between 0-360 indicating the device's heading. 0 is north."
    ),
    # Display 5x5 LED grid
    _(
        "microbit.display.show(x, delay=400, wait=True, loop=False, clear=False) \nUse show(x) to print the string or image 'x' to the display. If 'x' is a list\nof images they will be animated together.\nUse 'delay' to specify the speed of frame changes in milliseconds.\nIf wait is False animation will happen in the background while the program continues.\nIf loop is True the animation will repeat forever.\nIf clear is True the display will clear at the end of the animation."
    ),
    _(
        "microbit.display.scroll(string, delay=150, wait=True, loop=False, monospace=False) \nUse scroll(string) to scroll the string across the display.\nUse delay to control how fast the text scrolls.\nIf wait is False the text will scroll in the background while the program continues.\nIf loop is True the text will repeat forever.\nIf monospace is True the characters will always take up 5 pixel-columns."
    ),
    _("microbit.display.clear() \nUse clear() to clear micro:bit's display."),
    _(
        "microbit.display.get_pixel(x, y) \nUse get_pixel(x, y) to return the display's brightness at LED pixel (x,y).\nBrightness can be from 0 (LED is off) to 9 (maximum LED brightness)."
    ),
    _(
        "microbit.display.set_pixel(x, y, b) \nUse set_pixel(x, y, b) to set the display at LED pixel (x,y) to brightness 'b'\nwhich can be set between 0 (off) to 9 (full brightness)."
    ),
    _("microbit.display.on() \nUse on() to turn on the display."),
    _("microbit.display.off() \nUse off() to turn off the display."),
    _(
        "microbit.display.is_on() \nUse is_on() to query if the micro:bit's display is on (True) or off (False)."
    ),
    # Pins
    _(
        "microbit.pin0.is_touched() \nIf pin0 is_touched() on micro:bit, return True. If nothing is touching the\npin, return False."
    ),
    _(
        "microbit.pin0.read_digital() \nread_digital() value from pin0. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin0.write_digital(value) \nSet pin0 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin0.read_analog() \nRead the voltage applied to pin0. Return the reading as a number between\n0 (meaning 0v) and 1023 (meaning 3.3v)."
    ),
    _(
        "microbit.pin0.write_analog(value) \nSet pin0 to output a value between 0 and 1023."
    ),
    _(
        "microbit.pin0.set_analog_period(period) \nSet the period of the PWM signal output to period milliseconds."
    ),
    _(
        "microbit.pin0.set_analog_period_microseconds(period) \nSet the period of the PWM signal output to period microseconds."
    ),
    _(
        "microbit.pin1.is_touched() \nIf pin1 is_touched() on micro:bit, return True. If nothing is touching the\npin, return False."
    ),
    _(
        "microbit.pin1.read_digital() \nread_digital() value from pin1. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin1.write_digital(value) \nSet pin1 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin1.read_analog() \nRead the voltage applied to pin1. Return the reading as a number between\n0 (meaning 0v) and 1023 (meaning 3.3v)."
    ),
    _(
        "microbit.pin1.write_analog(value) \nSet pin1 to output a value between 0 and 1023."
    ),
    _(
        "microbit.pin1.set_analog_period(period) \nSet the period of the PWM signal output to period milliseconds."
    ),
    _(
        "microbit.pin1.set_analog_period_microseconds(period) \nSet the period of the PWM signal output to period microseconds."
    ),
    _(
        "microbit.pin2.is_touched() \nIf pin2 is_touched() on micro:bit, return True. If nothing is touching the\npin, return False."
    ),
    _(
        "microbit.pin2.read_digital() \nread_digital() value from pin2. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin2.write_digital(value) \nSet pin2 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin2.read_analog() \nRead the voltage applied to pin2. Return the reading as a number between\n0 (meaning 0v) and 1023 (meaning 3.3v)."
    ),
    _(
        "microbit.pin2.write_analog(value) \nSet pin2 to output a value between 0 and 1023."
    ),
    _(
        "microbit.pin2.set_analog_period(period) \nSet the period of the PWM signal output to period milliseconds."
    ),
    _(
        "microbit.pin2.set_analog_period_microseconds(period) \nSet the period of the PWM signal output to period microseconds."
    ),
    _(
        "microbit.pin3.read_digital() \nread_digital() value from pin3. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin2.write_digital(value) \nSet pin3 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin3.read_analog() \nRead the voltage applied to pin3. Return the reading as a number between\n0 (meaning 0v) and 1023 (meaning 3.3v)."
    ),
    _(
        "microbit.pin3.write_analog(value) \nSet pin3 to output a value between 0 and 1023."
    ),
    _(
        "microbit.pin3.set_analog_period(period) \nSet the period of the PWM signal output to period milliseconds."
    ),
    _(
        "microbit.pin3.set_analog_period_microseconds(period) \nSet the period of the PWM signal output to period microseconds."
    ),
    _(
        "microbit.pin4.read_digital() \nread_digital() value from pin4. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin4.write_digital(value) \nSet pin4 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin4.read_analog() \nRead the voltage applied to pin4. Return the reading as a number between\n0 (meaning 0v) and 1023 (meaning 3.3v)."
    ),
    _(
        "microbit.pin4.write_analog(value) \nSet pin4 to output a value between 0 and 1023."
    ),
    _(
        "microbit.pin4.set_analog_period(period) \nSet the period of the PWM signal output to period milliseconds."
    ),
    _(
        "microbit.pin4.set_analog_period_microseconds(period) \nSet the period of the PWM signal output to period microseconds."
    ),
    _(
        "microbit.pin5.read_digital() \nread_digital() value from pin5. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin5.write_digital(value) \nSet pin5 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin6.read_digital() \nread_digital() value from pin6. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin6.write_digital(value) \nSet pin6 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin7.read_digital() \nread_digital() value from pin7. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin7.write_digital(value) \nSet pin7 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin8.read_digital() \nread_digital() value from pin8. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin8.write_digital(value) \nSet pin8 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin9.read_digital() \nread_digital() value from pin9. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin9.write_digital(value) \nSet pin9 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin10.read_digital() \nread_digital() value from pin10. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin10.write_digital(value) \nSet pin10 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin10.read_analog() \nRead the voltage applied to pin10. Return the reading as a number between\n0 (meaning 0v) and 1023 (meaning 3.3v)."
    ),
    _(
        "microbit.pin10.write_analog(value) \nSet pin10 to output a value between 0 and 1023."
    ),
    _(
        "microbit.pin10.set_analog_period(period) \nSet the period of the PWM signal output to period milliseconds."
    ),
    _(
        "microbit.pin10.set_analog_period_microseconds(period) \nSet the period of the PWM signal output to period microseconds."
    ),
    _(
        "microbit.pin11.read_digital() \nread_digital() value from pin11. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin11.write_digital(value) \nSet pin11 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin12.read_digital() \nread_digital() value from pin12. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin12.write_digital(value) \nSet pin12 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin13.read_digital() \nread_digital() value from pin13. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin13.write_digital(value) \nSet pin13 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin14.read_digital() \nread_digital() value from pin14. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin14.write_digital(value) \nSet pin14 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin15.read_digital() \nread_digital() value from pin15. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin15.write_digital(value) \nSet pin15 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin16.read_digital() \nread_digital() value from pin16. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin16.write_digital(value) \nSet pin16 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin19.read_digital() \nread_digital() value from pin19. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin19.write_digital(value) \nSet pin19 to output high if value is 1, or to low, it it is 0."
    ),
    _(
        "microbit.pin20.read_digital() \nread_digital() value from pin20. The reading will be either 0 (lo) or 1 (hi)."
    ),
    _(
        "microbit.pin20.write_digital(value) \nSet pin20 to output high if value is 1, or to low, it it is 0."
    ),
    # I2C
    _(
        "microbit.i2c.read(address, n, repeat=False) \nUse read(address, n) to read 'n' bytes from the device with the 7-bit address.\nIf repeat is True, no stop bit will be sent."
    ),
    _(
        "microbit.i2c.write(adress, buffer, repeat=False) \nUse write(address, buffer) to write to the 'buffer' of the device at the 7-bit 'address'.\nIf repeat is True, no stop bit will be sent."
    ),
    _(
        "microbit.i2c.init(frequency, scl, sda) \nUse init(frequency, scl, sda) to set the bus frequency and pins."
    ),
    # Image
    _(
        "microbit.Image(string) \nCreate and use built-in IMAGES to show on the display. Use:\nImage(\n  '09090:'\n  '99999:'\n  '99999:'\n  '09990:'\n  '00900:')\n...to make a new 5x5 heart image. Numbers go from 0 (off) to 9 (brightest). Note\nthe colon ':' to set the end of a row."
    ),
    _("microbit.Image.width() \nReturn the width of the image in pixels."),
    _("microbit.Image.height() \nReturn the height of the image in pixels."),
    _(
        "microbit.Image.get_pixel(x, y) \nUse get_pixel(x, y) to return the image's brightness at LED pixel (x,y).\nBrightness can be from 0 (LED is off) to 9 (maximum LED brightness)."
    ),
    _(
        "microbit.Image.set_pixel(x, y, b) \nUse set_pixel(x, y, b) to set the LED pixel (x,y) in the image to brightness\n'b' which can be set between 0 (off) to 9 (full brightness)."
    ),
    _(
        "microbit.Image.shift_left(n) \nUse shift_left(n) to make a copy of the image but moved 'n' pixels to the left."
    ),
    _(
        "microbit.Image.shift_right(n) \nUse shift_right(n) to make a copy of the image but moved 'n' pixels to\nthe right."
    ),
    _(
        "microbit.Image.shift_up(n) \nUse shift_up(n) to make a copy of the image but moved 'n' pixels up."
    ),
    _(
        "microbit.Image.shift_down(n) \nUse shift_down(n) to make a copy of the image but moved 'n' pixels down."
    ),
    _(
        "microbit.Image.copy() \nUse copy() to make a new exact copy of the image."
    ),
    _(
        "microbit.Image.crop(x1, y1, x2, y2) \nUse crop(x1, y1, x2, y2) to make a cut-out copy of the image where coordinate\n(x1,y1) is the top left corner of the cut-out area and coordinate (x2,y2) is the\nbottom right corner."
    ),
    _(
        "microbit.Image.invert() \nUse invert() to make a negative copy of the image. Where a pixel was bright or\non in the original, it is dim or off in the negative copy."
    ),
    _("microbit.Image.HEART"),
    _("microbit.Image.HEART_SMALL"),
    _("microbit.Image.HAPPY"),
    _("microbit.Image.SMILE"),
    _("microbit.Image.SAD"),
    _("microbit.Image.CONFUSED"),
    _("microbit.Image.ANGRY"),
    _("microbit.Image.ASLEEP"),
    _("microbit.Image.SURPRISED"),
    _("microbit.Image.SILLY"),
    _("microbit.Image.FABULOUS"),
    _("microbit.Image.MEH"),
    _("microbit.Image.YES"),
    _("microbit.Image.NO"),
    _("microbit.Image.CLOCK12"),
    _("microbit.Image.CLOCK11"),
    _("microbit.Image.CLOCK10"),
    _("microbit.Image.CLOCK9"),
    _("microbit.Image.CLOCK8"),
    _("microbit.Image.CLOCK7"),
    _("microbit.Image.CLOCK6"),
    _("microbit.Image.CLOCK5"),
    _("microbit.Image.CLOCK4"),
    _("microbit.Image.CLOCK3"),
    _("microbit.Image.CLOCK2"),
    _("microbit.Image.CLOCK1"),
    _("microbit.Image.ARROW_N"),
    _("microbit.Image.ARROW_NE"),
    _("microbit.Image.ARROW_E"),
    _("microbit.Image.ARROW_SE"),
    _("microbit.Image.ARROW_S"),
    _("microbit.Image.ARROW_SW"),
    _("microbit.Image.ARROW_W"),
    _("microbit.Image.ARROW_NW"),
    _("microbit.Image.TRIANGLE"),
    _("microbit.Image.TRIANGLE_LEFT"),
    _("microbit.Image.CHESSBOARD"),
    _("microbit.Image.DIAMOND"),
    _("microbit.Image.DIAMOND_SMALL"),
    _("microbit.Image.SQUARE"),
    _("microbit.Image.SQUARE_SMALL"),
    _("microbit.Image.RABBIT"),
    _("microbit.Image.COW"),
    _("microbit.Image.MUSIC_CROTCHET"),
    _("microbit.Image.MUSIC_QUAVER"),
    _("microbit.Image.MUSIC_QUAVERS"),
    _("microbit.Image.PITCHFORK"),
    _("microbit.Image.XMAS"),
    _("microbit.Image.PACMAN"),
    _("microbit.Image.TARGET"),
    _("microbit.Image.TSHIRT"),
    _("microbit.Image.ROLLERSKATE"),
    _("microbit.Image.DUCK"),
    _("microbit.Image.HOUSE"),
    _("microbit.Image.TORTOISE"),
    _("microbit.Image.BUTTERFLY"),
    _("microbit.Image.STICKFIGURE"),
    _("microbit.Image.GHOST"),
    _("microbit.Image.SWORD"),
    _("microbit.Image.GIRAFFE"),
    _("microbit.Image.SKULL"),
    _("microbit.Image.UMBRELLA"),
    _("microbit.Image.SNAKE"),
    _("microbit.Image.ALL_CLOCKS"),
    _("microbit.Image.ALL_ARROWS"),
    # uart
    _(
        "microbit.uart.init(baudrate=9600, bits=8, parity=None, stop=1, tx=None, rx=None) \nUse init() to set up communication using the default values. \nOtherwise override the defaults as named arguments."
    ),
    _(
        "microbit.uart.any() \nIf there are incoming characters waiting to be read, any() will return True.\nOtherwise, returns False."
    ),
    _(
        "microbit.uart.read(n) \nUse read() to read characters.\nUse read(n) to read, at most, 'n' bytes of data."
    ),
    _(
        "microbit.uart.readall() \nUse readall() to read as much data as possible."
    ),
    _(
        "microbit.uart.readline() \nUse readline() to read a line that ends with a newline character."
    ),
    _(
        "microbit.uart.readinto(buf, n) \nUse readinto(buf) to read bytes into the buffer 'buf'.\nUse readinto(buff, n) to read, at most, 'n' number of bytes into 'buf'."
    ),
    _(
        "microbit.uart.write() \nUse write(buf) to write the bytes in buffer 'buf' to the connected device."
    ),
    # SPI
    _(
        "microbit.spi.init(baudrate=1000000, bits=8, mode=0, sclk=pin13, mosi=pin15, miso=pin14) \nSet up communication. Override the defaults for baudrate, mode,\nSCLK, MOSI and MISO. The default connections are pin13 for SCLK, pin15 for\nMOSI and pin14 for MISO."
    ),
    _(
        "microbit.spi.write(buf) \nUse write(buf) to write bytes in buffer 'buf' to the connected device."
    ),
    _("microbit.spi.read(n) \nUse read(n) to read 'n' bytes of data."),
    _(
        "microbit.spi.write_readinto(out, in) \nUse write_readinto(out, in) to write the 'out' buffer to the connected device\nand read any response into the 'in' buffer. The length of the buffers should\nbe the same. The buffers can be the same object."
    ),
    # Music module
    _(
        "music.set_tempo(number, bpm) \nMake a beat last a 'number' of ticks long and\nplayed at 'bpm' beats per minute."
    ),
    _(
        "music.pitch(freq, length=-1, pin=microbit.pin0, wait=True) \nMake micro:bit play a note at 'freq' frequency for\n'length' milliseconds. E.g. pitch(440, 1000) will play concert 'A' for 1 second.\nIf length is a negative number the pitch is played continuously.\nUse the optional pin argument to override the default output for the speaker.\nIf wait is False the music will play in the background while the program\ncontinues."
    ),
    _(
        "music.play(music, pin=microbit.pin0, wait=True, loop=False) \nMake micro:bit play 'music' list of notes. Try out the built in music to see\nhow it works. E.g. music.play(music.PUNCHLINE).\nUse the optional pin argument to override the default output for the speaker.\nIf wait is False the music will play in the background while the program\ncontinues.\nIf loop is True, the tune will repeat."
    ),
    _(
        "music.get_tempo() \nReturn the number of ticks in a beat and number of beats per minute."
    ),
    _(
        "music.stop(pin=microbit.pin0) \nStops all music playback on the given pin. If no pin is given, pin0 is assumed."
    ),
    _(
        "music.reset()\nIf things go wrong, reset() the music to its default settings."
    ),
    _("music.DADADADUM"),
    _("music.ENTERTAINER"),
    _("music.PRELUDE"),
    _("music.ODE"),
    _("music.NYAN"),
    _("music.RINGTONE"),
    _("music.FUNK"),
    _("music.BLUES"),
    _("music.BIRTHDAY"),
    _("music.WEDDING"),
    _("music.FUNERAL"),
    _("music.PUNCHLINE"),
    _("music.PYTHON"),
    _("music.BADDY"),
    _("music.CHASE"),
    _("music.BA_DING"),
    _("music.WAWAWAWAA"),
    _("music.JUMP_UP"),
    _("music.JUMP_DOWN"),
    _("music.POWER_UP"),
    _("music.POWER_DOWN"),
    # Antigravity
    _("antigravity"),
    # This module
    _(
        "this.authors() \nUse authors() to reveal the names of the people who created this software."
    ),
    # Love module
    _(
        "love.badaboom()\nHear my soul speak:\nThe very instant that I saw you, did\nMy heart fly to your service."
    ),
    # NeoPixel module
    _(
        "neopixel.NeoPixel(pin, n) \nCreate a list representing a strip of 'n' neopixels controlled from the\nspecified pin (e.g. microbit.pin0).\nUse the resulting object to change each pixel by position (starting from 0).\nIndividual pixels are given RGB (red, green, blue) values between 0-255 as a\ntupe. For example, (255, 255, 255) is white:\n\nnp = neopixel.NeoPixel(microbit.pin0, 8)\nnp[0] = (255, 0, 128)\nnp.show()"
    ),
    _("neopixel.NeoPixel.clear() \nClear all the pixels."),
    _(
        "neopixel.NeoPixel.show() \nShow the pixels. Must be called for any updates to become visible."
    ),
    # Radio
    _(
        "radio.on() \nTurns on the radio. This needs to be called since the radio draws power and\ntakes up memory that you may otherwise need."
    ),
    _("radio.off() \nTurns off the radio, thus saving power and memory."),
    _(
        "radio.config(length=32, queue=3, channel=7, power=0, address=0x75626974, group=0, data_rate=radio.RATE_1MBIT) \nConfigures the various settings relating to the radio. The specified default\nvalues are sensible.\n'length' is the maximum length, in bytes, of a message. It can be up to 251\nbytes long.\n'queue' is the number of messages to store on the message queue.\n'channel' (0-100) defines the channel to which the radio is tuned.\n'address' is an arbitrary 32-bit address that's used to filter packets.\n'group' is an 8-bit value used with 'address' when filtering packets.\n'data_rate' is the throughput speed. It can be one of: radio.RATE_250KbIT,\nradio.RATE_1MbIT (the default) or radio.2MBIT."
    ),
    _("radio.reset() \nReset the settings to their default value."),
    _("radio.send_bytes(message) \nSends a message containing bytes."),
    _(
        "radio.receive_bytes() \nReceive the next incoming message from the message queue. Returns 'None' if\nthere are no pending messages. Messages are returned as bytes."
    ),
    _("radio.send(message) \nSend a message string."),
    _(
        "radio.receive() \nReceive the next incoming message from the message queue as a string. Returns\n'None' if there are no pending messages."
    ),
    _("radio.RATE_250KBIT"),
    _("radio.RATE_1MBIT"),
    _("radio.RATE_2MBIT"),
    # Audio
    _(
        "audio.play(source, wait=True, pins=(pin0, pin1)) \nPlay the source to completion where 'source' is an iterable, each element of\nwhich must be an AudioFrame instance."
    ),
    _(
        "audio.AudioFrame()() \nRepresents a list of 32 samples each of which is a signed byte. It takes just\nover 4ms to play a single frame."
    ),
    # Speech
    _(
        "speech.translate(words) \nReturn a string containing the phonemes for the English words in the string\n'words'."
    ),
    _(
        "speech.say(words, pitch=64, speed=72, mouth=128, throat=128) \nSay the English words in the string 'words'. Override the optional pitch,\nspeed, mouth and throat settings to change the tone of voice."
    ),
    _(
        "speech.pronounce(phonemes, pitch=64, speed=72, mouth=128, throat=128) \nPronounce the phonemes in the string 'phonemes'. Override the optional pitch,\nspeed, mouth and throat settings to change the tone of voice."
    ),
    _(
        "speech.sing(song, pitch=64, speed=72, mouth=128, throat=128) \nSing the phonemes in the string 'song'. Add pitch information to a phoneme\nwith a hash followed by a number between 1-255 like this: '#112DOWWWWWWWW'.\nOverride the optional pitch, speed, mouth and throat settings to change the\ntone of voice."
    ),
    # Math functions
    _("math.sqrt(x) \nReturn the square root of 'x'."),
    _("math.pow(x, y) \nReturn 'x' raised to the power 'y'."),
    _("math.exp(x) \nReturn math.e**'x'."),
    _(
        "math.log(x, base=math.e) \nWith one argument, return the natural logarithm of 'x' (to base e).\nWith two arguments, return the logarithm of 'x' to the given 'base'."
    ),
    _("math.cos(x) \nReturn the cosine of 'x' radians."),
    _("math.sin(x) \nReturn the sine of 'x' radians."),
    _("math.tan(x) \nReturn the tangent of 'x' radians."),
    _("math.acos(x) \nReturn the arc cosine of 'x', in radians."),
    _("math.asin(x) \nReturn the arc sine of 'x', in radians."),
    _("math.atan(x) \nReturn the arc tangent of 'x', in radians."),
    _("math.atan2(x, y) \nReturn atan(y / x), in radians."),
    _(
        "math.ceil(x) \nReturn the ceiling of 'x', the smallest integer greater than or equal to 'x'."
    ),
    _(
        "math.copysign(x, y) \nReturn a float with the magnitude (absolute value) of 'x' but the sign of 'y'. "
    ),
    _("math.fabs(x) \nReturn the absolute value of 'x'."),
    _(
        "math.floor(x) \nReturn the floor of 'x', the largest integer less than or equal to 'x'."
    ),
    _("math.fmod(x, y) \nReturn 'x' modulo 'y'."),
    _(
        "math.frexp(x) \nReturn the mantissa and exponent of 'x' as the pair (m, e). "
    ),
    _("math.ldexp(x, i) \nReturn 'x' * (2**'i')."),
    _(
        "math.modf(x) \nReturn the fractional and integer parts of x.\nBoth results carry the sign of x and are floats."
    ),
    _(
        "math.isfinite(x) \nReturn True if 'x' is neither an infinity nor a NaN, and False otherwise."
    ),
    _(
        "math.isinf(x) \nReturn True if 'x' is a positive or negative infinity, and False otherwise."
    ),
    _(
        "math.isnan(x) \nReturn True if 'x' is a NaN (not a number), and False otherwise."
    ),
    _(
        "math.trunc(x) \nReturn the Real value 'x' truncated to an Integral (usually an integer)."
    ),
    _("math.radians(x) \nConvert angle 'x' from degrees to radians."),
    _("math.degrees(x) \nConvert angle 'x' from radians to degrees."),
]
