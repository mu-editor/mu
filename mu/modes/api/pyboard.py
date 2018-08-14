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
    _('pyb.delay(ms) \nDelay for the given number of milliseconds.\n\n\n\nParameters:\nms (int) -- the number of milliseconds to delay.\n'),
    _('pyb.udelay(us) \nDelay for the given number of microseconds.\n\n\n\nParameters:\nus (int) -- the number of microseconds to delay.\n'),
    _('pyb.millis() \nReturns the number of milliseconds since the board was last reset.\n\n\n\nReturns: milliseconds since reset.\n\nReturn type: int\n\n'),
    _('pyb.micros() \nReturns the number of microseconds since the board was last reset.\n\n\n\nReturns: microseconds since reset.\n\nReturn type: int\n\n'),
    _('pyb.elapsed_millis(start) \nReturns the number of milliseconds which have elapsed since start.\n\n\n\nParameters:\nstart (int) -- the number of milliseconds to start counting from.\n\n\n\nReturns: milliseconds since start.\n\nReturn type: int\n\n'),
    _('pyb.elapsed_micros(start) \nReturns the number of microseconds which have elapsed since start.\n\n\n\nParameters:\nstart (int) -- the number of microseconds to start counting from.\n\n\n\nReturns: microseconds since start.\n\nReturn type: int\n\n'),
    _('pyb.hard_reset() \nResets the board in a manner similar to pushing the external RESET button.\n'),
    _('pyb.bootloader() \nActivate the bootloader without BOOT* pins.\n'),
    _('pyb.fault_debug(valus) \nEnable or disable hard-fault debugging.\n\|A hard-fault is when there is a fatal error in the underlying system, like an invalid memory access.\n\n\n\nParameters:\nvalue (bool) -- \n\nFalse: board will automatically reset if there is a hard fault\nTrue:when the board has a hard fault, it will print the registers and the stack trace, and then cycle the LEDs indefinitely\n'),
    _('pyb.disable_irq() \nDisable interrupt requests.\n\n\n\nReturns: Previous IRQ state.\n\nReturn type: bool\n\n'),
    _('pyb.enable_irq(state=True) \nEnable interrupt requests.\n\n\n\nParameters:\nstate (bool) -- Whether the IRQs are enabled\n\n'),
    _('pyb.freq([sysclk[, hclk[, pclk1[, pclk2]]]]) \nIf given no arguments, returns a tuple of clock frequencies: (sysclk, hclk, pclk1, pclk2). Otherwise, sets the frequency of the CPU, and the busses if additional arguments are given.\n\n\n\nParameters:\nsysclk (int) [optional] -- frequency of the CPU in MHz.\nhclk (int) [optional] -- frequency of the AHB bus, core memory and DMA.\npclk1 (int) [optional] -- frequency of the APB1 bus.\npclk2 (int) [optional] -- frequency of the APB2 bus.\n\n\n\nReturns: clock frequencies.\n\nReturn type: tuple\n\n'),
    _('pyb.wfi() \nWait for an internal or external interrupt. This function will block for at most 1ms.\n'),
    _('pyb.stop() \nPut the board in a “sleeping” state. To wake from this sleep state requires an external interrupt or a real-time-clock event. Upon waking execution continues where it left off.\n'),
    _('pyb.standby() \nPut the board into a “deep sleep” state. To wake from this sleep state requires a real-time-clock event, or an external interrupt on X1 (PA0=WKUP) or X18 (PC13=TAMP1). Upon waking the system undergoes a hard reset.\n'),
    _('pyb.info([dump_alloc_table]) \nPrint out lots of information about the board.\n\n\n\nParameter:\ndump_alloc_table (bool) [optional] -- Whether to dump the alloc table.\n\n'),
    _('pyb.main(filename) \nSet the filename of the main script to run after boot.py is finished.\n\nIt only makes sense to call this function from within boot.py.\n\n\n\nParameter:\nfilename (string) -- name of the desired main file.\n\n'),
    _('pyb.mount(device, mountpoint, *, readonly=False, mkfs=False) \nMount a block device and make it available as part of the filesystem.\n\nSee online documentation for full instructions.\n'),
    _('pyb.repl_uart(uart) \nGet or set the UART object where the REPL is repeated on.\n\n\n\nParameter:\nuart (pyb.UART) -- The uart to use\n.'),
    _('pyb.rng() \nReturn a 30-bit hardware generated random number.\n\n\n\nReturns: 30-bit random number.\n\nReturn value: int\n\n'),
    _('pyb.sync() \nSync all file systems.\n'),
    _('pyb.unique_id() \nReturns a string of 12 bytes (96 bits), which is the unique ID of the MCU.\n\n\n\nReturns: unique ID of the MCU.\n\nReturn value: string\n\n'),
    _('pyb.usb_mode([modestr, ]vid=0xf055, pid=0x9801, hid=pyb.hid_mouse) \nIf called with no arguments, return the current USB mode as a string. If called with modestr provided, attempts to set USB mode.\n\nThis can only be done when called from boot.py before pyb.main() has been called.\n\nSee online documentation for full instructions.\n'),
]
