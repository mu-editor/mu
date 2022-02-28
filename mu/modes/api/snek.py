"""
Contains definitions for the Snek APIs so they can be
used in the editor for autocomplete and call tips.

Copyright © 2019 Keith Packard

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


SNEK_APIS = [
    # built-in functions
    _(
        "chr(i) \nReturn a string representing a character whose Unicode code point is the integer 'i'."
    ),
    _(
        "ord(c) \nGiven a string representing one Unicode character, return an integer representing the Unicode code point of that character."
    ),
    _("len(object) \nReturn the length (the number of items) in an 'object'."),
    _(
        "print(*objects, end='\\n') \nPrint objects followed by 'end'.\nAll non-keyword arguments are converted to strings."
    ),
    _("sys.stdout.flush() \nFlush pending output to the console."),
    _(
        "range(start, stop, step) \nReturn an immutable sequence containing items between 'start' and 'stop' with 'step' difference between them."
    ),
    # math
    # Number-theoretic and representation functions
    _(
        "math.ceil(x) \nReturn the ceiling of x, the smallest integer greater than or equal to x."
    ),
    _(
        "math.copysign(x,y) \nReturn a number with the magnitude (absolute value) of x but the sign of y."
    ),
    _("math.fabs(x) \nReturn the absolute value of x."),
    _("math.factorial(x) \nReturn the factorial of x."),
    _(
        "math.floor(x) \nReturn the floor of x, the largest integer less than or equal to x."
    ),
    _("math.fmod(x,y) \nReturn the modulus of x and y: x - trunc(x/y) * y."),
    _(
        "math.frexp(x) \nReturns the normalized fraction and exponent in a tuple (frac, exp). 0.5 ≤ abs(frac) < 1,\n"
        "and x = frac * pow(2,exp)."
    ),
    _(
        "math.fsum(l) \nReturns the sum of the numbers in l, which must be a list or tuple."
    ),
    _("math.gcd(x,y) \nReturn the greatest common divisor of x and y."),
    _(
        "math.isclose(x,y,rel_val=1e-6,abs_val=0.0) \nReturns a boolean indicating whether x and y are 'close'\n"
        "together. This is defined as abs(x-y) ≤ max(rel_tol * max(abs(a), abs(b)), abs_tol)."
    ),
    _("math.isfinite(x) \nReturns True if x is finite else False."),
    _("math.isinf \nReturns True if x is infinite else False."),
    _("math.isnan \nReturns True if x is not a number else False."),
    _("math.ldexp(x,y) \nReturns x * pow(2,y)."),
    _("math.modf(x) \nReturns (x - trunc(x), trunc(x))."),
    _(
        "math.remainder(x,y) \nReturns the remainder of x and y: x - round(x/y) * y."
    ),
    _(
        "math.trunc \nReturns the truncation of x, the integer closest to x which is no further from zero than x."
    ),
    _(
        "round(x) \nReturns the integer nearest x, with values midway between two integers rounding away from zero."
    ),
    # Power and logarithmic functions
    _("math.exp(x) \nReturns pow(e,x)."),
    _("math.expm1(x) \nReturns exp(x)-1."),
    _("math.exp2(x) \nReturns pow(2,x)."),
    _("math.log(x) \nReturns the natural logarithm of x."),
    _("math.log1p(x) \nReturns log(x+1)."),
    _("math.log2(x) \nReturns the log base 2 of x."),
    _("math.log10(x) \nReturns the log base 10 of x."),
    _("math.pow(x,y) \nReturns x raised to the y^th^ power."),
    _("math.sqrt(x) \nReturn the square root of x."),
    # Trigonometric functions
    _(
        "math.acos(x) \nReturns the arc cosine of x in the range of 0 ≤ acos(x) ≤ π."
    ),
    _(
        "math.asin(x) \nReturns the arc sine of x in the range of -π/2 ≤ asin(x) ≤ π/2."
    ),
    _(
        "math.atan(x) \nReturns the arc tangent of x in the range of -π/2 ≤ atan(x) ≤ π/2."
    ),
    _(
        "math.atan2(y,x) \nReturns the arc tangent of y/x in the range of -π ≤ atan2(y,x) ≤ π."
    ),
    _("math.cos(x) \nReturns the cosine of x."),
    _("math.hypot(x,y) \nReturns sqrt(x*x + y*y)."),
    _("math.sin(x) \nReturns the sine of x."),
    _("math.tan(x) \nReturns the tangent of x."),
    # Angular conversion
    _("math.degrees(x) \nReturns x * 180/π."),
    _("math.radians(x) \nReturns x * π/180."),
    # Hyperbolic functions
    _("math.acosh(x) \nReturns the inverse hyperbolic cosine of x."),
    _("math.asinh(x) \nReturns the inverse hyperbolic sine of x."),
    _("math.atanh(x) \nReturns the inverse hyperbolic tangent of x."),
    _(
        "math.cosh(x) \nReturns the hyperbolic cosine of x: (exp(x) + exp(-x)) / 2."
    ),
    _(
        "math.sinh(x) \nReturns the hyperbolic sine of x: (exp(x) - exp(-x)) / 2."
    ),
    _(
        "math.tanh(x) \nReturns the hyperbolic tangent of x: sinh(x) / cosh(x)."
    ),
    # Special functions
    _("math.erf(x) \nReturns the error function at x."),
    _(
        "math.erfc(x) \nReturns the complement of the error function at x. This is 1 - erf(x)."
    ),
    _("math.gamma(x) \nReturns the gamma function at x."),
    _("math.lgamma(x) \nReturns log(gamma(x))."),
    # GPIO
    _(
        "talkto(p) \nSets the current output pins. If p is a number, set both power and dir.\n"
        "If p is a list or tuple, set power to p[0] and dir to p[1]."
    ),
    _("setpower(p) \nSets output level for power pin to p."),
    _("setleft() \nSets dir pin to 1."),
    _("setright() \nSets dir pin to 0."),
    _("on() \nTurn power pin on."),
    _("off() \nTurn power pin off."),
    _("onfor(s) \nTurn power pin on for s seconds, then turn power pin off."),
    _("read(p) \nReturn current value on pin p."),
    _("pullnone(p) \nDisables pull-up/pull-down mode on pin p."),
    _("pullup(p) \nEnable pull-up on pin p."),
    _("pulldown(p) \nEnable pull-down on pin p."),
    _("stopall() \nTurn off all pins."),
    _("neopixel(pixels) \nSend new pixel data to neopixels on power pin."),
    # Common
    _("time.sleep(s) \nDelay execution for s seconds.\n"),
    _("time.monotonic() \nReturns time in seconds since some reference time"),
    _(
        "random.seed(s) \nRe-initialize random number generator using s as the seed."
    ),
    _(
        "random.randrange(m) \nReturns a random integer between 0 and m-1 inclusive."
    ),
]
