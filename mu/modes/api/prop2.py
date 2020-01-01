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


PROP2_APIS = [
    # OS
    _("os.listdir() \nReturn a list of the names of all the files contained within the local\non-device file system."),
    _("os.remove(filename) \nRemove (delete) the file named filename."),
    #_("os.size(filename) \nReturn the size, in bytes, of the file named filename."),
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
    # pyb.Pin class
    _("""pyb.Pin(x) \nP2 PIN class supported in the standard pyb module. You can
toggle pin 56 on the P2 board, for example, with:
```
>>> import pyb
>>> p = pyb.Pin(56)
>>> p.off()
>>> p.toggle()
```
(The LEDs on the P2 board are active low, weirdly enough, so p.off()
actually turns the LED on by pulling the pin low.)
"""),
    _("pyb.Pin.off() \nTdrives pin low"),
    _("pyb.Pin.on() \ndrives pin high"),
    _("pyb.Pin.toggle() \nToggle pin value"),
    _("pyb.Pin.read() \nRead input value of pin, returns 0 or 1"),
    # Smartpin modes
    _("pyb.Pin.makeinput() \nMake the pin an input, do this before setting up smartpin"),
    _("pyb.Pin.mode(0x4c) \nSet to NCO frequency mode"),
    _("pyb.Pin.xval(16000) \nSet bit period"),
    _("pyb.Pin.yval(858993) \nSet increment"),
    _("""pyb.Pin.makeoutput() \nEnable smartpin

Note that pyb.Pin.makeinput() is implied by pyb.Pin.read(), and
pyb.Pin.makeoutput() is implied by pyb.Pin.on(), pyb.Pin.off(), and
pyb.Pin..toggle(), so the makeinput() and makeoutput() methods are only r
eally needed for smart pin manipulation"""),
    _("pyb.Pin.readzval() \nRead the Z value (input) of the smartpin"),

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
