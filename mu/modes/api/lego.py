"""
Contains definitions for Lego Spike APIs so they can be used in the editor for
autocomplete and call tips.

Copyright (c) 2015-2021 Nicholas H.Tollervey and others (see the AUTHORS file).

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

LEGO_APIS = [
    _(
        "battery.capacity_left() \nReturns the capacity left on the battery as a percentage of fully charged.\n"
    ),
    _(
        "battery.charger_detect() \nReturns the charger detected.\nReturns False if  no charger is attached.\nIf a charger has been attached the following is returned:\n\n\nflipper.USB_CH_PORT_NONE = 0\nflipper.USB_CH_PORT_SDP  = 1\nflipper.USB_CH_PORT_CDP  = 2\nflipper.USB_CH_PORT_DCP  = 3\n\n\nSDP is a Standard Downstream Port (typical USB port)\nDCP is a Dedicated Charging Port (high current USB port)\nCDP is a Charging Downstream Port (wall charger)\n"
    ),
    _(
        "battery.current() \nReturn the battery current consumption in mA. This is the current flowing from the battery.\n"
    ),
    _(
        "battery.info() \nReturns a dict with the Battery subsystem information. Avoid calling\nthis function every time you need a specifc item. It’s better to save\nthe result in a local variable and then reference the dict elements as\nneeded:\n\nerror_state - A list of currently active errors incl. 0 (flipper.BATTERY_NO_ERROR) if no errors are active. Possible error are:\n\n\nbattery.BATTERY_NO_ERROR = 0\nbattery.BATTERY_HUB_TEMPERATURE_CRITICAL_OUT_OF_RANGE = -1\nbattery.BATTERY_TEMPERATURE_OUT_OF_RANGE = -2\nbattery.BATTERY_TEMPERATURE_SENSOR_FAIL = -3\nbattery.BATTERY_BAD_BATTERY = -4\nbattery.BATTERY_VOLTAGE_TOO_LOW = -5\n\n\n\ncharger_state - The state of the charter circuit:\n\n\nbattery.DISCHARGING = 0\nbattery.CHARGING_ONGOING = 1\nbattery.CHARGING_COMPLETED = 2\nbattery.FAIL = -1\n\n\n\ncharge_voltage - The battery volgate in mV\n\ncharge_voltage_filtered - The battery volgate (filtered) in mV\n\ntemperature - The battery temperature in degree Celcius.\n\ncharge_current - The battery charging current in mA (the current flowing into the battery)\n\n\nNote\nThe returned value is not calibrated.\n\n\n\nbattery_capacity_left - The battery capacity left in percent of full capacity\n\n\n"
    ),
    _(
        "battery.temperature() \nReturn the battery temperature in degree Celcius.\n"
    ),
    _("battery.voltage() \nReturn the battery voltage in millivolts.\n"),
    _("hub.BT_VCP() \nCreate a new BT_VCP object.\n\n"),
    _(
        "hub.Button() \nRepresents the set of methods that can be called on any of the 4 buttons\non the Hub.\n\n"
    ),
    _(
        "hub.Image(string) \nIf string is used, it has to consist of digits 0-9 arranged into\nlines, describing the image, for example:\n\nor:\n\nwill create a 5×5 image of an X. The end of a line is indicated by a colon.\nIt’s also possible to use a newline (n) to indicate the end of a line\nlike this:\n\nor:\n\nThe other form creates an empty image with width columns and\nheight rows. Optionally buffer can be an array of\nwidth``×``height integers in range 0-9 to initialize the image, for example:\n\nor:\n\n"
    ),
    _(
        "hub.Image.get_pixel(x, y) \nReturn the brightness of pixel at column x and row y as an\ninteger between 0 and 9.\n"
    ),
    _("hub.Image.height() \nReturn the numbers of rows in the image.\n"),
    _(
        "hub.Image.set_pixel(x, y, value) \nSet the brightness of the pixel at column x and row y to the\nvalue, which has to be between 0 (dark) and 9 (bright).\nThis method will raise an exception when called on any of the built-in\nread-only images, like Image.HEART.\n"
    ),
    _("hub.Image.width() \nReturn the number of columns in the image.\n"),
    _("hub.Led() \nRepresents the center RGB LED.\n\n"),
    _(
        "hub.MotorPair() \nRepresents the set of methods that can be called on a motor pair\nobject after it is created using the hub.port.X.motor.pair()\n\n"
    ),
    _(
        "hub.MotorPair.brake() \nForce the motor driver to the Brake state. The motor driver shorts its output\nterminals and the motor will stop more quickly than if it Floats. Note\nthat this is NOT the same as actively holding motor position.\n"
    ),
    _(
        "hub.MotorPair.callback(fun(v)) \nA callback function that is invoked when the command is interrupted or completes\nThe callback function accepts one and only one parameter that indicates why the callback was\ninitiated. The following reasons can apply:\n\n0 = MOTOR_EVENT_COMPLETED\n1 = MOTOR_EVENT_INTERRUPTED\n2 = MOTOR_EVENT_STALL\n\n"
    ),
    _(
        "hub.MotorPair.float() \nForce the motor driver to the Float state. The motor driver no longer delivers\na PWM signal and the motor will coast to a stop if it is running.\n"
    ),
    _(
        "hub.MotorPair.hold() \nForce the motor driver to the Brake state. The motor will actively hold its target position.\n"
    ),
    _("hub.MotorPair.id() \nReturns the paired motor ID.\n"),
    _(
        "hub.MotorPair.pid() \nWith no parameters returns a tuple with the current used P, I and D values\nif the values have been set using this function or motor.default(). If not\nset the values returned is 0 (zero) and is invalid.\n\nNote\nAt the moment it is not possible to readout the default PID values used\nin the low-level drivers. To do this it is required to implement additional\nsub-commands in the LPF2 protocol.\n\n"
    ),
    _(
        "hub.MotorPair.preset(position0, position1) \nPresets the motor encoder with a new position value.\n\n‘position0’ - [0 - 4294967296] - Encoder value.\n‘position1’ - [0 - 4294967296] - Encoder value.\n\n"
    ),
    _(
        "hub.MotorPair.primary() \nReturns the motor object that initiated the pair() operation.\n"
    ),
    _(
        "hub.MotorPair.pwm(value0, value1) \n\nvalue [-100 - 100] Applies a PWM signal to the power pins of the port.\n\nUseful for controlling directly. The polarity of the PWM signal matches the\nsign of the value.\nA value of zero stops the PWM signal and leaves the motor driver in\nthe floating state.\n"
    ),
    _(
        "hub.MotorPair.run_at_speed(speed0, speed1, max_power, acceleration, deceleration) \nKeyword arguments:\n\nspeed [-100 - 100] - specifies the speed of the motor.\nmax_power [0 - 100] - specifies the maximum power of the motor when regulating the speed\nacceleration [0 - 10000] - specifies the time in msec for the motor to achieve specified speed\ndeceleration [0 - 10000] - specifies the time in msec for the motor to come to stop from full speed\n\n"
    ),
    _(
        "hub.MotorPair.run_for_degrees(degrees, speed0, speed1, max_power, acceleration, deceleration, stop) \nKeyword arguments:\n\ndegrees [-MAXINT - +MAXINT] - specifies the degrees to turn from current target position\nspeed [-100 - 100] - specifies the speed of the motor.\nmax_power [0 - 100] - specifies the maximum power of the motor when regulating the speed\nacceleration [0 - 10000] - specifies the time in msec for the motor to achieve specified speed\ndeceleration [0 - 10000] - specifies the time in msec for the motor to come to stop from full speed\nstop - specifies the stop state of the motor. [0 = MOTOR_STOP_FLOAT, 1 = MOTOR_STOP_BRAKE, 2 = MOTOR_STOP_HOLD]\n\n"
    ),
    _(
        "hub.MotorPair.run_for_time(msec, speed0, speed1, max_power, acceleration, deceleration, stop) \n\nmsec [0 - 65535] - Force the motor driver to run for msec milliseconds at speed. When the msec time expires the motor driver is forced to the stop state. If msec is negative a time of 0 (zero) milliseconds is assumed.\nmsec [-100 - 10000] - specifies the amount of milliseconds.\nspeed [-100 - 100] - specifies the speed of the motor.\nmax_power [0 - 100] - specifies the maximum power of the motor when regulating the speed\nacceleration [0 - 10000] - specifies the time in msec for the motor to achieve specified speed\ndeceleration [0 - 10000] - specifies the time in msec for the motor to come to stop from full speed\nstop - specifies the stop state of the motor. See ‘run_for_degrees’ method for stop types.\n\n"
    ),
    _(
        "hub.MotorPair.run_to_position(position0, position1, speed, max_power, acceleration, deceleration, stop) \nKeyword arguments:\n\nposition [-MAXINT - +MAXINT] - specifies the position of the motor.\nspeed [-100 - 100] - specifies the speed of the motor.\nmax_power [0 - 100] - specifies the maximum power of the motor when regulating the speed\nacceleration [0 - 10000] - specifies the time in msec for the motor to achieve specified speed\ndeceleration [0 - 10000] - specifies the time in msec for the motor to come to stop from full speed\nstop - specifies the stop state of the motor. See ‘run_for_degrees’ method for stop types.\n\n"
    ),
    _(
        "hub.MotorPair.secondary() \nReturns the motor object that was the parameter in the pair() operation.\n"
    ),
    _(
        "hub.MotorPair.unpair() \nUndo a pair of two motors. After call of this method the <MotorPair> object\nis invalid.\nThis method will return True if the uppair was successful. Otherwize False\nis returned (if a timeout has happend).\n"
    ),
    _("hub.Sound() \nRepresents a sound generator.\n\n"),
    _(
        "hub.Sound.beep(100-10000, 0-32767, 0-3) \nPlay a beep tone on the sound system. The parameters are all optional, and\nin order are:\n\n\nfrequency: defaults to 1000 Hz\ntime: defaults to 1000 msec\nwaveform: defaults to 0 (see below)\n\n\nThere are 4 different waveforms available:\n\n\n0 = sin\n1 = square\n2 = triangle\n3 = sawtooth\n\n\n"
    ),
    _(
        "hub.Sound.callback(fun(v)) \nRegister the given function to be called when the sound completes\nor is interrupted. If fun is None, then the callback is disabled.\nThe function accepts one of the following values:\n0 if the sound completed playing\n1 if the sound was interrupted\n"
    ),
    _("hub.Sound.off() \nTurns off the internal amplifier chip.\n"),
    _(
        "hub.Sound.on() \nTurns on the internal amplifier chip. Default at power-up.\n"
    ),
    _(
        "hub.Sound.play(filename, 12000-20000) \nPlay a sound file at the current volume. The filename must be specified, if\nthe file does not exist no sound is played.\nThe sound file must be raw 8 bit data at 16 kHz, and the second optional\nparameter specifies the playback speed. Currently the range is 12-20 kHz\nbut we may chnage that to +/- 10 or some other reasonable value.\n"
    ),
    _(
        "hub.Sound.volume(0-10) \nGet or set the volume of the sound system\n\nWith no argument, return 0-10 depending on the current volume\nWith volume given, set the volume of the sound system\n\n"
    ),
    _("hub.USB_VCP() \nCreate a new USB_VCP object.\n\n"),
    _("hub.battery() \n"),
    _("hub.display() \nCreate and return a display object.\n\n"),
    _(
        "port.X() \nRepresents the set of methods that can be called on any of the 6 ports\non the Hub.\n\n"
    ),
    _(
        "port.X.callback(fun) \nSet the function to be called when t hotplug event occurs on the port.\nIf fun is None then the callback will be disabled.\nfun() should take one parameter that indicates why the callback was\ninitiated. The following reasons can apply:\n\n0 = PORT_EVENT_DETACHED\n1 = PORT_EVENT_ATTACHED\n\n"
    ),
    _(
        "port.X.device() \nRepresents the set of methods that can be called on a device plugged\ninto any of the 6 ports on the Hub.\n\n"
    ),
    _(
        "port.X.device.get() \nReturns a list of value(s) that the currently active device mode makes\navailable. A device can be in single or combi-mode. In either case\nthe return value is a list of one or more values representing the\ndata described in the corresponing mode command.\nThere are 3 different formats available:\n\n\n0 = Raw\n1 = Pct\n2 = SI\n\n\n"
    ),
    _(
        "port.X.device.mode() \nPuts the device in the specified mode(s) depending on the specified \nmode value(s).\nIf the mode specifier is an integer, then the device is put into that mode.\nThe data returned by get() is one or more values corresponding to the\nnumber of datasets available in that mode. For example, a color sensor in\nindex color mode returns exactly one value, but in RGB mode a list of three\nvalues is returned.\nIf the mode specifier is a list, then we are asking for the device to be put\ninto combi-mode. The get() function now returns exactly the values corresponding\nto the requested modes and the datasets within that mode.\n\nNote\nThe mode specifier must be a list of 2-element tuples. If one of the list\nelements is not a 2-element tuple then it is ignored without error or warning.\n\nIf the mode specifier is an integer and it is followed by an argument that contains\na byte array - this array will be sent to the device as an output mode write\n"
    ),
    _(
        "port.X.device.pwm(value) \nKeyword arguments:\n\nvalue [-100 - 100] Applies a PWM signal to the power pins of the port.\n\nUseful for controlling directly. The polarity of the PWM signal matches the\nsign of the value.\nA value of zero stops the PWM signal and leaves the port driver in\nthe floating state.\n"
    ),
    _(
        "port.X.info() \nReturns a dictionary describing the capabilities of the device connected\nto the port. If a port has nothing plugged in, then the result is a\ndictionary with only a type key with a value of None.\nA port with a PoweredUp compatible device plugged in returns a dictionary\nlike this:\n\nfw_version : Firmware version as a 32 bit unsigned integer\nhw_version : Hardware version as a 32 bit unsigned integer\ntype : PoweredUp device type as an integer\ncombi_modes : A list of legal combi-modes as 16 bit unsigend integers\nspeed : The maximum baud rate of the device (0 for simple IDs)\nmodes : A list of dictionaries representing available modes\n\nEach modes list item dictionary has the  following keys:\n\nname : The name of the mode as a string\ncapability : The 48 capability bits as a binary string of 6 characters\nsymbol : The SI ymbol name of the data returned by the device in SI format\nraw : The min and max range of raw data expressed as a 2 element tuple\npct : The min and max range of % range data expressed as a 2 element tuple\nsi : The min and max range of si data expressed as a 2 element tuple\nmap_out : The output mapping bits as an 8 bit value\nmap_in : The infou mapping bits as an 8 bit value\nformat : A dictionary representing the format data for this mode\n\nEach format dictionary has the  following keys:\n\ndatasets : The number of data values that this mode returns\nfigures : The number of digits in the data value\ndecimals : The number of digits after the implied decimal point\ntype : The type of return data (signed 8, 16, 32 or float)\n\n"
    ),
    _("port.X.mode(mode) \nSet the mode of the port.\n"),
    _(
        "port.X.motor() \nRepresents the set of methods that can be called on a motor plugged\ninto any of the 6 ports on the Hub.\n\n"
    ),
    _(
        "port.X.motor.brake() \nForce the motor driver to the Brake state. The motor driver shorts its output\nterminals and the motor will stop more quickly than if it Floats. Note\nthat this is NOT the same as actively holding motor position.\n"
    ),
    _(
        "port.X.motor.busy(type) \nCheck to see if the motor is busy.\nKeyword argument(s):\n\n‘type’ - specifies which operation type to check for: mode/sensor (BUSY_MODE) or motor (BUSY_MOTOR).\n\n"
    ),
    _(
        "port.X.motor.callback(fun(v)) \nA callback function that is invoked when the command is interrupted or completes\nThe callback function accepts one and only one parameter that indicates why the callback was\ninitiated. The following reasons can apply:\n\n0 = MOTOR_EVENT_COMPLETED\n1 = MOTOR_EVENT_INTERRUPTED\n2 = MOTOR_EVENT_STALL\n\n"
    ),
    _(
        "port.X.motor.default() \nWith no parameters, returns a dict with the current default values that are\nused for motor operations if the corresponding keyword arguments are not specified.\nThe current defaults may be:\n\nspeed - Not implemented\nmax_power - Max % pwm to be used in regulated speed commands\nacceleration - Time in msec to reach 100% of motor design speed from 0%\ndeceleration - Time in msec to reach 0% of motor design speed from 100%\nstop - Default stop action at end of comment\npid - Default PID value used if set here or by motor.pid(). If not set the values returned is 0 (zero)\nstall - Stall detection True/False.\ncallback - A callback function that is invoked when the command is interrupted or completes\n\nThe callback function accepts one and only one parameter that indicates why the callback was\ninitiated. The following reasons can apply:\n\n0 = MOTOR_EVENT_COMPLETED\n1 = MOTOR_EVENT_INTERRUPTED\n2 = MOTOR_EVENT_STALL\n\n\nNote\nAt the moment it is not possible to readout the default PID values used\nin the low-level drivers. To do this it is required to implement additional\nsub-commands in the LPF2 protocol.\n\n"
    ),
    _(
        "port.X.motor.float() \nForce the motor driver to the Float state. The motor driver no longer delivers\na PWM signal and the motor will coast to a stop if it is running.\n"
    ),
    _(
        "port.X.motor.get() \nReturns the value(s) that the currently active device mode makes\navailable.\n\nNote\nSee the detailed explanation in the port.X.device section\n\n"
    ),
    _(
        "port.X.motor.hold() \nForce the motor driver to the Brake state. The motor will actively hold its target position.\n"
    ),
    _(
        "port.X.motor.mode(value) \nPuts the device in the specified mode.\n\nNote\nSee the detailed explanation in the port.X.device section\n\n"
    ),
    _(
        "port.X.motor.pair(motor) \nCreate a <MotorPair> object. The motor parameter must be motor object\nand cannot be the motor object that the pair() method is called on.\nIf the <MotorPair> object cannot be created due to a timeout False is returned.\nIt the object could not be created due to another fault None is retuned.\nSee the MotorPair API for methods that can be applied to a motor pair.\n"
    ),
    _(
        "port.X.motor.pid() \nWith no parameters returns a tuple with the current used P, I and D values\nif the values have been set using this function or motor.default(). If not\nset the values returned is 0 (zero) and is invalid.\n\nNote\nAt the moment it is not possible to readout the default PID values used\nin the low-level drivers. To do this it is required to implement additional\nsub-commands in the LPF2 protocol.\n\n"
    ),
    _(
        "port.X.motor.preset(position) \nPresets the motor encoder with a new position value.\n\n‘position’ - [0 - 4294967295] - Encoder value.\n\n"
    ),
    _(
        "port.X.motor.pwm(value) \nKeyword arguments:\n\nvalue [-100 - 100] Applies a PWM signal to the power pins of the port.\n\nUseful for controlling directly. The polarity of the PWM signal matches the\nsign of the value.\nA value of zero stops the PWM signal and leaves the motor driver in\nthe floating state.\n"
    ),
    _(
        "port.X.motor.run_at_speed(speed, max_power, acceleration, deceleration, stall) \nKeyword arguments:\n\nspeed [-100 - 100] - specifies the speed of the motor.\nmax_power [0 - 100] - specifies the maximum power of the motor when regulating the speed\nacceleration [0 - 10000] - specifies the time in msec for the motor to achieve specified speed\ndeceleration [0 - 10000] - specifies the time in msec for the motor to come to stop from full speed\nstall - specifies if stall detection is enabled or disabled (True/False)\n\n"
    ),
    _(
        "port.X.motor.run_for_degrees(degrees, speed, max_power, stop, acceleration, deceleration, stall) \nKeyword arguments:\n\ndegrees [-MAXINT - +MAXINT] - specifies the degrees to turn from current target position\nspeed [-100 - 100] - specifies the speed of the motor.\nmax_power [0 - 100] - specifies the maximum power of the motor when regulating the speed\nstop - specifies the stop state of the motor. [0 = MOTOR_STOP_FLOAT, 1 = MOTOR_STOP_BRAKE, 2 = MOTOR_STOP_HOLD]\nacceleration [0 - 10000] - specifies the time in msec for the motor to achieve specified speed\ndeceleration [0 - 10000] - specifies the time in msec for the motor to come to stop from full speed\nstall - specifies if stall detection is enabled or disabled (True/False)\n\n"
    ),
    _(
        "port.X.motor.run_for_time(msec, speed, max_power, stop, acceleration, deceleration, stall) \n\nmsec [0 - 65535] - Force the motor driver to run for msec milliseconds at speed. When the msec time expires the motor driver is forced to the stop state. If msec is negative a time of 0 (zero) milliseconds is assumed.\nmax_power [0 - 100] - specifies the maximum power of the motor when regulating the speed\nstop - specifies the stop state of the motor. [0 = MOTOR_STOP_FLOAT, 1 = MOTOR_STOP_BRAKE, 2 = MOTOR_STOP_HOLD]\nacceleration [0 - 10000] - specifies the time in msec for the motor to achieve specified speed\ndeceleration [0 - 10000] - specifies the time in msec for the motor to come to stop from full speed\nstall - specifies if stall detection is enabled or disabled (True/False)\n\n"
    ),
    _(
        "port.X.motor.run_to_position(position, speed, max_power, stop, acceleration, deceleration, stall) \nKeyword arguments:\n\nposition [-MAXINT - +MAXINT] - specifies the position of the motor.\nspeed [-100 - 100] - specifies the speed of the motor.\nmax_power [0 - 100] - specifies the maximum power of the motor when regulating the speed\nstop - specifies the stop state of the motor. [0 = MOTOR_STOP_FLOAT, 1 = MOTOR_STOP_BRAKE, 2 = MOTOR_STOP_HOLD]\nacceleration [0 - 10000] - specifies the time in msec for the motor to achieve specified speed\ndeceleration [0 - 10000] - specifies the time in msec for the motor to come to stop from full speed\nstall - specifies if stall detection is enabled or disabled (True/False)\n\n"
    ),
    _(
        "port.X.pwm(value) \nKeyword arguments:\n\nvalue [-100 - 100] Applies a PWM signal to the power pins of the port.\n\nUseful for controlling directly. The polarity of the PWM signal matches the\nsign of the value.\nA value of zero stops the PWM signal and leaves the port driver in\nthe floating state.\n"
    ),
]
