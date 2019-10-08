"""
Contains definitions for the Python APIs shared by all modes so they can be
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


SHARED_APIS = [
    # String functions
    _(
        "find(sub, start, end) \nReturn the lowest index in the string where substring 'sub' is found. The optional\n'start' and 'end' arguments specify the slice of string to use.\nReturns -1 if 'sub' cannot be found."
    ),
    _(
        "rfind(sub, start, end) \nReturn the highest index in the string where substring 'sub' is found. The optional\n'start' and 'end' arguments specify the slice of string to use.\nReturns -1 if 'sub' cannot be found."
    ),
    _(
        "index(sub, start, end) \nReturn the lowest index in the string where substring 'sub' is found. The optional\n'start' and 'end' arguments specify the slice of string to use.\nRaises a ValueError if 'sub' cannot be found."
    ),
    _(
        "rindex(sub, start, end) \nReturn the highest index in the string where substring 'sub' is found. The optional\n'start' and 'end' arguments specify the slice of string to use.\nRaises a ValueError if 'sub' cannot be found."
    ),
    _(
        "join(iterable) \nReturn a string which is the concatenation of the strings in 'iterable'.\nThe separator between elements is the string providing this method."
    ),
    _(
        "split(sep=None, maxsplit=-1) \nReturn a list of the words in a string, using 'sep' as the delimiter string.\nIf 'sep' is not provided, the splitting algorithm uses whitespace.\nIf the optional 'maxsplit' is provided, splitting will occur 'maxsplit' times."
    ),
    _(
        "rsplit(sep=None, maxsplit=-1) \nReturn a list of the words in a string, using 'sep' as the delimiter string.\nIf 'sep' is not provided, the splitting algorithm uses whitespace.\nIf the optional 'maxsplit' is provided, splitting will only occur 'maxsplit'\ntimes from the right."
    ),
    _("startswith(prefix) \nReturns True if the string starts with 'prefix'."),
    _("endswith(suffix) \nReturns True if the string ends with 'suffix'."),
    _(
        "strip(chars) \nReturn a copy of the string with the leading and trailing characters removed.\nThe chars argument is a string specifying the set of characters to be removed.\nIf omitted or None, the chars argument defaults to removing whitespace.\nThe chars argument is not a prefix or suffix; rather, all combinations of its values are stripped"
    ),
    _(
        "lstrip(chars) \nReturn a copy of the string with leading characters removed. The chars argument\nis a string specifying the set of characters to be removed.\nIf omitted or None, the chars argument defaults to removing whitespace.\nThe chars argument is not a prefix; rather, all combinations of its values are\nstripped"
    ),
    _(
        "rstrip(chars) \nReturn a copy of the string with trailing characters removed. The chars argument\nis a string specifying the set of characters to be removed.\nIf omitted or None, the chars argument defaults to removing whitespace.\nThe chars argument is not a suffix; rather, all combinations of its values are\nstripped"
    ),
    _(
        "format(*args, **kwargs) \nPerform a string formatting operation. The string on which this method is called\ncan contain literal text or replacement fields delimited by braces {}. Each\nreplacement field contains either the numeric index of a positional argument,\nor the name of a keyword argument.\nReturns a copy of the string where each replacement field is replaced with the\nstring value of the corresponding argument."
    ),
    _(
        "replace(old, new) \nReturn a copy of the string with all othe occurrences of 'old' replaced with 'new'."
    ),
    _(
        "count(sub, start, end) \nReturn the number of non-overlapping occurrences of substring 'sub'.\nOptional arguments 'start' and 'end' specify the slice of the string to use. "
    ),
    _(
        "partition(sep) \nSplit the string at the first occurrence of 'sep', and return a 3-tuple containing\nthe part before the separator, the separator itself, and the part after the separator.\nIf the separator is not found, return a 3-tuple containing the string itself,\nfollowed by two empty strings."
    ),
    _(
        "rpartition(sep) \nSplit the string at the last occurrence of 'sep', and return a 3-tuple containing\nthe part before the separator, the separator itself, and the part after the separator.\nIf the separator is not found, return a 3-tuple containing two empty strings,\nfollowed by the string itself."
    ),
    _(
        "lower() \nReturn a copy of the string with all the cased characters converted to lowercase."
    ),
    _(
        "upper() \nReturn a copy of the string with all the cased characters converted to uppercase."
    ),
    _(
        "isspace() \nReturn True if there are only whitespace characters in the string and thers is\nat least one character."
    ),
    _(
        "isalpha() \nReturn True if all the characters in the string are alphabetic and there is\nat least one character."
    ),
    _(
        "isdigit() \nReturn True if all characters in the string are digits and there is\nat least one character."
    ),
    _(
        "isupper() \nReturn True if all characters in the string are uppercase and there is\nat least one character."
    ),
    _(
        "islower() \nReturn True if all characters in the string are lowercase and there is\nat least one character."
    ),
    # built-in functions
    _("abs(x) \nReturn the absolute value of the number 'x'."),
    _(
        "all(iterable) \nReturn True if all elements of iterable are true (or iterable is empty)."
    ),
    _(
        "any(iterable) \nReturn True if any element of iterable is true. If iterable is empty, return False."
    ),
    _("bin(x) \nConvert an integer (whole) number into a binary string."),
    _(
        "bool(x) \nReturn a Boolean value, i.e. one of True or False. The argument 'x' is used to\ngenerate the resulting truth value."
    ),
    _(
        "bytearray(seq) \nReturn a new array of bytes specified by the sequence 'seq' of integers."
    ),
    _(
        "bytes(seq) \nReturn a new 'bytes' object - an immutable sequence of 'seq' integers."
    ),
    _(
        "callable(object) \nReturn True if the 'object' appears to be callable. Otherwise return False."
    ),
    _(
        "chr(i) \nReturn a string representing a character whose Unicode code point is the integer 'i'."
    ),
    _(
        "classmethod(function) \nReturn a class method for a function. Usually used as a decorator:\n\nclass C:\n  @classmethod\n  def func(cls): ..."
    ),
    _("dict(): \nCreate a new dictionary object."),
    _(
        "dir(object) \nReturn a list of names in the scope of 'object'. If no object is supplied,\nreturns a ist of names in the current local scope."
    ),
    _(
        "divmod(a, b) \nTake two (non complex) numbers and return a pair of numbers consisting of the quotient and remainder. For example, divmod(5, 4) results in (1, 1). That is, what's is 5 divided by 4? It's 1 remainder 1."
    ),
    _(
        "enumerate(iterable, start=0) \nReturn an enumerate object from an iterable object.\nEach iteration of the resulting object returns a tuple containing a count and the value. For example:\n\nseasons = ['Spring', 'Summer', 'Autumn', 'Winter']\nlist(enumerate(seasons))\n[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]"
    ),
    _(
        "eval(expression, globals=None, locals=None) \nThe 'expression' string containing a Python expression is parsed and evaluated given\nthe context specified by 'globals' and 'locals' which must be dictionary objects."
    ),
    _(
        "exec(object, globals, locals) \nThis function supports dynamic execution of Python code. The 'object' must be\na string containing Python code that can be parsed and evaluated. If `globals` and\n`locals` are emitted the code is executed in the local scope. Otherwise, both\n'globals' and 'locals' must be dictionary objects."
    ),
    _(
        "filter(function, iterable) \nConstruct an iterator from those elements of 'iterable' for which 'function' returns True."
    ),
    _(
        "float(x) \nReturn a floating point number constructed from a number or string 'x'."
    ),
    _(
        "frozenset(iterable) \nReturn a new frozenset object, optionally with elements taken from 'iterable'."
    ),
    _(
        "getattr(object, name, default) \nReturn the value fo the named attribute of 'object'. 'name' must be a string.\nOptionally return 'default' if 'name' is not an attribute of 'object'."
    ),
    _(
        "globals() \nReturn a dictionary representing the current global symbol table.\nI.e. named objects that are currently in the global scope."
    ),
    _(
        "hasattr(object, name) \nReturns True if the 'object' has an attribute called 'name'. 'name' must be a string."
    ),
    _(
        "hash(object) \nReturn a hash value of the object (if it has one). Hash values are integers."
    ),
    _(
        "help(object) \nInvoke the built-in help system (intended for interactive use in the REPL."
    ),
    _(
        "hex(x) \nConvert an integer 'x' to a lowercase hexadevimal string prefixed with '0x'. For example, hex(255) returns '0xff'."
    ),
    _(
        "id(object) \nReturn the identity of an object. This is an integer that is guaranteed to be unique."
    ),
    _(
        "int(x, base=10) \nReturn an integer constructed from a number or string 'x'. The optional 'base' (indicating the base of the number) defaults to 10."
    ),
    _(
        "isinstance(object, classinfo) \nReturn True if the 'object' is an instance of 'classinfo'."
    ),
    _(
        "issubclass(class, classinfo) \nReturn True if the 'class' is a subclass (direct, indirect or virtual) of 'classinfo'."
    ),
    _(
        "iter(object) \nReturn an iterator object for the 'object' (that must support the iteration protocol."
    ),
    _("len(object) \nReturn the length (the number of items) in an 'object'."),
    _(
        "list(iterable) \nReturn a list, optionally based upon the members of 'iterable'."
    ),
    _(
        "locals() \nReturn a dictionary representing the current local symbol table. I.e. named objects\nthat are currently in the local scope."
    ),
    _(
        "map(function, iterable) \nReturn an iterator that applies 'function' to every item of 'iterable', yielding the results."
    ),
    _(
        "max(items) \nReturn the largest item in 'items', which can be either an iterable or two or more arguments."
    ),
    _(
        "min(items) \nReturn the smallest item in 'items', which can be either an iterable or two or more arguments."
    ),
    _("next(iterator) \nRetrieve the next item from the iterator."),
    _("object() \nReturn a new featureless object."),
    _("oct(x) \nConvert an integer number to an octal (base 8) string."),
    _(
        "open(file, mode='rt') \nOpen 'file' and return a corresponding file object. The 'mode' is an optional\nstring that specifies how the file is opened:\n'r' - open for reading\n'w' - open for writing\n'b' - binary mode\n't' - text mode."
    ),
    _(
        "ord(c) \nGiven a string representing one Unicode character, return an integer representing the Unicode code point of that character."
    ),
    _(
        "pow(x, y, z) \nReturn 'x' to the power of 'y'. If the optional 'z' is given, return 'x' to the power of 'y' modulo 'z' (giving the remainder)."
    ),
    _(
        "print(*objects, sep=' ', end='\\n') \nPrint objects, separated by 'sep' and followed by 'end'.\nAll non-keyword arguments are converted to strings."
    ),
    _(
        "range(start, stop, step) \nReturn an immutable sequence containing items between 'start' and 'stop' with 'step' difference between them."
    ),
    _(
        "repr(object) \nReturn a string containing a printable representation of an 'object'."
    ),
    _("reversed(seq) \nReturn a reverse iterator of the sequence 'seq'."),
    _(
        "round(number, ndigits) \nReturn the floating point 'number' rounded to the (optional) 'ndigits'.\nIf 'ndigits' is omitted, round to the nearest whole number."
    ),
    _(
        "set(iterable) \nReturn a new set object, optionally containing elements taken from iterable."
    ),
    _(
        "setattr(object, name, value) \nSet the 'value' to the attribute called 'name' on object 'object'. 'name' must be a string."
    ),
    _(
        "sorted(iterable, key, reverse) \nReturn a new sorted list from the items in iterable. The optional 'key' specifies\na function used for comparison and the optional 'reverse' is a boolean indicating the comparison should be reversed."
    ),
    _(
        "staticmethod(function) \nReturns a static method for a function. Usually used as a decorator:\n\nclass C:\n  @staticmethod\ndef func(): ..."
    ),
    _("str(object) \nReturn a string version of 'object'."),
    _(
        "sum(iterable, start=0) \nSums 'start' and items of an iterable from left to right and returns the total."
    ),
    _(
        "super(type, object-or-type) \nReturn a proxy object that delegates method calls to a parent or sibling class\nof 'type'. This is useful for accessing inherited methods that have been\noverridden in a class."
    ),
    _(
        "tuple(iterable) \nReturn an immutable sequence based upon the items in 'iterable'."
    ),
    _(
        "type(object) \nReturn the type of an object (i.e. what sort of thing it is)."
    ),
    _(
        "zip(*iterables) \nMake an iterator that aggregates elements from each of the passed in iterables.\nFor example:\nx = [1, 2, 3]\ny = [4, 5, 6]\nlist(zip(x, y))\n[(1, 4), (2, 5), (3, 6)]"
    ),
]
