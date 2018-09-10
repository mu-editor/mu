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

"""
Documentation pulled from: https://docs.micropython.org/en/latest/pyboard/
"""

PYBOARD_APIS = [
    _('pyb.delay(ms) \nDelay for the given number of milliseconds.\n\nParameters:\nms (int) -- the number of milliseconds to delay.\n'),
    _('pyb.udelay(us) \nDelay for the given number of microseconds.\n\nParameters:\nus (int) -- the number of microseconds to delay.\n'),
    _('pyb.millis() \nReturns the number of milliseconds since the board was last reset.\n\nReturns: milliseconds since reset.\n\nReturn type: int\n'),
    _('pyb.micros() \nReturns the number of microseconds since the board was last reset.\n\nReturns: microseconds since reset.\n\nReturn type: int\n'),
    _('pyb.elapsed_millis(start) \nReturns the number of milliseconds which have elapsed since start.\n\nParameters:\nstart (int) -- the number of milliseconds to start counting from.\n\nReturns: milliseconds since start.\n\nReturn type: int\n'),
    _('pyb.elapsed_micros(start) \nReturns the number of microseconds which have elapsed since start.\n\nParameters:\nstart (int) -- the number of microseconds to start counting from.\n\nReturns: microseconds since start.\n\nReturn type: int\n'),
    _('pyb.hard_reset() \nResets the board in a manner similar to pushing the external RESET button.\n'),
    _('pyb.bootloader() \nActivate the bootloader without BOOT* pins.\n'),
    _('pyb.fault_debug(valus) \nEnable or disable hard-fault debugging.\nA hard-fault is when there is a fatal error in the underlying system, like an\ninvalid memory access.\n\nParameters:\nvalue (bool) -- \n\nFalse: board will automatically reset if there is a hard fault\nTrue: when the board has a hard fault, it will print the registers and the stack\n\ttrace, and then cycle the LEDs indefinitely\n'),
    _('pyb.disable_irq() \nDisable interrupt requests.\n\nReturns: Previous IRQ state.\n\nReturn type: bool\n'),
    _('pyb.enable_irq(state=True) \nEnable interrupt requests.\n\nParameters:\nstate (bool) -- Whether the IRQs are enabled\n'),
    _('pyb.freq([sysclk[, hclk[, pclk1[, pclk2]]]]) \nIf given no arguments, returns a tuple of clock frequencies:\n(sysclk, hclk, pclk1, pclk2). Otherwise, sets the frequency of the CPU, and the\nbusses if additional arguments are given.\n\nParameters:\nsysclk (int) [optional] -- frequency of the CPU in MHz.\nhclk (int) [optional] -- frequency of the AHB bus, core memory and DMA.\npclk1 (int) [optional] -- frequency of the APB1 bus.\npclk2 (int) [optional] -- frequency of the APB2 bus.\n\nReturns: clock frequencies.\n\nReturn type: tuple\n'),
    _('pyb.wfi() \nWait for an internal or external interrupt.\nThis function will block for at most 1ms.\n'),
    _('pyb.stop() \nPut the board in a “sleeping” state. To wake from this sleep state requires an\nexternal interrupt or a real-time-clock event. Upon waking execution continues\nwhere it left off.\n'),
    _('pyb.standby() \nPut the board into a “deep sleep” state. To wake from this sleep state requires\na real-time-clock event, or an external interrupt on X1 (PA0=WKUP) or\nX18 (PC13=TAMP1). Upon waking the system undergoes a hard reset.\n'),
    _('pyb.info([dump_alloc_table]) \nPrint out lots of information about the board.\n\nParameter:\ndump_alloc_table (bool) [optional] -- Whether to dump the alloc table.\n'),
    _('pyb.main(filename) \nSet the filename of the main script to run after boot.py is finished.\n\nIt only makes sense to call this function from within boot.py.\n\nParameter:\nfilename (string) -- name of the desired main file.\n'),
    _('pyb.mount(device, mountpoint, *, readonly=False, mkfs=False) \nMount a block device and make it available as part of the filesystem.\n\nSee online documentation for full instructions.\n'),
    _('pyb.repl_uart(uart) \nGet or set the UART object where the REPL is repeated on.\n\nParameter:\nuart (pyb.UART) -- The uart to use\n.'),
    _('pyb.rng() \nReturn a 30-bit hardware generated random number.\n\nReturns: 30-bit random number.\n\nReturn value: int\n'),
    _('pyb.sync() \nSync all file systems.\n'),
    _('pyb.unique_id() \nReturns a string of 12 bytes (96 bits), which is the unique ID of the MCU.\n\nReturns: unique ID of the MCU.\n\nReturn value: string\n'),
    _('pyb.usb_mode([modestr, ]vid=0xf055, pid=0x9801, hid=pyb.hid_mouse) \nIf called with no arguments, return the current USB mode as a string. If called\nwith modestr provided, attempts to set USB mode.\n\nThis can only be done when called from boot.py before pyb.main() has been called.\n\nSee online documentation for full instructions.\n'),
    _('pyb.Accel() \nCreate an accelerometer object.\n\nReturns: an object that controls the accelerometer.\n\nReturn type: Accel class\n'),
    _('pyb.Accel.filtered_xyz() \nGet filtered x, y and z values.\n\nReturns: accelerometer x, y, and z values.\n\nReturn type: 3-tuple\n'),
    _('pyb.Accel.tilt() \nGet the tilt register.\n\nReturns: contents of tilt register,\n\nReturn type: int\n'),
    _('pyb.Accel.x() \nGet the x-axis register.\n\nReturns: contents of x-axis register,\n\nReturn type: int\n'),
    _('pyb.Accel.y() \nGet the y-axis register.\n\nReturns: contents of y-axis register,\n\nReturn type: int\n'),
    _('pyb.Accel.z() \nGet the z-axis register.\n\nReturns: contents of z-axis register,\n\nReturn type: int\n'),
    _('pyb.ADC(pin) \nAn Analog to Digital conversion object associated with the given pin\n\nParameter:\npin (pyb.Pin) -- the pin to read values from\n\nReturns: ADC object\n\nReturn type: ADC class\n'),
    _('pyb.ADC.read() \nRead the value on the analog pin and return it.\nThe returned value will be between 0 and 4095.\n\nReturns: analog value of pin.\n\nReturn type: int\n'),
    _('pyb.ADC.read_timed(buf, timer) \nRead analog values into buf at a rate set by the timer object.\n\nParameters:\nbuf (bytearray or array.array) -- The ADC values have 12-bit resolution and are\nstored directly into buf if its element size is 16 bits or greater. If buf has\nonly 8-bit elements (eg a bytearray) then the sample resolution will be reduced\nto 8 bits.\ntimer (pyb.Timer) -- a Timer object, a sample is read each time the timer triggers.'),
    _('pyb.CAN(bus, ...) \nConstruct a CAN object on the given bus. With no additional parameters, the CAN\nobject is created but not initialised. If extra arguments are given, the bus is\ninitialised. See CAN.init() for parameters of initialisation.\n\nParameters:\nbus can be 1-2, or \'YA\' or \'YB\'.'),
    _('pyb.CAN.init(mode, extframe=False, prescaler=100, *, sjw=1, bs1=6, bs2=8, auto_restart=False) \nInitialise the CAN bus with the given parameters.\n\nParameters:\nmode (int) -- one of: NORMAL, LOOPBACK, SILENT, SILENT_LOOPBACK. These are\nincluded in the pyb.CAN class as class variables.\nextframe (bool) -- if extframe is True then the bus uses extended identifiers in\nthe frames (29 bits); otherwise it uses standard 11 bit identifiers.\nprescaler (int) -- used to set the duration of 1 time quanta; the time quanta\nwill be the input clock divided by the prescaler.\nsjw (int) -- is the resynchronisation jump width in units of the time quanta; it\ncan be 1, 2, 3, 4\nbs1 (int) -- defines the location of the sample point in units of the time\nquanta; it can be between 1 and 1024 inclusive.\nbs2 (int) -- defines the location of the transmit point in units of the time\nquanta; it can be between 1 and 16 inclusive.\nauto_restart (bool) -- sets whether the controller will automatically try and\nrestart communications after entering the bus-off state.\n'),
    _('pyb.CAN.deinit() \nTurn off the CAN bus.\n'),
    _('pyb.CAN.restart() \nForce a software restart of the CAN controller without resetting its configuration.\n'),
    _('pyb.CAN.state() \nReturn the state of the controller.\n\nReturns: the state of the controller.\nCan be one of the following: CAN.STOPPED, CAN.ERROR_ACTIVE, CAN.ERROR_WARNING,\nCAN.ERROR_PASSIVE, CAN.BUS_OFF.\n\nReturn type: int\n'),
    _('pyb.CAN.info([list]) \nGet information about the controller’s error states and TX and RX buffers.\n\nParameters:\nlist (list) [optional] -- If list is provided then it should be a list object\nwith at least 8 entries, which will be filled in with the information.\n\nReturns: If list parameter is not provided, a new list will be created and filled in.\n\nReturn type: list\n'),
    _('pyb.CAN.setfilter(bank, mode, fifo, params, *, rtr) \nConfigure a filter bank\n\nParameters:\nbank (int) -- the filter bank that is to be configured\nmode (int) -- the mode the filter should operate in. One of the following:\nCAN.LIST16, CAN.LIST32, CAN.MASK16, CAN.MASK32\nfifo (int) -- which fifo (0 or 1) a message should be stored in, if it is\naccepted by this filter\nparams (array (int)) -- values that defines the filter. The contents of the array\ndepends on the mode argument\nrtr (array (bool)) [optional]  -- array that states if a filter should accept a\nremote transmission request message. If this argument is not given then it defaults to False for all entries.'),
    _('pyb.CAN.clearfilter(bank) \nClear and disables a filter bank\n\nParameters:\nbank (int) -- the filter bank that is to be cleared.\n'),
    _('pyb.CAN.any(fifo) \nWhether any message waiting on the FIFO\n\nParameters:\nfifo (int) -- the FIFO to check.\n\nReturns: Whether a message is waiting\n\nReturn type: bool\n'),
    _('pyb.DAC(port, bits=8, *, buffering=None) \nConstruct a new DAC object on the given port.\n\nParameters:\nport (pyb.Pin or int) -- can be a pin object, or an integer (1 or 2). DAC(1) is\non pin X5 and DAC(2) is on pin X6.\nbits (int) -- The resolution, and can be 8 or 12. The maximum value for the write\nand write_timed methods will be 2**bits-1\nbuffering (bool or None) -- The buffering parameter selects the behaviour of the\nDAC op-amp output buffer, whose purpose is to reduce the output impedance. It can\nbe None to select the default, False to disable buffering completely, or True to\nenable output buffering.\n\nReturns: DAC object\n\nReturn type: DAC class.\n'),
    _('pyb.DAC.init(bits=8, *, buffering=None) \nReinitialise the DAC.\n\nParameters:\nbits (int) -- The resolution, and can be 8 or 12. The maximum value for the write and write_timed methods will be 2**bits-1\nbuffering (bool or None) -- The buffering parameter selects the behaviour of the DAC op-amp output buffer, whose purpose is to reduce the output impedance. It can be None to select the default, False to disable buffering completely, or True to enable output buffering.\n'),
    _('pyb.DAC.deinit() \nDe-initialise the DAC making its pin available for other uses.\n'),
    _('pyb.DAC.noise(freq) \nGenerate a pseudo-random noise signal. A new random sample is written to the DAC\noutput at the given frequency.\n\nParameters:\nfreq (int) -- the frequency to generate noise at.\n'),
    _('pyb.DAC.triangle(freq) \nGenerate a triangle wave. The value on the DAC output changes at the given\nfrequency, and the frequency of the repeating triangle wave itself is 2048 times smaller.\n\nParameters: freq (int) -- the frequency to generate the wave at.\n'),
    _('pyb.DAC.write(value) \nDirect access to the DAC output. The minimum value is 0. The maximum value is 2**bits-1.\n\nParameters: value (int) -- the value to write to the DAC\n'),
    _('pyb.DAC.write_timed(data, freq, *, mode=DAC.NORMAL) \nInitiates a burst of RAM to DAC using a DMA transfer. The input data is treated\nas an array of bytes in 8-bit mode, and an array of unsigned half-words\n(array typecode ‘H’) in 12-bit mode.\n\nParameters:\ndata (array) -- data to be written to the DAC.\nfreq (int or Timer) -- frequency or Timer to determin how often to trigger DAC sample\nmode (constant) -- can be DAC.NORMAL or DAC.CIRCULAR.'),
    _('pyb.ExtInt(pin, mode, pull, callback) \nCreate an ExtInt object.\n\nParameters:\npin (pyb.Pin) -- the pin on which to enable the interrupt.\nmode (constant) can be one of: ExtInt.IRQ_RISING - trigger on a rising edge;\nExtInt.IRQ_FALLING - trigger on a falling edge; ExtInt.IRQ_RISING_FALLING - trigger\non a rising or falling edge.\npull (constant) -- can be one of: - pyb.Pin.PULL_NONE - no pull up or down\nresistors; pyb.Pin.PULL_UP - enable the pull-up resistor;\npyb.Pin.PULL_DOWN - enable the pull-down resistor.\ncallback (function) -- the function to call when the interrupt triggers. The\ncallback function must accept exactly 1 argument, which is the line that triggered the interrupt.\n\nReturns: ExtInt object\n\nReturn type: ExtInt class\n'),
    _('pyb.ExtInt.regs() \nPrints the values of the EXTI registers.\n'),
    _('pyb.ExtInt.disable() \nDisable the interrupt associated with the ExtInt object.\n'),
    _('pyb.ExtInt.enable() \nEnable a disabled interrupt.\n'),
    _('pyb.ExtInt.line() \nReturn the line number that the pin is mapped to.\n\nReturns: line number that the pin is mapped to\n\nReturn type: int\n'),
    _('pyb.ExtInt.swint() \nTrigger the callback from software.\n'),
    _('pyb.I2C(bus, ...) \nConstruct an I2C object on the given bus. bus can be 1 or 2, ‘X’ or ‘Y’. With no\nadditional parameters, the I2C object is created but not initialised. If extra\narguments are given, the bus is initialised. See init for parameters of initialisation.\n\nParameters:\nbus (int or string) -- the bus to attach to. Can be 1 or 2, ‘X’ or ‘Y’.\n'),
    _('pyb.I2C.deinit() \nTurn off the I2C bus.\n'),
    _('pyb.I2C.init(mode, *, addr=0x12, baudrate=400000, gencall=False, dma=False) \nInitialise the I2C bus with the given parameters\n\nParameters:\nmode (constant) -- must be either I2C.MASTER or I2C.SLAVE\naddr (int) -- the 7-bit address (only sensible for a slave)\nbaudrate (int) -- the SCL clock rate (only sensible for a master)\ngencall (bool) -- whether to support general call mode\ndma (bool) -- whether to allow the use of DMA for the I2C transfers\n'),
    _('pyb.I2C.is_ready(addr) \nCheck if an I2C device responds to the given address. Only valid when in master mode.\n\nParameters:\naddr (int) -- the address to check\n\nReturns: Whether the address responds\n\nReturn type: bool\n'),
    _('pyb.I2C.mem_read(data, addr, memaddr, *, timeout=5000, addr_size=8) \nRead from the memory of an I2C device\n\nParameters:\ndata (int or buffer) -- number of bytes to read or a buffer to read into\naddr (int) -- the I2C device address\nmemaddr (int) -- the memory location within the I2C device\ntimeout (int) the timeout in milliseconds to wait for the read\naddr_size (int) -- width of memaddr: 8 or 16 bits\n\nReturns: the read data. This is only valid in master mode.\n\nReturn type: bytes\n'),
    _('pyb.I2C.mem_write(data, addr, memaddr, *, timeout=5000, addr_size=8) \nWrite to the memory of an I2C device\nParameters:\ndata (int or buffer) -- number of bytes to write or a buffer to write into\naddr (int) -- the I2C device address\nmemaddr (int) -- the memory location within the I2C device\ntimeout (int) the timeout in milliseconds to wait for the write\naddr_size (int) -- width of memaddr: 8 or 16 bits\n'),
    _('pyb.I2C.recv(recv, addr=0x00, *, timeout=5000) \nReceive data on the bus.\n\nParameters:\nrecv (int or buffer) -- can be the number of bytes to receive, or a mutable\nbuffer, which will be filled with received bytes\naddr (int) -- the address to receive from (only required in master mode)\ntimeout (int) -- the timeout in milliseconds to wait for the receive\n\nReturns: if recv is an integer then a new buffer of the bytes received\n\nReturn type: bytes\n'),
    _('pyb.I2C.send(send, addr=0x00, *, timeout=5000) \nSend data on the bus.\n\nParameters:\nsend (int or buffer) -- the data to send\naddr (int) the address to send to (only required in master mode)\ntimeout (int) -- the timeout in milliseconds to wait for the send\n'),
    _('pyb.I2C.scan() \nScan all I2C addresses from 0x01 to 0x7f and return a list of those that respond.\nOnly valid when in master mode.\n\nReturns: valid I2C addresses on the bus\n\nReturn type: list\n'),
    _('pyb.LCD(skin_position) \nConstruct an LCD object in the given skin position.\n\nParameters:\nskin_position (string) -- can be ‘X’ or ‘Y’, and should match the position where\nthe LCD pyskin is plugged in.\n\nReturns: LCD object\n\nReturn type: LCD class\n'),
    _('pyb.LCD.command(instr_data, buf) \nSend an arbitrary command to the LCD controller.\n\nParameters:\ninstr_data (int) -- 0 for instr_data to send an instruction, otherwise pass 1\nto send data\nbuf (int or buffer) -- a buffer with the instructions/data to send\n'),
    _('pyb.LCD.contrast(value) \nSet the contrast of the LCD\n\nParameters:\nvalue (int) -- the contrast value, valid values are between 0 and 47.\n'),
    _('pyb.LCD.fill(color) \nFill the screen with the given colour.\n\nParameters:\ncolor (int) -- 0 or 1 for white or black respectively.\n'),
    _('pyb.LCD.get(x, y) \nGet the pixel at the position (x, y)\n\nParameters:\nx (int) -- the X coordinate\ny (int) -- the Y coordinate\n\nReturns: the pixel value, either 0 or 1.\n\nReturn type: int\n'),
    _('pyb.LCD.light(value) \nTurn the backlight on/off.\n\nParameters:\nvalue (int or bool) -- True or 1 turns it on, False or 0 turns it off.\n'),
    _('pyb.LCD.pixel(x, y, colour) \nSet the pixel at (x, y) to the given colour (0 or 1).\n\nParameters:\nx (int) -- the X coordinate\ny (int) -- the Y coordinate\ncolor (int) -- the color.\n'),
    _('pyb.LCD.show() \nShow the hidden buffer on the screen.\n'),
    _('pyb.LCD.text(str, x, y, colour) \nDraw the given text to the position (x, y) using the given colour (0 or 1).\n\nParameters:\nstr (string) -- the text to display.\nx (int) -- the X coordinate\ny (int) -- the Y coordinate\ncolor (int) -- the color.\n'),
    _('pyb.LCD.write(str) \nWrite the string str to the screen. It will appear immediately.\n\nParameters:\nstr (string) -- the text to display.\n'),
    _('pyb.LED(id) \nCreate an LED object associated with the given LED\n\nParameters:\nid (int) -- the LED number, 1-4\n\nReturns: LED object\n\nReturn type: LED class'),
    _('pyb.LED.intensity([value]) \nGet or set the LED intensity. If no argument is given, return the LED intensity.\n\nParameters:\nvalue (int) [optional] -- intensity value ranges between 0 (off) and 255 (full on)\n\nReturns: None or LED intensity\n\nReturn type: None or int\n'),
    _('pyb.LED.off() \nTurn the LED off.\n'),
    _('pyb.LED.on() \nTurn the LED on.\n'),
    _('pyb.LED.toggle() \nToggle the LED between on (maximum intensity) and off. If the LED is at non-zero\nintensity then it is considered “on” and toggle will turn it off.\n'),
    _('pyb.Pin(id, ...) \nCreate a new Pin object associated with the id. If additional arguments are given,\nthey are used to initialise the pin. See pyb.Pin.init()\n\nParameters:\nid (constant or string) -- the identifier of the pin to use\n\nReturns: Pin object\n\nReturn type: Pin class\n'),
    _('pyb.Pin.debug([state]) \nGet or set the debugging state\n\nParameters:\nstate (bool) [optional] -- the debugging state to set, if any.\n\nReturns: whether the debugging state is set (if nothing is passed to the method)\n\nReturn type: bool\n'),
    _('pyb.Pin.init(mode, pull=Pin.PULL_NONE, af=-1) \nInitialise the pin\n\nParameters:\nmode (constant) -- can be one of: Pin.IN, Pin.OUT_PP, Pin.OUT_OD, Pin.AF_PP, Pin.AF_OD, Pin.ANALOG\npull (constant) -- can be one of: Pin.PULL_NONE, Pin.PULL_UP, Pin.PULL_DOWN\naf (int) -- when mode is Pin.AF_PP or Pin.AF_OD, then af can be the index or name\nof one of the alternate functions associated with a pin\n'),
    _('pyb.Pin.value([value]) \nGet or set the digital logic level of the pin\n\nParameters:\nvalue (int or bool) [optional] -- if value converts to True, the pin is set high,\notherwise it is set low\n\nReturns: with no argument, return 0 or 1 depending on the logic level of the pin\n\nReturn type: int\n'),
    _('pyb.Pin.af() \nReturns the currently configured alternate-function of the pin\n\nReturns: one of the integer representations of the allowed constants for af\n\nReturn type: int\n'),
    _('pyb.Pin.af_list() \nReturns an array of alternate functions available for this pin.\n\nReturns:array of alternate functions available\n\nReturn type: list\n'),
    _('pyb.Pin.gpio() \nReturns the base address of the GPIO block associated with this pin.\n\nReturns: the base address of the GPIO block\n\nReturn type: int'),
    _('pyb.Pin.mode() \nReturns the currently configured mode of the pin.\n\nReturns: integer returned will match one of the allowed constants for the mode\n\nReturn type: int'),
    _('pyb.Pin.name() \nReturns the pin name.\n\nReturns: the name of the pin\n\nReturn type: string'),
    _('pyb.Pin.names() \nReturns the board and cpu names for the pin.\n\nReturns: the names of the pin\n\nReturn type: list'),
    _('pyb.Pin.pin() \nReturns the CPU pin number.\n\nReturns: the number of the pin\n\nReturn type: int'),
    _('pyb.Pin.port() \nReturns the CPU port number.\n\nReturns: the number of the port\n\nReturn type: int'),
    _('pyb.Pin.pull() \nReturns the currently configured pull of the pin.\n\nReturns: The integer returned will match one of the allowed constants for the pull\n\nReturn type: int'),
    _('pyb.RTC() \nCreate an RTC object.\n\nReturns: RTC object\n\nReturn type: RTC class\n'),
    _('pyb.RTC.datetime([datetimetuple]) \nGet or set the date and time of the RTC. With no arguments, this method returns\nan 8-tuple with the current date and time. With 1 argument (being an 8-tuple) it\nsets the date and time\n\nParameters:\ndatetimetuple (tuple) [optional] -- The 8-tuple has the following format:\n(year, month, day, weekday, hours, minutes, seconds, subseconds). All tuple\nelements are integers\n\nReturns: the current date and time\n\nReturn type: tuple (8 elements)\n'),
    _('pyb.RTC.wakeup(timeout, callback=None) \nSet the RTC wakeup timer to trigger repeatedly at every timeout milliseconds.\nThis trigger can wake the pyboard from both the sleep states: pyb.stop() and pyb.standby()\n\nParameters:\ntimeout (int or None) -- timeout in milliseconds or None to disable timer\ncallback (function or None) -- if callback is given then it is executed at every\ntrigger of the wakeup timer. callback must take exactly one argument\n'),
    _('pyb.RTC.info() \nGet information about the startup time and reset source\n\nReturns: RTC info: lower 0xffff are the number of milliseconds the RTC took to\nstart up, bit 0x10000 is set if a power-on reset occurred, bit 0x20000 is set if\nan external reset occurred\n\nReturn type: int\n'),
    _('pyb.RTC.calibration([cal]) \nGet or set RTC calibration.\n\nParameters: cal (int) [optional] -- The usable calibration range is: (-511 * 0.954) ~= -487.5 ppm up to (512 * 0.954) ~= 488.5 ppm\n\nReturns: with no arguments, the current calibration value, in the range [-511 : 512]\n\nReturn type: int\n'),


]
