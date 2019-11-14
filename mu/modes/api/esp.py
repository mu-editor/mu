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


ESP_APIS = [
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
    _("os.getcwd() \nReturn current working directory"),
    _("os.chdir(path) \nChange current working directory"),
    _("os.mkdir(path) \nMake new directory"),
    _("os.rmdir(path) \nRemove directory"),
    _(
        "os.listdir(path='.') \nReturn list of directory. Defaults to current working directory."
    ),
    # SYS
    _("sys.version \nReturn Python version as a string "),
    _("sys.version_info \nReturn Python version as a tuple"),
    _("sys.implementation \nReturn MicroPython version"),
    _(
        "sys.platform \nReturn hardware platform as string, e.g. 'esp8266' or 'esp32'"
    ),
    _(
        "sys.byteorder \nReturn platform endianness. 'little' for least-significant byte first or 'big' for most-significant byte first."
    ),
    _(
        "sys.print_exception(ex) \nPrint to the REPL information about the exception 'ex'."
    ),
    # Machine module
    _(
        "machine.reset() \nResets the device in a manner similar to pushing the external RESET button"
    ),
    _("machine.freq() \nReturns CPU frequency in hertz."),
    _(
        """machine.Pin(id [, mode, pull])\nCreate a Pin-object. Only id is mandatory.
mode (optional): specifies the pin mode (Pin.OUT or Pin.IN)
pull (optional): specifies if the pin has a pull resistor attached 
  pull can be one of: None, Pin.PULL_UP or Pin.PULL_DOWN."""
    ),
    _(
        """machine.Pin.value([x])\n This method allows to set and get the
value of the pin, depending on whether the argument x is supplied or not.
If the argument is omitted, the method returns the actual input value (0 or 1) on the pin.
If the argument is supplied, the method sets the output to the given value."""
    ),
    _("machine.Pin.OUT"),
    _("machine.Pin.IN"),
    _("machine.Pin.PULL_UP"),
    _("machine.Pin.PULL_DOWN"),
    _(
        """machine.ADC(pin)
Create an ADC object associated with the given pin. 
This allows you to then read analog values on that pin.
machine.ADC(machine.Pin(39))"""
    ),
    _(
        "machine.ADC.read() \nRead the analog pin value.\n\nadc = machine.ADC(machine.Pin(39))\nvalue = adc.read()"
    ),
    # Time module
    _("time.sleep(seconds) \nSleep the given number of seconds."),
    _("time.sleep_ms(milliseconds) \nSleep the given number of milliseconds."),
    _("time.sleep_us(milliseconds) \nSleep the given number of microseconds."),
    _(
        "time.ticks_ms() \nReturn number of milliseconds from an increasing counter. Wraps around after some value."
    ),
    _(
        "time.ticks_us() \nReturn number of microseconds from an increasing counter. Wraps around after some value."
    ),
    _(
        "time.ticks_diff() \nCompute difference between values ticks values obtained from time.ticks_ms() and time.ticks_us()."
    ),
    _(
        """time.time() 
Returns the number of seconds, as an integer, since the Epoch, 
assuming that underlying RTC is set and maintained. If an
RTC is not set, this function returns number of seconds since a
port-specific reference point in time (usually since boot or reset)."""
    ),
    # Network module
    _(
        """network.WLAN(interface_id) \n
Create a WLAN interface object. Supported interfaces are:
network.STA_IF (station aka client, connects to upstream WiFi access points) and 
network.AP_IF (access point mode, allows other WiFi clients to connect)."""
    ),
    _("network.WLAN.STA_IF"),
    _("network.WLAN.AP_IF"),
    _(
        """network.WLAN.active([ is_active ])
Activates or deactivates the network interface when given boolean
argument. When argument is omitted the function returns the current state."""
    ),
    _(
        """network.WLAN.connect(ssid, password)
Connect to the specified wireless network using the specified password."""
    ),
    _(
        "network.WLAN.disconnect() \nDisconnect from the currently connected wireless network."
    ),
    _(
        """network.WLAN.scan()
Scan for the available wireless networks. Scanning is only possible on
STA interface. Returns list of tuples with the information about WiFi
access points:
   (ssid, bssid, channel, RSSI, authmode, hidden)"""
    ),
    _(
        """network.WLAN.status()
Return the current status of the wireless connection. Possible values:
 - STAT_IDLE (no connection and no activity)
 - STAT_CONNECTING (connecting in progress)
 - STAT_WRONG_PASSWORD (failed due to incorrect password),
 - STAT_NO_AP_FOUND (failed because no access point replied),
 - STAT_CONNECT_FAIL (failed due to other problems),
 - STAT_GOT_IP (connection successful)"""
    ),
    _(
        """network.WLAN.isconnected()
In case of STA mode, returns True if connected to a WiFi access point
and has a valid IP address. In AP mode returns True when a station is
connected. Returns False otherwise."""
    ),
    _(
        """network.WLAN.ifconfig([ (ip, subnet, gateway, dns) ]) 
Get/set IP-level network interface parameters: IP address, subnet
mask, gateway and DNS server. When called with no arguments, this
method returns a 4-tuple with the above information. To set the above
values, pass a 4-tuple with the required information. For example:

nic = network.WLAN(network.WLAN.AP_IF)
nic.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))"""
    ),
    # urequests module
    _(
        """urequests.get(url, headers={})
Send HTTP GET request to the given URL. 
An optional dictionary of HTTP headers can be provided.
Returns a urequests.Response-object"""
    ),
    _(
        """urequests.post(url, data=None, json=None, headers={}) 
Send HTTP POST request to the given URL. Returns a
urequests.Response-object.
 - data (optional): bytes to send in the body of the request.
 - json (optional): JSON data to send in the body of the Request.
 - headers (optional): An optional dictionary of HTTP headers."""
    ),
    _("urequests.Response() \n Object returned by "),
    _("urequests.Response.text \n String representation of response "),
    _(
        "urequests.Response.json() \n Convert Response from JSON to Python dictionary."
    ),
    # NeoPixel module
    _(
        """neopixel.NeoPixel(pin, n) 

Create a list representing a strip of 'n' neopixels controlled from
the specified pin (e.g. machine.Pin(0)). Use the resulting object to
change each pixel by position (starting from 0). Individual pixels
are given RGB (red, green, blue) values between 0-255 as a tupel. For
example, (255, 255, 255) is white:

np = neopixel.NeoPixel(machine.Pin(0), 8)\nnp[0] = (255, 0, 128)
np.write()"""
    ),
    _(
        "neopixel.NeoPixel.write() \nShow the pixels. Must be called for any updates to become visible."
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
