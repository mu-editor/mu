"""
Contains definitions for the CircuitPython APIs used on Adafruit boards so they
can be used in the editor for autocomplete and call tips.

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


ADAFRUIT_APIS = [
    _(
        "_stage.Layer(width, height, graphic, palette, grid) \nKeep internal information about a layer of graphics (either a\nGrid or a Sprite) in a format suitable for fast rendering\nwith the render() function.\n\n\nParameters:\nwidth (int) -- The width of the grid in tiles, or 1 for sprites.\nheight (int) -- The height of the grid in tiles, or 1 for sprites.\ngraphic (bytearray) -- The graphic data of the tiles.\npalette (bytearray) -- The color palette to be used.\ngrid (bytearray) -- The contents of the grid map."
    ),
    _("_stage.Layer.frame(frame, rotation) \n"),
    _("_stage.Layer.move(x, y) \n"),
    _(
        "_stage.Text(width, height, font, palette, chars) \nKeep internal information about a text of text\nin a format suitable for fast rendering\nwith the render() function.\n\n\nParameters:\nwidth (int) -- The width of the grid in tiles, or 1 for sprites.\nheight (int) -- The height of the grid in tiles, or 1 for sprites.\nfont (bytearray) -- The font data of the characters.\npalette (bytearray) -- The color palette to be used.\nchars (bytearray) -- The contents of the character grid."
    ),
    _("_stage.Text.move(x, y) \n"),
    _(
        "_stage.render(x0, y0, x1, y1, layers, buffer, spi) \nRender and send to the display a fragment of the screen.\n\n\n\n\nParameters:\nx0 (int) -- Left edge of the fragment.\ny0 (int) -- Top edge of the fragment.\nx1 (int) -- Right edge of the fragment.\ny1 (int) -- Bottom edge of the fragment.\nlayers (list) -- A list of the Layer objects.\nbuffer (bytearray) -- A buffer to use for rendering.\nspi (SPI) -- The SPI bus to use.\n\n\n\n\n\nNote that this function only sends the raw pixel data. Setting up\nthe display for receiving it and handling the chip-select and\ndata-command pins has to be done outside of it.\nThere are also no sanity checks, outside of the basic overflow\nchecking. The caller is responsible for making the passed parameters\nvalid.\nThis function is intended for internal use in the stage library\nand all the necessary checks are performed there.\n"
    ),
    _(
        "analogio.AnalogIn(pin) \nUse the AnalogIn on the given pin. The reference voltage varies by\nplatform so use reference_voltage to read the configured setting.\n\n\nParameters:pin (Pin) -- the pin to read from"
    ),
    _(
        "analogio.AnalogIn(pin) \nUse the AnalogIn on the given pin. The reference voltage varies by\nplatform so use reference_voltage to read the configured setting.\n\n\nParameters:pin (Pin) -- the pin to read from"
    ),
    _(
        "analogio.AnalogIn.deinit() \nTurn off the AnalogIn and release the pin for other use.\n"
    ),
    _(
        "analogio.AnalogIn.deinit() \nTurn off the AnalogIn and release the pin for other use.\n"
    ),
    _(
        "analogio.AnalogIn.reference_voltage() \nThe maximum voltage measurable. Also known as the reference voltage.\n\n\n\n\nReturns:the reference voltage\n\nReturn type:float\n\n\n\n"
    ),
    _(
        "analogio.AnalogIn.reference_voltage() \nThe maximum voltage measurable (also known as the reference voltage) as a\nfloat in Volts.\n"
    ),
    _(
        "analogio.AnalogIn.value() \nRead the value on the analog pin and return it.  The returned value\nwill be between 0 and 65535 inclusive (16-bit). Even if the underlying\nanalog to digital converter (ADC) is lower resolution, the result will\nbe scaled to be 16-bit.\n\n\n\n\nReturns:the data read\n\nReturn type:int\n\n\n\n"
    ),
    _(
        "analogio.AnalogIn.value() \nThe value on the analog pin between 0 and 65535 inclusive (16-bit). (read-only)\nEven if the underlying analog to digital converter (ADC) is lower\nresolution, the value is 16-bit.\n"
    ),
    _(
        "analogio.AnalogOut(pin) \nUse the AnalogOut on the given pin.\n\n\nParameters:pin (Pin) -- the pin to output to"
    ),
    _(
        "analogio.AnalogOut(pin) \nUse the AnalogOut on the given pin.\n\n\nParameters:pin (Pin) -- the pin to output to"
    ),
    _(
        "analogio.AnalogOut.deinit() \nTurn off the AnalogOut and release the pin for other use.\n"
    ),
    _(
        "analogio.AnalogOut.deinit() \nTurn off the AnalogOut and release the pin for other use.\n"
    ),
    _(
        "analogio.AnalogOut.value() \nThe value on the analog pin.  The value must be between 0 and 65535\ninclusive (16-bit). Even if the underlying digital to analog converter\nis lower resolution, the input must be scaled to be 16-bit.\n\n\n\n\nReturns:the last value written\n\nReturn type:int\n\n\n\n"
    ),
    _(
        "analogio.AnalogOut.value() \nThe value on the analog pin between 0 and 65535 inclusive (16-bit). (write-only)\nEven if the underlying digital to analog converter (DAC) is lower\nresolution, the value is 16-bit.\n"
    ),
    _(
        "audiobusio.I2SOut(bit_clock, word_select, data, *, left_justified) \nCreate a I2SOut object associated with the given pins.\n\n\nParameters:\nbit_clock (Pin) -- The bit clock (or serial clock) pin\nword_select (Pin) -- The word select (or left/right clock) pin\ndata (Pin) -- The data pin\nleft_justified (bool) -- True when data bits are aligned with the word select clock. False\nwhen they are shifted by one to match classic I2S protocol."
    ),
    _(
        "audiobusio.I2SOut.deinit() \nDeinitialises the I2SOut and releases any hardware resources for reuse.\n"
    ),
    _(
        "audiobusio.I2SOut.paused() \nTrue when playback is paused. (read-only)\n"
    ),
    _(
        "audiobusio.I2SOut.playing() \nTrue when the audio sample is being output. (read-only)\n"
    ),
    _(
        "audiobusio.PDMIn(clock_pin, data_pin, *, frequency=8000, bit_depth=8, mono=True, oversample=64) \nCreate a PDMIn object associated with the given pins. This allows you to\nrecord audio signals from the given pins. Individual ports may put further\nrestrictions on the recording parameters.\n\n\nParameters:\nclock_pin (Pin) -- The pin to output the clock to\ndata_pin (Pin) -- The pin to read the data from\nfrequency (int) -- Target frequency of the resulting samples. Check frequency for real value.\nbit_depth (int) -- Final number of bits per sample. Must be divisible by 8\nmono (bool) -- True when capturing a single channel of audio, captures two channels otherwise\noversample (int) -- Number of single bit samples to decimate into a final sample. Must be divisible by 8"
    ),
    _(
        "audiobusio.PDMIn(clock_pin, data_pin, *, sample_rate=16000, bit_depth=8, mono=True, oversample=64, startup_delay=0.11) \nCreate a PDMIn object associated with the given pins. This allows you to\nrecord audio signals from the given pins. Individual ports may put further\nrestrictions on the recording parameters. The overall sample rate is\ndetermined by sample_rate x oversample, and the total must be 1MHz or\nhigher, so sample_rate must be a minimum of 16000.\n\n\nParameters:\nclock_pin (Pin) -- The pin to output the clock to\ndata_pin (Pin) -- The pin to read the data from\nsample_rate (int) -- Target sample_rate of the resulting samples. Check sample_rate for actual value.\nMinimum sample_rate is about 16000 Hz.\nbit_depth (int) -- Final number of bits per sample. Must be divisible by 8\nmono (bool) -- True when capturing a single channel of audio, captures two channels otherwise\noversample (int) -- Number of single bit samples to decimate into a final sample. Must be divisible by 8\nstartup_delay (float) -- seconds to wait after starting microphone clock\nto allow microphone to turn on. Most require only 0.01s; some require 0.1s. Longer is safer.\nMust be in range 0.0-1.0 seconds."
    ),
    _(
        "audiobusio.PDMIn.deinit() \nDeinitialises the PWMOut and releases any hardware resources for reuse.\n"
    ),
    _(
        "audiobusio.PDMIn.deinit() \nDeinitialises the PDMIn and releases any hardware resources for reuse.\n"
    ),
    _(
        "audiobusio.PDMIn.frequency() \nThe actual frequency of the recording. This may not match the constructed\nfrequency due to internal clock limitations.\n"
    ),
    _(
        "audiobusio.PDMIn.sample_rate() \nThe actual sample_rate of the recording. This may not match the constructed\nsample rate due to internal clock limitations.\n"
    ),
    _(
        "audioio.AudioOut(pin, sample_source) \nCreate a AudioOut object associated with the given pin. This allows you to\nplay audio signals out on the given pin. Sample_source must be a bytes-like object.\n\nThe sample itself should consist of 16 bit samples and be mono.\nMicrocontrollers with a lower output resolution will use the highest order\nbits to output. For example, the SAMD21 has a 10 bit DAC that ignores the\nlowest 6 bits when playing 16 bit samples.\n\n\nParameters:\npin (Pin) -- The pin to output to\nsample_source (bytes-like) -- The source of the sample"
    ),
    _(
        "audioio.AudioOut(left_channel, right_channel=None) \nCreate a AudioOut object associated with the given pin(s). This allows you to\nplay audio signals out on the given pin(s).\n\n\nParameters:\nleft_channel (Pin) -- The pin to output the left channel to\nright_channel (Pin) -- The pin to output the right channel to"
    ),
    _(
        "audioio.AudioOut.deinit() \nDeinitialises the PWMOut and releases any hardware resources for reuse.\n"
    ),
    _(
        "audioio.AudioOut.deinit() \nDeinitialises the AudioOut and releases any hardware resources for reuse.\n"
    ),
    _(
        "audioio.AudioOut.frequency() \n32 bit value that dictates how quickly samples are loaded into the DAC\nin Hertz (cycles per second). When the sample is looped, this can change\nthe pitch output without changing the underlying sample.\n"
    ),
    _(
        "audioio.AudioOut.paused() \nTrue when playback is paused. (read-only)\n"
    ),
    _(
        "audioio.AudioOut.playing() \nTrue when the audio sample is being output.\n"
    ),
    _(
        "audioio.AudioOut.playing() \nTrue when an audio sample is being output even if paused. (read-only)\n"
    ),
    _(
        "audioio.RawSample(buffer, *, channel_count=1, sample_rate=8000) \nCreate a RawSample based on the given buffer of signed values. If channel_count is more than\n1 then each channel’s samples should alternate. In other words, for a two channel buffer, the\nfirst sample will be for channel 1, the second sample will be for channel two, the third for\nchannel 1 and so on.\n\n\nParameters:\nbuffer (array) -- An array.array with samples\nchannel_count (int) -- The number of channels in the buffer\nsample_rate (int) -- The desired playback sample rate"
    ),
    _(
        "audioio.RawSample.deinit() \nDeinitialises the AudioOut and releases any hardware resources for reuse.\n"
    ),
    _(
        "audioio.RawSample.sample_rate() \n32 bit value that dictates how quickly samples are played in Hertz (cycles per second).\nWhen the sample is looped, this can change the pitch output without changing the underlying\nsample. This will not change the sample rate of any active playback. Call play again to\nchange it.\n"
    ),
    _(
        "audioio.WaveFile(filename) \nLoad a .wav file for playback with audioio.AudioOut or audiobusio.I2SOut.\n\n\nParameters:file (bytes-like) -- Already opened wave file"
    ),
    _(
        "audioio.WaveFile.deinit() \nDeinitialises the WaveFile and releases all memory resources for reuse.\n"
    ),
    _(
        "audioio.WaveFile.sample_rate() \n32 bit value that dictates how quickly samples are loaded into the DAC\nin Hertz (cycles per second). When the sample is looped, this can change\nthe pitch output without changing the underlying sample.\n"
    ),
    _(
        "bitbangio.I2C(scl, sda, *, frequency=400000) \nI2C is a two-wire protocol for communicating between devices.  At the\nphysical level it consists of 2 wires: SCL and SDA, the clock and data\nlines respectively.\n\n\nParameters:\nscl (Pin) -- The clock pin\nsda (Pin) -- The data pin\nfrequency (int) -- The clock frequency of the bus"
    ),
    _(
        "bitbangio.I2C(scl, sda, *, frequency=400000) \nI2C is a two-wire protocol for communicating between devices.  At the\nphysical level it consists of 2 wires: SCL and SDA, the clock and data\nlines respectively.\n\n\nParameters:\nscl (Pin) -- The clock pin\nsda (Pin) -- The data pin\nfrequency (int) -- The clock frequency of the bus\ntimeout (int) -- The maximum clock stretching timeout in microseconds"
    ),
    _(
        "bitbangio.I2C.deinit() \nReleases control of the underlying hardware so other classes can use it.\n"
    ),
    _(
        "bitbangio.I2C.deinit() \nReleases control of the underlying hardware so other classes can use it.\n"
    ),
    _(
        "bitbangio.OneWire(pin) \nCreate a OneWire object associated with the given pin. The object\nimplements the lowest level timing-sensitive bits of the protocol.\n\n\nParameters:pin (Pin) -- Pin to read pulses from."
    ),
    _(
        "bitbangio.OneWire(pin) \nCreate a OneWire object associated with the given pin. The object\nimplements the lowest level timing-sensitive bits of the protocol.\n\n\nParameters:pin (Pin) -- Pin to read pulses from."
    ),
    _(
        "bitbangio.OneWire.deinit() \nDeinitialize the OneWire bus and release any hardware resources for reuse.\n"
    ),
    _(
        "bitbangio.OneWire.deinit() \nDeinitialize the OneWire bus and release any hardware resources for reuse.\n"
    ),
    _(
        "bitbangio.SPI(clock, MOSI=None, MISO=None) \n\nParameters:\nclock (Pin) -- the pin to use for the clock.\nMOSI (Pin) -- the Master Out Slave In pin.\nMISO (Pin) -- the Master In Slave Out pin."
    ),
    _(
        "bitbangio.SPI(clock, MOSI=None, MISO=None) \n\nParameters:\nclock (Pin) -- the pin to use for the clock.\nMOSI (Pin) -- the Master Out Slave In pin.\nMISO (Pin) -- the Master In Slave Out pin."
    ),
    _("bitbangio.SPI.deinit() \nTurn off the SPI bus.\n"),
    _("bitbangio.SPI.deinit() \nTurn off the SPI bus.\n"),
    _(
        "busio.I2C(scl, sda, *, frequency=400000) \nI2C is a two-wire protocol for communicating between devices.  At the\nphysical level it consists of 2 wires: SCL and SDA, the clock and data\nlines respectively.\n\n\nParameters:\nscl (Pin) -- The clock pin\nsda (Pin) -- The data pin\nfrequency (int) -- The clock frequency in Hertz"
    ),
    _(
        "busio.I2C(scl, sda, *, frequency=400000) \nI2C is a two-wire protocol for communicating between devices.  At the\nphysical level it consists of 2 wires: SCL and SDA, the clock and data\nlines respectively.\n\n\nParameters:\nscl (Pin) -- The clock pin\nsda (Pin) -- The data pin\nfrequency (int) -- The clock frequency in Hertz\ntimeout (int) -- The maximum clock stretching timeut - only for bitbang"
    ),
    _(
        "busio.I2C.deinit() \nReleases control of the underlying hardware so other classes can use it.\n"
    ),
    _(
        "busio.I2C.deinit() \nReleases control of the underlying hardware so other classes can use it.\n"
    ),
    _(
        "busio.OneWire(pin) \nCreate a OneWire object associated with the given pin. The object\nimplements the lowest level timing-sensitive bits of the protocol.\n\n\nParameters:pin (Pin) -- Pin connected to the OneWire bus"
    ),
    _(
        "busio.OneWire(pin) \nCreate a OneWire object associated with the given pin. The object\nimplements the lowest level timing-sensitive bits of the protocol.\n\n\nParameters:pin (Pin) -- Pin connected to the OneWire bus"
    ),
    _(
        "busio.OneWire.deinit() \nDeinitialize the OneWire bus and release any hardware resources for reuse.\n"
    ),
    _(
        "busio.OneWire.deinit() \nDeinitialize the OneWire bus and release any hardware resources for reuse.\n"
    ),
    _(
        "busio.SPI(clock, MOSI=None, MISO=None) \n\nParameters:\nclock (Pin) -- the pin to use for the clock.\nMOSI (Pin) -- the Master Out Slave In pin.\nMISO (Pin) -- the Master In Slave Out pin."
    ),
    _(
        "busio.SPI(clock, MOSI=None, MISO=None) \n\nParameters:\nclock (Pin) -- the pin to use for the clock.\nMOSI (Pin) -- the Master Out Slave In pin.\nMISO (Pin) -- the Master In Slave Out pin."
    ),
    _("busio.SPI.deinit() \nTurn off the SPI bus.\n"),
    _("busio.SPI.deinit() \nTurn off the SPI bus.\n"),
    _(
        "busio.SPI.frequency() \nThe actual SPI bus frequency. This may not match the frequency requested\ndue to internal limitations.\n"
    ),
    _(
        "busio.UART(tx, rx, *, baudrate=9600, bits=8, parity=None, stop=1, timeout=1000, receiver_buffer_size=64) \nA common bidirectional serial protocol that uses an an agreed upon speed\nrather than a shared clock line.\n\n\nParameters:\ntx (Pin) -- the pin to transmit with\nrx (Pin) -- the pin to receive on\nbaudrate (int) -- the transmit and receive speed"
    ),
    _(
        "busio.UART(tx, rx, *, baudrate=9600, bits=8, parity=None, stop=1, timeout=1000, receiver_buffer_size=64) \nA common bidirectional serial protocol that uses an an agreed upon speed\nrather than a shared clock line.\n\n\nParameters:\ntx (Pin) -- the pin to transmit with, or None if this UART is receive-only.\nrx (Pin) -- the pin to receive on, or None if this UART is transmit-only.\nbaudrate (int) -- the transmit and receive speed."
    ),
    _(
        "busio.UART.Parity() \nEnum-like class to define the parity used to verify correct data transfer.\n\n"
    ),
    _(
        "busio.UART.Parity() \nEnum-like class to define the parity used to verify correct data transfer.\n\n"
    ),
    _("busio.UART.Parity.EVEN() \nTotal number of ones should be even.\n"),
    _("busio.UART.Parity.EVEN() \nTotal number of ones should be even.\n"),
    _("busio.UART.Parity.ODD() \nTotal number of ones should be odd.\n"),
    _("busio.UART.Parity.ODD() \nTotal number of ones should be odd.\n"),
    _("busio.UART.baudrate() \nThe current baudrate.\n"),
    _(
        "busio.UART.deinit() \nDeinitialises the UART and releases any hardware resources for reuse.\n"
    ),
    _(
        "busio.UART.deinit() \nDeinitialises the UART and releases any hardware resources for reuse.\n"
    ),
    _(
        "digitalio.DigitalInOut(pin) \nCreate a new DigitalInOut object associated with the pin. Defaults to input\nwith no pull. Use switch_to_input() and\nswitch_to_output() to change the direction.\n\n\nParameters:pin (Pin) -- The pin to control"
    ),
    _(
        "digitalio.DigitalInOut(pin) \nCreate a new DigitalInOut object associated with the pin. Defaults to input\nwith no pull. Use switch_to_input() and\nswitch_to_output() to change the direction.\n\n\nParameters:pin (Pin) -- The pin to control"
    ),
    _(
        "digitalio.DigitalInOut.Direction() \nEnum-like class to define which direction the digital values are\ngoing.\n\n"
    ),
    _(
        "digitalio.DigitalInOut.Direction() \nEnum-like class to define which direction the digital values are\ngoing.\n\n"
    ),
    _("digitalio.DigitalInOut.Direction.INPUT() \nRead digital data in\n"),
    _("digitalio.DigitalInOut.Direction.INPUT() \nRead digital data in\n"),
    _("digitalio.DigitalInOut.Direction.OUTPUT() \nWrite digital data out\n"),
    _("digitalio.DigitalInOut.Direction.OUTPUT() \nWrite digital data out\n"),
    _(
        "digitalio.DigitalInOut.deinit() \nTurn off the DigitalInOut and release the pin for other use.\n"
    ),
    _(
        "digitalio.DigitalInOut.deinit() \nTurn off the DigitalInOut and release the pin for other use.\n"
    ),
    _(
        "digitalio.DigitalInOut.direction() \nThe direction of the pin.\nSetting this will use the defaults from the corresponding\nswitch_to_input() or switch_to_output() method. If\nyou want to set pull, value or drive mode prior to switching, then use\nthose methods instead.\n"
    ),
    _(
        "digitalio.DigitalInOut.direction() \nThe direction of the pin.\nSetting this will use the defaults from the corresponding\nswitch_to_input() or switch_to_output() method. If\nyou want to set pull, value or drive mode prior to switching, then use\nthose methods instead.\n"
    ),
    _(
        "digitalio.DigitalInOut.drive_mode() \nGet or set the pin drive mode.\n"
    ),
    _(
        "digitalio.DigitalInOut.drive_mode() \nThe pin drive mode. One of:\n\ndigitalio.DriveMode.PUSH_PULL\ndigitalio.DriveMode.OPEN_DRAIN\n\n"
    ),
    _(
        "digitalio.DigitalInOut.pull() \nGet or set the pin pull. Values may be digitalio.Pull.UP,\ndigitalio.Pull.DOWN or None.\n\n\n\n\nRaises:AttributeError -- if the direction is ~`digitalio.Direction.OUTPUT`.\n\n\n\n"
    ),
    _(
        "digitalio.DigitalInOut.pull() \nThe pin pull direction. One of:\n\ndigitalio.Pull.UP\ndigitalio.Pull.DOWN\nNone\n\n\n\n\n\nRaises:AttributeError -- if direction is OUTPUT.\n\n\n\n"
    ),
    _(
        "digitalio.DigitalInOut.value() \nThe digital logic level of the pin.\n"
    ),
    _(
        "digitalio.DigitalInOut.value() \nThe digital logic level of the pin.\n"
    ),
    _(
        "digitalio.DriveMode() \nEnum-like class to define the drive mode used when outputting\ndigital values.\n\n"
    ),
    _(
        "digitalio.DriveMode() \nEnum-like class to define the drive mode used when outputting\ndigital values.\n\n"
    ),
    _(
        "digitalio.DriveMode.OPEN_DRAIN() \nOutput low digital values but go into high z for digital high. This is\nuseful for i2c and other protocols that share a digital line.\n"
    ),
    _(
        "digitalio.DriveMode.OPEN_DRAIN() \nOutput low digital values but go into high z for digital high. This is\nuseful for i2c and other protocols that share a digital line.\n"
    ),
    _(
        "digitalio.DriveMode.PUSH_PULL() \nOutput both high and low digital values\n"
    ),
    _(
        "digitalio.DriveMode.PUSH_PULL() \nOutput both high and low digital values\n"
    ),
    _(
        "digitalio.Pull() \nEnum-like class to define the pull value, if any, used while reading\ndigital values in.\n\n"
    ),
    _(
        "digitalio.Pull() \nEnum-like class to define the pull value, if any, used while reading\ndigital values in.\n\n"
    ),
    _(
        "digitalio.Pull.DOWN() \nWhen the input line isn’t being driven the pull down can pull the\nstate of the line low so it reads as false.\n"
    ),
    _(
        "digitalio.Pull.DOWN() \nWhen the input line isn’t being driven the pull down can pull the\nstate of the line low so it reads as false.\n"
    ),
    _(
        "digitalio.Pull.UP() \nWhen the input line isn’t being driven the pull up can pull the state\nof the line high so it reads as true.\n"
    ),
    _(
        "digitalio.Pull.UP() \nWhen the input line isn’t being driven the pull up can pull the state\nof the line high so it reads as true.\n"
    ),
    _(
        "gamepad.GamePad(b1, b2, b3, b4, b5, b6, b7, b8) \nInitializes button scanning routines.\n\nThe b1-b8 parameters are DigitalInOut objects, which\nimmediately get switched to input with a pull-up, and then scanned\nregularly for button presses. The order is the same as the order of\nbits returned by the get_pressed function. You can re-initialize\nit with different keys, then the new object will replace the previous\none.\n\nThe basic feature required here is the ability to poll the keys at\nregular intervals (so that de-bouncing is consistent) and fast enough\n(so that we don’t miss short button presses) while at the same time\nletting the user code run normally, call blocking functions and wait\non delays.\n\nThey button presses are accumulated, until the get_pressed method\nis called, at which point the button state is cleared, and the new\nbutton presses start to be recorded.\n\n"
    ),
    _("gamepad.GamePad.deinit() \nDisable button scanning.\n"),
    _(
        "gamepad.GamePad.get_pressed() \nGet the status of buttons pressed since the last call and clear it.\nReturns an 8-bit number, with bits that correspond to buttons,\nwhich have been pressed (or held down) since the last call to this\nfunction set to 1, and the remaining bits set to 0. Then it clears\nthe button state, so that new button presses (or buttons that are\nheld down) can be recorded for the next call.\n"
    ),
    _("math.acos(x) \nReturn the inverse cosine of x.\n"),
    _("math.asin(x) \nReturn the inverse sine of x.\n"),
    _("math.atan(x) \nReturn the inverse tangent of x.\n"),
    _(
        "math.atan2(y, x) \nReturn the principal value of the inverse tangent of y/x.\n"
    ),
    _(
        "math.ceil(x) \nReturn an integer, being x rounded towards positive infinity.\n"
    ),
    _("math.copysign(x, y) \nReturn x with the sign of y.\n"),
    _("math.cos(x) \nReturn the cosine of x.\n"),
    _("math.degrees(x) \nReturn radians x converted to degrees.\n"),
    _("math.exp(x) \nReturn the exponential of x.\n"),
    _("math.fabs(x) \nReturn the absolute value of x.\n"),
    _(
        "math.floor(x) \nReturn an integer, being x rounded towards negative infinity.\n"
    ),
    _("math.fmod(x, y) \nReturn the remainder of x/y.\n"),
    _(
        "math.frexp(x) \nDecomposes a floating-point number into its mantissa and exponent.\nThe returned value is the tuple (m, e) such that x == m * 2**e\nexactly.  If x == 0 then the function returns (0.0, 0), otherwise\nthe relation 0.5 <= abs(m) < 1 holds.\n"
    ),
    _("math.isfinite(x) \nReturn True if x is finite.\n"),
    _("math.isinf(x) \nReturn True if x is infinite.\n"),
    _("math.isnan(x) \nReturn True if x is not-a-number\n"),
    _("math.ldexp(x, exp) \nReturn x * (2**exp).\n"),
    _(
        "math.modf(x) \nReturn a tuple of two floats, being the fractional and integral parts of\nx.  Both return values have the same sign as x.\n"
    ),
    _("math.pow(x, y) \nReturns x to the power of y.\n"),
    _("math.radians(x) \nReturn degrees x converted to radians.\n"),
    _("math.sin(x) \nReturn the sine of x.\n"),
    _("math.sqrt(x) \nReturns the square root of x.\n"),
    _("math.tan(x) \nReturn the tangent of x.\n"),
    _("math.trunc(x) \nReturn an integer, being x rounded towards 0.\n"),
    _(
        "microcontroller.Pin() \nIdentifies an IO pin on the microcontroller. They are fixed by the\nhardware so they cannot be constructed on demand. Instead, use\nboard or microcontroller.pin to reference the desired pin.\n\n"
    ),
    _(
        "microcontroller.Pin() \nIdentifies an IO pin on the microcontroller. They are fixed by the\nhardware so they cannot be constructed on demand. Instead, use\nboard or microcontroller.pin to reference the desired pin.\n\n"
    ),
    _("microcontroller.Processor() \n"),
    _(
        "microcontroller.Processor() \nYou cannot create an instance of microcontroller.Processor.\nUse microcontroller.cpu to access the sole instance available.\n\n"
    ),
    _(
        "microcontroller.Processor.frequency() \nThe CPU operating frequency as an int, in Hertz. (read-only)\n"
    ),
    _(
        "microcontroller.Processor.temperature() \nThe on-chip temperature, in Celsius, as a float. (read-only)\nIs None if the temperature is not available.\n"
    ),
    _(
        "microcontroller.Processor.uid() \nThe unique id (aka serial number) of the chip as a bytearray. (read-only)\n"
    ),
    _(
        "microcontroller.RunMode() \nEnum-like class to define the run mode of the microcontroller and\nCircuitPython.\n\n"
    ),
    _("microcontroller.RunMode.BOOTLOADER() \nRun the bootloader.\n"),
    _("microcontroller.RunMode.NORMAL() \nRun CircuitPython as normal.\n"),
    _(
        "microcontroller.RunMode.SAFE_MODE() \nRun CircuitPython in safe mode. User code will not be run and the\nfile system will be writeable over USB.\n"
    ),
    _(
        "multiterminal.clear_secondary_terminal() \nClears the secondary terminal.\n"
    ),
    _(
        "multiterminal.clear_secondary_terminal() \nClears the secondary terminal.\n"
    ),
    _(
        "multiterminal.get_secondary_terminal() \nReturns the current secondary terminal.\n"
    ),
    _(
        "multiterminal.get_secondary_terminal() \nReturns the current secondary terminal.\n"
    ),
    _(
        "multiterminal.schedule_secondary_terminal_read(socket) \nIn cases where the underlying OS is doing task scheduling, this notifies\nthe OS when more data is available on the socket to read. This is useful\nas a callback for lwip sockets.\n"
    ),
    _(
        "multiterminal.schedule_secondary_terminal_read(socket) \nIn cases where the underlying OS is doing task scheduling, this notifies\nthe OS when more data is available on the socket to read. This is useful\nas a callback for lwip sockets.\n"
    ),
    _(
        "multiterminal.set_secondary_terminal(stream) \nRead additional input from the given stream and write out back to it.\nThis doesn’t replace the core stream (usually UART or native USB) but is\nmixed in instead.\n\n\n\n\nParameters:stream (stream) -- secondary stream\n\n\n\n"
    ),
    _(
        "multiterminal.set_secondary_terminal(stream) \nRead additional input from the given stream and write out back to it.\nThis doesn’t replace the core stream (usually UART or native USB) but is\nmixed in instead.\n\n\n\n\nParameters:stream (stream) -- secondary stream\n\n\n\n"
    ),
    _(
        "nvm.ByteArray() \nNot currently dynamically supported. Access the sole instance through microcontroller.nvm.\n\n"
    ),
    _(
        "nvm.ByteArray() \nNot currently dynamically supported. Access the sole instance through microcontroller.nvm.\n\n"
    ),
    _("os.chdir(path) \nChange current directory.\n"),
    _("os.chdir(path) \nChange current directory.\n"),
    _("os.getcwd() \nGet the current directory.\n"),
    _("os.getcwd() \nGet the current directory.\n"),
    _(
        "os.listdir(dir) \nWith no argument, list the current directory.  Otherwise list the given directory.\n"
    ),
    _(
        "os.listdir(dir) \nWith no argument, list the current directory.  Otherwise list the given directory.\n"
    ),
    _("os.mkdir(path) \nCreate a new directory.\n"),
    _("os.mkdir(path) \nCreate a new directory.\n"),
    _("os.remove(path) \nRemove a file.\n"),
    _("os.remove(path) \nRemove a file.\n"),
    _("os.rename(old_path, new_path) \nRename a file.\n"),
    _("os.rename(old_path, new_path) \nRename a file.\n"),
    _("os.rmdir(path) \nRemove a directory.\n"),
    _("os.rmdir(path) \nRemove a directory.\n"),
    _("os.stat(path) \nGet the status of a file or directory.\n"),
    _("os.stat(path) \nGet the status of a file or directory.\n"),
    _(
        "os.statvfs(path) \nGet the status of a fileystem.\nReturns a tuple with the filesystem information in the following order:\n\n\nf_bsize -- file system block size\nf_frsize -- fragment size\nf_blocks -- size of fs in f_frsize units\nf_bfree -- number of free blocks\nf_bavail -- number of free blocks for unpriviliged users\nf_files -- number of inodes\nf_ffree -- number of free inodes\nf_favail -- number of free inodes for unpriviliged users\nf_flag -- mount flags\nf_namemax -- maximum filename length\n\n\nParameters related to inodes: f_files, f_ffree, f_avail\nand the f_flags parameter may return 0 as they can be unavailable\nin a port-specific implementation.\n"
    ),
    _(
        "os.statvfs(path) \nGet the status of a fileystem.\nReturns a tuple with the filesystem information in the following order:\n\n\nf_bsize -- file system block size\nf_frsize -- fragment size\nf_blocks -- size of fs in f_frsize units\nf_bfree -- number of free blocks\nf_bavail -- number of free blocks for unpriviliged users\nf_files -- number of inodes\nf_ffree -- number of free inodes\nf_favail -- number of free inodes for unpriviliged users\nf_flag -- mount flags\nf_namemax -- maximum filename length\n\n\nParameters related to inodes: f_files, f_ffree, f_avail\nand the f_flags parameter may return 0 as they can be unavailable\nin a port-specific implementation.\n"
    ),
    _("os.sync() \nSync all filesystems.\n"),
    _("os.sync() \nSync all filesystems.\n"),
    _(
        "os.uname() \nReturns a named tuple of operating specific and CircuitPython port\nspecific information.\n"
    ),
    _(
        "os.uname() \nReturns a named tuple of operating specific and CircuitPython port\nspecific information.\n"
    ),
    _(
        "os.urandom(size) \nReturns a string of size random bytes based on a hardware True Random\nNumber Generator. When not available, it will raise a NotImplementedError.\n"
    ),
    _(
        "os.urandom(size) \nReturns a string of size random bytes based on a hardware True Random\nNumber Generator. When not available, it will raise a NotImplementedError.\n"
    ),
    _(
        "pulseio.PWMOut(pin, *, duty_cycle=0, frequency=500, variable_frequency=False) \nCreate a PWM object associated with the given pin. This allows you to\nwrite PWM signals out on the given pin. Frequency is fixed after init\nunless variable_frequency is True.\n\n\nParameters:\npin (Pin) -- The pin to output to\nduty_cycle (int) -- The fraction of each pulse which is high. 16-bit\nfrequency (int) -- The target frequency in Hertz (32-bit)\nvariable_frequency (bool) -- True if the frequency will change over time"
    ),
    _(
        "pulseio.PWMOut(pin, *, duty_cycle=0, frequency=500, variable_frequency=False) \nCreate a PWM object associated with the given pin. This allows you to\nwrite PWM signals out on the given pin. Frequency is fixed after init\nunless variable_frequency is True.\n\n\nParameters:\npin (Pin) -- The pin to output to\nduty_cycle (int) -- The fraction of each pulse which is high. 16-bit\nfrequency (int) -- The target frequency in Hertz (32-bit)\nvariable_frequency (bool) -- True if the frequency will change over time"
    ),
    _(
        "pulseio.PWMOut.deinit() \nDeinitialises the PWMOut and releases any hardware resources for reuse.\n"
    ),
    _(
        "pulseio.PWMOut.deinit() \nDeinitialises the PWMOut and releases any hardware resources for reuse.\n"
    ),
    _(
        "pulseio.PWMOut.duty_cycle() \n16 bit value that dictates how much of one cycle is high (1) versus low\n(0). 0xffff will always be high, 0 will always be low and 0x7fff will\nbe half high and then half low.\n"
    ),
    _(
        "pulseio.PWMOut.duty_cycle() \n16 bit value that dictates how much of one cycle is high (1) versus low\n(0). 0xffff will always be high, 0 will always be low and 0x7fff will\nbe half high and then half low.\n"
    ),
    _(
        "pulseio.PWMOut.frequency() \n32 bit value that dictates the PWM frequency in Hertz (cycles per\nsecond). Only writeable when constructed with variable_frequency=True.\n"
    ),
    _(
        "pulseio.PWMOut.frequency() \n32 bit value that dictates the PWM frequency in Hertz (cycles per\nsecond). Only writeable when constructed with variable_frequency=True.\n"
    ),
    _(
        "pulseio.PulseIn(pin, maxlen=2, *, idle_state=False) \nCreate a PulseIn object associated with the given pin. The object acts as\na read-only sequence of pulse lengths with a given max length. When it is\nactive, new pulse lengths are added to the end of the list. When there is\nno more room (len() == maxlen) the oldest pulse length is removed to\nmake room.\n\n\nParameters:\npin (Pin) -- Pin to read pulses from.\nmaxlen (int) -- Maximum number of pulse durations to store at once\nidle_state (bool) -- Idle state of the pin. At start and after resume\nthe first recorded pulse will the opposite state from idle."
    ),
    _(
        "pulseio.PulseIn(pin, maxlen=2, *, idle_state=False) \nCreate a PulseIn object associated with the given pin. The object acts as\na read-only sequence of pulse lengths with a given max length. When it is\nactive, new pulse lengths are added to the end of the list. When there is\nno more room (len() == maxlen) the oldest pulse length is removed to\nmake room.\n\n\nParameters:\npin (Pin) -- Pin to read pulses from.\nmaxlen (int) -- Maximum number of pulse durations to store at once\nidle_state (bool) -- Idle state of the pin. At start and after resume\nthe first recorded pulse will the opposite state from idle."
    ),
    _(
        "pulseio.PulseIn.deinit() \nDeinitialises the PulseIn and releases any hardware resources for reuse.\n"
    ),
    _(
        "pulseio.PulseIn.deinit() \nDeinitialises the PulseIn and releases any hardware resources for reuse.\n"
    ),
    _(
        "pulseio.PulseIn.maxlen() \nReturns the maximum length of the PulseIn. When len() is equal to maxlen,\nit is unclear which pulses are active and which are idle.\n"
    ),
    _(
        "pulseio.PulseIn.maxlen() \nThe maximum length of the PulseIn. When len() is equal to maxlen,\nit is unclear which pulses are active and which are idle.\n"
    ),
    _(
        "pulseio.PulseIn.paused() \nTrue when pulse capture is paused as a result of pause() or an error during capture\nsuch as a signal that is too fast.\n"
    ),
    _(
        "pulseio.PulseOut(carrier) \nCreate a PulseOut object associated with the given PWM out experience.\n\n\nParameters:carrier (PWMOut) -- PWMOut that is set to output on the desired pin."
    ),
    _(
        "pulseio.PulseOut(carrier) \nCreate a PulseOut object associated with the given PWM out experience.\n\n\nParameters:carrier (PWMOut) -- PWMOut that is set to output on the desired pin."
    ),
    _(
        "pulseio.PulseOut.deinit() \nDeinitialises the PulseOut and releases any hardware resources for reuse.\n"
    ),
    _(
        "pulseio.PulseOut.deinit() \nDeinitialises the PulseOut and releases any hardware resources for reuse.\n"
    ),
    _(
        "random.choice(seq) \nReturns a randomly selected element from the given sequence. Raises\nIndexError when the sequence is empty.\n"
    ),
    _(
        "random.choice(seq) \nReturns a randomly selected element from the given sequence. Raises\nIndexError when the sequence is empty.\n"
    ),
    _("random.getrandbits(k) \nReturns an integer with k random bits.\n"),
    _("random.getrandbits(k) \nReturns an integer with k random bits.\n"),
    _(
        "random.randint(a, b) \nReturns a randomly selected integer between a and b inclusive. Equivalent\nto randrange(a, b + 1, 1)\n"
    ),
    _(
        "random.randint(a, b) \nReturns a randomly selected integer between a and b inclusive. Equivalent\nto randrange(a, b + 1, 1)\n"
    ),
    _("random.random() \nReturns a random float between 0 and 1.0.\n"),
    _("random.random() \nReturns a random float between 0 and 1.0.\n"),
    _(
        "random.randrange(stop) \nReturns a randomly selected integer from range(start, stop, step).\n"
    ),
    _(
        "random.randrange(stop) \nReturns a randomly selected integer from range(start, stop, step).\n"
    ),
    _(
        "random.seed(seed) \nSets the starting seed of the random  number generation. Further calls to\nrandom will return deterministic results afterwards.\n"
    ),
    _(
        "random.seed(seed) \nSets the starting seed of the random  number generation. Further calls to\nrandom will return deterministic results afterwards.\n"
    ),
    _(
        "random.uniform(a, b) \nReturns a random float between a and b. It may or may not be inclusive\ndepending on float rounding.\n"
    ),
    _(
        "random.uniform(a, b) \nReturns a random float between a and b. It may or may not be inclusive\ndepending on float rounding.\n"
    ),
    _(
        "rotaryio.IncrementalEncoder(pin_a, pin_b) \nCreate an IncrementalEncoder object associated with the given pins. It tracks the positional\nstate of an incremental rotary encoder (also known as a quadrature encoder.) Position is\nrelative to the position when the object is contructed.\n\n\nParameters:\npin_a (Pin) -- First pin to read pulses from.\npin_b (Pin) -- Second pin to read pulses from."
    ),
    _(
        "rotaryio.IncrementalEncoder.deinit() \nDeinitializes the IncrementalEncoder and releases any hardware resources for reuse.\n"
    ),
    _(
        "rotaryio.IncrementalEncoder.position() \nThe current position in terms of pulses. The number of pulses per rotation is defined by the\nspecific hardware.\n"
    ),
    _(
        "rtc.RTC() \nThis class represents the onboard Real Time Clock. It is a singleton and will always return the same instance.\n\n"
    ),
    _(
        "rtc.RTC.calibration() \nThe RTC calibration value.\nA positive value speeds up the clock and a negative value slows it down.\nRange and value is hardware specific, but one step is often approx. 1 ppm.\n"
    ),
    _("rtc.RTC.datetime() \nThe date and time of the RTC.\n"),
    _(
        "rtc.set_time_source(rtc) \nSets the rtc time source used by time.localtime().\nThe default is rtc.RTC().\nExample usage:\nimport rtc\nimport time\n\nclass RTC(object):\n    @property\n    def datetime(self):\n        return time.struct_time((2018, 3, 17, 21, 1, 47, 0, 0, 0))\n\nr = RTC()\nrtc.set_time_source(r)\n\n\n"
    ),
    _(
        "storage.VfsFat(block_device) \nCreate a new VfsFat filesystem around the given block device.\n\n\nParameters:block_device -- Block device the the filesystem lives on"
    ),
    _(
        "storage.VfsFat(block_device) \nCreate a new VfsFat filesystem around the given block device.\n\n\nParameters:block_device -- Block device the the filesystem lives on"
    ),
    _(
        "storage.VfsFat.ilistdir(path) \nReturn an iterator whose values describe files and folders within\npath\n"
    ),
    _(
        "storage.VfsFat.label() \nThe filesystem label, up to 11 case-insensitive bytes.  Note that\nthis property can only be set when the device is writable by the\nmicrocontroller.\n"
    ),
    _("storage.VfsFat.mkdir(path) \nLike os.mkdir\n"),
    _(
        "storage.VfsFat.mkfs() \nFormat the block device, deleting any data that may have been there\n"
    ),
    _(
        "storage.VfsFat.mount(readonly, mkfs) \nDon’t call this directly, call storage.mount.\n"
    ),
    _("storage.VfsFat.open(path, mode) \nLike builtin open()\n"),
    _("storage.VfsFat.rmdir(path) \nLike os.rmdir\n"),
    _("storage.VfsFat.stat(path) \nLike os.stat\n"),
    _("storage.VfsFat.statvfs(path) \nLike os.statvfs\n"),
    _(
        "storage.VfsFat.umount() \nDon’t call this directly, call storage.umount.\n"
    ),
    _(
        "storage.erase_filesystem() \nErase and re-create the CIRCUITPY filesystem.\nOn boards that present USB-visible CIRCUITPY drive (e.g., SAMD21 and SAMD51),\nthen call microcontroller.reset() to restart CircuitPython and have the\nhost computer remount CIRCUITPY.\nThis function can be called from the REPL when CIRCUITPY\nhas become corrupted.\n\nWarning\nAll the data on CIRCUITPY will be lost, and\nCircuitPython will restart on certain boards.\n\n"
    ),
    _(
        "storage.getmount(mount_path) \nRetrieves the mount object associated with the mount path\n"
    ),
    _(
        "storage.mount(filesystem, mount_path, *, readonly=False) \nMounts the given filesystem object at the given path.\nThis is the CircuitPython analog to the UNIX mount command.\n"
    ),
    _(
        "storage.mount(filesystem, mount_path, *, readonly=False) \nMounts the given filesystem object at the given path.\nThis is the CircuitPython analog to the UNIX mount command.\n"
    ),
    _(
        "storage.remount(mount_path, readonly) \nRemounts the given path with new parameters.\n"
    ),
    _(
        "storage.remount(mount_path, readonly=False) \nRemounts the given path with new parameters.\n"
    ),
    _(
        "storage.umount(mount) \nUnmounts the given filesystem object or if mount is a path, then unmount\nthe filesystem mounted at that location.\nThis is the CircuitPython analog to the UNIX umount command.\n"
    ),
    _(
        "storage.umount(mount) \nUnmounts the given filesystem object or if mount is a path, then unmount\nthe filesystem mounted at that location.\nThis is the CircuitPython analog to the UNIX umount command.\n"
    ),
    _(
        "struct.calcsize(fmt) \nReturn the number of bytes needed to store the given fmt.\n"
    ),
    _(
        "struct.pack(fmt, v1, v2, ...) \nPack the values v1, v2, … according to the format string fmt.\nThe return value is a bytes object encoding the values.\n"
    ),
    _(
        "struct.pack_into(fmt, buffer, offset, v1, v2, ...) \nPack the values v1, v2, … according to the format string fmt into a buffer\nstarting at offset. offset may be negative to count from the end of buffer.\n"
    ),
    _(
        "struct.unpack(fmt, data) \nUnpack from the data according to the format string fmt. The return value\nis a tuple of the unpacked values.\n"
    ),
    _(
        "struct.unpack_from(fmt, data, offset) \nUnpack from the data starting at offset according to the format string fmt.\noffset may be negative to count from the end of buffer. The return value is\na tuple of the unpacked values.\n"
    ),
    _(
        "supervisor.Runtime() \nYou cannot create an instance of supervisor.Runtime.\nUse supervisor.runtime to access the sole instance available.\n\n"
    ),
    _(
        "supervisor.Runtime.serial_connected() \nReturns the USB serial communication status (read-only).\n"
    ),
    _(
        "time.struct_time((tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)) \nStructure used to capture a date and time. Note that it takes a tuple!\n\n\nParameters:\ntm_year (int) -- the year, 2017 for example\ntm_mon (int) -- the month, range [1, 12]\ntm_mday (int) -- the day of the month, range [1, 31]\ntm_hour (int) -- the hour, range [0, 23]\ntm_min (int) -- the minute, range [0, 59]\ntm_sec (int) -- the second, range [0, 61]\ntm_wday (int) -- the day of the week, range [0, 6], Monday is 0\ntm_yday (int) -- the day of the year, range [1, 366], -1 indicates not known\ntm_isdst (int) -- 1 when in daylight savings, 0 when not, -1 if unknown."
    ),
    _(
        "time.struct_time((tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)) \nStructure used to capture a date and time. Note that it takes a tuple!\n\n\nParameters:\ntm_year (int) -- the year, 2017 for example\ntm_mon (int) -- the month, range [1, 12]\ntm_mday (int) -- the day of the month, range [1, 31]\ntm_hour (int) -- the hour, range [0, 23]\ntm_min (int) -- the minute, range [0, 59]\ntm_sec (int) -- the second, range [0, 61]\ntm_wday (int) -- the day of the week, range [0, 6], Monday is 0\ntm_yday (int) -- the day of the year, range [1, 366], -1 indicates not known\ntm_isdst (int) -- 1 when in daylight savings, 0 when not, -1 if unknown."
    ),
    _(
        "touchio.TouchIn(pin) \nUse the TouchIn on the given pin.\n\n\nParameters:pin (Pin) -- the pin to read from"
    ),
    _(
        "touchio.TouchIn(pin) \nUse the TouchIn on the given pin.\n\n\nParameters:pin (Pin) -- the pin to read from"
    ),
    _(
        "touchio.TouchIn.deinit() \nDeinitialises the TouchIn and releases any hardware resources for reuse.\n"
    ),
    _(
        "touchio.TouchIn.deinit() \nDeinitialises the TouchIn and releases any hardware resources for reuse.\n"
    ),
    _(
        "touchio.TouchIn.raw_value() \nThe raw touch measurement as an int. (read-only)\n"
    ),
    _(
        "touchio.TouchIn.threshold() \nMinimum raw_value needed to detect a touch (and for value to be True).\nWhen the TouchIn object is created, an initial raw_value is read from the pin,\nand then threshold is set to be 100 + that value.\nYou can adjust threshold to make the pin more or less sensitive.\n"
    ),
    _(
        "touchio.TouchIn.value() \nWhether the touch pad is being touched or not.\n\n\n\n\nReturns:True when touched, False otherwise.\n\nReturn type:bool\n\n\n\n"
    ),
    _(
        "touchio.TouchIn.value() \nWhether the touch pad is being touched or not. (read-only)\nTrue when raw_value > threshold.\n"
    ),
    _("usb_hid.Device() \nNot currently dynamically supported.\n\n"),
    _("usb_hid.Device() \nNot currently dynamically supported.\n\n"),
    _("usb_hid.Device.send_report(buf) \nSend a HID report.\n"),
    _("usb_hid.Device.send_report(buf) \nSend a HID report.\n"),
    _(
        "usb_hid.Device.usage() \nThe functionality of the device. For example Keyboard is 0x06 within the\ngeneric desktop usage page 0x01. Mouse is 0x02 within the same usage\npage.\n\n\n\n\nReturns:the usage within the usage page\n\nReturn type:int\n\n\n\n"
    ),
    _(
        "usb_hid.Device.usage() \nThe functionality of the device as an int. (read-only)\nFor example, Keyboard is 0x06 within the generic desktop usage page 0x01.\nMouse is 0x02 within the same usage page.\n"
    ),
    _(
        "usb_hid.Device.usage_page() \nThe usage page of the device. Can be thought of a category.\n\n\n\n\nReturns:the device’s usage page\n\nReturn type:int\n\n\n\n"
    ),
    _(
        "usb_hid.Device.usage_page() \nThe usage page of the device as an int. Can be thought of a category. (read-only)\n"
    ),
]
