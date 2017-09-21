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
    _('busio.UART(tx, rx, *, baudrate=9600, bits=8, parity=None, stop=1, timeout=1000, receiver_buffer_size=64) \nA common bidirectional serial protocol that uses an an agreed upon speed\nrather than a shared clock line.\n\n\nParameters:\ntx (Pin) -- the pin to transmit with\nrx (Pin) -- the pin to receive on\nbaudrate (int) -- the transmit and receive speed'),
    _('busio.UART.deinit() \nDeinitialises the UART and releases any hardware resources for reuse.\n'),
    _('busio.UART.Parity() \nEnum-like class to define the parity used to verify correct data transfer.\n\n'),
    _('microcontroller.Processor() \n'),
    _('microcontroller.Pin() \nIdentifies an IO pin on the microcontroller. They are fixed by the\nhardware so they cannot be constructed on demand. Instead, use\nboard or microcontroller.pin to reference the desired pin.\n\n'),
    _('busio.SPI(clock, MOSI=None, MISO=None) \n\nParameters:\nclock (Pin) -- the pin to use for the clock.\nMOSI (Pin) -- the Master Out Slave In pin.\nMISO (Pin) -- the Master In Slave Out pin.'),
    _('busio.SPI.deinit() \nTurn off the SPI bus.\n'),
    _('digitalio.DigitalInOut(pin) \nCreate a new DigitalInOut object associated with the pin. Defaults to input\nwith no pull. Use switch_to_input() and\nswitch_to_output() to change the direction.\n\n\nParameters:pin (Pin) -- The pin to control'),
    _('digitalio.DigitalInOut.deinit() \nTurn off the DigitalInOut and release the pin for other use.\n'),
    _('digitalio.DigitalInOut.Direction() \nEnum-like class to define which direction the digital values are\ngoing.\n\n'),
    _('digitalio.DriveMode() \nEnum-like class to define the drive mode used when outputting\ndigital values.\n\n'),
    _('digitalio.Pull() \nEnum-like class to define the pull value, if any, used while reading\ndigital values in.\n\n'),
    _('busio.OneWire(pin) \nCreate a OneWire object associated with the given pin. The object\nimplements the lowest level timing-sensitive bits of the protocol.\n\n\nParameters:pin (Pin) -- Pin connected to the OneWire bus'),
    _('busio.OneWire.deinit() \nDeinitialize the OneWire bus and release any hardware resources for reuse.\n'),
    _('busio.I2C(scl, sda, *, frequency=400000) \nI2C is a two-wire protocol for communicating between devices.  At the\nphysical level it consists of 2 wires: SCL and SDA, the clock and data\nlines respectively.\n\n\nParameters:\nscl (Pin) -- The clock pin\nsda (Pin) -- The data pin\nfrequency (int) -- The clock frequency in Hertz'),
    _('busio.I2C.deinit() \nReleases control of the underlying hardware so other classes can use it.\n'),
    _('bitbangio.SPI(clock, MOSI=None, MISO=None) \n\nParameters:\nclock (Pin) -- the pin to use for the clock.\nMOSI (Pin) -- the Master Out Slave In pin.\nMISO (Pin) -- the Master In Slave Out pin.'),
    _('bitbangio.SPI.deinit() \nTurn off the SPI bus.\n'),
    _('usb_hid.Device() \nNot currently dynamically supported.\n\n'),
    _('usb_hid.Device.send_report(buf) \nSend a HID report.\n'),
    _('usb_hid.Device.send_report() \nSend a HID report.\n'),
    _('usb_hid.Device.send_report() \nSend a HID report.\n'),
    _('touchio.TouchIn(pin) \nUse the TouchIn on the given pin.\n\n\nParameters:pin (Pin) -- the pin to read from'),
    _('touchio.TouchIn.deinit() \nDeinitialises the TouchIn and releases any hardware resources for reuse.\n'),
    _('time.struct_time((tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)) \nStructure used to capture a date and time. Note that it takes a tuple!\n\n\nParameters:\ntm_year (int) -- the year, 2017 for example\ntm_mon (int) -- the month, range [1, 12]\ntm_mday (int) -- the day of the month, range [1, 31]\ntm_hour (int) -- the hour, range [0, 23]\ntm_min (int) -- the minute, range [0, 59]\ntm_sec (int) -- the second, range [0, 61]\ntm_wday (int) -- the day of the week, range [0, 6], Monday is 0\ntm_yday (int) -- the day of the year, range [1, 366], -1 indicates not known\ntm_isdst (int) -- 1 when in daylight savings, 0 when not, -1 if unknown.'),
    _('storage.mount(filesystem, mount_path, *, readonly=False) \nMounts the given filesystem object at the given path.\nThis is the CircuitPython analog to the UNIX mount command.\n'),
    _('storage.umount(mount) \nUnmounts the given filesystem object or if mount is a path, then unmount\nthe filesystem mounted at that location.\nThis is the CircuitPython analog to the UNIX umount command.\n'),
    _('storage.remount(mount_path, readonly) \nRemounts the given path with new parameters.\n'),
    _('storage.VfsFat(block_device) \nCreate a new VfsFat filesystem around the given block device.\n\n\nParameters:block_device -- Block device the the filesystem lives on'),
    _('random.seed(seed) \nSets the starting seed of the random  number generation. Further calls to\nrandom will return deterministic results afterwards.\n'),
    _('random.getrandbits(k) \nReturns an integer with k random bits.\n'),
    _('random.randrange(stop) \nReturns a randomly selected integer from range(start, stop, step).\n'),
    _('random.randint(a, b) \nReturns a randomly selected integer between a and b inclusive. Equivalent\nto randrange(a, b + 1, 1)\n'),
    _('random.choice(seq) \nReturns a randomly selected element from the given sequence. Raises\nIndexError when the sequence is empty.\n'),
    _('random.random() \nReturns a random float between 0 and 1.0.\n'),
    _('random.uniform(a, b) \nReturns a random float between a and b. It may or may not be inclusive\ndepending on float rounding.\n'),
    _('pulseio.PWMOut(pin, *, duty_cycle=0, frequency=500, variable_frequency=False) \nCreate a PWM object associated with the given pin. This allows you to\nwrite PWM signals out on the given pin. Frequency is fixed after init\nunless variable_frequency is True.\n\n\nParameters:\npin (Pin) -- The pin to output to\nduty_cycle (int) -- The fraction of each pulse which is high. 16-bit\nfrequency (int) -- The target frequency in Hertz (32-bit)\nvariable_frequency (bool) -- True if the frequency will change over time'),
    _('pulseio.PWMOut.deinit() \nDeinitialises the PWMOut and releases any hardware resources for reuse.\n'),
    _('pulseio.PulseIn(pin, maxlen=2, *, idle_state=False) \nCreate a PulseIn object associated with the given pin. The object acts as\na read-only sequence of pulse lengths with a given max length. When it is\nactive, new pulse lengths are added to the end of the list. When there is\nno more room (len() == maxlen) the oldest pulse length is removed to\nmake room.\n\n\nParameters:\npin (Pin) -- Pin to read pulses from.\nmaxlen (int) -- Maximum number of pulse durations to store at once\nidle_state (bool) -- Idle state of the pin. At start and after resume\nthe first recorded pulse will the opposite state from idle.'),
    _('pulseio.PulseOut(carrier) \nCreate a PulseOut object associated with the given PWM out experience.\n\n\nParameters:carrier (PWMOut) -- PWMOut that is set to output on the desired pin.'),
    _('pulseio.PulseIn.deinit() \nDeinitialises the PulseIn and releases any hardware resources for reuse.\n'),
    _('pulseio.PulseOut.deinit() \nDeinitialises the PulseOut and releases any hardware resources for reuse.\n'),
    _('os.uname() \nReturns a named tuple of operating specific and CircuitPython port\nspecific information.\n'),
    _('os.chdir(path) \nChange current directory.\n'),
    _('os.getcwd() \nGet the current directory.\n'),
    _('os.listdir(dir) \nWith no argument, list the current directory.  Otherwise list the given directory.\n'),
    _('os.mkdir(path) \nCreate a new directory.\n'),
    _('os.remove(path) \nRemove a file.\n'),
    _('os.rmdir(path) \nRemove a directory.\n'),
    _('os.rename(old_path, new_path) \nRename a file.\n'),
    _('nvm.ByteArray() \nNot currently dynamically supported. Access the sole instance through microcontroller.nvm.\n\n'),
    _('os.stat(path) \nGet the status of a file or directory.\n'),
    _('os.statvfs(path) \nGet the status of a fileystem.\nReturns a tuple with the filesystem information in the following order:\n\n\nf_bsize -- file system block size\nf_frsize -- fragment size\nf_blocks -- size of fs in f_frsize units\nf_bfree -- number of free blocks\nf_bavail -- number of free blocks for unpriviliged users\nf_files -- number of inodes\nf_ffree -- number of free inodes\nf_favail -- number of free inodes for unpriviliged users\nf_flag -- mount flags\nf_namemax -- maximum filename length\n\n\nParameters related to inodes: f_files, f_ffree, f_avail\nand the f_flags parameter may return 0 as they can be unavailable\nin a port-specific implementation.\n'),
    _('os.sync() \nSync all filesystems.\n'),
    _('os.urandom(size) \nReturns a string of size random bytes based on a hardware True Random\nNumber Generator. When not available, it will raise a NotImplementedError.\n'),
    _('multiterminal.get_secondary_terminal() \nReturns the current secondary terminal.\n'),
    _('multiterminal.set_secondary_terminal(stream) \nRead additional input from the given stream and write out back to it.\nThis doesn’t replace the core stream (usually UART or native USB) but is\nmixed in instead.\n\n\n\n\nParameters:stream (stream) -- secondary stream\n\n\n\n'),
    _('multiterminal.clear_secondary_terminal() \nClears the secondary terminal.\n'),
    _('multiterminal.schedule_secondary_terminal_read(socket) \nIn cases where the underlying OS is doing task scheduling, this notifies\nthe OS when more data is available on the socket to read. This is useful\nas a callback for lwip sockets.\n'),
    _('bitbangio.OneWire(pin) \nCreate a OneWire object associated with the given pin. The object\nimplements the lowest level timing-sensitive bits of the protocol.\n\n\nParameters:pin (Pin) -- Pin to read pulses from.'),
    _('bitbangio.OneWire.deinit() \nDeinitialize the OneWire bus and release any hardware resources for reuse.\n'),
    _('bitbangio.I2C(scl, sda, *, frequency=400000) \nI2C is a two-wire protocol for communicating between devices.  At the\nphysical level it consists of 2 wires: SCL and SDA, the clock and data\nlines respectively.\n\n\nParameters:\nscl (Pin) -- The clock pin\nsda (Pin) -- The data pin\nfrequency (int) -- The clock frequency of the bus'),
    _('audioio.AudioOut(pin, sample_source) \nCreate a AudioOut object associated with the given pin. This allows you to\nplay audio signals out on the given pin. Sample_source must be a bytes-like object.\n\nThe sample itself should consist of 16 bit samples and be mono.\nMicrocontrollers with a lower output resolution will use the highest order\nbits to output. For example, the SAMD21 has a 10 bit DAC that ignores the\nlowest 6 bits when playing 16 bit samples.\n\n\nParameters:\npin (Pin) -- The pin to output to\nsample_source (bytes-like) -- The source of the sample'),
    _('bitbangio.I2C.deinit() \nReleases control of the underlying hardware so other classes can use it.\n'),
    _('audioio.AudioOut.deinit() \nDeinitialises the PWMOut and releases any hardware resources for reuse.\n'),
    _('audiobusio.PDMIn(clock_pin, data_pin, *, frequency=8000, bit_depth=8, mono=True, oversample=64) \nCreate a PDMIn object associated with the given pins. This allows you to\nrecord audio signals from the given pins. Individual ports may put further\nrestrictions on the recording parameters.\n\n\nParameters:\nclock_pin (Pin) -- The pin to output the clock to\ndata_pin (Pin) -- The pin to read the data from\nfrequency (int) -- Target frequency of the resulting samples. Check frequency for real value.\nbit_depth (int) -- Final number of bits per sample. Must be divisible by 8\nmono (bool) -- True when capturing a single channel of audio, captures two channels otherwise\noversample (int) -- Number of single bit samples to decimate into a final sample. Must be divisible by 8'),
    _('analogio.AnalogOut(pin) \nUse the AnalogOut on the given pin.\n\n\nParameters:pin (Pin) -- the pin to output to'),
    _('analogio.AnalogOut.deinit() \nTurn off the AnalogOut and release the pin for other use.\n'),
    _('audiobusio.PDMIn.deinit() \nDeinitialises the PWMOut and releases any hardware resources for reuse.\n'),
    _('analogio.AnalogIn(pin) \nUse the AnalogIn on the given pin. The reference voltage varies by\nplatform so use reference_voltage to read the configured setting.\n\n\nParameters:pin (Pin) -- the pin to read from'),
    _('analogio.AnalogIn.deinit() \nTurn off the AnalogIn and release the pin for other use.\n'),
]
