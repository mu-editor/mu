"""
Contains definitions for Python 3 APIs so they can be used in the editor for
autocomplete and call tips.

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


PYTHON3_APIS = [
    _(
        "argparse.Action(option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None) \nInformation about how to convert command line strings to Python objects.\n\nAction objects are used by an ArgumentParser to represent the information\nneeded to parse a single argument from one or more strings from the\ncommand line. The keyword arguments to the Action constructor are also\nall attributes of Action instances.\n\nKeyword Arguments:\n\n    - option_strings -- A list of command-line option strings which\n        should be associated with this action.\n\n    - dest -- The name of the attribute to hold the created object(s)\n\n    - nargs -- The number of command-line arguments that should be\n        consumed. By default, one argument will be consumed and a single\n        value will be produced.  Other values include:\n            - N (an integer) consumes N arguments (and produces a list)\n            - '?' consumes zero or one arguments\n            - '*' consumes zero or more arguments (and produces a list)\n            - '+' consumes one or more arguments (and produces a list)\n        Note that the difference between the default and nargs=1 is that\n        with the default, a single value will be produced, while with\n        nargs=1, a list containing a single value will be produced.\n\n    - const -- The value to be produced if the option is specified and the\n        option uses an action that takes no values.\n\n    - default -- The value to be produced if the option is not specified.\n\n    - type -- A callable that accepts a single string argument, and\n        returns the converted value.  The standard Python types str, int,\n        float, and complex are useful examples of such callables.  If None,\n        str is used.\n\n    - choices -- A container of values that should be allowed. If not None,\n        after a command-line argument has been converted to the appropriate\n        type, an exception will be raised if it is not a member of this\n        collection.\n\n    - required -- True if the action must always be specified at the\n        command line. This is only meaningful for optional command-line\n        arguments.\n\n    - help -- The help string describing the argument.\n\n    - metavar -- The name to be used for the option's argument with the\n        help string. If None, the 'dest' value will be used as the name."
    ),
    _(
        "argparse.ArgumentDefaultsHelpFormatter(prog, indent_increment=2, max_help_position=24, width=None) \nHelp message formatter which adds default values to argument help.\n\nOnly the name of this class is considered a public API. All the methods\nprovided by the class are considered an implementation detail."
    ),
    _(
        "argparse.ArgumentError(argument, message) \nAn error from creating or using an argument (optional or positional).\n\nThe string value of this exception is the message, augmented with\ninformation about the argument that caused it."
    ),
    _(
        "argparse.ArgumentParser(prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=<class 'argparse.HelpFormatter'>, prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True, allow_abbrev=True) \nObject for parsing command line strings into Python objects.\n\nKeyword Arguments:\n    - prog -- The name of the program (default: sys.argv[0])\n    - usage -- A usage message (default: auto-generated from arguments)\n    - description -- A description of what the program does\n    - epilog -- Text following the argument descriptions\n    - parents -- Parsers whose arguments should be copied into this one\n    - formatter_class -- HelpFormatter class for printing help messages\n    - prefix_chars -- Characters that prefix optional arguments\n    - fromfile_prefix_chars -- Characters that prefix files containing\n        additional arguments\n    - argument_default -- The default value for all arguments\n    - conflict_handler -- String indicating how to handle conflicts\n    - add_help -- Add a -h/-help option\n    - allow_abbrev -- Allow long options to be abbreviated unambiguously"
    ),
    _(
        "argparse.ArgumentTypeError() \nAn error from trying to convert a command line string to a type."
    ),
    _(
        "argparse.FileType(mode='r', bufsize=-1, encoding=None, errors=None) \nFactory for creating file object types\n\nInstances of FileType are typically passed as type= arguments to the\nArgumentParser add_argument() method.\n\nKeyword Arguments:\n    - mode -- A string indicating how the file is to be opened. Accepts the\n        same values as the builtin open() function.\n    - bufsize -- The file's desired buffer size. Accepts the same values as\n        the builtin open() function.\n    - encoding -- The file's encoding. Accepts the same values as the\n        builtin open() function.\n    - errors -- A string indicating how encoding and decoding errors are to\n        be handled. Accepts the same value as the builtin open() function."
    ),
    _(
        "argparse.HelpFormatter(prog, indent_increment=2, max_help_position=24, width=None) \nFormatter for generating usage messages and argument help strings.\n\nOnly the name of this class is considered a public API. All the methods\nprovided by the class are considered an implementation detail."
    ),
    _(
        "argparse.MetavarTypeHelpFormatter(prog, indent_increment=2, max_help_position=24, width=None) \nHelp message formatter which uses the argument 'type' as the default\nmetavar value (instead of the argument 'dest')\n\nOnly the name of this class is considered a public API. All the methods\nprovided by the class are considered an implementation detail."
    ),
    _(
        "argparse.Namespace(**kwargs) \nSimple object for storing attributes.\n\nImplements equality by attribute names and values, and provides a simple\nstring representation."
    ),
    _(
        "argparse.RawDescriptionHelpFormatter(prog, indent_increment=2, max_help_position=24, width=None) \nHelp message formatter which retains any formatting in descriptions.\n\nOnly the name of this class is considered a public API. All the methods\nprovided by the class are considered an implementation detail."
    ),
    _(
        "argparse.RawTextHelpFormatter(prog, indent_increment=2, max_help_position=24, width=None) \nHelp message formatter which retains formatting of all help text.\n\nOnly the name of this class is considered a public API. All the methods\nprovided by the class are considered an implementation detail."
    ),
    _(
        "array.array() \narray(typecode [, initializer]) -> array\n\nReturn a new array whose items are restricted by typecode, and\ninitialized from the optional initializer value, which must be a list,\nstring or iterable over elements of the appropriate type.\n\nArrays represent basic values and behave very much like lists, except\nthe type of objects stored in them is constrained. The type is specified\nat object creation time by using a type code, which is a single character.\nThe following type codes are defined:\n\n    Type code   C Type             Minimum size in bytes \n    'b'         signed integer     1 \n    'B'         unsigned integer   1 \n    'u'         Unicode character  2 (see note) \n    'h'         signed integer     2 \n    'H'         unsigned integer   2 \n    'i'         signed integer     2 \n    'I'         unsigned integer   2 \n    'l'         signed integer     4 \n    'L'         unsigned integer   4 \n    'q'         signed integer     8 (see note) \n    'Q'         unsigned integer   8 (see note) \n    'f'         floating point     4 \n    'd'         floating point     8 \n\nNOTE: The 'u' typecode corresponds to Python's unicode character. On \nnarrow builds this is 2-bytes on wide builds this is 4-bytes.\n\nNOTE: The 'q' and 'Q' type codes are only available if the platform \nC compiler used to build Python supports 'long long', or, on Windows, \n'__int64'.\n\nMethods:\n\nappend() -- append a new item to the end of the array\nbuffer_info() -- return information giving the current memory info\nbyteswap() -- byteswap all the items of the array\ncount() -- return number of occurrences of an object\nextend() -- extend array by appending multiple elements from an iterable\nfromfile() -- read items from a file object\nfromlist() -- append items from the list\nfrombytes() -- append items from the string\nindex() -- return index of first occurrence of an object\ninsert() -- insert a new item into the array at a provided position\npop() -- remove and return item (default last)\nremove() -- remove first occurrence of an object\nreverse() -- reverse the order of the items in the array\ntofile() -- write all items to a file object\ntolist() -- return the array converted to an ordinary list\ntobytes() -- return the array converted to a string\n\nAttributes:\n\ntypecode -- the typecode character used to create the array\nitemsize -- the length in bytes of one array item"
    ),
    _(
        "array.array() \narray(typecode [, initializer]) -> array\n\nReturn a new array whose items are restricted by typecode, and\ninitialized from the optional initializer value, which must be a list,\nstring or iterable over elements of the appropriate type.\n\nArrays represent basic values and behave very much like lists, except\nthe type of objects stored in them is constrained. The type is specified\nat object creation time by using a type code, which is a single character.\nThe following type codes are defined:\n\n    Type code   C Type             Minimum size in bytes \n    'b'         signed integer     1 \n    'B'         unsigned integer   1 \n    'u'         Unicode character  2 (see note) \n    'h'         signed integer     2 \n    'H'         unsigned integer   2 \n    'i'         signed integer     2 \n    'I'         unsigned integer   2 \n    'l'         signed integer     4 \n    'L'         unsigned integer   4 \n    'q'         signed integer     8 (see note) \n    'Q'         unsigned integer   8 (see note) \n    'f'         floating point     4 \n    'd'         floating point     8 \n\nNOTE: The 'u' typecode corresponds to Python's unicode character. On \nnarrow builds this is 2-bytes on wide builds this is 4-bytes.\n\nNOTE: The 'q' and 'Q' type codes are only available if the platform \nC compiler used to build Python supports 'long long', or, on Windows, \n'__int64'.\n\nMethods:\n\nappend() -- append a new item to the end of the array\nbuffer_info() -- return information giving the current memory info\nbyteswap() -- byteswap all the items of the array\ncount() -- return number of occurrences of an object\nextend() -- extend array by appending multiple elements from an iterable\nfromfile() -- read items from a file object\nfromlist() -- append items from the list\nfrombytes() -- append items from the string\nindex() -- return index of first occurrence of an object\ninsert() -- insert a new item into the array at a provided position\npop() -- remove and return item (default last)\nremove() -- remove first occurrence of an object\nreverse() -- reverse the order of the items in the array\ntofile() -- write all items to a file object\ntolist() -- return the array converted to an ordinary list\ntobytes() -- return the array converted to a string\n\nAttributes:\n\ntypecode -- the typecode character used to create the array\nitemsize -- the length in bytes of one array item"
    ),
    _(
        "base64.a85decode(b, *, foldspaces=False, adobe=False, ignorechars=b' \\t\\n\\r\\x0b') \nDecode the Ascii85 encoded bytes-like object or ASCII string b.\n\nfoldspaces is a flag that specifies whether the 'y' short sequence should be\naccepted as shorthand for 4 consecutive spaces (ASCII 0x20). This feature is\nnot supported by the \"standard\" Adobe encoding.\n\nadobe controls whether the input sequence is in Adobe Ascii85 format (i.e.\nis framed with <~ and ~>).\n\nignorechars should be a byte string containing characters to ignore from the\ninput. This should only contain whitespace characters, and by default\ncontains all whitespace characters in ASCII.\n\nThe result is returned as a bytes object."
    ),
    _(
        "base64.a85encode(b, *, foldspaces=False, wrapcol=0, pad=False, adobe=False) \nEncode bytes-like object b using Ascii85 and return a bytes object.\n\nfoldspaces is an optional flag that uses the special short sequence 'y'\ninstead of 4 consecutive spaces (ASCII 0x20) as supported by 'btoa'. This\nfeature is not supported by the \"standard\" Adobe encoding.\n\nwrapcol controls whether the output should have newline (b'\\n') characters\nadded to it. If this is non-zero, each output line will be at most this\nmany characters long.\n\npad controls whether the input is padded to a multiple of 4 before\nencoding. Note that the btoa implementation always pads.\n\nadobe controls whether the encoded byte sequence is framed with <~ and ~>,\nwhich is used by the Adobe implementation."
    ),
    _(
        "base64.b16decode(s, casefold=False) \nDecode the Base16 encoded bytes-like object or ASCII string s.\n\nOptional casefold is a flag specifying whether a lowercase alphabet is\nacceptable as input.  For security purposes, the default is False.\n\nThe result is returned as a bytes object.  A binascii.Error is raised if\ns is incorrectly padded or if there are non-alphabet characters present\nin the input."
    ),
    _(
        "base64.b16encode(s) \nEncode the bytes-like object s using Base16 and return a bytes object.\n    "
    ),
    _(
        "base64.b32decode(s, casefold=False, map01=None) \nDecode the Base32 encoded bytes-like object or ASCII string s.\n\nOptional casefold is a flag specifying whether a lowercase alphabet is\nacceptable as input.  For security purposes, the default is False.\n\nRFC 3548 allows for optional mapping of the digit 0 (zero) to the\nletter O (oh), and for optional mapping of the digit 1 (one) to\neither the letter I (eye) or letter L (el).  The optional argument\nmap01 when not None, specifies which letter the digit 1 should be\nmapped to (when map01 is not None, the digit 0 is always mapped to\nthe letter O).  For security purposes the default is None, so that\n0 and 1 are not allowed in the input.\n\nThe result is returned as a bytes object.  A binascii.Error is raised if\nthe input is incorrectly padded or if there are non-alphabet\ncharacters present in the input."
    ),
    _(
        "base64.b32encode(s) \nEncode the bytes-like object s using Base32 and return a bytes object.\n    "
    ),
    _(
        "base64.b64decode(s, altchars=None, validate=False) \nDecode the Base64 encoded bytes-like object or ASCII string s.\n\nOptional altchars must be a bytes-like object or ASCII string of length 2\nwhich specifies the alternative alphabet used instead of the '+' and '/'\ncharacters.\n\nThe result is returned as a bytes object.  A binascii.Error is raised if\ns is incorrectly padded.\n\nIf validate is False (the default), characters that are neither in the\nnormal base-64 alphabet nor the alternative alphabet are discarded prior\nto the padding check.  If validate is True, these non-alphabet characters\nin the input result in a binascii.Error."
    ),
    _(
        "base64.b64encode(s, altchars=None) \nEncode the bytes-like object s using Base64 and return a bytes object.\n\nOptional altchars should be a byte string of length 2 which specifies an\nalternative alphabet for the '+' and '/' characters.  This allows an\napplication to e.g. generate url or filesystem safe Base64 strings."
    ),
    _(
        "base64.b85decode(b) \nDecode the base85-encoded bytes-like object or ASCII string b\n\nThe result is returned as a bytes object."
    ),
    _(
        "base64.b85encode(b, pad=False) \nEncode bytes-like object b in base85 format and return a bytes object.\n\nIf pad is true, the input is padded with b'\\0' so its length is a multiple of\n4 bytes before encoding."
    ),
    _("base64.binascii() \nConversion between binary data and ASCII"),
    _(
        "base64.decode(input, output) \nDecode a file; input and output are binary files."
    ),
    _(
        "base64.decodebytes(s) \nDecode a bytestring of base-64 data into a bytes object."
    ),
    _("base64.decodestring(s) \nLegacy alias of decodebytes()."),
    _(
        "base64.encode(input, output) \nEncode a file; input and output are binary files."
    ),
    _(
        "base64.encodebytes(s) \nEncode a bytestring into a bytes object containing multiple lines\nof base-64 data."
    ),
    _("base64.encodestring(s) \nLegacy alias of encodebytes()."),
    _("base64.main() \nSmall main program"),
    _(
        'base64.re() \nSupport for regular expressions (RE).\n\nThis module provides regular expression matching operations similar to\nthose found in Perl.  It supports both 8-bit and Unicode strings; both\nthe pattern and the strings being processed can contain null bytes and\ncharacters outside the US ASCII range.\n\nRegular expressions can contain both special and ordinary characters.\nMost ordinary characters, like "A", "a", or "0", are the simplest\nregular expressions; they simply match themselves.  You can\nconcatenate ordinary characters, so last matches the string \'last\'.\n\nThe special characters are:\n    "."      Matches any character except a newline.\n    "^"      Matches the start of the string.\n    "$"      Matches the end of the string or just before the newline at\n             the end of the string.\n    "*"      Matches 0 or more (greedy) repetitions of the preceding RE.\n             Greedy means that it will match as many repetitions as possible.\n    "+"      Matches 1 or more (greedy) repetitions of the preceding RE.\n    "?"      Matches 0 or 1 (greedy) of the preceding RE.\n    *?,+?,?? Non-greedy versions of the previous three special characters.\n    {m,n}    Matches from m to n repetitions of the preceding RE.\n    {m,n}?   Non-greedy version of the above.\n    "\\\\"     Either escapes special characters or signals a special sequence.\n    []       Indicates a set of characters.\n             A "^" as the first character indicates a complementing set.\n    "|"      A|B, creates an RE that will match either A or B.\n    (...)    Matches the RE inside the parentheses.\n             The contents can be retrieved or matched later in the string.\n    (?aiLmsux) Set the A, I, L, M, S, U, or X flag for the RE (see below).\n    (?:...)  Non-grouping version of regular parentheses.\n    (?P<name>...) The substring matched by the group is accessible by name.\n    (?P=name)     Matches the text matched earlier by the group named name.\n    (?#...)  A comment; ignored.\n    (?=...)  Matches if ... matches next, but doesn\'t consume the string.\n    (?!...)  Matches if ... doesn\'t match next.\n    (?<=...) Matches if preceded by ... (must be fixed length).\n    (?<!...) Matches if not preceded by ... (must be fixed length).\n    (?(id/name)yes|no) Matches yes pattern if the group with id/name matched,\n                       the (optional) no pattern otherwise.\n\nThe special sequences consist of "\\\\" and a character from the list\nbelow.  If the ordinary character is not on the list, then the\nresulting RE will match the second character.\n    \\number  Matches the contents of the group of the same number.\n    \\A       Matches only at the start of the string.\n    \\Z       Matches only at the end of the string.\n    \\b       Matches the empty string, but only at the start or end of a word.\n    \\B       Matches the empty string, but not at the start or end of a word.\n    \\d       Matches any decimal digit; equivalent to the set [0-9] in\n             bytes patterns or string patterns with the ASCII flag.\n             In string patterns without the ASCII flag, it will match the whole\n             range of Unicode digits.\n    \\D       Matches any non-digit character; equivalent to [^\\d].\n    \\s       Matches any whitespace character; equivalent to [ \\t\\n\\r\\f\\v] in\n             bytes patterns or string patterns with the ASCII flag.\n             In string patterns without the ASCII flag, it will match the whole\n             range of Unicode whitespace characters.\n    \\S       Matches any non-whitespace character; equivalent to [^\\s].\n    \\w       Matches any alphanumeric character; equivalent to [a-zA-Z0-9_]\n             in bytes patterns or string patterns with the ASCII flag.\n             In string patterns without the ASCII flag, it will match the\n             range of Unicode alphanumeric characters (letters plus digits\n             plus underscore).\n             With LOCALE, it will match the set [0-9_] plus characters defined\n             as letters for the current locale.\n    \\W       Matches the complement of \\w.\n    \\\\       Matches a literal backslash.\n\nThis module exports the following functions:\n    match     Match a regular expression pattern to the beginning of a string.\n    fullmatch Match a regular expression pattern to all of a string.\n    search    Search a string for the presence of a pattern.\n    sub       Substitute occurrences of a pattern found in a string.\n    subn      Same as sub, but also return the number of substitutions made.\n    split     Split a string by the occurrences of a pattern.\n    findall   Find all occurrences of a pattern in a string.\n    finditer  Return an iterator yielding a match object for each match.\n    compile   Compile a pattern into a RegexObject.\n    purge     Clear the regular expression cache.\n    escape    Backslash all non-alphanumerics in a string.\n\nSome of the functions in this module takes flags as optional parameters:\n    A  ASCII       For string patterns, make \\w, \\W, \\b, \\B, \\d, \\D\n                   match the corresponding ASCII character categories\n                   (rather than the whole Unicode categories, which is the\n                   default).\n                   For bytes patterns, this flag is the only available\n                   behaviour and needn\'t be specified.\n    I  IGNORECASE  Perform case-insensitive matching.\n    L  LOCALE      Make \\w, \\W, \\b, \\B, dependent on the current locale.\n    M  MULTILINE   "^" matches the beginning of lines (after a newline)\n                   as well as the string.\n                   "$" matches the end of lines (before a newline) as well\n                   as the end of the string.\n    S  DOTALL      "." matches any character at all, including the newline.\n    X  VERBOSE     Ignore whitespace and comments for nicer looking RE\'s.\n    U  UNICODE     For compatibility only. Ignored for string patterns (it\n                   is the default), and forbidden for bytes patterns.\n\nThis module also defines an exception \'error\'.'
    ),
    _(
        "base64.standard_b64decode(s) \nDecode bytes encoded with the standard Base64 alphabet.\n\nArgument s is a bytes-like object or ASCII string to decode.  The result\nis returned as a bytes object.  A binascii.Error is raised if the input\nis incorrectly padded.  Characters that are not in the standard alphabet\nare discarded prior to the padding check."
    ),
    _(
        "base64.standard_b64encode(s) \nEncode bytes-like object s using the standard Base64 alphabet.\n\nThe result is returned as a bytes object."
    ),
    _(
        "base64.struct() \nFunctions to convert between Python values and C structs.\nPython bytes objects are used to hold the data representing the C struct\nand also as format strings (explained below) to describe the layout of data\nin the C struct.\n\nThe optional first format char indicates byte order, size and alignment:\n  @: native order, size & alignment (default)\n  =: native order, std. size & alignment\n  <: little-endian, std. size & alignment\n  >: big-endian, std. size & alignment\n  !: same as >\n\nThe remaining chars indicate types of args and must match exactly;\nthese can be preceded by a decimal repeat count:\n  x: pad byte (no data); c:char; b:signed byte; B:unsigned byte;\n  ?: _Bool (requires C99; if not available, char is used instead)\n  h:short; H:unsigned short; i:int; I:unsigned int;\n  l:long; L:unsigned long; f:float; d:double; e:half-float.\nSpecial cases (preceding decimal count indicates length):\n  s:string (array of char); p: pascal string (with count byte).\nSpecial cases (only available in native format):\n  n:ssize_t; N:size_t;\n  P:an integer type that is wide enough to hold a pointer.\nSpecial case (not in native mode unless 'long long' in platform C):\n  q:long long; Q:unsigned long long\nWhitespace between formats is ignored.\n\nThe variable struct.error is an exception raised on errors."
    ),
    _(
        "base64.urlsafe_b64decode(s) \nDecode bytes using the URL- and filesystem-safe Base64 alphabet.\n\nArgument s is a bytes-like object or ASCII string to decode.  The result\nis returned as a bytes object.  A binascii.Error is raised if the input\nis incorrectly padded.  Characters that are not in the URL-safe base-64\nalphabet, and are not a plus '+' or slash '/', are discarded prior to the\npadding check.\n\nThe alphabet uses '-' instead of '+' and '_' instead of '/'."
    ),
    _(
        "base64.urlsafe_b64encode(s) \nEncode bytes using the URL- and filesystem-safe Base64 alphabet.\n\nArgument s is a bytes-like object to encode.  The result is returned as a\nbytes object.  The alphabet uses '-' instead of '+' and '_' instead of\n'/'."
    ),
    _(
        "collections.ByteString() \nThis unifies bytes and bytearray.\n\nXXX Should add all their methods."
    ),
    _(
        "collections.ChainMap(*maps) \nA ChainMap groups multiple dicts (or other mappings) together\nto create a single, updateable view.\n\nThe underlying mappings are stored in a list.  That list is public and can\nbe accessed or updated using the *maps* attribute.  There is no other\nstate.\n\nLookups search the underlying mappings successively until a key is found.\nIn contrast, writes, updates, and deletions only operate on the first\nmapping."
    ),
    _(
        "collections.Counter(*args, **kwds) \nDict subclass for counting hashable items.  Sometimes called a bag\nor multiset.  Elements are stored as dictionary keys and their counts\nare stored as dictionary values.\n\n>>> c = Counter('abcdeabcdabcaba')  # count elements from a string\n\n>>> c.most_common(3)                # three most common elements\n[('a', 5), ('b', 4), ('c', 3)]\n>>> sorted(c)                       # list all unique elements\n['a', 'b', 'c', 'd', 'e']\n>>> ''.join(sorted(c.elements()))   # list elements with repetitions\n'aaaaabbbbcccdde'\n>>> sum(c.values())                 # total of all counts\n15\n\n>>> c['a']                          # count of letter 'a'\n5\n>>> for elem in 'shazam':           # update counts from an iterable\n...     c[elem] += 1                # by adding 1 to each element's count\n>>> c['a']                          # now there are seven 'a'\n7\n>>> del c['b']                      # remove all 'b'\n>>> c['b']                          # now there are zero 'b'\n0\n\n>>> d = Counter('simsalabim')       # make another counter\n>>> c.update(d)                     # add in the second counter\n>>> c['a']                          # now there are nine 'a'\n9\n\n>>> c.clear()                       # empty the counter\n>>> c\nCounter()\n\nNote:  If a count is set to zero or reduced to zero, it will remain\nin the counter until the entry is deleted or the counter is cleared:\n\n>>> c = Counter('aaabbc')\n>>> c['b'] -= 2                     # reduce the count of 'b' by two\n>>> c.most_common()                 # 'b' is still in, but its count is zero\n[('a', 3), ('c', 1), ('b', 0)]"
    ),
    _(
        "collections.ItemsView(mapping) \nA set is a finite, iterable container.\n\nThis class provides concrete generic implementations of all\nmethods except for __contains__, __iter__ and __len__.\n\nTo override the comparisons (presumably for speed, as the\nsemantics are fixed), redefine __le__ and __ge__,\nthen the other operations will automatically follow suit."
    ),
    _(
        "collections.KeysView(mapping) \nA set is a finite, iterable container.\n\nThis class provides concrete generic implementations of all\nmethods except for __contains__, __iter__ and __len__.\n\nTo override the comparisons (presumably for speed, as the\nsemantics are fixed), redefine __le__ and __ge__,\nthen the other operations will automatically follow suit."
    ),
    _(
        "collections.MutableSequence() \nAll the operations on a read-only sequence.\n\nConcrete subclasses must override __new__ or __init__,\n__getitem__, and __len__."
    ),
    _(
        "collections.MutableSet() \nA mutable set is a finite, iterable container.\n\nThis class provides concrete generic implementations of all\nmethods except for __contains__, __iter__, __len__,\nadd(), and discard().\n\nTo override the comparisons (presumably for speed, as the\nsemantics are fixed), all you have to do is redefine __le__ and\nthen the other operations will automatically follow suit."
    ),
    _("collections.OrderedDict() \nDictionary that remembers insertion order"),
    _(
        "collections.Sequence() \nAll the operations on a read-only sequence.\n\nConcrete subclasses must override __new__ or __init__,\n__getitem__, and __len__."
    ),
    _(
        "collections.Set() \nA set is a finite, iterable container.\n\nThis class provides concrete generic implementations of all\nmethods except for __contains__, __iter__ and __len__.\n\nTo override the comparisons (presumably for speed, as the\nsemantics are fixed), redefine __le__ and __ge__,\nthen the other operations will automatically follow suit."
    ),
    _(
        "collections.UserList(initlist=None) \nA more or less complete user-defined wrapper around list objects."
    ),
    _(
        "collections.UserString(seq) \nAll the operations on a read-only sequence.\n\nConcrete subclasses must override __new__ or __init__,\n__getitem__, and __len__."
    ),
    _(
        "collections.defaultdict() \ndefaultdict(default_factory[, ...]) --> dict with default factory\n\nThe default factory is called without arguments to produce\na new value when a key is not present, in __getitem__ only.\nA defaultdict compares equal to a dict with the same items.\nAll remaining arguments are treated the same as if they were\npassed to the dict constructor, including keyword arguments."
    ),
    _(
        "collections.deque() \ndeque([iterable[, maxlen]]) --> deque object\n\nA list-like sequence optimized for data accesses near its endpoints."
    ),
    _(
        "collections.namedtuple(typename, field_names, *, verbose=False, rename=False, module=None) \nReturns a new subclass of tuple with named fields.\n\n>>> Point = namedtuple('Point', ['x', 'y'])\n>>> Point.__doc__                   # docstring for the new class\n'Point(x, y)'\n>>> p = Point(11, y=22)             # instantiate with positional args or keywords\n>>> p[0] + p[1]                     # indexable like a plain tuple\n33\n>>> x, y = p                        # unpack like a regular tuple\n>>> x, y\n(11, 22)\n>>> p.x + p.y                       # fields also accessible by name\n33\n>>> d = p._asdict()                 # convert to a dictionary\n>>> d['x']\n11\n>>> Point(**d)                      # convert from a dictionary\nPoint(x=11, y=22)\n>>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields\nPoint(x=100, y=22)"
    ),
    _(
        "csv.Dialect() \nDescribe a CSV dialect.\n\nThis must be subclassed (see csv.excel).  Valid attributes are:\ndelimiter, quotechar, escapechar, doublequote, skipinitialspace,\nlineterminator, quoting."
    ),
    _("csv.Error() \nCommon base class for all non-exit exceptions."),
    _("csv.OrderedDict() \nDictionary that remembers insertion order"),
    _(
        'csv.Sniffer() \n"Sniffs" the format of a CSV file (i.e. delimiter, quotechar)\nReturns a Dialect object.'
    ),
    _(
        "csv.StringIO(initial_value='', newline='\\n') \nText I/O implementation using an in-memory buffer.\n\nThe initial_value argument sets the value of object.  The newline\nargument is like the one of TextIOWrapper's constructor."
    ),
    _(
        "csv.excel() \nDescribe the usual properties of Excel-generated CSV files."
    ),
    _(
        "csv.excel_tab() \nDescribe the usual properties of Excel-generated TAB-delimited files."
    ),
    _(
        "csv.field_size_limit() \nSets an upper limit on parsed fields.\n    csv.field_size_limit([limit])\n\nReturns old limit. If limit is not given, no new limit is set and\nthe old limit is returned"
    ),
    _(
        "csv.get_dialect() \nReturn the dialect instance associated with name.\ndialect = csv.get_dialect(name)"
    ),
    _(
        "csv.list_dialects() \nReturn a list of all know dialect names.\nnames = csv.list_dialects()"
    ),
    _(
        'csv.re() \nSupport for regular expressions (RE).\n\nThis module provides regular expression matching operations similar to\nthose found in Perl.  It supports both 8-bit and Unicode strings; both\nthe pattern and the strings being processed can contain null bytes and\ncharacters outside the US ASCII range.\n\nRegular expressions can contain both special and ordinary characters.\nMost ordinary characters, like "A", "a", or "0", are the simplest\nregular expressions; they simply match themselves.  You can\nconcatenate ordinary characters, so last matches the string \'last\'.\n\nThe special characters are:\n    "."      Matches any character except a newline.\n    "^"      Matches the start of the string.\n    "$"      Matches the end of the string or just before the newline at\n             the end of the string.\n    "*"      Matches 0 or more (greedy) repetitions of the preceding RE.\n             Greedy means that it will match as many repetitions as possible.\n    "+"      Matches 1 or more (greedy) repetitions of the preceding RE.\n    "?"      Matches 0 or 1 (greedy) of the preceding RE.\n    *?,+?,?? Non-greedy versions of the previous three special characters.\n    {m,n}    Matches from m to n repetitions of the preceding RE.\n    {m,n}?   Non-greedy version of the above.\n    "\\\\"     Either escapes special characters or signals a special sequence.\n    []       Indicates a set of characters.\n             A "^" as the first character indicates a complementing set.\n    "|"      A|B, creates an RE that will match either A or B.\n    (...)    Matches the RE inside the parentheses.\n             The contents can be retrieved or matched later in the string.\n    (?aiLmsux) Set the A, I, L, M, S, U, or X flag for the RE (see below).\n    (?:...)  Non-grouping version of regular parentheses.\n    (?P<name>...) The substring matched by the group is accessible by name.\n    (?P=name)     Matches the text matched earlier by the group named name.\n    (?#...)  A comment; ignored.\n    (?=...)  Matches if ... matches next, but doesn\'t consume the string.\n    (?!...)  Matches if ... doesn\'t match next.\n    (?<=...) Matches if preceded by ... (must be fixed length).\n    (?<!...) Matches if not preceded by ... (must be fixed length).\n    (?(id/name)yes|no) Matches yes pattern if the group with id/name matched,\n                       the (optional) no pattern otherwise.\n\nThe special sequences consist of "\\\\" and a character from the list\nbelow.  If the ordinary character is not on the list, then the\nresulting RE will match the second character.\n    \\number  Matches the contents of the group of the same number.\n    \\A       Matches only at the start of the string.\n    \\Z       Matches only at the end of the string.\n    \\b       Matches the empty string, but only at the start or end of a word.\n    \\B       Matches the empty string, but not at the start or end of a word.\n    \\d       Matches any decimal digit; equivalent to the set [0-9] in\n             bytes patterns or string patterns with the ASCII flag.\n             In string patterns without the ASCII flag, it will match the whole\n             range of Unicode digits.\n    \\D       Matches any non-digit character; equivalent to [^\\d].\n    \\s       Matches any whitespace character; equivalent to [ \\t\\n\\r\\f\\v] in\n             bytes patterns or string patterns with the ASCII flag.\n             In string patterns without the ASCII flag, it will match the whole\n             range of Unicode whitespace characters.\n    \\S       Matches any non-whitespace character; equivalent to [^\\s].\n    \\w       Matches any alphanumeric character; equivalent to [a-zA-Z0-9_]\n             in bytes patterns or string patterns with the ASCII flag.\n             In string patterns without the ASCII flag, it will match the\n             range of Unicode alphanumeric characters (letters plus digits\n             plus underscore).\n             With LOCALE, it will match the set [0-9_] plus characters defined\n             as letters for the current locale.\n    \\W       Matches the complement of \\w.\n    \\\\       Matches a literal backslash.\n\nThis module exports the following functions:\n    match     Match a regular expression pattern to the beginning of a string.\n    fullmatch Match a regular expression pattern to all of a string.\n    search    Search a string for the presence of a pattern.\n    sub       Substitute occurrences of a pattern found in a string.\n    subn      Same as sub, but also return the number of substitutions made.\n    split     Split a string by the occurrences of a pattern.\n    findall   Find all occurrences of a pattern in a string.\n    finditer  Return an iterator yielding a match object for each match.\n    compile   Compile a pattern into a RegexObject.\n    purge     Clear the regular expression cache.\n    escape    Backslash all non-alphanumerics in a string.\n\nSome of the functions in this module takes flags as optional parameters:\n    A  ASCII       For string patterns, make \\w, \\W, \\b, \\B, \\d, \\D\n                   match the corresponding ASCII character categories\n                   (rather than the whole Unicode categories, which is the\n                   default).\n                   For bytes patterns, this flag is the only available\n                   behaviour and needn\'t be specified.\n    I  IGNORECASE  Perform case-insensitive matching.\n    L  LOCALE      Make \\w, \\W, \\b, \\B, dependent on the current locale.\n    M  MULTILINE   "^" matches the beginning of lines (after a newline)\n                   as well as the string.\n                   "$" matches the end of lines (before a newline) as well\n                   as the end of the string.\n    S  DOTALL      "." matches any character at all, including the newline.\n    X  VERBOSE     Ignore whitespace and comments for nicer looking RE\'s.\n    U  UNICODE     For compatibility only. Ignored for string patterns (it\n                   is the default), and forbidden for bytes patterns.\n\nThis module also defines an exception \'error\'.'
    ),
    _(
        'csv.reader() \ncsv_reader = reader(iterable [, dialect=\'excel\']\n                        [optional keyword args])\n    for row in csv_reader:\n        process(row)\n\nThe "iterable" argument can be any object that returns a line\nof input for each iteration, such as a file object or a list.  The\noptional "dialect" parameter is discussed below.  The function\nalso accepts optional keyword arguments which override settings\nprovided by the dialect.\n\nThe returned object is an iterator.  Each iteration returns a row\nof the CSV file (which can span multiple input lines).'
    ),
    _(
        "csv.register_dialect() \nCreate a mapping from a string name to a dialect class.\ndialect = csv.register_dialect(name[, dialect[, **fmtparams]])"
    ),
    _(
        "csv.unix_dialect() \nDescribe the usual properties of Unix-generated CSV files."
    ),
    _(
        "csv.unregister_dialect() \nDelete the name/dialect mapping associated with a string name.\ncsv.unregister_dialect(name)"
    ),
    _(
        "csv.writer() \ncsv_writer = csv.writer(fileobj [, dialect='excel']\n                            [optional keyword args])\n    for row in sequence:\n        csv_writer.writerow(row)\n\n    [or]\n\n    csv_writer = csv.writer(fileobj [, dialect='excel']\n                            [optional keyword args])\n    csv_writer.writerows(rows)\n\nThe \"fileobj\" argument can be any object that supports the file API."
    ),
    _("datetime.date() \ndate(year, month, day) --> date object"),
    _("datetime.date() \ndate(year, month, day) --> date object"),
    _(
        "datetime.datetime() \ndatetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])\n\nThe year, month and day arguments are required. tzinfo may be None, or an\ninstance of a tzinfo subclass. The remaining arguments may be ints."
    ),
    _(
        "datetime.datetime() \ndatetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])\n\nThe year, month and day arguments are required. tzinfo may be None, or an\ninstance of a tzinfo subclass. The remaining arguments may be ints."
    ),
    _(
        "datetime.time() \ntime([hour[, minute[, second[, microsecond[, tzinfo]]]]]) --> a time object\n\nAll arguments are optional. tzinfo may be None, or an instance of\na tzinfo subclass. The remaining arguments may be ints."
    ),
    _(
        "datetime.time() \ntime([hour[, minute[, second[, microsecond[, tzinfo]]]]]) --> a time object\n\nAll arguments are optional. tzinfo may be None, or an instance of\na tzinfo subclass. The remaining arguments may be ints."
    ),
    _("datetime.timedelta() \nDifference between two datetime values."),
    _("datetime.timedelta() \nDifference between two datetime values."),
    _("datetime.timezone() \nFixed offset from UTC implementation of tzinfo."),
    _("datetime.timezone() \nFixed offset from UTC implementation of tzinfo."),
    _("datetime.tzinfo() \nAbstract base class for time zone info objects."),
    _("datetime.tzinfo() \nAbstract base class for time zone info objects."),
    _(
        "functools.WeakKeyDictionary(dict=None) \nMapping class that references keys weakly.\n\nEntries in the dictionary will be discarded when there is no\nlonger a strong reference to the key. This can be used to\nassociate additional data with an object owned by other parts of\nan application without adding attributes to those objects. This\ncan be especially useful with objects that override attribute\naccesses."
    ),
    _(
        "functools.cmp_to_key() \nConvert a cmp= function into a key= function."
    ),
    _(
        "functools.get_cache_token() \nReturns the current ABC cache token.\n\nThe token is an opaque object (supporting equality testing) identifying the\ncurrent version of the ABC cache for virtual subclasses. The token changes\nwith every call to ``register()`` on any ABC."
    ),
    _(
        "functools.lru_cache(maxsize=128, typed=False) \nLeast-recently-used cache decorator.\n\nIf *maxsize* is set to None, the LRU features are disabled and the cache\ncan grow without bound.\n\nIf *typed* is True, arguments of different types will be cached separately.\nFor example, f(3.0) and f(3) will be treated as distinct calls with\ndistinct results.\n\nArguments to the cached function must be hashable.\n\nView the cache statistics named tuple (hits, misses, maxsize, currsize)\nwith f.cache_info().  Clear the cache and statistics with f.cache_clear().\nAccess the underlying function with f.__wrapped__.\n\nSee:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used"
    ),
    _(
        "functools.namedtuple(typename, field_names, *, verbose=False, rename=False, module=None) \nReturns a new subclass of tuple with named fields.\n\n>>> Point = namedtuple('Point', ['x', 'y'])\n>>> Point.__doc__                   # docstring for the new class\n'Point(x, y)'\n>>> p = Point(11, y=22)             # instantiate with positional args or keywords\n>>> p[0] + p[1]                     # indexable like a plain tuple\n33\n>>> x, y = p                        # unpack like a regular tuple\n>>> x, y\n(11, 22)\n>>> p.x + p.y                       # fields also accessible by name\n33\n>>> d = p._asdict()                 # convert to a dictionary\n>>> d['x']\n11\n>>> Point(**d)                      # convert from a dictionary\nPoint(x=11, y=22)\n>>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields\nPoint(x=100, y=22)"
    ),
    _(
        "functools.partial() \npartial(func, *args, **keywords) - new function with partial application\nof the given arguments and keywords."
    ),
    _(
        "functools.partialmethod(func, *args, **keywords) \nMethod descriptor with partial application of the given arguments\nand keywords.\n\nSupports wrapping existing descriptors and handles non-descriptor\ncallables as instance methods."
    ),
    _(
        "functools.recursive_repr(fillvalue='...') \nDecorator to make a repr function return fillvalue for a recursive call"
    ),
    _(
        "functools.reduce() \nreduce(function, sequence[, initial]) -> value\n\nApply a function of two arguments cumulatively to the items of a sequence,\nfrom left to right, so as to reduce the sequence to a single value.\nFor example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates\n((((1+2)+3)+4)+5).  If initial is present, it is placed before the items\nof the sequence in the calculation, and serves as a default when the\nsequence is empty."
    ),
    _(
        "functools.singledispatch(func) \nSingle-dispatch generic function decorator.\n\nTransforms a function into a generic function, which can have different\nbehaviours depending upon the type of its first argument. The decorated\nfunction acts as the default implementation, and additional\nimplementations can be registered using the register() attribute of the\ngeneric function."
    ),
    _(
        "functools.total_ordering(cls) \nClass decorator that fills in missing ordering methods"
    ),
    _(
        "functools.update_wrapper(wrapper, wrapped, assigned='__module__', '__name__', '__qualname__', '__doc__', '__annotations__', updated='__dict__',) \nUpdate a wrapper function to look like the wrapped function\n\nwrapper is the function to be updated\nwrapped is the original function\nassigned is a tuple naming the attributes assigned directly\nfrom the wrapped function to the wrapper function (defaults to\nfunctools.WRAPPER_ASSIGNMENTS)\nupdated is a tuple naming the attributes of the wrapper that\nare updated with the corresponding attribute from the wrapped\nfunction (defaults to functools.WRAPPER_UPDATES)"
    ),
    _(
        "functools.wraps(wrapped, assigned='__module__', '__name__', '__qualname__', '__doc__', '__annotations__', updated='__dict__',) \nDecorator factory to apply update_wrapper() to a wrapper function\n\nReturns a decorator that invokes update_wrapper() with the decorated\nfunction as the wrapper argument and the arguments to wraps() as the\nremaining arguments. Default arguments are as for update_wrapper().\nThis is a convenience function to simplify applying partial() to\nupdate_wrapper()."
    ),
    _(
        "hashlib.__hash_new(name, data=b'', **kwargs) \nnew(name, data=b'') - Return a new hashing object using the named algorithm;\noptionally initialized with data (which must be bytes)."
    ),
    _("hashlib.blake2b() \nReturn a new BLAKE2b hash object."),
    _("hashlib.blake2s() \nReturn a new BLAKE2s hash object."),
    _(
        "hashlib.openssl_md5() \nReturns a md5 hash object; optionally initialized with a string"
    ),
    _(
        "hashlib.openssl_sha1() \nReturns a sha1 hash object; optionally initialized with a string"
    ),
    _(
        "hashlib.openssl_sha224() \nReturns a sha224 hash object; optionally initialized with a string"
    ),
    _(
        "hashlib.openssl_sha256() \nReturns a sha256 hash object; optionally initialized with a string"
    ),
    _(
        "hashlib.openssl_sha384() \nReturns a sha384 hash object; optionally initialized with a string"
    ),
    _(
        "hashlib.openssl_sha512() \nReturns a sha512 hash object; optionally initialized with a string"
    ),
    _(
        "hashlib.pbkdf2_hmac() \npbkdf2_hmac(hash_name, password, salt, iterations, dklen=None) -> key\n\nPassword based key derivation function 2 (PKCS #5 v2.0) with HMAC as\npseudorandom function."
    ),
    _(
        "hashlib.sha3_224(string=None) \nReturn a new SHA3 hash object with a hashbit length of 28 bytes."
    ),
    _(
        "hashlib.sha3_256() \nsha3_256([string]) -> SHA3 object\n\nReturn a new SHA3 hash object with a hashbit length of 32 bytes."
    ),
    _(
        "hashlib.sha3_384() \nsha3_384([string]) -> SHA3 object\n\nReturn a new SHA3 hash object with a hashbit length of 48 bytes."
    ),
    _(
        "hashlib.sha3_512() \nsha3_512([string]) -> SHA3 object\n\nReturn a new SHA3 hash object with a hashbit length of 64 bytes."
    ),
    _(
        "hashlib.shake_128() \nshake_128([string]) -> SHAKE object\n\nReturn a new SHAKE hash object."
    ),
    _(
        "hashlib.shake_256() \nshake_256([string]) -> SHAKE object\n\nReturn a new SHAKE hash object."
    ),
    _(
        "itertools.accumulate() \naccumulate(iterable[, func]) --> accumulate object\n\nReturn series of accumulated sums (or other binary function results)."
    ),
    _(
        "itertools.chain() \nchain(*iterables) --> chain object\n\nReturn a chain object whose .__next__() method returns elements from the\nfirst iterable until it is exhausted, then elements from the next\niterable, until all of the iterables are exhausted."
    ),
    _(
        "itertools.combinations() \ncombinations(iterable, r) --> combinations object\n\nReturn successive r-length combinations of elements in the iterable.\n\ncombinations(range(4), 3) --> (0,1,2), (0,1,3), (0,2,3), (1,2,3)"
    ),
    _(
        "itertools.combinations_with_replacement() \ncombinations_with_replacement(iterable, r) --> combinations_with_replacement object\n\nReturn successive r-length combinations of elements in the iterable\nallowing individual elements to have successive repeats.\ncombinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC"
    ),
    _(
        "itertools.compress() \ncompress(data, selectors) --> iterator over selected data\n\nReturn data elements corresponding to true selector elements.\nForms a shorter iterator from selected data elements using the\nselectors to choose the data elements."
    ),
    _(
        "itertools.count() \ncount(start=0, step=1) --> count object\n\nReturn a count object whose .__next__() method returns consecutive values.\nEquivalent to:\n\n    def count(firstval=0, step=1):\n        x = firstval\n        while 1:\n            yield x\n            x += step"
    ),
    _(
        "itertools.cycle() \ncycle(iterable) --> cycle object\n\nReturn elements from the iterable until it is exhausted.\nThen repeat the sequence indefinitely."
    ),
    _(
        "itertools.dropwhile() \ndropwhile(predicate, iterable) --> dropwhile object\n\nDrop items from the iterable while predicate(item) is true.\nAfterwards, return every element until the iterable is exhausted."
    ),
    _(
        "itertools.filterfalse() \nfilterfalse(function or None, sequence) --> filterfalse object\n\nReturn those items of sequence for which function(item) is false.\nIf function is None, return the items that are false."
    ),
    _(
        "itertools.groupby() \ngroupby(iterable[, keyfunc]) -> create an iterator which returns\n(key, sub-iterator) grouped by each value of key(value)."
    ),
    _(
        "itertools.islice() \nislice(iterable, stop) --> islice object\nislice(iterable, start, stop[, step]) --> islice object\n\nReturn an iterator whose next() method returns selected values from an\niterable.  If start is specified, will skip all preceding elements;\notherwise, start defaults to zero.  Step defaults to one.  If\nspecified as another value, step determines how many values are \nskipped between successive calls.  Works like a slice() on a list\nbut returns an iterator."
    ),
    _(
        "itertools.permutations() \npermutations(iterable[, r]) --> permutations object\n\nReturn successive r-length permutations of elements in the iterable.\n\npermutations(range(3), 2) --> (0,1), (0,2), (1,0), (1,2), (2,0), (2,1)"
    ),
    _(
        "itertools.product() \nproduct(*iterables, repeat=1) --> product object\n\nCartesian product of input iterables.  Equivalent to nested for-loops.\n\nFor example, product(A, B) returns the same as:  ((x,y) for x in A for y in B).\nThe leftmost iterators are in the outermost for-loop, so the output tuples\ncycle in a manner similar to an odometer (with the rightmost element changing\non every iteration).\n\nTo compute the product of an iterable with itself, specify the number\nof repetitions with the optional repeat keyword argument. For example,\nproduct(A, repeat=4) means the same as product(A, A, A, A).\n\nproduct('ab', range(3)) --> ('a',0) ('a',1) ('a',2) ('b',0) ('b',1) ('b',2)\nproduct((0,1), (0,1), (0,1)) --> (0,0,0) (0,0,1) (0,1,0) (0,1,1) (1,0,0) ..."
    ),
    _(
        "itertools.repeat() \nrepeat(object [,times]) -> create an iterator which returns the object\nfor the specified number of times.  If not specified, returns the object\nendlessly."
    ),
    _(
        "itertools.starmap() \nstarmap(function, sequence) --> starmap object\n\nReturn an iterator whose values are returned from the function evaluated\nwith an argument tuple taken from the given sequence."
    ),
    _(
        "itertools.takewhile() \ntakewhile(predicate, iterable) --> takewhile object\n\nReturn successive entries from an iterable as long as the \npredicate evaluates to true for each entry."
    ),
    _(
        "itertools.tee() \ntee(iterable, n=2) --> tuple of n independent iterators."
    ),
    _(
        "itertools.zip_longest() \nzip_longest(iter1 [,iter2 [...]], [fillvalue=None]) --> zip_longest object\n\nReturn a zip_longest object whose .__next__() method returns a tuple where\nthe i-th element comes from the i-th iterable argument.  The .__next__()\nmethod continues until the longest iterable in the argument sequence\nis exhausted and then it raises StopIteration.  When the shorter iterables\nare exhausted, the fillvalue is substituted in their place.  The fillvalue\ndefaults to None or can be specified by a keyword argument."
    ),
    _(
        "json.JSONDecodeError(msg, doc, pos) \nSubclass of ValueError with the following additional properties:\n\nmsg: The unformatted error message\ndoc: The JSON document being parsed\npos: The start index of doc where parsing failed\nlineno: The line corresponding to pos\ncolno: The column corresponding to pos"
    ),
    _(
        "json.JSONDecoder(*, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None) \nSimple JSON <http://json.org> decoder\n\nPerforms the following translations in decoding by default:\n\n+---------------+-------------------+\n| JSON          | Python            |\n+===============+===================+\n| object        | dict              |\n+---------------+-------------------+\n| array         | list              |\n+---------------+-------------------+\n| string        | str               |\n+---------------+-------------------+\n| number (int)  | int               |\n+---------------+-------------------+\n| number (real) | float             |\n+---------------+-------------------+\n| true          | True              |\n+---------------+-------------------+\n| false         | False             |\n+---------------+-------------------+\n| null          | None              |\n+---------------+-------------------+\n\nIt also understands ``NaN``, ``Infinity``, and ``-Infinity`` as\ntheir corresponding ``float`` values, which is outside the JSON spec."
    ),
    _(
        "json.JSONEncoder(*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None) \nExtensible JSON <http://json.org> encoder for Python data structures.\n\nSupports the following objects and types by default:\n\n+-------------------+---------------+\n| Python            | JSON          |\n+===================+===============+\n| dict              | object        |\n+-------------------+---------------+\n| list, tuple       | array         |\n+-------------------+---------------+\n| str               | string        |\n+-------------------+---------------+\n| int, float        | number        |\n+-------------------+---------------+\n| True              | true          |\n+-------------------+---------------+\n| False             | false         |\n+-------------------+---------------+\n| None              | null          |\n+-------------------+---------------+\n\nTo extend this to recognize other objects, subclass and implement a\n``.default()`` method with another method that returns a serializable\nobject for ``o`` if possible, otherwise it should call the superclass\nimplementation (to raise ``TypeError``)."
    ),
    _(
        "json.codecs() \ncodecs -- Python Codec Registry, API and helpers.\n\n\nWritten by Marc-Andre Lemburg (mal@lemburg.com).\n\n(c) Copyright CNRI, All Rights Reserved. NO WARRANTY."
    ),
    _(
        "json.dump(obj, fp, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw) \nSerialize ``obj`` as a JSON formatted stream to ``fp`` (a\n``.write()``-supporting file-like object).\n\nIf ``skipkeys`` is true then ``dict`` keys that are not basic types\n(``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped\ninstead of raising a ``TypeError``.\n\nIf ``ensure_ascii`` is false, then the strings written to ``fp`` can\ncontain non-ASCII characters if they appear in strings contained in\n``obj``. Otherwise, all such characters are escaped in JSON strings.\n\nIf ``check_circular`` is false, then the circular reference check\nfor container types will be skipped and a circular reference will\nresult in an ``OverflowError`` (or worse).\n\nIf ``allow_nan`` is false, then it will be a ``ValueError`` to\nserialize out of range ``float`` values (``nan``, ``inf``, ``-inf``)\nin strict compliance of the JSON specification, instead of using the\nJavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).\n\nIf ``indent`` is a non-negative integer, then JSON array elements and\nobject members will be pretty-printed with that indent level. An indent\nlevel of 0 will only insert newlines. ``None`` is the most compact\nrepresentation.\n\nIf specified, ``separators`` should be an ``(item_separator, key_separator)``\ntuple.  The default is ``(', ', ': ')`` if *indent* is ``None`` and\n``(',', ': ')`` otherwise.  To get the most compact JSON representation,\nyou should specify ``(',', ':')`` to eliminate whitespace.\n\n``default(obj)`` is a function that should return a serializable version\nof obj or raise TypeError. The default simply raises TypeError.\n\nIf *sort_keys* is true (default: ``False``), then the output of\ndictionaries will be sorted by key.\n\nTo use a custom ``JSONEncoder`` subclass (e.g. one that overrides the\n``.default()`` method to serialize additional types), specify it with\nthe ``cls`` kwarg; otherwise ``JSONEncoder`` is used."
    ),
    _(
        "json.dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw) \nSerialize ``obj`` to a JSON formatted ``str``.\n\nIf ``skipkeys`` is true then ``dict`` keys that are not basic types\n(``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped\ninstead of raising a ``TypeError``.\n\nIf ``ensure_ascii`` is false, then the return value can contain non-ASCII\ncharacters if they appear in strings contained in ``obj``. Otherwise, all\nsuch characters are escaped in JSON strings.\n\nIf ``check_circular`` is false, then the circular reference check\nfor container types will be skipped and a circular reference will\nresult in an ``OverflowError`` (or worse).\n\nIf ``allow_nan`` is false, then it will be a ``ValueError`` to\nserialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in\nstrict compliance of the JSON specification, instead of using the\nJavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).\n\nIf ``indent`` is a non-negative integer, then JSON array elements and\nobject members will be pretty-printed with that indent level. An indent\nlevel of 0 will only insert newlines. ``None`` is the most compact\nrepresentation.\n\nIf specified, ``separators`` should be an ``(item_separator, key_separator)``\ntuple.  The default is ``(', ', ': ')`` if *indent* is ``None`` and\n``(',', ': ')`` otherwise.  To get the most compact JSON representation,\nyou should specify ``(',', ':')`` to eliminate whitespace.\n\n``default(obj)`` is a function that should return a serializable version\nof obj or raise TypeError. The default simply raises TypeError.\n\nIf *sort_keys* is true (default: ``False``), then the output of\ndictionaries will be sorted by key.\n\nTo use a custom ``JSONEncoder`` subclass (e.g. one that overrides the\n``.default()`` method to serialize additional types), specify it with\nthe ``cls`` kwarg; otherwise ``JSONEncoder`` is used."
    ),
    _("json.json.decoder() \nImplementation of JSONDecoder"),
    _("json.json.encoder() \nImplementation of JSONEncoder"),
    _("json.json.scanner() \nJSON token scanner"),
    _(
        "json.load(fp, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw) \nDeserialize ``fp`` (a ``.read()``-supporting file-like object containing\na JSON document) to a Python object.\n\n``object_hook`` is an optional function that will be called with the\nresult of any object literal decode (a ``dict``). The return value of\n``object_hook`` will be used instead of the ``dict``. This feature\ncan be used to implement custom decoders (e.g. JSON-RPC class hinting).\n\n``object_pairs_hook`` is an optional function that will be called with the\nresult of any object literal decoded with an ordered list of pairs.  The\nreturn value of ``object_pairs_hook`` will be used instead of the ``dict``.\nThis feature can be used to implement custom decoders that rely on the\norder that the key and value pairs are decoded (for example,\ncollections.OrderedDict will remember the order of insertion). If\n``object_hook`` is also defined, the ``object_pairs_hook`` takes priority.\n\nTo use a custom ``JSONDecoder`` subclass, specify it with the ``cls``\nkwarg; otherwise ``JSONDecoder`` is used."
    ),
    _(
        "json.loads(s, *, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw) \nDeserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance\ncontaining a JSON document) to a Python object.\n\n``object_hook`` is an optional function that will be called with the\nresult of any object literal decode (a ``dict``). The return value of\n``object_hook`` will be used instead of the ``dict``. This feature\ncan be used to implement custom decoders (e.g. JSON-RPC class hinting).\n\n``object_pairs_hook`` is an optional function that will be called with the\nresult of any object literal decoded with an ordered list of pairs.  The\nreturn value of ``object_pairs_hook`` will be used instead of the ``dict``.\nThis feature can be used to implement custom decoders that rely on the\norder that the key and value pairs are decoded (for example,\ncollections.OrderedDict will remember the order of insertion). If\n``object_hook`` is also defined, the ``object_pairs_hook`` takes priority.\n\n``parse_float``, if specified, will be called with the string\nof every JSON float to be decoded. By default this is equivalent to\nfloat(num_str). This can be used to use another datatype or parser\nfor JSON floats (e.g. decimal.Decimal).\n\n``parse_int``, if specified, will be called with the string\nof every JSON int to be decoded. By default this is equivalent to\nint(num_str). This can be used to use another datatype or parser\nfor JSON integers (e.g. float).\n\n``parse_constant``, if specified, will be called with one of the\nfollowing strings: -Infinity, Infinity, NaN.\nThis can be used to raise an exception if invalid JSON numbers\nare encountered.\n\nTo use a custom ``JSONDecoder`` subclass, specify it with the ``cls``\nkwarg; otherwise ``JSONDecoder`` is used.\n\nThe ``encoding`` argument is ignored and deprecated."
    ),
    _("os.OSError() \nBase class for I/O related errors."),
    _(
        "os.PathLike() \nAbstract base class for implementing the file system path protocol."
    ),
    _(
        "os.WCOREDUMP(status, /) \nReturn True if the process returning status was dumped to a core file."
    ),
    _("os.WEXITSTATUS(status) \nReturn the process return code from status."),
    _(
        "os.WIFCONTINUED(status) \nReturn True if a particular process was continued from a job control stop.\n\nReturn True if the process returning status was continued from a\njob control stop."
    ),
    _(
        "os.WIFEXITED(status) \nReturn True if the process returning status exited via the exit() system call."
    ),
    _(
        "os.WIFSIGNALED(status) \nReturn True if the process returning status was terminated by a signal."
    ),
    _(
        "os.WIFSTOPPED(status) \nReturn True if the process returning status was stopped."
    ),
    _(
        "os.WSTOPSIG(status) \nReturn the signal that stopped the process that provided the status value."
    ),
    _(
        "os.WTERMSIG(status) \nReturn the signal that terminated the process that provided the status value."
    ),
    _("os.abc() \nAbstract Base Classes (ABCs) according to PEP 3119."),
    _(
        "os.abort() \nAbort the interpreter immediately.\n\nThis function 'dumps core' or otherwise fails in the hardest way possible\non the hosting operating system.  This function never returns."
    ),
    _(
        "os.access(path, mode, *, dir_fd=None, effective_ids=False, follow_symlinks=True) \nUse the real uid/gid to test for access to a path.\n\n  path\n    Path to be tested; can be string or bytes\n  mode\n    Operating-system mode bitfield.  Can be F_OK to test existence,\n    or the inclusive-OR of R_OK, W_OK, and X_OK.\n  dir_fd\n    If not None, it should be a file descriptor open to a directory,\n    and path should be relative; path will then be relative to that\n    directory.\n  effective_ids\n    If True, access will use the effective uid/gid instead of\n    the real uid/gid.\n  follow_symlinks\n    If False, and the last element of the path is a symbolic link,\n    access will examine the symbolic link itself instead of the file\n    the link points to.\n\ndir_fd, effective_ids, and follow_symlinks may not be implemented\n  on your platform.  If they are unavailable, using them will raise a\n  NotImplementedError.\n\nNote that most operations will use the effective uid/gid, therefore this\n  routine can be used in a suid/sgid environment to test if the invoking user\n  has the specified access to the path."
    ),
    _(
        "os.chdir(path) \nChange the current working directory to the specified path.\n\npath may always be specified as a string.\nOn some platforms, path may also be specified as an open file descriptor.\n  If this functionality is unavailable, using it raises an exception."
    ),
    _(
        "os.chmod(path, mode, *, dir_fd=None, follow_symlinks=True) \nChange the access permissions of a file.\n\n  path\n    Path to be modified.  May always be specified as a str or bytes.\n    On some platforms, path may also be specified as an open file descriptor.\n    If this functionality is unavailable, using it raises an exception.\n  mode\n    Operating-system mode bitfield.\n  dir_fd\n    If not None, it should be a file descriptor open to a directory,\n    and path should be relative; path will then be relative to that\n    directory.\n  follow_symlinks\n    If False, and the last element of the path is a symbolic link,\n    chmod will modify the symbolic link itself instead of the file\n    the link points to.\n\nIt is an error to use dir_fd or follow_symlinks when specifying path as\n  an open file descriptor.\ndir_fd and follow_symlinks may not be implemented on your platform.\n  If they are unavailable, using them will raise a NotImplementedError."
    ),
    _(
        "os.chown(path, uid, gid, *, dir_fd=None, follow_symlinks=True) \nChange the owner and group id of path to the numeric uid and gid.\\\n\n  path\n    Path to be examined; can be string, bytes, or open-file-descriptor int.\n  dir_fd\n    If not None, it should be a file descriptor open to a directory,\n    and path should be relative; path will then be relative to that\n    directory.\n  follow_symlinks\n    If False, and the last element of the path is a symbolic link,\n    stat will examine the symbolic link itself instead of the file\n    the link points to.\n\npath may always be specified as a string.\nOn some platforms, path may also be specified as an open file descriptor.\n  If this functionality is unavailable, using it raises an exception.\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\nIf follow_symlinks is False, and the last element of the path is a symbolic\n  link, chown will modify the symbolic link itself instead of the file the\n  link points to.\nIt is an error to use dir_fd or follow_symlinks when specifying path as\n  an open file descriptor.\ndir_fd and follow_symlinks may not be implemented on your platform.\n  If they are unavailable, using them will raise a NotImplementedError."
    ),
    _("os.chroot(path) \nChange root directory to path."),
    _("os.close(fd) \nClose a file descriptor."),
    _(
        "os.closerange(fd_low, fd_high, /) \nCloses all file descriptors in [fd_low, fd_high), ignoring errors."
    ),
    _(
        "os.confstr(name, /) \nReturn a string-valued system configuration variable."
    ),
    _(
        "os.cpu_count() \nReturn the number of CPUs in the system; return None if indeterminable.\n\nThis number is not equivalent to the number of CPUs the current process can\nuse.  The number of usable CPUs can be obtained with\n``len(os.sched_getaffinity(0))``"
    ),
    _(
        "os.ctermid() \nReturn the name of the controlling terminal for this process."
    ),
    _(
        "os.device_encoding(fd) \nReturn a string describing the encoding of a terminal's file descriptor.\n\nThe file descriptor must be attached to a terminal.\nIf the device is not a terminal, return None."
    ),
    _("os.dup(fd, /) \nReturn a duplicate of a file descriptor."),
    _("os.dup2(fd, fd2, inheritable=True) \nDuplicate file descriptor."),
    _(
        "os.errno() \nThis module makes available standard errno system symbols.\n\nThe value of each symbol is the corresponding integer value,\ne.g., on most systems, errno.ENOENT equals the integer 2.\n\nThe dictionary errno.errorcode maps numeric codes to symbol names,\ne.g., errno.errorcode[2] could be the string 'ENOENT'.\n\nSymbols that are not relevant to the underlying system are not defined.\n\nTo map error codes to error messages, use the function os.strerror(),\ne.g. os.strerror(2) could return 'No such file or directory'."
    ),
    _(
        "os.execl(file, *args) \nexecl(file, *args)\n\nExecute the executable file with argument list args, replacing the\ncurrent process. "
    ),
    _(
        "os.execle(file, *args) \nexecle(file, *args, env)\n\nExecute the executable file with argument list args and\nenvironment env, replacing the current process. "
    ),
    _(
        "os.execlp(file, *args) \nexeclp(file, *args)\n\nExecute the executable file (which is searched for along $PATH)\nwith argument list args, replacing the current process. "
    ),
    _(
        "os.execlpe(file, *args) \nexeclpe(file, *args, env)\n\nExecute the executable file (which is searched for along $PATH)\nwith argument list args and environment env, replacing the current\nprocess. "
    ),
    _(
        "os.execv(path, argv, /) \nExecute an executable path with arguments, replacing current process.\n\npath\n  Path of executable file.\nargv\n  Tuple or list of strings."
    ),
    _(
        "os.execve(path, argv, env) \nExecute an executable path with arguments, replacing current process.\n\npath\n  Path of executable file.\nargv\n  Tuple or list of strings.\nenv\n  Dictionary of strings mapping to strings."
    ),
    _(
        "os.execvp(file, args) \nexecvp(file, args)\n\nExecute the executable file (which is searched for along $PATH)\nwith argument list args, replacing the current process.\nargs may be a list or tuple of strings. "
    ),
    _(
        "os.execvpe(file, args, env) \nexecvpe(file, args, env)\n\nExecute the executable file (which is searched for along $PATH)\nwith argument list args and environment env , replacing the\ncurrent process.\nargs may be a list or tuple of strings. "
    ),
    _(
        "os.fchdir(fd) \nChange to the directory of the given file descriptor.\n\nfd must be opened on a directory, not a file.\nEquivalent to os.chdir(fd)."
    ),
    _(
        "os.fchmod(fd, mode) \nChange the access permissions of the file given by file descriptor fd.\n\nEquivalent to os.chmod(fd, mode)."
    ),
    _(
        "os.fchown(fd, uid, gid) \nChange the owner and group id of the file specified by file descriptor.\n\nEquivalent to os.chown(fd, uid, gid)."
    ),
    _(
        "os.fdatasync(fd) \nForce write of fd to disk without forcing update of metadata."
    ),
    _(
        "os.fork() \nFork a child process.\n\nReturn 0 to child process and PID of child to parent process."
    ),
    _(
        "os.forkpty() \nFork a new process with a new pseudo-terminal as controlling tty.\n\nReturns a tuple of (pid, master_fd).\nLike fork(), return pid of 0 to the child process,\nand pid of child to the parent process.\nTo both, return fd of newly opened pseudo-terminal."
    ),
    _(
        "os.fpathconf(fd, name, /) \nReturn the configuration limit name for the file descriptor fd.\n\nIf there is no limit, return -1."
    ),
    _(
        "os.fsdecode(filename) \nDecode filename (an os.PathLike, bytes, or str) from the filesystem\nencoding with 'surrogateescape' error handler, return str unchanged. On\nWindows, use 'strict' error handler if the file system encoding is\n'mbcs' (which is the default encoding)."
    ),
    _(
        "os.fsencode(filename) \nEncode filename (an os.PathLike, bytes, or str) to the filesystem\nencoding with 'surrogateescape' error handler, return bytes unchanged.\nOn Windows, use 'strict' error handler if the file system encoding is\n'mbcs' (which is the default encoding)."
    ),
    _(
        "os.fspath(path) \nReturn the file system path representation of the object.\n\nIf the object is str or bytes, then allow it to pass through as-is. If the\nobject defines __fspath__(), then return the result of that method. All other\ntypes raise a TypeError."
    ),
    _(
        "os.fstat(fd) \nPerform a stat system call on the given file descriptor.\n\nLike stat(), but for an open file descriptor.\nEquivalent to os.stat(fd)."
    ),
    _(
        "os.fstatvfs(fd, /) \nPerform an fstatvfs system call on the given fd.\n\nEquivalent to statvfs(fd)."
    ),
    _("os.fsync(fd) \nForce write of fd to disk."),
    _(
        "os.ftruncate(fd, length, /) \nTruncate a file, specified by file descriptor, to a specific length."
    ),
    _(
        "os.fwalk(top='.', topdown=True, onerror=None, *, follow_symlinks=False, dir_fd=None) \nDirectory tree generator.\n\nThis behaves exactly like walk(), except that it yields a 4-tuple\n\n    dirpath, dirnames, filenames, dirfd\n\n`dirpath`, `dirnames` and `filenames` are identical to walk() output,\nand `dirfd` is a file descriptor referring to the directory `dirpath`.\n\nThe advantage of fwalk() over walk() is that it's safe against symlink\nraces (when follow_symlinks is False).\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and top should be relative; top will then be relative to that directory.\n  (dir_fd is always supported for fwalk.)\n\nCaution:\nSince fwalk() yields file descriptors, those are only valid until the\nnext iteration step, so you should dup() them if you want to keep them\nfor a longer period.\n\nExample:\n\nimport os\nfor root, dirs, files, rootfd in os.fwalk('python/Lib/email'):\n    print(root, \"consumes\", end=\"\")\n    print(sum([os.stat(name, dir_fd=rootfd).st_size for name in files]),\n          end=\"\")\n    print(\"bytes in\", len(files), \"non-directory files\")\n    if 'CVS' in dirs:\n        dirs.remove('CVS')  # don't visit CVS directories"
    ),
    _(
        "os.get_blocking() \nget_blocking(fd) -> bool\n\nGet the blocking mode of the file descriptor:\nFalse if the O_NONBLOCK flag is set, True if the flag is cleared."
    ),
    _(
        "os.get_exec_path(env=None) \nReturns the sequence of directories that will be searched for the\nnamed executable (similar to a shell) when launching a process.\n\n*env* must be an environment variable dict or None.  If *env* is None,\nos.environ will be used."
    ),
    _(
        "os.get_inheritable(fd, /) \nGet the close-on-exe flag of the specified file descriptor."
    ),
    _(
        "os.get_terminal_size() \nReturn the size of the terminal window as (columns, lines).\n\nThe optional argument fd (default standard output) specifies\nwhich file descriptor should be queried.\n\nIf the file descriptor is not connected to a terminal, an OSError\nis thrown.\n\nThis function will only be defined if an implementation is\navailable for this system.\n\nshutil.get_terminal_size is the high-level function which should \nnormally be used, os.get_terminal_size is the low-level implementation."
    ),
    _(
        "os.getcwd() \nReturn a unicode string representing the current working directory."
    ),
    _(
        "os.getcwdb() \nReturn a bytes string representing the current working directory."
    ),
    _("os.getegid() \nReturn the current process's effective group id."),
    _(
        "os.getenv(key, default=None) \nGet an environment variable, return None if it doesn't exist.\nThe optional second argument can specify an alternate default.\nkey, default and the result are str."
    ),
    _(
        "os.getenvb(key, default=None) \nGet an environment variable, return None if it doesn't exist.\nThe optional second argument can specify an alternate default.\nkey, default and the result are bytes."
    ),
    _("os.geteuid() \nReturn the current process's effective user id."),
    _("os.getgid() \nReturn the current process's group id."),
    _(
        "os.getgrouplist() \ngetgrouplist(user, group) -> list of groups to which a user belongs\n\nReturns a list of groups to which a user belongs.\n\n    user: username to lookup\n    group: base group id of the user"
    ),
    _(
        "os.getgroups() \nReturn list of supplemental group IDs for the process."
    ),
    _(
        "os.getloadavg() \nReturn average recent system load information.\n\nReturn the number of processes in the system run queue averaged over\nthe last 1, 5, and 15 minutes as a tuple of three floats.\nRaises OSError if the load average was unobtainable."
    ),
    _("os.getlogin() \nReturn the actual login name."),
    _(
        "os.getpgid(pid) \nCall the system call getpgid(), and return the result."
    ),
    _("os.getpgrp() \nReturn the current process group id."),
    _("os.getpid() \nReturn the current process id."),
    _(
        "os.getppid() \nReturn the parent's process id.\n\nIf the parent process has already exited, Windows machines will still\nreturn its id; others systems will return the id of the 'init' process (1)."
    ),
    _("os.getpriority(which, who) \nReturn program scheduling priority."),
    _("os.getrandom(size, flags=0) \nObtain a series of random bytes."),
    _(
        "os.getresgid() \nReturn a tuple of the current process's real, effective, and saved group ids."
    ),
    _(
        "os.getresuid() \nReturn a tuple of the current process's real, effective, and saved user ids."
    ),
    _(
        "os.getsid(pid, /) \nCall the system call getsid(pid) and return the result."
    ),
    _("os.getuid() \nReturn the current process's user id."),
    _(
        "os.getxattr(path, attribute, *, follow_symlinks=True) \nReturn the value of extended attribute attribute on path.\n\npath may be either a string or an open file descriptor.\nIf follow_symlinks is False, and the last element of the path is a symbolic\n  link, getxattr will examine the symbolic link itself instead of the file\n  the link points to."
    ),
    _(
        "os.initgroups() \ninitgroups(username, gid) -> None\n\nCall the system initgroups() to initialize the group access list with all of\nthe groups of which the specified username is a member, plus the specified\ngroup id."
    ),
    _(
        "os.isatty(fd, /) \nReturn True if the fd is connected to a terminal.\n\nReturn True if the file descriptor is an open file descriptor\nconnected to the slave end of a terminal."
    ),
    _("os.kill(pid, signal, /) \nKill a process with a signal."),
    _("os.killpg(pgid, signal, /) \nKill a process group with a signal."),
    _(
        "os.lchown(path, uid, gid) \nChange the owner and group id of path to the numeric uid and gid.\n\nThis function will not follow symbolic links.\nEquivalent to os.chown(path, uid, gid, follow_symlinks=False)."
    ),
    _(
        "os.link(src, dst, *, src_dir_fd=None, dst_dir_fd=None, follow_symlinks=True) \nCreate a hard link to a file.\n\nIf either src_dir_fd or dst_dir_fd is not None, it should be a file\n  descriptor open to a directory, and the respective path string (src or dst)\n  should be relative; the path will then be relative to that directory.\nIf follow_symlinks is False, and the last element of src is a symbolic\n  link, link will create a link to the symbolic link itself instead of the\n  file the link points to.\nsrc_dir_fd, dst_dir_fd, and follow_symlinks may not be implemented on your\n  platform.  If they are unavailable, using them will raise a\n  NotImplementedError."
    ),
    _(
        "os.listdir(path=None) \nReturn a list containing the names of the files in the directory.\n\npath can be specified as either str or bytes.  If path is bytes,\n  the filenames returned will also be bytes; in all other circumstances\n  the filenames returned will be str.\nIf path is None, uses the path='.'.\nOn some platforms, path may also be specified as an open file descriptor;\\\n  the file descriptor must refer to a directory.\n  If this functionality is unavailable, using it raises NotImplementedError.\n\nThe list is in arbitrary order.  It does not include the special\nentries '.' and '..' even if they are present in the directory."
    ),
    _(
        "os.listxattr(path=None, *, follow_symlinks=True) \nReturn a list of extended attributes on path.\n\npath may be either None, a string, or an open file descriptor.\nif path is None, listxattr will examine the current directory.\nIf follow_symlinks is False, and the last element of the path is a symbolic\n  link, listxattr will examine the symbolic link itself instead of the file\n  the link points to."
    ),
    _(
        "os.lockf(fd, command, length, /) \nApply, test or remove a POSIX lock on an open file descriptor.\n\nfd\n  An open file descriptor.\ncommand\n  One of F_LOCK, F_TLOCK, F_ULOCK or F_TEST.\nlength\n  The number of bytes to lock, starting at the current position."
    ),
    _(
        "os.lseek(fd, position, how, /) \nSet the position of a file descriptor.  Return the new position.\n\nReturn the new cursor position in number of bytes\nrelative to the beginning of the file."
    ),
    _(
        "os.lstat(path, *, dir_fd=None) \nPerform a stat system call on the given path, without following symbolic links.\n\nLike stat(), but do not follow symbolic links.\nEquivalent to stat(path, follow_symlinks=False)."
    ),
    _(
        "os.major(device, /) \nExtracts a device major number from a raw device number."
    ),
    _(
        "os.makedev(major, minor, /) \nComposes a raw device number from the major and minor device numbers."
    ),
    _(
        "os.makedirs(name, mode=511, exist_ok=False) \nmakedirs(name [, mode=0o777][, exist_ok=False])\n\nSuper-mkdir; create a leaf directory and all intermediate ones.  Works like\nmkdir, except that any intermediate path segment (not just the rightmost)\nwill be created if it does not exist. If the target directory already\nexists, raise an OSError if exist_ok is False. Otherwise no exception is\nraised.  This is recursive."
    ),
    _(
        "os.minor(device, /) \nExtracts a device minor number from a raw device number."
    ),
    _(
        "os.mkdir(path, mode=511, *, dir_fd=None) \nCreate a directory.\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\ndir_fd may not be implemented on your platform.\n  If it is unavailable, using it will raise a NotImplementedError.\n\nThe mode argument is ignored on Windows."
    ),
    _(
        'os.mkfifo(path, mode=438, *, dir_fd=None) \nCreate a "fifo" (a POSIX named pipe).\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\ndir_fd may not be implemented on your platform.\n  If it is unavailable, using it will raise a NotImplementedError.'
    ),
    _(
        "os.mknod(path, mode=384, device=0, *, dir_fd=None) \nCreate a node in the file system.\n\nCreate a node in the file system (file, device special file or named pipe)\nat path.  mode specifies both the permissions to use and the\ntype of node to be created, being combined (bitwise OR) with one of\nS_IFREG, S_IFCHR, S_IFBLK, and S_IFIFO.  If S_IFCHR or S_IFBLK is set on mode,\ndevice defines the newly created device special file (probably using\nos.makedev()).  Otherwise device is ignored.\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\ndir_fd may not be implemented on your platform.\n  If it is unavailable, using it will raise a NotImplementedError."
    ),
    _(
        "os.nice(increment, /) \nAdd increment to the priority of process and return the new priority."
    ),
    _(
        "os.open(path, flags, mode=511, *, dir_fd=None) \nOpen a file for low level IO.  Returns a file descriptor (integer).\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\ndir_fd may not be implemented on your platform.\n  If it is unavailable, using it will raise a NotImplementedError."
    ),
    _(
        "os.openpty() \nOpen a pseudo-terminal.\n\nReturn a tuple of (master_fd, slave_fd) containing open file descriptors\nfor both the master and slave ends."
    ),
    _("os.path.abspath(path) \nReturn an absolute path."),
    _("os.path.basename(p) \nReturns the final component of a pathname"),
    _(
        "os.path.commonpath(paths) \nGiven a sequence of path names, returns the longest common sub-path."
    ),
    _(
        "os.path.commonprefix(m) \nGiven a list of pathnames, returns the longest common leading component"
    ),
    _("os.path.dirname(p) \nReturns the directory component of a pathname"),
    _(
        "os.path.exists(path) \nTest whether a path exists.  Returns False for broken symbolic links"
    ),
    _(
        "os.path.expanduser(path) \nExpand ~ and ~user constructions.  If user or $HOME is unknown,\ndo nothing."
    ),
    _(
        "os.path.expandvars(path) \nExpand shell variables of form $var and ${var}.  Unknown variables\nare left unchanged."
    ),
    _(
        "os.path.genericpath() \nPath operations common to more than one OS\nDo not use directly.  The OS specific modules import the appropriate\nfunctions from this module themselves."
    ),
    _(
        "os.path.getatime(filename) \nReturn the last access time of a file, reported by os.stat()."
    ),
    _(
        "os.path.getctime(filename) \nReturn the metadata change time of a file, reported by os.stat()."
    ),
    _(
        "os.path.getmtime(filename) \nReturn the last modification time of a file, reported by os.stat()."
    ),
    _(
        "os.path.getsize(filename) \nReturn the size of a file, reported by os.stat()."
    ),
    _("os.path.isabs(s) \nTest whether a path is absolute"),
    _(
        "os.path.isdir(s) \nReturn true if the pathname refers to an existing directory."
    ),
    _("os.path.isfile(path) \nTest whether a path is a regular file"),
    _("os.path.islink(path) \nTest whether a path is a symbolic link"),
    _("os.path.ismount(path) \nTest whether a path is a mount point"),
    _(
        "os.path.join(a, *p) \nJoin two or more pathname components, inserting '/' as needed.\nIf any component is an absolute path, all previous path components\nwill be discarded.  An empty last part will result in a path that\nends with a separator."
    ),
    _(
        "os.path.lexists(path) \nTest whether a path exists.  Returns True for broken symbolic links"
    ),
    _(
        "os.path.normcase(s) \nNormalize case of pathname.  Has no effect under Posix"
    ),
    _(
        "os.path.normpath(path) \nNormalize path, eliminating double slashes, etc."
    ),
    _(
        "os.path.os() \nOS routines for NT or Posix depending on what system we're on.\n\nThis exports:\n  - all functions from posix or nt, e.g. unlink, stat, etc.\n  - os.path is either posixpath or ntpath\n  - os.name is either 'posix' or 'nt'\n  - os.curdir is a string representing the current directory (always '.')\n  - os.pardir is a string representing the parent directory (always '..')\n  - os.sep is the (or a most common) pathname separator ('/' or '\\\\')\n  - os.extsep is the extension separator (always '.')\n  - os.altsep is the alternate pathname separator (None or '/')\n  - os.pathsep is the component separator used in $PATH etc\n  - os.linesep is the line separator in text files ('\\r' or '\\n' or '\\r\\n')\n  - os.defpath is the default search path for executables\n  - os.devnull is the file path of the null device ('/dev/null', etc.)\n\nPrograms that import and use 'os' stand a better chance of being\nportable between different platforms.  Of course, they must then\nonly use functions that are defined by all platforms (e.g., unlink\nand opendir), and leave all pathname manipulation to os.path\n(e.g., split and join)."
    ),
    _(
        "os.path.realpath(filename) \nReturn the canonical path of the specified filename, eliminating any\nsymbolic links encountered in the path."
    ),
    _(
        "os.path.relpath(path, start=None) \nReturn a relative version of a path"
    ),
    _(
        "os.path.samefile(f1, f2) \nTest whether two pathnames reference the same actual file"
    ),
    _(
        "os.path.sameopenfile(fp1, fp2) \nTest whether two open file objects reference the same file"
    ),
    _(
        "os.path.samestat(s1, s2) \nTest whether two stat buffers reference the same file"
    ),
    _(
        'os.path.split(p) \nSplit a pathname.  Returns tuple "(head, tail)" where "tail" is\neverything after the final slash.  Either part may be empty.'
    ),
    _(
        "os.path.splitdrive(p) \nSplit a pathname into drive and path. On Posix, drive is always\nempty."
    ),
    _(
        'os.path.splitext(p) \nSplit the extension from a pathname.\n\nExtension is everything from the last dot to the end, ignoring\nleading dots.  Returns "(root, ext)"; ext may be empty.'
    ),
    _(
        "os.path.stat() \nConstants/functions for interpreting results of os.stat() and os.lstat().\n\nSuggested usage: from stat import *"
    ),
    _(
        "os.path.sys() \nThis module provides access to some objects used or maintained by the\ninterpreter and to functions that interact strongly with the interpreter.\n\nDynamic objects:\n\nargv -- command line arguments; argv[0] is the script pathname if known\npath -- module search path; path[0] is the script directory, else ''\nmodules -- dictionary of loaded modules\n\ndisplayhook -- called to show results in an interactive session\nexcepthook -- called to handle any uncaught exception other than SystemExit\n  To customize printing in an interactive session or to install a custom\n  top-level exception handler, assign other functions to replace these.\n\nstdin -- standard input file object; used by input()\nstdout -- standard output file object; used by print()\nstderr -- standard error object; used for error messages\n  By assigning other file objects (or objects that behave like files)\n  to these, it is possible to redirect all of the interpreter's I/O.\n\nlast_type -- type of last uncaught exception\nlast_value -- value of last uncaught exception\nlast_traceback -- traceback of last uncaught exception\n  These three are only available in an interactive session after a\n  traceback has been printed.\n\nStatic objects:\n\nbuiltin_module_names -- tuple of module names built into this interpreter\ncopyright -- copyright notice pertaining to this interpreter\nexec_prefix -- prefix used to find the machine-specific Python library\nexecutable -- absolute path of the executable binary of the Python interpreter\nfloat_info -- a struct sequence with information about the float implementation.\nfloat_repr_style -- string indicating the style of repr() output for floats\nhash_info -- a struct sequence with information about the hash algorithm.\nhexversion -- version information encoded as a single integer\nimplementation -- Python implementation information.\nint_info -- a struct sequence with information about the int implementation.\nmaxsize -- the largest supported length of containers.\nmaxunicode -- the value of the largest Unicode code point\nplatform -- platform identifier\nprefix -- prefix used to find the Python library\nthread_info -- a struct sequence with information about the thread implementation.\nversion -- the version of this interpreter as a string\nversion_info -- version information as a named tuple\n__stdin__ -- the original stdin; don't touch!\n__stdout__ -- the original stdout; don't touch!\n__stderr__ -- the original stderr; don't touch!\n__displayhook__ -- the original displayhook; don't touch!\n__excepthook__ -- the original excepthook; don't touch!\n\nFunctions:\n\ndisplayhook() -- print an object to the screen, and save it in builtins._\nexcepthook() -- print an exception and its traceback to sys.stderr\nexc_info() -- return thread-safe information about the current exception\nexit() -- exit the interpreter by raising SystemExit\ngetdlopenflags() -- returns flags to be used for dlopen() calls\ngetprofile() -- get the global profiling function\ngetrefcount() -- return the reference count for an object (plus one :-)\ngetrecursionlimit() -- return the max recursion depth for the interpreter\ngetsizeof() -- return the size of an object in bytes\ngettrace() -- get the global debug tracing function\nsetcheckinterval() -- control how often the interpreter checks for events\nsetdlopenflags() -- set the flags to be used for dlopen() calls\nsetprofile() -- set the global profiling function\nsetrecursionlimit() -- set the max recursion depth for the interpreter\nsettrace() -- set the global debug tracing function"
    ),
    _(
        "os.pathconf(path, name) \nReturn the configuration limit name for the file or directory path.\n\nIf there is no limit, return -1.\nOn some platforms, path may also be specified as an open file descriptor.\n  If this functionality is unavailable, using it raises an exception."
    ),
    _(
        "os.pipe() \nCreate a pipe.\n\nReturns a tuple of two file descriptors:\n  (read_fd, write_fd)"
    ),
    _(
        "os.pipe2(flags, /) \nCreate a pipe with flags set atomically.\n\nReturns a tuple of two file descriptors:\n  (read_fd, write_fd)\n\nflags can be constructed by ORing together one or more of these values:\nO_NONBLOCK, O_CLOEXEC."
    ),
    _(
        "os.posix_fadvise(fd, offset, length, advice, /) \nAnnounce an intention to access data in a specific pattern.\n\nAnnounce an intention to access data in a specific pattern, thus allowing\nthe kernel to make optimizations.\nThe advice applies to the region of the file specified by fd starting at\noffset and continuing for length bytes.\nadvice is one of POSIX_FADV_NORMAL, POSIX_FADV_SEQUENTIAL,\nPOSIX_FADV_RANDOM, POSIX_FADV_NOREUSE, POSIX_FADV_WILLNEED, or\nPOSIX_FADV_DONTNEED."
    ),
    _(
        "os.posix_fallocate(fd, offset, length, /) \nEnsure a file has allocated at least a particular number of bytes on disk.\n\nEnsure that the file specified by fd encompasses a range of bytes\nstarting at offset bytes from the beginning and continuing for length bytes."
    ),
    _(
        'os.posixpath() \nCommon operations on Posix pathnames.\n\nInstead of importing this module directly, import os and refer to\nthis module as os.path.  The "os.path" name is an alias for this\nmodule on Posix systems; on other systems (e.g. Mac, Windows),\nos.path provides the same operations in a manner specific to that\nplatform, and is an alias to another module (e.g. macpath, ntpath).\n\nSome of this can actually be useful on non-Posix systems too, e.g.\nfor manipulation of the pathname component of URLs.'
    ),
    _(
        "os.pread(fd, length, offset, /) \nRead a number of bytes from a file descriptor starting at a particular offset.\n\nRead length bytes from file descriptor fd, starting at offset bytes from\nthe beginning of the file.  The file offset remains unchanged."
    ),
    _("os.putenv(name, value, /) \nChange or add an environment variable."),
    _(
        "os.pwrite(fd, buffer, offset, /) \nWrite bytes to a file descriptor starting at a particular offset.\n\nWrite buffer to fd, starting at offset bytes from the beginning of\nthe file.  Returns the number of bytes writte.  Does not change the\ncurrent file offset."
    ),
    _(
        "os.read(fd, length, /) \nRead from a file descriptor.  Returns a bytes object."
    ),
    _(
        "os.readlink() \nreadlink(path, *, dir_fd=None) -> path\n\nReturn a string representing the path to which the symbolic link points.\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\ndir_fd may not be implemented on your platform.\n  If it is unavailable, using it will raise a NotImplementedError."
    ),
    _(
        "os.readv(fd, buffers, /) \nRead from a file descriptor fd into an iterable of buffers.\n\nThe buffers should be mutable buffers accepting bytes.\nreadv will transfer data into each buffer until it is full\nand then move on to the next buffer in the sequence to hold\nthe rest of the data.\n\nreadv returns the total number of bytes read,\nwhich may be less than the total capacity of all the buffers."
    ),
    _(
        "os.remove(path, *, dir_fd=None) \nRemove a file (same as unlink()).\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\ndir_fd may not be implemented on your platform.\n  If it is unavailable, using it will raise a NotImplementedError."
    ),
    _(
        "os.removedirs(name) \nremovedirs(name)\n\nSuper-rmdir; remove a leaf directory and all empty intermediate\nones.  Works like rmdir except that, if the leaf directory is\nsuccessfully removed, directories corresponding to rightmost path\nsegments will be pruned away until either the whole path is\nconsumed or an error occurs.  Errors during this latter phase are\nignored -- they generally mean that a directory was not empty."
    ),
    _(
        "os.removexattr(path, attribute, *, follow_symlinks=True) \nRemove extended attribute attribute on path.\n\npath may be either a string or an open file descriptor.\nIf follow_symlinks is False, and the last element of the path is a symbolic\n  link, removexattr will modify the symbolic link itself instead of the file\n  the link points to."
    ),
    _(
        "os.rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None) \nRename a file or directory.\n\nIf either src_dir_fd or dst_dir_fd is not None, it should be a file\n  descriptor open to a directory, and the respective path string (src or dst)\n  should be relative; the path will then be relative to that directory.\nsrc_dir_fd and dst_dir_fd, may not be implemented on your platform.\n  If they are unavailable, using them will raise a NotImplementedError."
    ),
    _(
        "os.renames(old, new) \nrenames(old, new)\n\nSuper-rename; create directories as necessary and delete any left\nempty.  Works like rename, except creation of any intermediate\ndirectories needed to make the new pathname good is attempted\nfirst.  After the rename, directories corresponding to rightmost\npath segments of the old name will be pruned until either the\nwhole path is consumed or a nonempty directory is found.\n\nNote: this function can fail with the new directory structure made\nif you lack permissions needed to unlink the leaf directory or\nfile."
    ),
    _(
        'os.replace(src, dst, *, src_dir_fd=None, dst_dir_fd=None) \nRename a file or directory, overwriting the destination.\n\nIf either src_dir_fd or dst_dir_fd is not None, it should be a file\n  descriptor open to a directory, and the respective path string (src or dst)\n  should be relative; the path will then be relative to that directory.\nsrc_dir_fd and dst_dir_fd, may not be implemented on your platform.\n  If they are unavailable, using them will raise a NotImplementedError."'
    ),
    _(
        "os.rmdir(path, *, dir_fd=None) \nRemove a directory.\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\ndir_fd may not be implemented on your platform.\n  If it is unavailable, using it will raise a NotImplementedError."
    ),
    _(
        "os.scandir() \nscandir(path='.') -> iterator of DirEntry objects for given path"
    ),
    _(
        "os.sched_get_priority_max(policy) \nGet the maximum scheduling priority for policy."
    ),
    _(
        "os.sched_get_priority_min(policy) \nGet the minimum scheduling priority for policy."
    ),
    _(
        "os.sched_getaffinity(pid, /) \nReturn the affinity of the process identified by pid (or the current process if zero).\n\nThe affinity is returned as a set of CPU identifiers."
    ),
    _(
        "os.sched_getparam(pid, /) \nReturns scheduling parameters for the process identified by pid.\n\nIf pid is 0, returns parameters for the calling process.\nReturn value is an instance of sched_param."
    ),
    _(
        "os.sched_getscheduler(pid, /) \nGet the scheduling policy for the process identifiedy by pid.\n\nPassing 0 for pid returns the scheduling policy for the calling process."
    ),
    _(
        'os.sched_param(sched_priority) \nCurrent has only one field: sched_priority");\n\nsched_priority\n  A scheduling parameter.'
    ),
    _(
        "os.sched_rr_get_interval(pid, /) \nReturn the round-robin quantum for the process identified by pid, in seconds.\n\nValue returned is a float."
    ),
    _(
        "os.sched_setaffinity(pid, mask, /) \nSet the CPU affinity of the process identified by pid to mask.\n\nmask should be an iterable of integers identifying CPUs."
    ),
    _(
        "os.sched_setparam(pid, param, /) \nSet scheduling parameters for the process identified by pid.\n\nIf pid is 0, sets parameters for the calling process.\nparam should be an instance of sched_param."
    ),
    _(
        "os.sched_setscheduler(pid, policy, param, /) \nSet the scheduling policy for the process identified by pid.\n\nIf pid is 0, the calling process is changed.\nparam is an instance of sched_param."
    ),
    _("os.sched_yield() \nVoluntarily relinquish the CPU."),
    _(
        "os.sendfile() \nsendfile(out, in, offset, count) -> byteswritten\nsendfile(out, in, offset, count[, headers][, trailers], flags=0)\n            -> byteswritten\nCopy count bytes from file descriptor in to file descriptor out."
    ),
    _(
        "os.set_blocking() \nset_blocking(fd, blocking)\n\nSet the blocking mode of the specified file descriptor.\nSet the O_NONBLOCK flag if blocking is False,\nclear the O_NONBLOCK flag otherwise."
    ),
    _(
        "os.set_inheritable(fd, inheritable, /) \nSet the inheritable flag of the specified file descriptor."
    ),
    _("os.setegid(egid, /) \nSet the current process's effective group id."),
    _("os.seteuid(euid, /) \nSet the current process's effective user id."),
    _("os.setgid(gid, /) \nSet the current process's group id."),
    _(
        "os.setgroups(groups, /) \nSet the groups of the current process to list."
    ),
    _("os.setpgid(pid, pgrp, /) \nCall the system call setpgid(pid, pgrp)."),
    _(
        "os.setpgrp() \nMake the current process the leader of its process group."
    ),
    _(
        "os.setpriority(which, who, priority) \nSet program scheduling priority."
    ),
    _(
        "os.setregid(rgid, egid, /) \nSet the current process's real and effective group ids."
    ),
    _(
        "os.setresgid(rgid, egid, sgid, /) \nSet the current process's real, effective, and saved group ids."
    ),
    _(
        "os.setresuid(ruid, euid, suid, /) \nSet the current process's real, effective, and saved user ids."
    ),
    _(
        "os.setreuid(ruid, euid, /) \nSet the current process's real and effective user ids."
    ),
    _("os.setsid() \nCall the system call setsid()."),
    _("os.setuid(uid, /) \nSet the current process's user id."),
    _(
        "os.setxattr(path, attribute, value, flags=0, *, follow_symlinks=True) \nSet extended attribute attribute on path to value.\n\npath may be either a string or an open file descriptor.\nIf follow_symlinks is False, and the last element of the path is a symbolic\n  link, setxattr will modify the symbolic link itself instead of the file\n  the link points to."
    ),
    _(
        "os.spawnl(mode, file, *args) \nspawnl(mode, file, *args) -> integer\n\nExecute file with arguments from args in a subprocess.\nIf mode == P_NOWAIT return the pid of the process.\nIf mode == P_WAIT return the process's exit code if it exits normally;\notherwise return -SIG, where SIG is the signal that killed it. "
    ),
    _(
        "os.spawnle(mode, file, *args) \nspawnle(mode, file, *args, env) -> integer\n\nExecute file with arguments from args in a subprocess with the\nsupplied environment.\nIf mode == P_NOWAIT return the pid of the process.\nIf mode == P_WAIT return the process's exit code if it exits normally;\notherwise return -SIG, where SIG is the signal that killed it. "
    ),
    _(
        "os.spawnlp(mode, file, *args) \nspawnlp(mode, file, *args) -> integer\n\nExecute file (which is looked for along $PATH) with arguments from\nargs in a subprocess with the supplied environment.\nIf mode == P_NOWAIT return the pid of the process.\nIf mode == P_WAIT return the process's exit code if it exits normally;\notherwise return -SIG, where SIG is the signal that killed it. "
    ),
    _(
        "os.spawnlpe(mode, file, *args) \nspawnlpe(mode, file, *args, env) -> integer\n\nExecute file (which is looked for along $PATH) with arguments from\nargs in a subprocess with the supplied environment.\nIf mode == P_NOWAIT return the pid of the process.\nIf mode == P_WAIT return the process's exit code if it exits normally;\notherwise return -SIG, where SIG is the signal that killed it. "
    ),
    _(
        "os.spawnv(mode, file, args) \nspawnv(mode, file, args) -> integer\n\nExecute file with arguments from args in a subprocess.\nIf mode == P_NOWAIT return the pid of the process.\nIf mode == P_WAIT return the process's exit code if it exits normally;\notherwise return -SIG, where SIG is the signal that killed it. "
    ),
    _(
        "os.spawnve(mode, file, args, env) \nspawnve(mode, file, args, env) -> integer\n\nExecute file with arguments from args in a subprocess with the\nspecified environment.\nIf mode == P_NOWAIT return the pid of the process.\nIf mode == P_WAIT return the process's exit code if it exits normally;\notherwise return -SIG, where SIG is the signal that killed it. "
    ),
    _(
        "os.spawnvp(mode, file, args) \nspawnvp(mode, file, args) -> integer\n\nExecute file (which is looked for along $PATH) with arguments from\nargs in a subprocess.\nIf mode == P_NOWAIT return the pid of the process.\nIf mode == P_WAIT return the process's exit code if it exits normally;\notherwise return -SIG, where SIG is the signal that killed it. "
    ),
    _(
        "os.spawnvpe(mode, file, args, env) \nspawnvpe(mode, file, args, env) -> integer\n\nExecute file (which is looked for along $PATH) with arguments from\nargs in a subprocess with the supplied environment.\nIf mode == P_NOWAIT return the pid of the process.\nIf mode == P_WAIT return the process's exit code if it exits normally;\notherwise return -SIG, where SIG is the signal that killed it. "
    ),
    _(
        "os.stat() \nConstants/functions for interpreting results of os.stat() and os.lstat().\n\nSuggested usage: from stat import *"
    ),
    _(
        "os.stat(path, *, dir_fd=None, follow_symlinks=True) \nPerform a stat system call on the given path.\n\n  path\n    Path to be examined; can be string, bytes, path-like object or\n    open-file-descriptor int.\n  dir_fd\n    If not None, it should be a file descriptor open to a directory,\n    and path should be a relative string; path will then be relative to\n    that directory.\n  follow_symlinks\n    If False, and the last element of the path is a symbolic link,\n    stat will examine the symbolic link itself instead of the file\n    the link points to.\n\ndir_fd and follow_symlinks may not be implemented\n  on your platform.  If they are unavailable, using them will raise a\n  NotImplementedError.\n\nIt's an error to use dir_fd or follow_symlinks when specifying path as\n  an open file descriptor."
    ),
    _(
        "os.stat_float_times() \nstat_float_times([newval]) -> oldval\n\nDetermine whether os.[lf]stat represents time stamps as float objects.\n\nIf value is True, future calls to stat() return floats; if it is False,\nfuture calls return ints.\nIf value is omitted, return the current setting."
    ),
    _(
        "os.stat_result() \nstat_result: Result from stat, fstat, or lstat.\n\nThis object may be accessed either as a tuple of\n  (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)\nor via the attributes st_mode, st_ino, st_dev, st_nlink, st_uid, and so on.\n\nPosix/windows: If your platform supports st_blksize, st_blocks, st_rdev,\nor st_flags, they are available as attributes only.\n\nSee os.stat for more information."
    ),
    _(
        "os.statvfs(path) \nPerform a statvfs system call on the given path.\n\npath may always be specified as a string.\nOn some platforms, path may also be specified as an open file descriptor.\n  If this functionality is unavailable, using it raises an exception."
    ),
    _(
        "os.statvfs_result() \nstatvfs_result: Result from statvfs or fstatvfs.\n\nThis object may be accessed either as a tuple of\n  (bsize, frsize, blocks, bfree, bavail, files, ffree, favail, flag, namemax),\nor via the attributes f_bsize, f_frsize, f_blocks, f_bfree, and so on.\n\nSee os.statvfs for more information."
    ),
    _("os.strerror(code, /) \nTranslate an error code to a message string."),
    _(
        "os.symlink(src, dst, target_is_directory=False, *, dir_fd=None) \nCreate a symbolic link pointing to src named dst.\n\ntarget_is_directory is required on Windows if the target is to be\n  interpreted as a directory.  (On Windows, symlink requires\n  Windows 6.0 or greater, and raises a NotImplementedError otherwise.)\n  target_is_directory is ignored on non-Windows platforms.\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\ndir_fd may not be implemented on your platform.\n  If it is unavailable, using it will raise a NotImplementedError."
    ),
    _("os.sync() \nForce write of everything to disk."),
    _(
        "os.sys() \nThis module provides access to some objects used or maintained by the\ninterpreter and to functions that interact strongly with the interpreter.\n\nDynamic objects:\n\nargv -- command line arguments; argv[0] is the script pathname if known\npath -- module search path; path[0] is the script directory, else ''\nmodules -- dictionary of loaded modules\n\ndisplayhook -- called to show results in an interactive session\nexcepthook -- called to handle any uncaught exception other than SystemExit\n  To customize printing in an interactive session or to install a custom\n  top-level exception handler, assign other functions to replace these.\n\nstdin -- standard input file object; used by input()\nstdout -- standard output file object; used by print()\nstderr -- standard error object; used for error messages\n  By assigning other file objects (or objects that behave like files)\n  to these, it is possible to redirect all of the interpreter's I/O.\n\nlast_type -- type of last uncaught exception\nlast_value -- value of last uncaught exception\nlast_traceback -- traceback of last uncaught exception\n  These three are only available in an interactive session after a\n  traceback has been printed.\n\nStatic objects:\n\nbuiltin_module_names -- tuple of module names built into this interpreter\ncopyright -- copyright notice pertaining to this interpreter\nexec_prefix -- prefix used to find the machine-specific Python library\nexecutable -- absolute path of the executable binary of the Python interpreter\nfloat_info -- a struct sequence with information about the float implementation.\nfloat_repr_style -- string indicating the style of repr() output for floats\nhash_info -- a struct sequence with information about the hash algorithm.\nhexversion -- version information encoded as a single integer\nimplementation -- Python implementation information.\nint_info -- a struct sequence with information about the int implementation.\nmaxsize -- the largest supported length of containers.\nmaxunicode -- the value of the largest Unicode code point\nplatform -- platform identifier\nprefix -- prefix used to find the Python library\nthread_info -- a struct sequence with information about the thread implementation.\nversion -- the version of this interpreter as a string\nversion_info -- version information as a named tuple\n__stdin__ -- the original stdin; don't touch!\n__stdout__ -- the original stdout; don't touch!\n__stderr__ -- the original stderr; don't touch!\n__displayhook__ -- the original displayhook; don't touch!\n__excepthook__ -- the original excepthook; don't touch!\n\nFunctions:\n\ndisplayhook() -- print an object to the screen, and save it in builtins._\nexcepthook() -- print an exception and its traceback to sys.stderr\nexc_info() -- return thread-safe information about the current exception\nexit() -- exit the interpreter by raising SystemExit\ngetdlopenflags() -- returns flags to be used for dlopen() calls\ngetprofile() -- get the global profiling function\ngetrefcount() -- return the reference count for an object (plus one :-)\ngetrecursionlimit() -- return the max recursion depth for the interpreter\ngetsizeof() -- return the size of an object in bytes\ngettrace() -- get the global debug tracing function\nsetcheckinterval() -- control how often the interpreter checks for events\nsetdlopenflags() -- set the flags to be used for dlopen() calls\nsetprofile() -- set the global profiling function\nsetrecursionlimit() -- set the max recursion depth for the interpreter\nsettrace() -- set the global debug tracing function"
    ),
    _(
        "os.sysconf(name, /) \nReturn an integer-valued system configuration variable."
    ),
    _("os.system(command) \nExecute the command in a subshell."),
    _(
        "os.tcgetpgrp(fd, /) \nReturn the process group associated with the terminal specified by fd."
    ),
    _(
        "os.tcsetpgrp(fd, pgid, /) \nSet the process group associated with the terminal specified by fd."
    ),
    _(
        "os.terminal_size() \nA tuple of (columns, lines) for holding terminal window size"
    ),
    _(
        "os.times() \nReturn a collection containing process timing information.\n\nThe object returned behaves like a named tuple with these fields:\n  (utime, stime, cutime, cstime, elapsed_time)\nAll fields are floating point numbers."
    ),
    _(
        "os.times_result() \ntimes_result: Result from os.times().\n\nThis object may be accessed either as a tuple of\n  (user, system, children_user, children_system, elapsed),\nor via the attributes user, system, children_user, children_system,\nand elapsed.\n\nSee os.times for more information."
    ),
    _(
        "os.truncate(path, length) \nTruncate a file, specified by path, to a specific length.\n\nOn some platforms, path may also be specified as an open file descriptor.\n  If this functionality is unavailable, using it raises an exception."
    ),
    _(
        "os.ttyname(fd, /) \nReturn the name of the terminal device connected to 'fd'.\n\nfd\n  Integer file descriptor handle."
    ),
    _(
        "os.umask(mask, /) \nSet the current numeric umask and return the previous umask."
    ),
    _(
        "os.uname() \nReturn an object identifying the current operating system.\n\nThe object behaves like a named tuple with the following fields:\n  (sysname, nodename, release, version, machine)"
    ),
    _(
        "os.uname_result() \nuname_result: Result from os.uname().\n\nThis object may be accessed either as a tuple of\n  (sysname, nodename, release, version, machine),\nor via the attributes sysname, nodename, release, version, and machine.\n\nSee os.uname for more information."
    ),
    _(
        "os.unlink(path, *, dir_fd=None) \nRemove a file (same as remove()).\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\ndir_fd may not be implemented on your platform.\n  If it is unavailable, using it will raise a NotImplementedError."
    ),
    _("os.unsetenv(name, /) \nDelete an environment variable."),
    _(
        "os.urandom(size, /) \nReturn a bytes object containing random bytes suitable for cryptographic use."
    ),
    _(
        "os.utime(path, times=None, *, ns=None, dir_fd=None, follow_symlinks=True) \nSet the access and modified time of path.\n\npath may always be specified as a string.\nOn some platforms, path may also be specified as an open file descriptor.\n  If this functionality is unavailable, using it raises an exception.\n\nIf times is not None, it must be a tuple (atime, mtime);\n    atime and mtime should be expressed as float seconds since the epoch.\nIf ns is specified, it must be a tuple (atime_ns, mtime_ns);\n    atime_ns and mtime_ns should be expressed as integer nanoseconds\n    since the epoch.\nIf times is None and ns is unspecified, utime uses the current time.\nSpecifying tuples for both times and ns is an error.\n\nIf dir_fd is not None, it should be a file descriptor open to a directory,\n  and path should be relative; path will then be relative to that directory.\nIf follow_symlinks is False, and the last element of the path is a symbolic\n  link, utime will modify the symbolic link itself instead of the file the\n  link points to.\nIt is an error to use dir_fd or follow_symlinks when specifying path\n  as an open file descriptor.\ndir_fd and follow_symlinks may not be available on your platform.\n  If they are unavailable, using them will raise a NotImplementedError."
    ),
    _(
        "os.wait() \nWait for completion of a child process.\n\nReturns a tuple of information about the child process:\n    (pid, status)"
    ),
    _(
        "os.wait3(options) \nWait for completion of a child process.\n\nReturns a tuple of information about the child process:\n  (pid, status, rusage)"
    ),
    _(
        "os.wait4(pid, options) \nWait for completion of a specific child process.\n\nReturns a tuple of information about the child process:\n  (pid, status, rusage)"
    ),
    _(
        "os.waitid(idtype, id, options, /) \nReturns the result of waiting for a process or processes.\n\n  idtype\n    Must be one of be P_PID, P_PGID or P_ALL.\n  id\n    The id to wait on.\n  options\n    Constructed from the ORing of one or more of WEXITED, WSTOPPED\n    or WCONTINUED and additionally may be ORed with WNOHANG or WNOWAIT.\n\nReturns either waitid_result or None if WNOHANG is specified and there are\nno children in a waitable state."
    ),
    _(
        "os.waitid_result() \nwaitid_result: Result from waitid.\n\nThis object may be accessed either as a tuple of\n  (si_pid, si_uid, si_signo, si_status, si_code),\nor via the attributes si_pid, si_uid, and so on.\n\nSee os.waitid for more information."
    ),
    _(
        "os.waitpid(pid, options, /) \nWait for completion of a given child process.\n\nReturns a tuple of information regarding the child process:\n    (pid, status)\n\nThe options argument is ignored on Windows."
    ),
    _(
        "os.walk(top, topdown=True, onerror=None, followlinks=False) \nDirectory tree generator.\n\nFor each directory in the directory tree rooted at top (including top\nitself, but excluding '.' and '..'), yields a 3-tuple\n\n    dirpath, dirnames, filenames\n\ndirpath is a string, the path to the directory.  dirnames is a list of\nthe names of the subdirectories in dirpath (excluding '.' and '..').\nfilenames is a list of the names of the non-directory files in dirpath.\nNote that the names in the lists are just names, with no path components.\nTo get a full path (which begins with top) to a file or directory in\ndirpath, do os.path.join(dirpath, name).\n\nIf optional arg 'topdown' is true or not specified, the triple for a\ndirectory is generated before the triples for any of its subdirectories\n(directories are generated top down).  If topdown is false, the triple\nfor a directory is generated after the triples for all of its\nsubdirectories (directories are generated bottom up).\n\nWhen topdown is true, the caller can modify the dirnames list in-place\n(e.g., via del or slice assignment), and walk will only recurse into the\nsubdirectories whose names remain in dirnames; this can be used to prune the\nsearch, or to impose a specific order of visiting.  Modifying dirnames when\ntopdown is false is ineffective, since the directories in dirnames have\nalready been generated by the time dirnames itself is generated. No matter\nthe value of topdown, the list of subdirectories is retrieved before the\ntuples for the directory and its subdirectories are generated.\n\nBy default errors from the os.scandir() call are ignored.  If\noptional arg 'onerror' is specified, it should be a function; it\nwill be called with one argument, an OSError instance.  It can\nreport the error to continue with the walk, or raise the exception\nto abort the walk.  Note that the filename is available as the\nfilename attribute of the exception object.\n\nBy default, os.walk does not follow symbolic links to subdirectories on\nsystems that support them.  In order to get this functionality, set the\noptional argument 'followlinks' to true.\n\nCaution:  if you pass a relative pathname for top, don't change the\ncurrent working directory between resumptions of walk.  walk never\nchanges the current directory, and assumes that the client doesn't\neither.\n\nExample:\n\nimport os\nfrom os.path import join, getsize\nfor root, dirs, files in os.walk('python/Lib/email'):\n    print(root, \"consumes\", end=\"\")\n    print(sum([getsize(join(root, name)) for name in files]), end=\"\")\n    print(\"bytes in\", len(files), \"non-directory files\")\n    if 'CVS' in dirs:\n        dirs.remove('CVS')  # don't visit CVS directories"
    ),
    _("os.write(fd, data, /) \nWrite a bytes object to a file descriptor."),
    _(
        "os.writev(fd, buffers, /) \nIterate over buffers, and write the contents of each to a file descriptor.\n\nReturns the total number of bytes written.\nbuffers must be a sequence of bytes-like objects."
    ),
    _(
        "random.Random(x=None) \nRandom number generator base class used by bound module functions.\n\nUsed to instantiate instances of Random to get generators that don't\nshare state.\n\nClass Random can also be subclassed if you want to use a different basic\ngenerator of your own devising: in that case, override the following\nmethods:  random(), seed(), getstate(), and setstate().\nOptionally, implement a getrandbits() method so that randrange()\ncan cover arbitrarily large ranges."
    ),
    _(
        "random.SystemRandom(x=None) \nAlternate random number generator using sources provided\nby the operating system (such as /dev/urandom on Unix or\nCryptGenRandom on Windows).\n\n Not available on all systems (see os.urandom() for details)."
    ),
    _(
        "random.betavariate(alpha, beta) \nBeta distribution.\n\nConditions on the parameters are alpha > 0 and beta > 0.\nReturned values range between 0 and 1."
    ),
    _(
        "random.choice(seq) \nChoose a random element from a non-empty sequence."
    ),
    _(
        "random.choices(population, weights=None, *, cum_weights=None, k=1) \nReturn a k sized list of population elements chosen with replacement.\n\nIf the relative weights or cumulative weights are not specified,\nthe selections are made with equal probability."
    ),
    _(
        'random.expovariate(lambd) \nExponential distribution.\n\nlambd is 1.0 divided by the desired mean.  It should be\nnonzero.  (The parameter would be called "lambda", but that is\na reserved word in Python.)  Returned values range from 0 to\npositive infinity if lambd is positive, and from negative\ninfinity to 0 if lambd is negative.'
    ),
    _(
        "random.gammavariate(alpha, beta) \nGamma distribution.  Not the gamma function!\n\nConditions on the parameters are alpha > 0 and beta > 0.\n\nThe probability distribution function is:\n\n            x ** (alpha - 1) * math.exp(-x / beta)\n  pdf(x) =  --------------------------------------\n              math.gamma(alpha) * beta ** alpha"
    ),
    _(
        "random.gauss(mu, sigma) \nGaussian distribution.\n\nmu is the mean, and sigma is the standard deviation.  This is\nslightly faster than the normalvariate() function.\n\nNot thread-safe without a lock around calls."
    ),
    _(
        "random.getrandbits() \ngetrandbits(k) -> x.  Generates an int with k random bits."
    ),
    _(
        "random.getstate() \nReturn internal state; can be passed to setstate() later."
    ),
    _(
        "random.lognormvariate(mu, sigma) \nLog normal distribution.\n\nIf you take the natural logarithm of this distribution, you'll get a\nnormal distribution with mean mu and standard deviation sigma.\nmu can have any value, and sigma must be greater than zero."
    ),
    _(
        "random.normalvariate(mu, sigma) \nNormal distribution.\n\nmu is the mean, and sigma is the standard deviation."
    ),
    _(
        "random.paretovariate(alpha) \nPareto distribution.  alpha is the shape parameter."
    ),
    _(
        "random.randint(a, b) \nReturn random integer in range [a, b], including both end points.\n        "
    ),
    _("random.random() \nrandom() -> x in the interval [0, 1)."),
    _(
        "random.randrange(start, stop=None, step=1, _int=<class 'int'>) \nChoose a random item from range(start, stop[, step]).\n\nThis fixes the problem with randint() which includes the\nendpoint; in Python this is usually not what you want."
    ),
    _(
        "random.sample(population, k) \nChooses k unique random elements from a population sequence or set.\n\nReturns a new list containing elements from the population while\nleaving the original population unchanged.  The resulting list is\nin selection order so that all sub-slices will also be valid random\nsamples.  This allows raffle winners (the sample) to be partitioned\ninto grand prize and second place winners (the subslices).\n\nMembers of the population need not be hashable or unique.  If the\npopulation contains repeats, then each occurrence is a possible\nselection in the sample.\n\nTo choose a sample in a range of integers, use range as an argument.\nThis is especially fast and space efficient for sampling from a\nlarge population:   sample(range(10000000), 60)"
    ),
    _(
        "random.seed(a=None, version=2) \nInitialize internal state from hashable object.\n\nNone or no argument seeds from current time or from an operating\nsystem specific randomness source if available.\n\nIf *a* is an int, all bits are used.\n\nFor version 2 (the default), all of the bits are used if *a* is a str,\nbytes, or bytearray.  For version 1 (provided for reproducing random\nsequences from older versions of Python), the algorithm for str and\nbytes generates a narrower range of seeds."
    ),
    _(
        "random.setstate(state) \nRestore internal state from object returned by getstate()."
    ),
    _(
        "random.shuffle(x, random=None) \nShuffle list x in place, and return None.\n\nOptional argument random is a 0-argument function returning a\nrandom float in [0.0, 1.0); if it is the default None, the\nstandard random.random will be used."
    ),
    _(
        "random.triangular(low=0.0, high=1.0, mode=None) \nTriangular distribution.\n\nContinuous distribution bounded by given lower and upper limits,\nand having a given mode value in-between.\n\nhttp://en.wikipedia.org/wiki/Triangular_distribution"
    ),
    _(
        "random.uniform(a, b) \nGet a random number in the range [a, b) or [a, b] depending on rounding."
    ),
    _(
        "random.vonmisesvariate(mu, kappa) \nCircular data distribution.\n\nmu is the mean angle, expressed in radians between 0 and 2*pi, and\nkappa is the concentration parameter, which must be greater than or\nequal to zero.  If kappa is equal to zero, this distribution reduces\nto a uniform random angle over the range 0 to 2*pi."
    ),
    _(
        "random.weibullvariate(alpha, beta) \nWeibull distribution.\n\nalpha is the scale parameter and beta is the shape parameter."
    ),
    _(
        "socket.AddressFamily(value, names=None, *, module=None, qualname=None, type=None, start=1) \nAn enumeration."
    ),
    _(
        "socket.AddressInfo(value, names=None, *, module=None, qualname=None, type=None, start=1) \nAn enumeration."
    ),
    _(
        "socket.CMSG_LEN() \nCMSG_LEN(length) -> control message length\n\nReturn the total length, without trailing padding, of an ancillary\ndata item with associated data of the given length.  This value can\noften be used as the buffer size for recvmsg() to receive a single\nitem of ancillary data, but RFC 3542 requires portable applications to\nuse CMSG_SPACE() and thus include space for padding, even when the\nitem will be the last in the buffer.  Raises OverflowError if length\nis outside the permissible range of values."
    ),
    _(
        "socket.CMSG_SPACE() \nCMSG_SPACE(length) -> buffer size\n\nReturn the buffer size needed for recvmsg() to receive an ancillary\ndata item with associated data of the given length, along with any\ntrailing padding.  The buffer space needed to receive multiple items\nis the sum of the CMSG_SPACE() values for their associated data\nlengths.  Raises OverflowError if length is outside the permissible\nrange of values."
    ),
    _(
        "socket.IntEnum(value, names=None, *, module=None, qualname=None, type=None, start=1) \nEnum where members are also (and must be) ints"
    ),
    _(
        "socket.IntFlag(value, names=None, *, module=None, qualname=None, type=None, start=1) \nSupport for integer-based Flags"
    ),
    _(
        "socket.MsgFlag(value, names=None, *, module=None, qualname=None, type=None, start=1) \nAn enumeration."
    ),
    _("socket.OSError() \nBase class for I/O related errors."),
    _(
        "socket.SocketIO(sock, mode) \nRaw I/O implementation for stream sockets.\n\nThis class supports the makefile() method on sockets.  It provides\nthe raw I/O interface on top of a socket object."
    ),
    _(
        "socket.SocketKind(value, names=None, *, module=None, qualname=None, type=None, start=1) \nAn enumeration."
    ),
    _(
        "socket.create_connection(address, timeout=<object object at 0x7fcbd4efa180>, source_address=None) \nConnect to *address* and return the socket object.\n\nConvenience function.  Connect to *address* (a 2-tuple ``(host,\nport)``) and return the socket object.  Passing the optional\n*timeout* parameter will set the timeout on the socket instance\nbefore attempting to connect.  If no *timeout* is supplied, the\nglobal default timeout setting returned by :func:`getdefaulttimeout`\nis used.  If *source_address* is set it must be a tuple of (host, port)\nfor the socket to bind as a source address before making the connection.\nA host of '' or port 0 tells the OS to use the default."
    ),
    _(
        "socket.dup() \ndup(integer) -> integer\n\nDuplicate an integer socket file descriptor.  This is like os.dup(), but for\nsockets; on some platforms os.dup() won't work for socket file descriptors."
    ),
    _(
        "socket.errno() \nThis module makes available standard errno system symbols.\n\nThe value of each symbol is the corresponding integer value,\ne.g., on most systems, errno.ENOENT equals the integer 2.\n\nThe dictionary errno.errorcode maps numeric codes to symbol names,\ne.g., errno.errorcode[2] could be the string 'ENOENT'.\n\nSymbols that are not relevant to the underlying system are not defined.\n\nTo map error codes to error messages, use the function os.strerror(),\ne.g. os.strerror(2) could return 'No such file or directory'."
    ),
    _(
        "socket.fromfd(fd, family, type, proto=0) \nfromfd(fd, family, type[, proto]) -> socket object\n\nCreate a socket object from a duplicate of the given file\ndescriptor.  The remaining arguments are the same as for socket()."
    ),
    _("socket.gaierror() \nBase class for I/O related errors."),
    _(
        "socket.getaddrinfo(host, port, family=0, type=0, proto=0, flags=0) \nResolve host and port into list of address info entries.\n\nTranslate the host/port argument into a sequence of 5-tuples that contain\nall the necessary arguments for creating a socket connected to that service.\nhost is a domain name, a string representation of an IPv4/v6 address or\nNone. port is a string service name such as 'http', a numeric port number or\nNone. By passing None as the value of host and port, you can pass NULL to\nthe underlying C API.\n\nThe family, type and proto arguments can be optionally specified in order to\nnarrow the list of addresses returned. Passing zero as a value for each of\nthese arguments selects the full range of results."
    ),
    _(
        "socket.getdefaulttimeout() \ngetdefaulttimeout() -> timeout\n\nReturns the default timeout in seconds (float) for new socket objects.\nA value of None indicates that new socket objects have no timeout.\nWhen the socket module is first imported, the default is None."
    ),
    _(
        "socket.getfqdn(name='') \nGet fully qualified domain name from name.\n\nAn empty argument is interpreted as meaning the local host.\n\nFirst the hostname returned by gethostbyaddr() is checked, then\npossibly existing aliases. In case no FQDN is available, hostname\nfrom gethostname() is returned."
    ),
    _(
        "socket.gethostbyaddr() \ngethostbyaddr(host) -> (name, aliaslist, addresslist)\n\nReturn the true host name, a list of aliases, and a list of IP addresses,\nfor a host.  The host argument is a string giving a host name or IP number."
    ),
    _(
        "socket.gethostbyname() \ngethostbyname(host) -> address\n\nReturn the IP address (a string of the form '255.255.255.255') for a host."
    ),
    _(
        "socket.gethostbyname_ex() \ngethostbyname_ex(host) -> (name, aliaslist, addresslist)\n\nReturn the true host name, a list of aliases, and a list of IP addresses,\nfor a host.  The host argument is a string giving a host name or IP number."
    ),
    _(
        "socket.gethostname() \ngethostname() -> string\n\nReturn the current host name."
    ),
    _(
        "socket.getnameinfo() \ngetnameinfo(sockaddr, flags) --> (host, port)\n\nGet host and port for a sockaddr."
    ),
    _(
        "socket.getprotobyname() \ngetprotobyname(name) -> integer\n\nReturn the protocol number for the named protocol.  (Rarely used.)"
    ),
    _(
        "socket.getservbyname() \ngetservbyname(servicename[, protocolname]) -> integer\n\nReturn a port number from a service name and protocol name.\nThe optional protocol name, if given, should be 'tcp' or 'udp',\notherwise any protocol will match."
    ),
    _(
        "socket.getservbyport() \ngetservbyport(port[, protocolname]) -> string\n\nReturn the service name from a port number and protocol name.\nThe optional protocol name, if given, should be 'tcp' or 'udp',\notherwise any protocol will match."
    ),
    _("socket.herror() \nBase class for I/O related errors."),
    _(
        "socket.htonl() \nhtonl(integer) -> integer\n\nConvert a 32-bit integer from host to network byte order."
    ),
    _(
        "socket.htons() \nhtons(integer) -> integer\n\nConvert a 16-bit integer from host to network byte order."
    ),
    _(
        "socket.if_indextoname() \nif_indextoname(if_index)\n\nReturns the interface name corresponding to the interface index if_index."
    ),
    _(
        "socket.if_nameindex() \nif_nameindex()\n\nReturns a list of network interface information (index, name) tuples."
    ),
    _(
        "socket.if_nametoindex() \nif_nametoindex(if_name)\n\nReturns the interface index corresponding to the interface name if_name."
    ),
    _(
        "socket.inet_aton() \ninet_aton(string) -> bytes giving packed 32-bit IP representation\n\nConvert an IP address in string format (123.45.67.89) to the 32-bit packed\nbinary format used in low-level network functions."
    ),
    _(
        "socket.inet_ntoa() \ninet_ntoa(packed_ip) -> ip_address_string\n\nConvert an IP address from 32-bit packed binary format to string format"
    ),
    _(
        "socket.inet_ntop() \ninet_ntop(af, packed_ip) -> string formatted IP address\n\nConvert a packed IP address of the given family to string format."
    ),
    _(
        "socket.inet_pton() \ninet_pton(af, ip) -> packed IP address string\n\nConvert an IP address from string format to a packed string suitable\nfor use with low-level network functions."
    ),
    _(
        "socket.io() \nThe io module provides the Python interfaces to stream handling. The\nbuiltin open function is defined in this module.\n\nAt the top of the I/O hierarchy is the abstract base class IOBase. It\ndefines the basic interface to a stream. Note, however, that there is no\nseparation between reading and writing to streams; implementations are\nallowed to raise an OSError if they do not support a given operation.\n\nExtending IOBase is RawIOBase which deals simply with the reading and\nwriting of raw bytes to a stream. FileIO subclasses RawIOBase to provide\nan interface to OS files.\n\nBufferedIOBase deals with buffering on a raw byte stream (RawIOBase). Its\nsubclasses, BufferedWriter, BufferedReader, and BufferedRWPair buffer\nstreams that are readable, writable, and both respectively.\nBufferedRandom provides a buffered interface to random access\nstreams. BytesIO is a simple stream of in-memory bytes.\n\nAnother IOBase subclass, TextIOBase, deals with the encoding and decoding\nof streams into text. TextIOWrapper, which extends it, is a buffered text\ninterface to a buffered raw stream (`BufferedIOBase`). Finally, StringIO\nis an in-memory stream for text.\n\nArgument names are not part of the specification, and only the arguments\nof open() are intended to be used as keyword arguments.\n\ndata:\n\nDEFAULT_BUFFER_SIZE\n\n   An int containing the default buffer size used by the module's buffered\n   I/O classes. open() uses the file's blksize (as obtained by os.stat) if\n   possible."
    ),
    _(
        "socket.ntohl() \nntohl(integer) -> integer\n\nConvert a 32-bit integer from network to host byte order."
    ),
    _(
        "socket.ntohs() \nntohs(integer) -> integer\n\nConvert a 16-bit integer from network to host byte order."
    ),
    _(
        "socket.os() \nOS routines for NT or Posix depending on what system we're on.\n\nThis exports:\n  - all functions from posix or nt, e.g. unlink, stat, etc.\n  - os.path is either posixpath or ntpath\n  - os.name is either 'posix' or 'nt'\n  - os.curdir is a string representing the current directory (always '.')\n  - os.pardir is a string representing the parent directory (always '..')\n  - os.sep is the (or a most common) pathname separator ('/' or '\\\\')\n  - os.extsep is the extension separator (always '.')\n  - os.altsep is the alternate pathname separator (None or '/')\n  - os.pathsep is the component separator used in $PATH etc\n  - os.linesep is the line separator in text files ('\\r' or '\\n' or '\\r\\n')\n  - os.defpath is the default search path for executables\n  - os.devnull is the file path of the null device ('/dev/null', etc.)\n\nPrograms that import and use 'os' stand a better chance of being\nportable between different platforms.  Of course, they must then\nonly use functions that are defined by all platforms (e.g., unlink\nand opendir), and leave all pathname manipulation to os.path\n(e.g., split and join)."
    ),
    _(
        "socket.selectors() \nSelectors module.\n\nThis module allows high-level and efficient I/O multiplexing, built upon the\n`select` module primitives."
    ),
    _(
        "socket.setdefaulttimeout() \nsetdefaulttimeout(timeout)\n\nSet the default timeout in seconds (float) for new socket objects.\nA value of None indicates that new socket objects have no timeout.\nWhen the socket module is first imported, the default is None."
    ),
    _(
        "socket.sethostname() \nsethostname(name)\n\nSets the hostname to name."
    ),
    _(
        "socket.socket() \nsocket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None) -> socket object\n\nOpen a socket of the given type.  The family argument specifies the\naddress family; it defaults to AF_INET.  The type argument specifies\nwhether this is a stream (SOCK_STREAM, this is the default)\nor datagram (SOCK_DGRAM) socket.  The protocol argument defaults to 0,\nspecifying the default protocol.  Keyword arguments are accepted.\nThe socket is created as non-inheritable.\n\nA socket object represents one endpoint of a network connection.\n\nMethods of socket objects (keyword arguments not allowed):\n\n_accept() -- accept connection, returning new socket fd and client address\nbind(addr) -- bind the socket to a local address\nclose() -- close the socket\nconnect(addr) -- connect the socket to a remote address\nconnect_ex(addr) -- connect, return an error code instead of an exception\ndup() -- return a new socket fd duplicated from fileno()\nfileno() -- return underlying file descriptor\ngetpeername() -- return remote address [*]\ngetsockname() -- return local address\ngetsockopt(level, optname[, buflen]) -- get socket options\ngettimeout() -- return timeout or None\nlisten([n]) -- start listening for incoming connections\nrecv(buflen[, flags]) -- receive data\nrecv_into(buffer[, nbytes[, flags]]) -- receive data (into a buffer)\nrecvfrom(buflen[, flags]) -- receive data and sender's address\nrecvfrom_into(buffer[, nbytes, [, flags])\n  -- receive data and sender's address (into a buffer)\nsendall(data[, flags]) -- send all data\nsend(data[, flags]) -- send data, may not send all of it\nsendto(data[, flags], addr) -- send data to a given address\nsetblocking(0 | 1) -- set or clear the blocking I/O flag\nsetsockopt(level, optname, value[, optlen]) -- set socket options\nsettimeout(None | float) -- set or clear the timeout\nshutdown(how) -- shut down traffic in one or both directions\nif_nameindex() -- return all network interface indices and names\nif_nametoindex(name) -- return the corresponding interface index\nif_indextoname(index) -- return the corresponding interface name\n\n [*] not available on all platforms!"
    ),
    _(
        "socket.socket(family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, proto=0, fileno=None) \nA subclass of _socket.socket adding the makefile() method."
    ),
    _(
        "socket.socketpair(family=None, type=<SocketKind.SOCK_STREAM: 1>, proto=0) \nsocketpair([family[, type[, proto]]]) -> (socket object, socket object)\nCreate a pair of socket objects from the sockets returned by the platform\nsocketpair() function.\nThe arguments are the same as for socket() except the default family is AF_UNIX\nif defined on the platform; otherwise, the default is AF_INET."
    ),
    _(
        "socket.sys() \nThis module provides access to some objects used or maintained by the\ninterpreter and to functions that interact strongly with the interpreter.\n\nDynamic objects:\n\nargv -- command line arguments; argv[0] is the script pathname if known\npath -- module search path; path[0] is the script directory, else ''\nmodules -- dictionary of loaded modules\n\ndisplayhook -- called to show results in an interactive session\nexcepthook -- called to handle any uncaught exception other than SystemExit\n  To customize printing in an interactive session or to install a custom\n  top-level exception handler, assign other functions to replace these.\n\nstdin -- standard input file object; used by input()\nstdout -- standard output file object; used by print()\nstderr -- standard error object; used for error messages\n  By assigning other file objects (or objects that behave like files)\n  to these, it is possible to redirect all of the interpreter's I/O.\n\nlast_type -- type of last uncaught exception\nlast_value -- value of last uncaught exception\nlast_traceback -- traceback of last uncaught exception\n  These three are only available in an interactive session after a\n  traceback has been printed.\n\nStatic objects:\n\nbuiltin_module_names -- tuple of module names built into this interpreter\ncopyright -- copyright notice pertaining to this interpreter\nexec_prefix -- prefix used to find the machine-specific Python library\nexecutable -- absolute path of the executable binary of the Python interpreter\nfloat_info -- a struct sequence with information about the float implementation.\nfloat_repr_style -- string indicating the style of repr() output for floats\nhash_info -- a struct sequence with information about the hash algorithm.\nhexversion -- version information encoded as a single integer\nimplementation -- Python implementation information.\nint_info -- a struct sequence with information about the int implementation.\nmaxsize -- the largest supported length of containers.\nmaxunicode -- the value of the largest Unicode code point\nplatform -- platform identifier\nprefix -- prefix used to find the Python library\nthread_info -- a struct sequence with information about the thread implementation.\nversion -- the version of this interpreter as a string\nversion_info -- version information as a named tuple\n__stdin__ -- the original stdin; don't touch!\n__stdout__ -- the original stdout; don't touch!\n__stderr__ -- the original stderr; don't touch!\n__displayhook__ -- the original displayhook; don't touch!\n__excepthook__ -- the original excepthook; don't touch!\n\nFunctions:\n\ndisplayhook() -- print an object to the screen, and save it in builtins._\nexcepthook() -- print an exception and its traceback to sys.stderr\nexc_info() -- return thread-safe information about the current exception\nexit() -- exit the interpreter by raising SystemExit\ngetdlopenflags() -- returns flags to be used for dlopen() calls\ngetprofile() -- get the global profiling function\ngetrefcount() -- return the reference count for an object (plus one :-)\ngetrecursionlimit() -- return the max recursion depth for the interpreter\ngetsizeof() -- return the size of an object in bytes\ngettrace() -- get the global debug tracing function\nsetcheckinterval() -- control how often the interpreter checks for events\nsetdlopenflags() -- set the flags to be used for dlopen() calls\nsetprofile() -- set the global profiling function\nsetrecursionlimit() -- set the max recursion depth for the interpreter\nsettrace() -- set the global debug tracing function"
    ),
    _("socket.timeout() \nBase class for I/O related errors."),
    _(
        "sys.call_tracing() \ncall_tracing(func, args) -> object\n\nCall func(*args), while tracing is enabled.  The tracing state is\nsaved, and restored afterwards.  This is intended to be called from\na debugger from a checkpoint, to recursively debug some other code."
    ),
    _(
        "sys.callstats() \ncallstats() -> tuple of integers\n\nReturn a tuple of function call statistics, if CALL_PROFILE was defined\nwhen Python was built.  Otherwise, return None.\n\nWhen enabled, this function returns detailed, implementation-specific\ndetails about the number of function calls executed. The return value is\na 11-tuple where the entries in the tuple are counts of:\n0. all function calls\n1. calls to PyFunction_Type objects\n2. PyFunction calls that do not create an argument tuple\n3. PyFunction calls that do not create an argument tuple\n   and bypass PyEval_EvalCodeEx()\n4. PyMethod calls\n5. PyMethod calls on bound methods\n6. PyType calls\n7. PyCFunction calls\n8. generator calls\n9. All other calls\n10. Number of stack pops performed by call_function()"
    ),
    _(
        "sys.displayhook() \ndisplayhook(object) -> None\n\nPrint an object to sys.stdout and also save it in builtins._"
    ),
    _(
        "sys.exc_info() \nexc_info() -> (type, value, traceback)\n\nReturn information about the most recent exception caught by an except\nclause in the current stack frame or in an older stack frame."
    ),
    _(
        "sys.excepthook() \nexcepthook(exctype, value, traceback) -> None\n\nHandle an exception by displaying it with a traceback on sys.stderr."
    ),
    _(
        "sys.exit() \nexit([status])\n\nExit the interpreter by raising SystemExit(status).\nIf the status is omitted or None, it defaults to zero (i.e., success).\nIf the status is an integer, it will be used as the system exit status.\nIf it is another kind of object, it will be printed and the system\nexit status will be one (i.e., failure)."
    ),
    _(
        "sys.get_asyncgen_hooks() \nget_asyncgen_hooks()\n\nReturn a namedtuple of installed asynchronous generators hooks (firstiter, finalizer)."
    ),
    _(
        "sys.get_coroutine_wrapper() \nget_coroutine_wrapper()\n\nReturn the wrapper for coroutine objects set by sys.set_coroutine_wrapper."
    ),
    _(
        "sys.getallocatedblocks() \ngetallocatedblocks() -> integer\n\nReturn the number of memory blocks currently allocated, regardless of their\nsize."
    ),
    _(
        "sys.getcheckinterval() \ngetcheckinterval() -> current check interval; see setcheckinterval()."
    ),
    _(
        "sys.getdefaultencoding() \ngetdefaultencoding() -> string\n\nReturn the current default string encoding used by the Unicode \nimplementation."
    ),
    _(
        "sys.getdlopenflags() \ngetdlopenflags() -> int\n\nReturn the current value of the flags that are used for dlopen calls.\nThe flag constants are defined in the os module."
    ),
    _(
        "sys.getfilesystemencodeerrors() \ngetfilesystemencodeerrors() -> string\n\nReturn the error mode used to convert Unicode filenames in\noperating system filenames."
    ),
    _(
        "sys.getfilesystemencoding() \ngetfilesystemencoding() -> string\n\nReturn the encoding used to convert Unicode filenames in\noperating system filenames."
    ),
    _(
        "sys.getprofile() \ngetprofile()\n\nReturn the profiling function set with sys.setprofile.\nSee the profiler chapter in the library manual."
    ),
    _(
        "sys.getrecursionlimit() \ngetrecursionlimit()\n\nReturn the current value of the recursion limit, the maximum depth\nof the Python interpreter stack.  This limit prevents infinite\nrecursion from causing an overflow of the C stack and crashing Python."
    ),
    _(
        "sys.getrefcount() \ngetrefcount(object) -> integer\n\nReturn the reference count of object.  The count returned is generally\none higher than you might expect, because it includes the (temporary)\nreference as an argument to getrefcount()."
    ),
    _(
        "sys.getsizeof() \ngetsizeof(object, default) -> int\n\nReturn the size of object in bytes."
    ),
    _(
        "sys.getswitchinterval() \ngetswitchinterval() -> current thread switch interval; see setswitchinterval()."
    ),
    _(
        "sys.gettrace() \ngettrace()\n\nReturn the global debug tracing function set with sys.settrace.\nSee the debugger chapter in the library manual."
    ),
    _(
        "sys.intern() \nintern(string) -> string\n\n``Intern'' the given string.  This enters the string in the (global)\ntable of interned strings whose purpose is to speed up dictionary lookups.\nReturn the string itself or the previously interned string object with the\nsame value."
    ),
    _(
        "sys.is_finalizing() \nis_finalizing()\nReturn True if Python is exiting."
    ),
    _(
        "sys.set_asyncgen_hooks() \nset_asyncgen_hooks(*, firstiter=None, finalizer=None)\n\nSet a finalizer for async generators objects."
    ),
    _(
        "sys.set_coroutine_wrapper() \nset_coroutine_wrapper(wrapper)\n\nSet a wrapper for coroutine objects."
    ),
    _(
        "sys.setcheckinterval() \nsetcheckinterval(n)\n\nTell the Python interpreter to check for asynchronous events every\nn instructions.  This also affects how often thread switches occur."
    ),
    _(
        "sys.setdlopenflags() \nsetdlopenflags(n) -> None\n\nSet the flags used by the interpreter for dlopen calls, such as when the\ninterpreter loads extension modules.  Among other things, this will enable\na lazy resolving of symbols when importing a module, if called as\nsys.setdlopenflags(0).  To share symbols across extension modules, call as\nsys.setdlopenflags(os.RTLD_GLOBAL).  Symbolic names for the flag modules\ncan be found in the os module (RTLD_xxx constants, e.g. os.RTLD_LAZY)."
    ),
    _(
        "sys.setprofile() \nsetprofile(function)\n\nSet the profiling function.  It will be called on each function call\nand return.  See the profiler chapter in the library manual."
    ),
    _(
        "sys.setrecursionlimit() \nsetrecursionlimit(n)\n\nSet the maximum depth of the Python interpreter stack to n.  This\nlimit prevents infinite recursion from causing an overflow of the C\nstack and crashing Python.  The highest possible limit is platform-\ndependent."
    ),
    _(
        "sys.setswitchinterval() \nsetswitchinterval(n)\n\nSet the ideal thread switching delay inside the Python interpreter\nThe actual frequency of switching threads can be lower if the\ninterpreter executes long sequences of uninterruptible code\n(this is implementation-specific and workload-dependent).\n\nThe parameter must represent the desired switching delay in seconds\nA typical value is 0.005 (5 milliseconds)."
    ),
    _(
        "sys.settrace() \nsettrace(function)\n\nSet the global debug tracing function.  It will be called on each\nfunction call.  See the debugger chapter in the library manual."
    ),
    _(
        "time.asctime() \nasctime([tuple]) -> string\n\nConvert a time tuple to a string, e.g. 'Sat Jun 06 16:26:11 1998'.\nWhen the time tuple is not present, current time as returned by localtime()\nis used."
    ),
    _(
        "time.clock() \nclock() -> floating point number\n\nReturn the CPU time or real time since the start of the process or since\nthe first call to clock().  This has as much precision as the system\nrecords."
    ),
    _(
        "time.clock_getres() \nclock_getres(clk_id) -> floating point number\n\nReturn the resolution (precision) of the specified clock clk_id."
    ),
    _(
        "time.clock_gettime() \nclock_gettime(clk_id) -> floating point number\n\nReturn the time of the specified clock clk_id."
    ),
    _(
        "time.clock_settime() \nclock_settime(clk_id, time)\n\nSet the time of the specified clock clk_id."
    ),
    _(
        "time.ctime() \nctime(seconds) -> string\n\nConvert a time in seconds since the Epoch to a string in local time.\nThis is equivalent to asctime(localtime(seconds)). When the time tuple is\nnot present, current time as returned by localtime() is used."
    ),
    _(
        "time.get_clock_info() \nget_clock_info(name: str) -> dict\n\nGet information of the specified clock."
    ),
    _(
        "time.gmtime() \ngmtime([seconds]) -> (tm_year, tm_mon, tm_mday, tm_hour, tm_min,\n                       tm_sec, tm_wday, tm_yday, tm_isdst)\n\nConvert seconds since the Epoch to a time tuple expressing UTC (a.k.a.\nGMT).  When 'seconds' is not passed in, convert the current time instead.\n\nIf the platform supports the tm_gmtoff and tm_zone, they are available as\nattributes only."
    ),
    _(
        "time.localtime() \nlocaltime([seconds]) -> (tm_year,tm_mon,tm_mday,tm_hour,tm_min,\n                          tm_sec,tm_wday,tm_yday,tm_isdst)\n\nConvert seconds since the Epoch to a time tuple expressing local time.\nWhen 'seconds' is not passed in, convert the current time instead."
    ),
    _(
        "time.mktime() \nmktime(tuple) -> floating point number\n\nConvert a time tuple in local time to seconds since the Epoch.\nNote that mktime(gmtime(0)) will not generally return zero for most\ntime zones; instead the returned value will either be equal to that\nof the timezone or altzone attributes on the time module."
    ),
    _(
        "time.monotonic() \nmonotonic() -> float\n\nMonotonic clock, cannot go backward."
    ),
    _(
        "time.perf_counter() \nperf_counter() -> float\n\nPerformance counter for benchmarking."
    ),
    _(
        "time.process_time() \nprocess_time() -> float\n\nProcess time for profiling: sum of the kernel and user-space CPU time."
    ),
    _(
        "time.sleep() \nsleep(seconds)\n\nDelay execution for a given number of seconds.  The argument may be\na floating point number for subsecond precision."
    ),
    _(
        "time.strftime() \nstrftime(format[, tuple]) -> string\n\nConvert a time tuple to a string according to a format specification.\nSee the library reference manual for formatting codes. When the time tuple\nis not present, current time as returned by localtime() is used.\n\nCommonly used format codes:\n\n%Y  Year with century as a decimal number.\n%m  Month as a decimal number [01,12].\n%d  Day of the month as a decimal number [01,31].\n%H  Hour (24-hour clock) as a decimal number [00,23].\n%M  Minute as a decimal number [00,59].\n%S  Second as a decimal number [00,61].\n%z  Time zone offset from UTC.\n%a  Locale's abbreviated weekday name.\n%A  Locale's full weekday name.\n%b  Locale's abbreviated month name.\n%B  Locale's full month name.\n%c  Locale's appropriate date and time representation.\n%I  Hour (12-hour clock) as a decimal number [01,12].\n%p  Locale's equivalent of either AM or PM.\n\nOther codes may be available on your platform.  See documentation for\nthe C library strftime function."
    ),
    _(
        "time.strptime() \nstrptime(string, format) -> struct_time\n\nParse a string to a time tuple according to a format specification.\nSee the library reference manual for formatting codes (same as\nstrftime()).\n\nCommonly used format codes:\n\n%Y  Year with century as a decimal number.\n%m  Month as a decimal number [01,12].\n%d  Day of the month as a decimal number [01,31].\n%H  Hour (24-hour clock) as a decimal number [00,23].\n%M  Minute as a decimal number [00,59].\n%S  Second as a decimal number [00,61].\n%z  Time zone offset from UTC.\n%a  Locale's abbreviated weekday name.\n%A  Locale's full weekday name.\n%b  Locale's abbreviated month name.\n%B  Locale's full month name.\n%c  Locale's appropriate date and time representation.\n%I  Hour (12-hour clock) as a decimal number [01,12].\n%p  Locale's equivalent of either AM or PM.\n\nOther codes may be available on your platform.  See documentation for\nthe C library strftime function."
    ),
    _(
        "time.struct_time() \nThe time value as returned by gmtime(), localtime(), and strptime(), and\naccepted by asctime(), mktime() and strftime().  May be considered as a\nsequence of 9 integers.\n\nNote that several fields' values are not the same as those defined by\nthe C language standard for struct tm.  For example, the value of the\nfield tm_year is the actual year, not year - 1900.  See individual\nfields' descriptions for details."
    ),
    _(
        "time.time() \ntime() -> floating point number\n\nReturn the current time in seconds since the Epoch.\nFractions of a second may be present if the system clock provides them."
    ),
    _(
        "time.tzset() \ntzset()\n\nInitialize, or reinitialize, the local timezone to the value stored in\nos.environ['TZ']. The TZ environment variable should be specified in\nstandard Unix timezone format as documented in the tzset man page\n(eg. 'US/Eastern', 'Europe/Amsterdam'). Unknown timezones will silently\nfall back to UTC. If the TZ environment variable is not set, the local\ntimezone is set to the systems best guess of wallclock time.\nChanging the TZ environment variable without calling tzset *may* change\nthe local timezone used by methods such as localtime, but this behaviour\nshould not be relied on."
    ),
    _(
        "turtle.Canvas(master=None, cnf={}, **kw) \nCanvas widget to display graphical elements like lines or text."
    ),
    _(
        "turtle.RawTurtle(canvas=None, shape='classic', undobuffersize=1000, visible=True) \nAnimation part of the RawTurtle.\nPuts RawTurtle upon a TurtleScreen and provides tools for\nits animation."
    ),
    _(
        "turtle.RawTurtle(canvas=None, shape='classic', undobuffersize=1000, visible=True) \nAnimation part of the RawTurtle.\nPuts RawTurtle upon a TurtleScreen and provides tools for\nits animation."
    ),
    _(
        "turtle.Screen() \nReturn the singleton screen object.\nIf none exists at the moment, create a new one and return it,\nelse return the existing one."
    ),
    _(
        "turtle.ScrolledCanvas(master, width=500, height=350, canvwidth=600, canvheight=500) \nModeled after the scrolled canvas class from Grayons's Tkinter book.\n\nUsed as the default canvas, which pops up automatically when\nusing turtle graphics functions or the Turtle class."
    ),
    _(
        'turtle.Shape(type_, data=None) \nData structure modeling shapes.\n\nattribute _type is one of "polygon", "image", "compound"\nattribute _data is - depending on _type a poygon-tuple,\nan image or a list constructed using the addcomponent method.'
    ),
    _(
        "turtle.TNavigator(mode='standard') \nNavigation part of the RawTurtle.\nImplements methods for turtle movement."
    ),
    _(
        "turtle.TPen(resizemode='noresize') \nDrawing part of the RawTurtle.\nImplements drawing properties."
    ),
    _(
        "turtle.Tbuffer(bufsize=10) \nRing buffer used as undobuffer for RawTurtle objects."
    ),
    _(
        "turtle.Terminator() \nWill be raised in TurtleScreen.update, if _RUNNING becomes False.\n\nThis stops execution of a turtle graphics script.\nMain purpose: use in the Demo-Viewer turtle.Demo.py."
    ),
    _(
        "turtle.Turtle(shape='classic', undobuffersize=1000, visible=True) \nRawTurtle auto-creating (scrolled) canvas.\n\nWhen a Turtle object is created or a function derived from some\nTurtle method is called a TurtleScreen object is automatically created."
    ),
    _(
        "turtle.Turtle(shape='classic', undobuffersize=1000, visible=True) \nRawTurtle auto-creating (scrolled) canvas.\n\nWhen a Turtle object is created or a function derived from some\nTurtle method is called a TurtleScreen object is automatically created."
    ),
    _("turtle.TurtleGraphicsError() \nSome TurtleGraphics Error\n    "),
    _(
        "turtle.TurtleScreen(cv, mode='standard', colormode=1.0, delay=10) \nProvides screen oriented methods like setbg etc.\n\nOnly relies upon the methods of TurtleScreenBase and NOT\nupon components of the underlying graphics toolkit -\nwhich is Tkinter in this case."
    ),
    _(
        "turtle.TurtleScreenBase(cv) \nProvide the basic graphics functionality.\nInterface between Tkinter and turtle.py.\n\nTo port turtle.py to some different graphics toolkit\na corresponding TurtleScreenBase class has to be implemented."
    ),
    _(
        "turtle.Vec2D(x, y) \nA 2 dimensional vector class, used as a helper class\nfor implementing turtle graphics.\nMay be useful for turtle graphics programs also.\nDerived from tuple, so a vector is a tuple!\n\nProvides (for a, b vectors, k number):\n   a+b vector addition\n   a-b vector subtraction\n   a*b inner product\n   k*a and a*k multiplication with scalar\n   |a| absolute value of a\n   a.rotate(angle) rotation"
    ),
    _(
        'turtle.addshape(name, shape=None) \nAdds a turtle shape to TurtleScreen\'s shapelist.\n\nArguments:\n(1) name is the name of a gif-file and shape is None.\n    Installs the corresponding image shape.\n    !! Image-shapes DO NOT rotate when turning the turtle,\n    !! so they do not display the heading of the turtle!\n(2) name is an arbitrary string and shape is a tuple\n    of pairs of coordinates. Installs the corresponding\n    polygon shape\n(3) name is an arbitrary string and shape is a\n    (compound) Shape object. Installs the corresponding\n    compound shape.\nTo use a shape, you have to issue the command shape(shapename).\n\ncall: register_shape("turtle.gif")\n--or: register_shape("tri", ((0,0), (10,10), (-10,10)))\n\nExample:\n>>> register_shape("triangle", ((5,-3),(0,5),(-5,-3)))'
    ),
    _(
        "turtle.back(distance) \nMove the turtle backward by distance.\n\nAliases: back | backward | bk\n\nArgument:\ndistance -- a number\n\nMove the turtle backward by distance ,opposite to the direction the\nturtle is headed. Do not change the turtle's heading.\n\nExample:\n>>> position()\n(0.00, 0.00)\n>>> backward(30)\n>>> position()\n(-30.00, 0.00)"
    ),
    _(
        "turtle.backward(distance) \nMove the turtle backward by distance.\n\nAliases: back | backward | bk\n\nArgument:\ndistance -- a number\n\nMove the turtle backward by distance ,opposite to the direction the\nturtle is headed. Do not change the turtle's heading.\n\nExample:\n>>> position()\n(0.00, 0.00)\n>>> backward(30)\n>>> position()\n(-30.00, 0.00)"
    ),
    _(
        'turtle.begin_fill() \nCalled just before drawing a shape to be filled.\n\nNo argument.\n\nExample:\n>>> color("black", "red")\n>>> begin_fill()\n>>> circle(60)\n>>> end_fill()'
    ),
    _(
        "turtle.begin_poly() \nStart recording the vertices of a polygon.\n\nNo argument.\n\nStart recording the vertices of a polygon. Current turtle position\nis first point of polygon.\n\nExample:\n>>> begin_poly()"
    ),
    _(
        "turtle.bgcolor(*args) \nSet or return backgroundcolor of the TurtleScreen.\n\nArguments (if given): a color string or three numbers\nin the range 0..colormode or a 3-tuple of such numbers.\n\nExample:\n>>> bgcolor(\"orange\")\n>>> bgcolor()\n'orange'\n>>> bgcolor(0.5,0,0.5)\n>>> bgcolor()\n'#800080'"
    ),
    _(
        'turtle.bgpic(picname=None) \nSet background image or return name of current backgroundimage.\n\nOptional argument:\npicname -- a string, name of a gif-file or "nopic".\n\nIf picname is a filename, set the corresponding image as background.\nIf picname is "nopic", delete backgroundimage, if present.\nIf picname is None, return the filename of the current backgroundimage.\n\nExample:\n>>> bgpic()\n\'nopic\'\n>>> bgpic("landscape.gif")\n>>> bgpic()\n\'landscape.gif\''
    ),
    _(
        "turtle.bk(distance) \nMove the turtle backward by distance.\n\nAliases: back | backward | bk\n\nArgument:\ndistance -- a number\n\nMove the turtle backward by distance ,opposite to the direction the\nturtle is headed. Do not change the turtle's heading.\n\nExample:\n>>> position()\n(0.00, 0.00)\n>>> backward(30)\n>>> position()\n(-30.00, 0.00)"
    ),
    _("turtle.bye() \nShut the turtlegraphics window.\n\nExample:\n>>> bye()"),
    _(
        "turtle.circle(radius, extent=None, steps=None) \nDraw a circle with given radius.\n\nArguments:\nradius -- a number\nextent (optional) -- a number\nsteps (optional) -- an integer\n\nDraw a circle with given radius. The center is radius units left\nof the turtle; extent - an angle - determines which part of the\ncircle is drawn. If extent is not given, draw the entire circle.\nIf extent is not a full circle, one endpoint of the arc is the\ncurrent pen position. Draw the arc in counterclockwise direction\nif radius is positive, otherwise in clockwise direction. Finally\nthe direction of the turtle is changed by the amount of extent.\n\nAs the circle is approximated by an inscribed regular polygon,\nsteps determines the number of steps to use. If not given,\nit will be calculated automatically. Maybe used to draw regular\npolygons.\n\ncall: circle(radius)                  # full circle\n--or: circle(radius, extent)          # arc\n--or: circle(radius, extent, steps)\n--or: circle(radius, steps=6)         # 6-sided polygon\n\nExample:\n>>> circle(50)\n>>> circle(120, 180)  # semicircle"
    ),
    _(
        "turtle.clear() \nDelete the turtle's drawings from the screen. Do not move \n\nNo arguments.\n\nDelete the turtle's drawings from the screen. Do not move \nState and position of the turtle as well as drawings of other\nturtles are not affected.\n\nExamples:\n>>> clear()"
    ),
    _(
        "turtle.clearscreen() \nDelete all drawings and all turtles from the TurtleScreen.\n\nNo argument.\n\nReset empty TurtleScreen to its initial state: white background,\nno backgroundimage, no eventbindings and tracing on.\n\nExample:\n>>> clear()\n\nNote: this method is not available as function."
    ),
    _(
        'turtle.clearstamp(stampid) \nDelete stamp with given stampid\n\nArgument:\nstampid - an integer, must be return value of previous stamp() call.\n\nExample:\n>>> color("blue")\n>>> astamp = stamp()\n>>> fd(50)\n>>> clearstamp(astamp)'
    ),
    _(
        "turtle.clearstamps(n=None) \nDelete all or first/last n of turtle's stamps.\n\nOptional argument:\nn -- an integer\n\nIf n is None, delete all of pen's stamps,\nelse if n > 0 delete first n stamps\nelse if n < 0 delete last n stamps.\n\nExample:\n>>> for i in range(8):\n...     stamp(); fd(30)\n...\n>>> clearstamps(2)\n>>> clearstamps(-2)\n>>> clearstamps()"
    ),
    _(
        "turtle.clone() \nCreate and return a clone of the \n\nNo argument.\n\nCreate and return a clone of the turtle with same position, heading\nand turtle properties.\n\nExample (for a Turtle instance named mick):\nmick = Turtle()\njoe = mick.clone()"
    ),
    _(
        "turtle.color(*args) \nReturn or set the pencolor and fillcolor.\n\nArguments:\nSeveral input formats are allowed.\nThey use 0, 1, 2, or 3 arguments as follows:\n\ncolor()\n    Return the current pencolor and the current fillcolor\n    as a pair of color specification strings as are returned\n    by pencolor and fillcolor.\ncolor(colorstring), color((r,g,b)), color(r,g,b)\n    inputs as in pencolor, set both, fillcolor and pencolor,\n    to the given value.\ncolor(colorstring1, colorstring2),\ncolor((r1,g1,b1), (r2,g2,b2))\n    equivalent to pencolor(colorstring1) and fillcolor(colorstring2)\n    and analogously, if the other input format is used.\n\nIf turtleshape is a polygon, outline and interior of that polygon\nis drawn with the newly set colors.\nFor mor info see: pencolor, fillcolor\n\nExample:\n>>> color('red', 'green')\n>>> color()\n('red', 'green')\n>>> colormode(255)\n>>> color((40, 80, 120), (160, 200, 240))\n>>> color()\n('#285078', '#a0c8f0')"
    ),
    _(
        "turtle.colormode(cmode=None) \nReturn the colormode or set it to 1.0 or 255.\n\nOptional argument:\ncmode -- one of the values 1.0 or 255\n\nr, g, b values of colortriples have to be in range 0..cmode.\n\nExample:\n>>> colormode()\n1.0\n>>> colormode(255)\n>>> pencolor(240,160,80)"
    ),
    _(
        "turtle.config_dict(filename) \nConvert content of config-file into dictionary."
    ),
    _(
        "turtle.deepcopy(x, memo=None, _nil=[]) \nDeep copy operation on arbitrary Python objects.\n\nSee the module's __doc__ string for more info."
    ),
    _(
        "turtle.degrees(fullcircle=360.0) \nSet angle measurement units to degrees.\n\nOptional argument:\nfullcircle -  a number\n\nSet angle measurement units, i. e. set number\nof 'degrees' for a full circle. Dafault value is\n360 degrees.\n\nExample:\n>>> left(90)\n>>> heading()\n90\n\nChange angle measurement unit to grad (also known as gon,\ngrade, or gradian and equals 1/100-th of the right angle.)\n>>> degrees(400.0)\n>>> heading()\n100"
    ),
    _(
        "turtle.delay(delay=None) \nReturn or set the drawing delay in milliseconds.\n\nOptional argument:\ndelay -- positive integer\n\nExample:\n>>> delay(15)\n>>> delay()\n15"
    ),
    _(
        "turtle.distance(x, y=None) \nReturn the distance from the turtle to (x,y) in turtle step units.\n\nArguments:\nx -- a number   or  a pair/vector of numbers   or   a turtle instance\ny -- a number       None                            None\n\ncall: distance(x, y)         # two coordinates\n--or: distance((x, y))       # a pair (tuple) of coordinates\n--or: distance(vec)          # e.g. as returned by pos()\n--or: distance(mypen)        # where mypen is another turtle\n\nExample:\n>>> pos()\n(0.00, 0.00)\n>>> distance(30,40)\n50.0\n>>> pen = Turtle()\n>>> pen.forward(77)\n>>> distance(pen)\n77.0"
    ),
    _(
        'turtle.dot(size=None, *color) \nDraw a dot with diameter size, using color.\n\nOptional arguments:\nsize -- an integer >= 1 (if given)\ncolor -- a colorstring or a numeric color tuple\n\nDraw a circular dot with diameter size, using color.\nIf size is not given, the maximum of pensize+4 and 2*pensize is used.\n\nExample:\n>>> dot()\n>>> fd(50); dot(20, "blue"); fd(50)'
    ),
    _(
        "turtle.down() \nPull the pen down -- drawing when moving.\n\nAliases: pendown | pd | down\n\nNo argument.\n\nExample:\n>>> pendown()"
    ),
    _(
        'turtle.end_fill() \nFill the shape drawn after the call begin_fill().\n\nNo argument.\n\nExample:\n>>> color("black", "red")\n>>> begin_fill()\n>>> circle(60)\n>>> end_fill()'
    ),
    _(
        "turtle.end_poly() \nStop recording the vertices of a polygon.\n\nNo argument.\n\nStop recording the vertices of a polygon. Current turtle position is\nlast point of polygon. This will be connected with the first point.\n\nExample:\n>>> end_poly()"
    ),
    _(
        'turtle.exitonclick() \nGo into mainloop until the mouse is clicked.\n\nNo arguments.\n\nBind bye() method to mouseclick on TurtleScreen.\nIf "using_IDLE" - value in configuration dictionary is False\n(default value), enter mainloop.\nIf IDLE with -n switch (no subprocess) is used, this value should be\nset to True in turtle.cfg. In this case IDLE\'s mainloop\nis active also for the client script.\n\nThis is a method of the Screen-class and not available for\nTurtleScreen instances.\n\nExample:\n>>> exitonclick()'
    ),
    _(
        "turtle.fd(distance) \nMove the turtle forward by the specified distance.\n\nAliases: forward | fd\n\nArgument:\ndistance -- a number (integer or float)\n\nMove the turtle forward by the specified distance, in the direction\nthe turtle is headed.\n\nExample:\n>>> position()\n(0.00, 0.00)\n>>> forward(25)\n>>> position()\n(25.00,0.00)\n>>> forward(-75)\n>>> position()\n(-50.00,0.00)"
    ),
    _(
        'turtle.fillcolor(*args) \nReturn or set the fillcolor.\n\nArguments:\nFour input formats are allowed:\n  - fillcolor()\n    Return the current fillcolor as color specification string,\n    possibly in hex-number format (see example).\n    May be used as input to another color/pencolor/fillcolor call.\n  - fillcolor(colorstring)\n    s is a Tk color specification string, such as "red" or "yellow"\n  - fillcolor((r, g, b))\n    *a tuple* of r, g, and b, which represent, an RGB color,\n    and each of r, g, and b are in the range 0..colormode,\n    where colormode is either 1.0 or 255\n  - fillcolor(r, g, b)\n    r, g, and b represent an RGB color, and each of r, g, and b\n    are in the range 0..colormode\n\nIf turtleshape is a polygon, the interior of that polygon is drawn\nwith the newly set fillcolor.\n\nExample:\n>>> fillcolor(\'violet\')\n>>> col = pencolor()\n>>> fillcolor(col)\n>>> fillcolor(0, .5, 0)'
    ),
    _(
        "turtle.filling() \nReturn fillstate (True if filling, False else).\n\nNo argument.\n\nExample:\n>>> begin_fill()\n>>> if filling():\n...     pensize(5)\n... else:\n...     pensize(3)"
    ),
    _(
        "turtle.forward(distance) \nMove the turtle forward by the specified distance.\n\nAliases: forward | fd\n\nArgument:\ndistance -- a number (integer or float)\n\nMove the turtle forward by the specified distance, in the direction\nthe turtle is headed.\n\nExample:\n>>> position()\n(0.00, 0.00)\n>>> forward(25)\n>>> position()\n(25.00,0.00)\n>>> forward(-75)\n>>> position()\n(-50.00,0.00)"
    ),
    _(
        'turtle.get_poly() \nReturn the lastly recorded polygon.\n\nNo argument.\n\nExample:\n>>> p = get_poly()\n>>> register_shape("myFavouriteShape", p)'
    ),
    _(
        'turtle.get_shapepoly() \nReturn the current shape polygon as tuple of coordinate pairs.\n\nNo argument.\n\nExamples:\n>>> shape("square")\n>>> shapetransform(4, -1, 0, 2)\n>>> get_shapepoly()\n((50, -20), (30, 20), (-50, 20), (-30, -20))'
    ),
    _(
        "turtle.getcanvas() \nReturn the Canvas of this TurtleScreen.\n\nNo argument.\n\nExample:\n>>> cv = getcanvas()\n>>> cv\n<turtle.ScrolledCanvas instance at 0x010742D8>"
    ),
    _(
        'turtle.getmethparlist(ob) \nGet strings describing the arguments for the given object\n\nReturns a pair of strings representing function parameter lists\nincluding parenthesis.  The first string is suitable for use in\nfunction definition and the second is suitable for use in function\ncall.  The "self" parameter is not included.'
    ),
    _(
        "turtle.getpen() \nReturn the Turtleobject itself.\n\nNo argument.\n\nOnly reasonable use: as a function to return the 'anonymous turtle':\n\nExample:\n>>> pet = getturtle()\n>>> pet.fd(50)\n>>> pet\n<Turtle object at 0x0187D810>\n>>> turtles()\n[<Turtle object at 0x0187D810>]"
    ),
    _(
        'turtle.getscreen() \nReturn the TurtleScreen object, the turtle is drawing  on.\n\nNo argument.\n\nReturn the TurtleScreen object, the turtle is drawing  on.\nSo TurtleScreen-methods can be called for that object.\n\nExample:\n>>> ts = getscreen()\n>>> ts\n<TurtleScreen object at 0x0106B770>\n>>> ts.bgcolor("pink")'
    ),
    _(
        "turtle.getshapes() \nReturn a list of names of all currently available turtle shapes.\n\nNo argument.\n\nExample:\n>>> getshapes()\n['arrow', 'blank', 'circle', ... , 'turtle']"
    ),
    _(
        "turtle.getturtle() \nReturn the Turtleobject itself.\n\nNo argument.\n\nOnly reasonable use: as a function to return the 'anonymous turtle':\n\nExample:\n>>> pet = getturtle()\n>>> pet.fd(50)\n>>> pet\n<Turtle object at 0x0187D810>\n>>> turtles()\n[<Turtle object at 0x0187D810>]"
    ),
    _(
        "turtle.goto(x, y=None) \nMove turtle to an absolute position.\n\nAliases: setpos | setposition | goto:\n\nArguments:\nx -- a number      or     a pair/vector of numbers\ny -- a number             None\n\ncall: goto(x, y)         # two coordinates\n--or: goto((x, y))       # a pair (tuple) of coordinates\n--or: goto(vec)          # e.g. as returned by pos()\n\nMove turtle to an absolute position. If the pen is down,\na line will be drawn. The turtle's orientation does not change.\n\nExample:\n>>> tp = pos()\n>>> tp\n(0.00, 0.00)\n>>> setpos(60,30)\n>>> pos()\n(60.00,30.00)\n>>> setpos((20,80))\n>>> pos()\n(20.00,80.00)\n>>> setpos(tp)\n>>> pos()\n(0.00,0.00)"
    ),
    _(
        "turtle.heading() \nReturn the turtle's current heading.\n\nNo arguments.\n\nExample:\n>>> left(67)\n>>> heading()\n67.0"
    ),
    _(
        "turtle.hideturtle() \nMakes the turtle invisible.\n\nAliases: hideturtle | ht\n\nNo argument.\n\nIt's a good idea to do this while you're in the\nmiddle of a complicated drawing, because hiding\nthe turtle speeds up the drawing observably.\n\nExample:\n>>> hideturtle()"
    ),
    _(
        "turtle.home() \nMove turtle to the origin - coordinates (0,0).\n\nNo arguments.\n\nMove turtle to the origin - coordinates (0,0) and set its\nheading to its start-orientation (which depends on mode).\n\nExample:\n>>> home()"
    ),
    _(
        "turtle.ht() \nMakes the turtle invisible.\n\nAliases: hideturtle | ht\n\nNo argument.\n\nIt's a good idea to do this while you're in the\nmiddle of a complicated drawing, because hiding\nthe turtle speeds up the drawing observably.\n\nExample:\n>>> hideturtle()"
    ),
    _(
        "turtle.inspect() \nGet useful information from live Python objects.\n\nThis module encapsulates the interface provided by the internal special\nattributes (co_*, im_*, tb_*, etc.) in a friendlier fashion.\nIt also provides some help for examining source code and class layout.\n\nHere are some of the useful functions provided by this module:\n\n    ismodule(), isclass(), ismethod(), isfunction(), isgeneratorfunction(),\n        isgenerator(), istraceback(), isframe(), iscode(), isbuiltin(),\n        isroutine() - check object types\n    getmembers() - get members of an object that satisfy a given condition\n\n    getfile(), getsourcefile(), getsource() - find an object's source code\n    getdoc(), getcomments() - get documentation on an object\n    getmodule() - determine the module that an object came from\n    getclasstree() - arrange classes so as to represent their hierarchy\n\n    getargvalues(), getcallargs() - get info about function arguments\n    getfullargspec() - same, with support for Python 3 features\n    formatargspec(), formatargvalues() - format an argument spec\n    getouterframes(), getinnerframes() - get info about frames\n    currentframe() - get the current stack frame\n    stack(), trace() - get info about frames on the stack or in a traceback\n\n    signature() - get a Signature object for the callable"
    ),
    _(
        "turtle.isdown() \nReturn True if pen is down, False if it's up.\n\nNo argument.\n\nExample:\n>>> penup()\n>>> isdown()\nFalse\n>>> pendown()\n>>> isdown()\nTrue"
    ),
    _("turtle.isfile(path) \nTest whether a path is a regular file"),
    _(
        "turtle.isvisible() \nReturn True if the Turtle is shown, False if it's hidden.\n\nNo argument.\n\nExample:\n>>> hideturtle()\n>>> print isvisible():\nFalse"
    ),
    _(
        "turtle.join(a, *p) \nJoin two or more pathname components, inserting '/' as needed.\nIf any component is an absolute path, all previous path components\nwill be discarded.  An empty last part will result in a path that\nends with a separator."
    ),
    _(
        "turtle.left(angle) \nTurn turtle left by angle units.\n\nAliases: left | lt\n\nArgument:\nangle -- a number (integer or float)\n\nTurn turtle left by angle units. (Units are by default degrees,\nbut can be set via the degrees() and radians() functions.)\nAngle orientation depends on mode. (See this.)\n\nExample:\n>>> heading()\n22.0\n>>> left(45)\n>>> heading()\n67.0"
    ),
    _(
        "turtle.listen(xdummy=None, ydummy=None) \nSet focus on TurtleScreen (in order to collect key-events)\n\nNo arguments.\nDummy arguments are provided in order\nto be able to pass listen to the onclick method.\n\nExample:\n>>> listen()"
    ),
    _(
        "turtle.lt(angle) \nTurn turtle left by angle units.\n\nAliases: left | lt\n\nArgument:\nangle -- a number (integer or float)\n\nTurn turtle left by angle units. (Units are by default degrees,\nbut can be set via the degrees() and radians() functions.)\nAngle orientation depends on mode. (See this.)\n\nExample:\n>>> heading()\n22.0\n>>> left(45)\n>>> heading()\n67.0"
    ),
    _(
        "turtle.mainloop() \nStarts event loop - calling Tkinter's mainloop function.\n\nNo argument.\n\nMust be last statement in a turtle graphics program.\nMust NOT be used if a script is run from within IDLE in -n mode\n(No subprocess) - for interactive use of turtle graphics.\n\nExample:\n>>> mainloop()"
    ),
    _(
        "turtle.mainloop() \nStarts event loop - calling Tkinter's mainloop function.\n\nNo argument.\n\nMust be last statement in a turtle graphics program.\nMust NOT be used if a script is run from within IDLE in -n mode\n(No subprocess) - for interactive use of turtle graphics.\n\nExample:\n>>> mainloop()"
    ),
    _(
        "turtle.math() \nThis module is always available.  It provides access to the\nmathematical functions defined by the C standard."
    ),
    _(
        "turtle.mode(mode=None) \nSet turtle-mode ('standard', 'logo' or 'world') and perform reset.\n\nOptional argument:\nmode -- one of the strings 'standard', 'logo' or 'world'\n\nMode 'standard' is compatible with turtle.py.\nMode 'logo' is compatible with most Logo-Turtle-Graphics.\nMode 'world' uses userdefined 'worldcoordinates'. *Attention*: in\nthis mode angles appear distorted if x/y unit-ratio doesn't equal 1.\nIf mode is not given, return the current mode.\n\n     Mode      Initial turtle heading     positive angles\n ------------|-------------------------|-------------------\n  'standard'    to the right (east)       counterclockwise\n    'logo'        upward    (north)         clockwise\n\nExamples:\n>>> mode('logo')   # resets turtle heading to north\n>>> mode()\n'logo'"
    ),
    _(
        'turtle.numinput(title, prompt, default=None, minval=None, maxval=None) \nPop up a dialog window for input of a number.\n\nArguments: title is the title of the dialog window,\nprompt is a text mostly describing what numerical information to input.\ndefault: default value\nminval: minimum value for imput\nmaxval: maximum value for input\n\nThe number input must be in the range minval .. maxval if these are\ngiven. If not, a hint is issued and the dialog remains open for\ncorrection. Return the number input.\nIf the dialog is canceled,  return None.\n\nExample:\n>>> numinput("Poker", "Your stakes:", 1000, minval=10, maxval=10000)'
    ),
    _(
        "turtle.onclick(fun, btn=1, add=None) \nBind fun to mouse-click event on this turtle on canvas.\n\nArguments:\nfun --  a function with two arguments, to which will be assigned\n        the coordinates of the clicked point on the canvas.\nnum --  number of the mouse-button defaults to 1 (left mouse button).\nadd --  True or False. If True, new binding will be added, otherwise\n        it will replace a former binding.\n\nExample for the anonymous turtle, i. e. the procedural way:\n\n>>> def turn(x, y):\n...     left(360)\n...\n>>> onclick(turn)  # Now clicking into the turtle will turn it.\n>>> onclick(None)  # event-binding will be removed"
    ),
    _(
        "turtle.ondrag(fun, btn=1, add=None) \nBind fun to mouse-move event on this turtle on canvas.\n\nArguments:\nfun -- a function with two arguments, to which will be assigned\n       the coordinates of the clicked point on the canvas.\nnum -- number of the mouse-button defaults to 1 (left mouse button).\n\nEvery sequence of mouse-move-events on a turtle is preceded by a\nmouse-click event on that \n\nExample:\n>>> ondrag(goto)\n\nSubsequently clicking and dragging a Turtle will move it\nacross the screen thereby producing handdrawings (if pen is\ndown)."
    ),
    _(
        'turtle.onkey(fun, key) \nBind fun to key-release event of key.\n\nArguments:\nfun -- a function with no arguments\nkey -- a string: key (e.g. "a") or key-symbol (e.g. "space")\n\nIn order to be able to register key-events, TurtleScreen\nmust have focus. (See method listen.)\n\nExample:\n\n>>> def f():\n...     fd(50)\n...     lt(60)\n...\n>>> onkey(f, "Up")\n>>> listen()\n\nSubsequently the turtle can be moved by repeatedly pressing\nthe up-arrow key, consequently drawing a hexagon'
    ),
    _(
        'turtle.onkeypress(fun, key=None) \nBind fun to key-press event of key if key is given,\nor to any key-press-event if no key is given.\n\nArguments:\nfun -- a function with no arguments\nkey -- a string: key (e.g. "a") or key-symbol (e.g. "space")\n\nIn order to be able to register key-events, TurtleScreen\nmust have focus. (See method listen.)\n\nExample (for a TurtleScreen instance named screen\nand a Turtle instance named turtle):\n\n>>> def f():\n...     fd(50)\n...     lt(60)\n...\n>>> onkeypress(f, "Up")\n>>> listen()\n\nSubsequently the turtle can be moved by repeatedly pressing\nthe up-arrow key, or by keeping pressed the up-arrow key.\nconsequently drawing a hexagon.'
    ),
    _(
        'turtle.onkeyrelease(fun, key) \nBind fun to key-release event of key.\n\nArguments:\nfun -- a function with no arguments\nkey -- a string: key (e.g. "a") or key-symbol (e.g. "space")\n\nIn order to be able to register key-events, TurtleScreen\nmust have focus. (See method listen.)\n\nExample:\n\n>>> def f():\n...     fd(50)\n...     lt(60)\n...\n>>> onkey(f, "Up")\n>>> listen()\n\nSubsequently the turtle can be moved by repeatedly pressing\nthe up-arrow key, consequently drawing a hexagon'
    ),
    _(
        'turtle.onrelease(fun, btn=1, add=None) \nBind fun to mouse-button-release event on this turtle on canvas.\n\nArguments:\nfun -- a function with two arguments, to which will be assigned\n        the coordinates of the clicked point on the canvas.\nnum --  number of the mouse-button defaults to 1 (left mouse button).\n\nExample (for a MyTurtle instance named joe):\n>>> class MyTurtle(Turtle):\n...     def glow(self,x,y):\n...             self.fillcolor("red")\n...     def unglow(self,x,y):\n...             self.fillcolor("")\n...\n>>> joe = MyTurtle()\n>>> joe.onclick(joe.glow)\n>>> joe.onrelease(joe.unglow)\n\nClicking on joe turns fillcolor red, unclicking turns it to\ntransparent.'
    ),
    _(
        "turtle.onscreenclick(fun, btn=1, add=None) \nBind fun to mouse-click event on canvas.\n\nArguments:\nfun -- a function with two arguments, the coordinates of the\n       clicked point on the canvas.\nnum -- the number of the mouse-button, defaults to 1\n\nExample (for a TurtleScreen instance named screen)\n\n>>> onclick(goto)\n>>> # Subsequently clicking into the TurtleScreen will\n>>> # make the turtle move to the clicked point.\n>>> onclick(None)"
    ),
    _(
        "turtle.ontimer(fun, t=0) \nInstall a timer, which calls fun after t milliseconds.\n\nArguments:\nfun -- a function with no arguments.\nt -- a number >= 0\n\nExample:\n\n>>> running = True\n>>> def f():\n...     if running:\n...             fd(50)\n...             lt(60)\n...             ontimer(f, 250)\n...\n>>> f()   # makes the turtle marching around\n>>> running = False"
    ),
    _(
        "turtle.pd() \nPull the pen down -- drawing when moving.\n\nAliases: pendown | pd | down\n\nNo argument.\n\nExample:\n>>> pendown()"
    ),
    _(
        "turtle.pen(pen=None, **pendict) \nReturn or set the pen's attributes.\n\nArguments:\n    pen -- a dictionary with some or all of the below listed keys.\n    **pendict -- one or more keyword-arguments with the below\n                 listed keys as keywords.\n\nReturn or set the pen's attributes in a 'pen-dictionary'\nwith the following key/value pairs:\n   \"shown\"      :   True/False\n   \"pendown\"    :   True/False\n   \"pencolor\"   :   color-string or color-tuple\n   \"fillcolor\"  :   color-string or color-tuple\n   \"pensize\"    :   positive number\n   \"speed\"      :   number in range 0..10\n   \"resizemode\" :   \"auto\" or \"user\" or \"noresize\"\n   \"stretchfactor\": (positive number, positive number)\n   \"shearfactor\":   number\n   \"outline\"    :   positive number\n   \"tilt\"       :   number\n\nThis dictionary can be used as argument for a subsequent\npen()-call to restore the former pen-state. Moreover one\nor more of these attributes can be provided as keyword-arguments.\nThis can be used to set several pen attributes in one statement.\n\n\nExamples:\n>>> pen(fillcolor=\"black\", pencolor=\"red\", pensize=10)\n>>> pen()\n{'pensize': 10, 'shown': True, 'resizemode': 'auto', 'outline': 1,\n'pencolor': 'red', 'pendown': True, 'fillcolor': 'black',\n'stretchfactor': (1,1), 'speed': 3, 'shearfactor': 0.0}\n>>> penstate=pen()\n>>> color(\"yellow\",\"\")\n>>> penup()\n>>> pen()\n{'pensize': 10, 'shown': True, 'resizemode': 'auto', 'outline': 1,\n'pencolor': 'yellow', 'pendown': False, 'fillcolor': '',\n'stretchfactor': (1,1), 'speed': 3, 'shearfactor': 0.0}\n>>> p.pen(penstate, fillcolor=\"green\")\n>>> p.pen()\n{'pensize': 10, 'shown': True, 'resizemode': 'auto', 'outline': 1,\n'pencolor': 'red', 'pendown': True, 'fillcolor': 'green',\n'stretchfactor': (1,1), 'speed': 3, 'shearfactor': 0.0}"
    ),
    _(
        "turtle.pencolor(*args) \nReturn or set the pencolor.\n\nArguments:\nFour input formats are allowed:\n  - pencolor()\n    Return the current pencolor as color specification string,\n    possibly in hex-number format (see example).\n    May be used as input to another color/pencolor/fillcolor call.\n  - pencolor(colorstring)\n    s is a Tk color specification string, such as \"red\" or \"yellow\"\n  - pencolor((r, g, b))\n    *a tuple* of r, g, and b, which represent, an RGB color,\n    and each of r, g, and b are in the range 0..colormode,\n    where colormode is either 1.0 or 255\n  - pencolor(r, g, b)\n    r, g, and b represent an RGB color, and each of r, g, and b\n    are in the range 0..colormode\n\nIf turtleshape is a polygon, the outline of that polygon is drawn\nwith the newly set pencolor.\n\nExample:\n>>> pencolor('brown')\n>>> tup = (0.2, 0.8, 0.55)\n>>> pencolor(tup)\n>>> pencolor()\n'#33cc8c'"
    ),
    _(
        "turtle.pendown() \nPull the pen down -- drawing when moving.\n\nAliases: pendown | pd | down\n\nNo argument.\n\nExample:\n>>> pendown()"
    ),
    _(
        'turtle.pensize(width=None) \nSet or return the line thickness.\n\nAliases:  pensize | width\n\nArgument:\nwidth -- positive number\n\nSet the line thickness to width or return it. If resizemode is set\nto "auto" and turtleshape is a polygon, that polygon is drawn with\nthe same line thickness. If no argument is given, current pensize\nis returned.\n\nExample:\n>>> pensize()\n1\n>>> pensize(10)   # from here on lines of width 10 are drawn'
    ),
    _(
        "turtle.penup() \nPull the pen up -- no drawing when moving.\n\nAliases: penup | pu | up\n\nNo argument\n\nExample:\n>>> penup()"
    ),
    _(
        "turtle.pos() \nReturn the turtle's current location (x,y), as a Vec2D-vector.\n\nAliases: pos | position\n\nNo arguments.\n\nExample:\n>>> pos()\n(0.00, 240.00)"
    ),
    _(
        "turtle.position() \nReturn the turtle's current location (x,y), as a Vec2D-vector.\n\nAliases: pos | position\n\nNo arguments.\n\nExample:\n>>> pos()\n(0.00, 240.00)"
    ),
    _(
        "turtle.pu() \nPull the pen up -- no drawing when moving.\n\nAliases: penup | pu | up\n\nNo argument\n\nExample:\n>>> penup()"
    ),
    _(
        "turtle.radians() \nSet the angle measurement units to radians.\n\nNo arguments.\n\nExample:\n>>> heading()\n90\n>>> radians()\n>>> heading()\n1.5707963267948966"
    ),
    _(
        "turtle.read_docstrings(lang) \nRead in docstrings from lang-specific docstring dictionary.\n\nTransfer docstrings, translated to lang, from a dictionary-file\nto the methods of classes Screen and Turtle and - in revised form -\nto the corresponding functions."
    ),
    _(
        "turtle.readconfig(cfgdict) \nRead config-files, change configuration-dict accordingly.\n\nIf there is a turtle.cfg file in the current working directory,\nread it from there. If this contains an importconfig-value,\nsay 'myway', construct filename turtle_mayway.cfg else use\nturtle.cfg and read it from the import-directory, where\nturtle.py is located.\nUpdate configuration dictionary first according to config-file,\nin the import directory, then according to config-file in the\ncurrent working directory.\nIf no config-file is found, the default configuration is used."
    ),
    _(
        'turtle.register_shape(name, shape=None) \nAdds a turtle shape to TurtleScreen\'s shapelist.\n\nArguments:\n(1) name is the name of a gif-file and shape is None.\n    Installs the corresponding image shape.\n    !! Image-shapes DO NOT rotate when turning the turtle,\n    !! so they do not display the heading of the turtle!\n(2) name is an arbitrary string and shape is a tuple\n    of pairs of coordinates. Installs the corresponding\n    polygon shape\n(3) name is an arbitrary string and shape is a\n    (compound) Shape object. Installs the corresponding\n    compound shape.\nTo use a shape, you have to issue the command shape(shapename).\n\ncall: register_shape("turtle.gif")\n--or: register_shape("tri", ((0,0), (10,10), (-10,10)))\n\nExample:\n>>> register_shape("triangle", ((5,-3),(0,5),(-5,-3)))'
    ),
    _(
        "turtle.reset() \nDelete the turtle's drawings and restore its default values.\n\nNo argument.\n\nDelete the turtle's drawings from the screen, re-center the turtle\nand set variables to the default values.\n\nExample:\n>>> position()\n(0.00,-22.00)\n>>> heading()\n100.0\n>>> reset()\n>>> position()\n(0.00,0.00)\n>>> heading()\n0.0"
    ),
    _(
        "turtle.resetscreen() \nReset all Turtles on the Screen to their initial state.\n\nNo argument.\n\nExample:\n>>> reset()"
    ),
    _(
        'turtle.resizemode(rmode=None) \nSet resizemode to one of the values: "auto", "user", "noresize".\n\n(Optional) Argument:\nrmode -- one of the strings "auto", "user", "noresize"\n\nDifferent resizemodes have the following effects:\n  - "auto" adapts the appearance of the turtle\n           corresponding to the value of pensize.\n  - "user" adapts the appearance of the turtle according to the\n           values of stretchfactor and outlinewidth (outline),\n           which are set by shapesize()\n  - "noresize" no adaption of the turtle\'s appearance takes place.\nIf no argument is given, return current resizemode.\nresizemode("user") is called by a call of shapesize with arguments.\n\n\nExamples:\n>>> resizemode("noresize")\n>>> resizemode()\n\'noresize\''
    ),
    _(
        "turtle.right(angle) \nTurn turtle right by angle units.\n\nAliases: right | rt\n\nArgument:\nangle -- a number (integer or float)\n\nTurn turtle right by angle units. (Units are by default degrees,\nbut can be set via the degrees() and radians() functions.)\nAngle orientation depends on mode. (See this.)\n\nExample:\n>>> heading()\n22.0\n>>> right(45)\n>>> heading()\n337.0"
    ),
    _(
        "turtle.rt(angle) \nTurn turtle right by angle units.\n\nAliases: right | rt\n\nArgument:\nangle -- a number (integer or float)\n\nTurn turtle right by angle units. (Units are by default degrees,\nbut can be set via the degrees() and radians() functions.)\nAngle orientation depends on mode. (See this.)\n\nExample:\n>>> heading()\n22.0\n>>> right(45)\n>>> heading()\n337.0"
    ),
    _(
        "turtle.screensize(canvwidth=None, canvheight=None, bg=None) \nResize the canvas the turtles are drawing on.\n\nOptional arguments:\ncanvwidth -- positive integer, new width of canvas in pixels\ncanvheight --  positive integer, new height of canvas in pixels\nbg -- colorstring or color-tuple, new backgroundcolor\nIf no arguments are given, return current (canvaswidth, canvasheight)\n\nDo not alter the drawing window. To observe hidden parts of\nthe canvas use the scrollbars. (Can make visible those parts\nof a drawing, which were outside the canvas before!)\n\nExample (for a Turtle instance named turtle):\n>>> turtle.screensize(2000,1500)\n>>> # e.g. to search for an erroneously escaped turtle ;-)"
    ),
    _(
        "turtle.seth(to_angle) \nSet the orientation of the turtle to to_angle.\n\nAliases:  setheading | seth\n\nArgument:\nto_angle -- a number (integer or float)\n\nSet the orientation of the turtle to to_angle.\nHere are some common directions in degrees:\n\n standard - mode:          logo-mode:\n-------------------|--------------------\n   0 - east                0 - north\n  90 - north              90 - east\n 180 - west              180 - south\n 270 - south             270 - west\n\nExample:\n>>> setheading(90)\n>>> heading()\n90"
    ),
    _(
        "turtle.setheading(to_angle) \nSet the orientation of the turtle to to_angle.\n\nAliases:  setheading | seth\n\nArgument:\nto_angle -- a number (integer or float)\n\nSet the orientation of the turtle to to_angle.\nHere are some common directions in degrees:\n\n standard - mode:          logo-mode:\n-------------------|--------------------\n   0 - east                0 - north\n  90 - north              90 - east\n 180 - west              180 - south\n 270 - south             270 - west\n\nExample:\n>>> setheading(90)\n>>> heading()\n90"
    ),
    _(
        "turtle.setpos(x, y=None) \nMove turtle to an absolute position.\n\nAliases: setpos | setposition | goto:\n\nArguments:\nx -- a number      or     a pair/vector of numbers\ny -- a number             None\n\ncall: goto(x, y)         # two coordinates\n--or: goto((x, y))       # a pair (tuple) of coordinates\n--or: goto(vec)          # e.g. as returned by pos()\n\nMove turtle to an absolute position. If the pen is down,\na line will be drawn. The turtle's orientation does not change.\n\nExample:\n>>> tp = pos()\n>>> tp\n(0.00, 0.00)\n>>> setpos(60,30)\n>>> pos()\n(60.00,30.00)\n>>> setpos((20,80))\n>>> pos()\n(20.00,80.00)\n>>> setpos(tp)\n>>> pos()\n(0.00,0.00)"
    ),
    _(
        "turtle.setposition(x, y=None) \nMove turtle to an absolute position.\n\nAliases: setpos | setposition | goto:\n\nArguments:\nx -- a number      or     a pair/vector of numbers\ny -- a number             None\n\ncall: goto(x, y)         # two coordinates\n--or: goto((x, y))       # a pair (tuple) of coordinates\n--or: goto(vec)          # e.g. as returned by pos()\n\nMove turtle to an absolute position. If the pen is down,\na line will be drawn. The turtle's orientation does not change.\n\nExample:\n>>> tp = pos()\n>>> tp\n(0.00, 0.00)\n>>> setpos(60,30)\n>>> pos()\n(60.00,30.00)\n>>> setpos((20,80))\n>>> pos()\n(20.00,80.00)\n>>> setpos(tp)\n>>> pos()\n(0.00,0.00)"
    ),
    _(
        'turtle.settiltangle(angle) \nRotate the turtleshape to point in the specified direction\n\nArgument: angle -- number\n\nRotate the turtleshape to point in the direction specified by angle,\nregardless of its current tilt-angle. DO NOT change the turtle\'s\nheading (direction of movement).\n\n\nExamples:\n>>> shape("circle")\n>>> shapesize(5,2)\n>>> settiltangle(45)\n>>> stamp()\n>>> fd(50)\n>>> settiltangle(-45)\n>>> stamp()\n>>> fd(50)'
    ),
    _(
        "turtle.setundobuffer(size) \nSet or disable undobuffer.\n\nArgument:\nsize -- an integer or None\n\nIf size is an integer an empty undobuffer of given size is installed.\nSize gives the maximum number of turtle-actions that can be undone\nby the undo() function.\nIf size is None, no undobuffer is present.\n\nExample:\n>>> setundobuffer(42)"
    ),
    _(
        "turtle.setup(width=0.5, height=0.75, startx=None, starty=None) \nSet the size and position of the main window.\n\nArguments:\nwidth: as integer a size in pixels, as float a fraction of the \n  Default is 50% of \nheight: as integer the height in pixels, as float a fraction of the\n   Default is 75% of \nstartx: if positive, starting position in pixels from the left\n  edge of the screen, if negative from the right edge\n  Default, startx=None is to center window horizontally.\nstarty: if positive, starting position in pixels from the top\n  edge of the screen, if negative from the bottom edge\n  Default, starty=None is to center window vertically.\n\nExamples:\n>>> setup (width=200, height=200, startx=0, starty=0)\n\nsets window to 200x200 pixels, in upper left of screen\n\n>>> setup(width=.75, height=0.5, startx=None, starty=None)\n\nsets window to 75% of screen by 50% of screen and centers"
    ),
    _(
        "turtle.setworldcoordinates(llx, lly, urx, ury) \nSet up a user defined coordinate-system.\n\nArguments:\nllx -- a number, x-coordinate of lower left corner of canvas\nlly -- a number, y-coordinate of lower left corner of canvas\nurx -- a number, x-coordinate of upper right corner of canvas\nury -- a number, y-coordinate of upper right corner of canvas\n\nSet up user coodinat-system and switch to mode 'world' if necessary.\nThis performs a reset. If mode 'world' is already active,\nall drawings are redrawn according to the new coordinates.\n\nBut ATTENTION: in user-defined coordinatesystems angles may appear\ndistorted. (see Screen.mode())\n\nExample:\n>>> setworldcoordinates(-10,-0.5,50,1.5)\n>>> for _ in range(36):\n...     left(10)\n...     forward(0.5)"
    ),
    _(
        "turtle.setx(x) \nSet the turtle's first coordinate to x\n\nArgument:\nx -- a number (integer or float)\n\nSet the turtle's first coordinate to x, leave second coordinate\nunchanged.\n\nExample:\n>>> position()\n(0.00, 240.00)\n>>> setx(10)\n>>> position()\n(10.00, 240.00)"
    ),
    _(
        "turtle.sety(y) \nSet the turtle's second coordinate to y\n\nArgument:\ny -- a number (integer or float)\n\nSet the turtle's first coordinate to x, second coordinate remains\nunchanged.\n\nExample:\n>>> position()\n(0.00, 40.00)\n>>> sety(-10)\n>>> position()\n(0.00, -10.00)"
    ),
    _(
        "turtle.shape(name=None) \nSet turtle shape to shape with given name / return current shapename.\n\nOptional argument:\nname -- a string, which is a valid shapename\n\nSet turtle shape to shape with given name or, if name is not given,\nreturn name of current shape.\nShape with name must exist in the TurtleScreen's shape dictionary.\nInitially there are the following polygon shapes:\n'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'.\nTo learn about how to deal with shapes see Screen-method register_shape.\n\nExample:\n>>> shape()\n'arrow'\n>>> shape(\"turtle\")\n>>> shape()\n'turtle'"
    ),
    _(
        'turtle.shapesize(stretch_wid=None, stretch_len=None, outline=None) \nSet/return turtle\'s stretchfactors/outline. Set resizemode to "user".\n\nOptional arguments:\n   stretch_wid : positive number\n   stretch_len : positive number\n   outline  : positive number\n\nReturn or set the pen\'s attributes x/y-stretchfactors and/or outline.\nSet resizemode to "user".\nIf and only if resizemode is set to "user", the turtle will be displayed\nstretched according to its stretchfactors:\nstretch_wid is stretchfactor perpendicular to orientation\nstretch_len is stretchfactor in direction of turtles orientation.\noutline determines the width of the shapes\'s outline.\n\nExamples:\n>>> resizemode("user")\n>>> shapesize(5, 5, 12)\n>>> shapesize(outline=8)'
    ),
    _(
        'turtle.shapetransform(t11=None, t12=None, t21=None, t22=None) \nSet or return the current transformation matrix of the turtle shape.\n\nOptional arguments: t11, t12, t21, t22 -- numbers.\n\nIf none of the matrix elements are given, return the transformation\nmatrix.\nOtherwise set the given elements and transform the turtleshape\naccording to the matrix consisting of first row t11, t12 and\nsecond row t21, 22.\nModify stretchfactor, shearfactor and tiltangle according to the\ngiven matrix.\n\nExamples:\n>>> shape("square")\n>>> shapesize(4,2)\n>>> shearfactor(-0.5)\n>>> shapetransform()\n(4.0, -1.0, -0.0, 2.0)'
    ),
    _(
        'turtle.shearfactor(shear=None) \nSet or return the current shearfactor.\n\nOptional argument: shear -- number, tangent of the shear angle\n\nShear the turtleshape according to the given shearfactor shear,\nwhich is the tangent of the shear angle. DO NOT change the\nturtle\'s heading (direction of movement).\nIf shear is not given: return the current shearfactor, i. e. the\ntangent of the shear angle, by which lines parallel to the\nheading of the turtle are sheared.\n\nExamples:\n>>> shape("circle")\n>>> shapesize(5,2)\n>>> shearfactor(0.5)\n>>> shearfactor()\n>>> 0.5'
    ),
    _(
        "turtle.showturtle() \nMakes the turtle visible.\n\nAliases: showturtle | st\n\nNo argument.\n\nExample:\n>>> hideturtle()\n>>> showturtle()"
    ),
    _(
        "turtle.speed(speed=None) \nReturn or set the turtle's speed.\n\nOptional argument:\nspeed -- an integer in the range 0..10 or a speedstring (see below)\n\nSet the turtle's speed to an integer value in the range 0 .. 10.\nIf no argument is given: return current speed.\n\nIf input is a number greater than 10 or smaller than 0.5,\nspeed is set to 0.\nSpeedstrings  are mapped to speedvalues in the following way:\n    'fastest' :  0\n    'fast'    :  10\n    'normal'  :  6\n    'slow'    :  3\n    'slowest' :  1\nspeeds from 1 to 10 enforce increasingly faster animation of\nline drawing and turtle turning.\n\nAttention:\nspeed = 0 : *no* animation takes place. forward/back makes turtle jump\nand likewise left/right make the turtle turn instantly.\n\nExample:\n>>> speed(3)"
    ),
    _(
        'turtle.split(p) \nSplit a pathname.  Returns tuple "(head, tail)" where "tail" is\neverything after the final slash.  Either part may be empty.'
    ),
    _(
        "turtle.st() \nMakes the turtle visible.\n\nAliases: showturtle | st\n\nNo argument.\n\nExample:\n>>> hideturtle()\n>>> showturtle()"
    ),
    _(
        'turtle.stamp() \nStamp a copy of the turtleshape onto the canvas and return its id.\n\nNo argument.\n\nStamp a copy of the turtle shape onto the canvas at the current\nturtle position. Return a stamp_id for that stamp, which can be\nused to delete it by calling clearstamp(stamp_id).\n\nExample:\n>>> color("blue")\n>>> stamp()\n13\n>>> fd(50)'
    ),
    _(
        "turtle.sys() \nThis module provides access to some objects used or maintained by the\ninterpreter and to functions that interact strongly with the interpreter.\n\nDynamic objects:\n\nargv -- command line arguments; argv[0] is the script pathname if known\npath -- module search path; path[0] is the script directory, else ''\nmodules -- dictionary of loaded modules\n\ndisplayhook -- called to show results in an interactive session\nexcepthook -- called to handle any uncaught exception other than SystemExit\n  To customize printing in an interactive session or to install a custom\n  top-level exception handler, assign other functions to replace these.\n\nstdin -- standard input file object; used by input()\nstdout -- standard output file object; used by print()\nstderr -- standard error object; used for error messages\n  By assigning other file objects (or objects that behave like files)\n  to these, it is possible to redirect all of the interpreter's I/O.\n\nlast_type -- type of last uncaught exception\nlast_value -- value of last uncaught exception\nlast_traceback -- traceback of last uncaught exception\n  These three are only available in an interactive session after a\n  traceback has been printed.\n\nStatic objects:\n\nbuiltin_module_names -- tuple of module names built into this interpreter\ncopyright -- copyright notice pertaining to this interpreter\nexec_prefix -- prefix used to find the machine-specific Python library\nexecutable -- absolute path of the executable binary of the Python interpreter\nfloat_info -- a struct sequence with information about the float implementation.\nfloat_repr_style -- string indicating the style of repr() output for floats\nhash_info -- a struct sequence with information about the hash algorithm.\nhexversion -- version information encoded as a single integer\nimplementation -- Python implementation information.\nint_info -- a struct sequence with information about the int implementation.\nmaxsize -- the largest supported length of containers.\nmaxunicode -- the value of the largest Unicode code point\nplatform -- platform identifier\nprefix -- prefix used to find the Python library\nthread_info -- a struct sequence with information about the thread implementation.\nversion -- the version of this interpreter as a string\nversion_info -- version information as a named tuple\n__stdin__ -- the original stdin; don't touch!\n__stdout__ -- the original stdout; don't touch!\n__stderr__ -- the original stderr; don't touch!\n__displayhook__ -- the original displayhook; don't touch!\n__excepthook__ -- the original excepthook; don't touch!\n\nFunctions:\n\ndisplayhook() -- print an object to the screen, and save it in builtins._\nexcepthook() -- print an exception and its traceback to sys.stderr\nexc_info() -- return thread-safe information about the current exception\nexit() -- exit the interpreter by raising SystemExit\ngetdlopenflags() -- returns flags to be used for dlopen() calls\ngetprofile() -- get the global profiling function\ngetrefcount() -- return the reference count for an object (plus one :-)\ngetrecursionlimit() -- return the max recursion depth for the interpreter\ngetsizeof() -- return the size of an object in bytes\ngettrace() -- get the global debug tracing function\nsetcheckinterval() -- control how often the interpreter checks for events\nsetdlopenflags() -- set the flags to be used for dlopen() calls\nsetprofile() -- set the global profiling function\nsetrecursionlimit() -- set the max recursion depth for the interpreter\nsettrace() -- set the global debug tracing function"
    ),
    _(
        'turtle.textinput(title, prompt) \nPop up a dialog window for input of a string.\n\nArguments: title is the title of the dialog window,\nprompt is a text mostly describing what information to input.\n\nReturn the string input\nIf the dialog is canceled, return None.\n\nExample:\n>>> textinput("NIM", "Name of first player:")'
    ),
    _(
        'turtle.tilt(angle) \nRotate the turtleshape by angle.\n\nArgument:\nangle - a number\n\nRotate the turtleshape by angle from its current tilt-angle,\nbut do NOT change the turtle\'s heading (direction of movement).\n\nExamples:\n>>> shape("circle")\n>>> shapesize(5,2)\n>>> tilt(30)\n>>> fd(50)\n>>> tilt(30)\n>>> fd(50)'
    ),
    _(
        'turtle.tiltangle(angle=None) \nSet or return the current tilt-angle.\n\nOptional argument: angle -- number\n\nRotate the turtleshape to point in the direction specified by angle,\nregardless of its current tilt-angle. DO NOT change the turtle\'s\nheading (direction of movement).\nIf angle is not given: return the current tilt-angle, i. e. the angle\nbetween the orientation of the turtleshape and the heading of the\nturtle (its direction of movement).\n\nDeprecated since Python 3.1\n\nExamples:\n>>> shape("circle")\n>>> shapesize(5,2)\n>>> tilt(45)\n>>> tiltangle()'
    ),
    _(
        "turtle.time() \nThis module provides various functions to manipulate time values.\n\nThere are two standard representations of time.  One is the number\nof seconds since the Epoch, in UTC (a.k.a. GMT).  It may be an integer\nor a floating point number (to represent fractions of seconds).\nThe Epoch is system-defined; on Unix, it is generally January 1st, 1970.\nThe actual value can be retrieved by calling gmtime(0).\n\nThe other representation is a tuple of 9 integers giving local time.\nThe tuple items are:\n  year (including century, e.g. 1998)\n  month (1-12)\n  day (1-31)\n  hours (0-23)\n  minutes (0-59)\n  seconds (0-59)\n  weekday (0-6, Monday is 0)\n  Julian day (day in the year, 1-366)\n  DST (Daylight Savings Time) flag (-1, 0 or 1)\nIf the DST flag is 0, the time is given in the regular time zone;\nif it is 1, the time is given in the DST time zone;\nif it is -1, mktime() should guess based on the date and time.\n\nVariables:\n\ntimezone -- difference in seconds between UTC and local standard time\naltzone -- difference in  seconds between UTC and local DST time\ndaylight -- whether local time should reflect DST\ntzname -- tuple of (standard time zone name, DST time zone name)\n\nFunctions:\n\ntime() -- return current time in seconds since the Epoch as a float\nclock() -- return CPU time since process start as a float\nsleep() -- delay for a number of seconds given as a float\ngmtime() -- convert seconds since Epoch to UTC tuple\nlocaltime() -- convert seconds since Epoch to local time tuple\nasctime() -- convert time tuple to string\nctime() -- convert time in seconds to string\nmktime() -- convert local time tuple to seconds since Epoch\nstrftime() -- convert time tuple to string according to format specification\nstrptime() -- parse string to time tuple according to format specification\ntzset() -- change the local timezone"
    ),
    _(
        'turtle.title(titlestring) \nSet title of turtle-window\n\nArgument:\ntitlestring -- a string, to appear in the titlebar of the\n               turtle graphics window.\n\nThis is a method of Screen-class. Not available for TurtleScreen-\nobjects.\n\nExample:\n>>> title("Welcome to the turtle-zoo!")'
    ),
    _(
        'turtle.tkinter() \nWrapper functions for Tcl/Tk.\n\nTkinter provides classes which allow the display, positioning and\ncontrol of widgets. Toplevel widgets are Tk and Toplevel. Other\nwidgets are Frame, Label, Entry, Text, Canvas, Button, Radiobutton,\nCheckbutton, Scale, Listbox, Scrollbar, OptionMenu, Spinbox\nLabelFrame and PanedWindow.\n\nProperties of the widgets are specified with keyword arguments.\nKeyword arguments have the same name as the corresponding resource\nunder Tk.\n\nWidgets are positioned with one of the geometry managers Place, Pack\nor Grid. These managers can be called with methods place, pack, grid\navailable in every Widget.\n\nActions are bound to events by resources (e.g. keyword argument\ncommand) or with the method bind.\n\nExample (Hello, World):\nimport tkinter\nfrom tkinter.constants import *\ntk = tkinter.Tk()\nframe = tkinter.Frame(tk, relief=RIDGE, borderwidth=2)\nframe.pack(fill=BOTH,expand=1)\nlabel = tkinter.Label(frame, text="Hello, World")\nlabel.pack(fill=X, expand=1)\nbutton = tkinter.Button(frame,text="Exit",command=tk.destroy)\nbutton.pack(side=BOTTOM)\ntk.mainloop()'
    ),
    _(
        "turtle.tkinter.simpledialog() \nThis modules handles dialog boxes.\n\nIt contains the following public symbols:\n\nSimpleDialog -- A simple but flexible modal dialog box\n\nDialog -- a base class for dialogs\n\naskinteger -- get an integer from the user\n\naskfloat -- get a float from the user\n\naskstring -- get a string from the user"
    ),
    _(
        'turtle.towards(x, y=None) \nReturn the angle of the line from the turtle\'s position to (x, y).\n\nArguments:\nx -- a number   or  a pair/vector of numbers   or   a turtle instance\ny -- a number       None                            None\n\ncall: distance(x, y)         # two coordinates\n--or: distance((x, y))       # a pair (tuple) of coordinates\n--or: distance(vec)          # e.g. as returned by pos()\n--or: distance(mypen)        # where mypen is another turtle\n\nReturn the angle, between the line from turtle-position to position\nspecified by x, y and the turtle\'s start orientation. (Depends on\nmodes - "standard" or "logo")\n\nExample:\n>>> pos()\n(10.00, 10.00)\n>>> towards(0,0)\n225.0'
    ),
    _(
        "turtle.tracer(n=None, delay=None) \nTurns turtle animation on/off and set delay for update drawings.\n\nOptional arguments:\nn -- nonnegative  integer\ndelay -- nonnegative  integer\n\nIf n is given, only each n-th regular screen update is really performed.\n(Can be used to accelerate the drawing of complex graphics.)\nSecond arguments sets delay value (see RawTurtle.delay())\n\nExample:\n>>> tracer(8, 25)\n>>> dist = 2\n>>> for i in range(200):\n...     fd(dist)\n...     rt(90)\n...     dist += 2"
    ),
    _(
        "turtle.turtles() \nReturn the list of turtles on the \n\nExample:\n>>> turtles()\n[<turtle.Turtle object at 0x00E11FB0>]"
    ),
    _(
        'turtle.turtlesize(stretch_wid=None, stretch_len=None, outline=None) \nSet/return turtle\'s stretchfactors/outline. Set resizemode to "user".\n\nOptional arguments:\n   stretch_wid : positive number\n   stretch_len : positive number\n   outline  : positive number\n\nReturn or set the pen\'s attributes x/y-stretchfactors and/or outline.\nSet resizemode to "user".\nIf and only if resizemode is set to "user", the turtle will be displayed\nstretched according to its stretchfactors:\nstretch_wid is stretchfactor perpendicular to orientation\nstretch_len is stretchfactor in direction of turtles orientation.\noutline determines the width of the shapes\'s outline.\n\nExamples:\n>>> resizemode("user")\n>>> shapesize(5, 5, 12)\n>>> shapesize(outline=8)'
    ),
    _(
        "turtle.types() \nDefine names for built-in types that aren't directly accessible as a builtin."
    ),
    _(
        "turtle.undo() \nundo (repeatedly) the last turtle action.\n\nNo argument.\n\nundo (repeatedly) the last turtle action.\nNumber of available undo actions is determined by the size of\nthe undobuffer.\n\nExample:\n>>> for i in range(4):\n...     fd(50); lt(80)\n...\n>>> for i in range(8):\n...     undo()\n..."
    ),
    _(
        "turtle.undobufferentries() \nReturn count of entries in the undobuffer.\n\nNo argument.\n\nExample:\n>>> while undobufferentries():\n...     undo()"
    ),
    _(
        "turtle.up() \nPull the pen up -- no drawing when moving.\n\nAliases: penup | pu | up\n\nNo argument\n\nExample:\n>>> penup()"
    ),
    _("turtle.update() \nPerform a TurtleScreen update.\n        "),
    _(
        'turtle.width(width=None) \nSet or return the line thickness.\n\nAliases:  pensize | width\n\nArgument:\nwidth -- positive number\n\nSet the line thickness to width or return it. If resizemode is set\nto "auto" and turtleshape is a polygon, that polygon is drawn with\nthe same line thickness. If no argument is given, current pensize\nis returned.\n\nExample:\n>>> pensize()\n1\n>>> pensize(10)   # from here on lines of width 10 are drawn'
    ),
    _(
        "turtle.window_height() \nReturn the height of the turtle window.\n\nExample:\n>>> window_height()\n480"
    ),
    _(
        "turtle.window_width() \nReturn the width of the turtle window.\n\nExample:\n>>> window_width()\n640"
    ),
    _(
        'turtle.write(arg, move=False, align=\'left\', font=\'Arial\', 8, \'normal\') \nWrite text at the current turtle position.\n\nArguments:\narg -- info, which is to be written to the TurtleScreen\nmove (optional) -- True/False\nalign (optional) -- one of the strings "left", "center" or right"\nfont (optional) -- a triple (fontname, fontsize, fonttype)\n\nWrite text - the string representation of arg - at the current\nturtle position according to align ("left", "center" or right")\nand with the given font.\nIf move is True, the pen is moved to the bottom-right corner\nof the text. By default, move is False.\n\nExample:\n>>> write(\'Home = \', True, align="center")\n>>> write((0,0), True)'
    ),
    _(
        "turtle.write_docstringdict(filename='turtle_docstringdict') \nCreate and write docstring-dictionary to file.\n\nOptional argument:\nfilename -- a string, used as filename\n            default value is turtle_docstringdict\n\nHas to be called explicitly, (not used by the turtle-graphics classes)\nThe docstring dictionary will be written to the Python script <filname>.py\nIt is intended to serve as a template for translation of the docstrings\ninto different languages."
    ),
    _(
        "turtle.xcor() \nReturn the turtle's x coordinate.\n\nNo arguments.\n\nExample:\n>>> reset()\n>>> left(60)\n>>> forward(100)\n>>> print xcor()\n50.0"
    ),
    _(
        "turtle.ycor() \nReturn the turtle's y coordinate\n---\nNo arguments.\n\nExample:\n>>> reset()\n>>> left(60)\n>>> forward(100)\n>>> print ycor()\n86.6025403784"
    ),
    _(
        "uuid.UUID(hex=None, bytes=None, bytes_le=None, fields=None, int=None, version=None) \nInstances of the UUID class represent UUIDs as specified in RFC 4122.\nUUID objects are immutable, hashable, and usable as dictionary keys.\nConverting a UUID to a string with str() yields something in the form\n'12345678-1234-1234-1234-123456789abc'.  The UUID constructor accepts\nfive possible forms: a similar string of hexadecimal digits, or a tuple\nof six integer fields (with 32-bit, 16-bit, 16-bit, 8-bit, 8-bit, and\n48-bit values respectively) as an argument named 'fields', or a string\nof 16 bytes (with all the integer fields in big-endian order) as an\nargument named 'bytes', or a string of 16 bytes (with the first three\nfields in little-endian order) as an argument named 'bytes_le', or a\nsingle 128-bit integer as an argument named 'int'.\n\nUUIDs have these read-only attributes:\n\n    bytes       the UUID as a 16-byte string (containing the six\n                integer fields in big-endian byte order)\n\n    bytes_le    the UUID as a 16-byte string (with time_low, time_mid,\n                and time_hi_version in little-endian byte order)\n\n    fields      a tuple of the six integer fields of the UUID,\n                which are also available as six individual attributes\n                and two derived attributes:\n\n        time_low                the first 32 bits of the UUID\n        time_mid                the next 16 bits of the UUID\n        time_hi_version         the next 16 bits of the UUID\n        clock_seq_hi_variant    the next 8 bits of the UUID\n        clock_seq_low           the next 8 bits of the UUID\n        node                    the last 48 bits of the UUID\n\n        time                    the 60-bit timestamp\n        clock_seq               the 14-bit sequence number\n\n    hex         the UUID as a 32-character hexadecimal string\n\n    int         the UUID as a 128-bit integer\n\n    urn         the UUID as a URN as specified in RFC 4122\n\n    variant     the UUID variant (one of the constants RESERVED_NCS,\n                RFC_4122, RESERVED_MICROSOFT, or RESERVED_FUTURE)\n\n    version     the UUID version number (1 through 5, meaningful only\n                when the variant is RFC_4122)"
    ),
    _(
        "uuid.bytes() \nbytes(iterable_of_ints) -> bytes\nbytes(string, encoding[, errors]) -> bytes\nbytes(bytes_or_buffer) -> immutable copy of bytes_or_buffer\nbytes(int) -> bytes object of size given by the parameter initialized with null bytes\nbytes() -> empty bytes object\n\nConstruct an immutable array of bytes from:\n  - an iterable yielding integers in range(256)\n  - a text string encoded using the specified encoding\n  - any object implementing the buffer API.\n  - an integer"
    ),
    _("uuid.ctypes() \ncreate and manipulate C data types in Python"),
    _(
        "uuid.getnode() \nGet the hardware address as a 48-bit positive integer.\n\nThe first time this runs, it may launch a separate program, which could\nbe quite slow.  If all attempts to obtain the hardware address fail, we\nchoose a random 48-bit number with its eighth bit set to 1 as recommended\nin RFC 4122."
    ),
    _(
        "uuid.int() \nint(x=0) -> integer\nint(x, base=10) -> integer\n\nConvert a number or string to an integer, or return 0 if no arguments\nare given.  If x is a number, return x.__int__().  For floating point\nnumbers, this truncates towards zero.\n\nIf x is not a number or if base is given, then x must be a string,\nbytes, or bytearray instance representing an integer literal in the\ngiven base.  The literal can be preceded by '+' or '-' and be surrounded\nby whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.\nBase 0 means to interpret the base from the string as an integer literal.\n>>> int('0b100', base=0)\n4"
    ),
    _(
        "uuid.os() \nOS routines for NT or Posix depending on what system we're on.\n\nThis exports:\n  - all functions from posix or nt, e.g. unlink, stat, etc.\n  - os.path is either posixpath or ntpath\n  - os.name is either 'posix' or 'nt'\n  - os.curdir is a string representing the current directory (always '.')\n  - os.pardir is a string representing the parent directory (always '..')\n  - os.sep is the (or a most common) pathname separator ('/' or '\\\\')\n  - os.extsep is the extension separator (always '.')\n  - os.altsep is the alternate pathname separator (None or '/')\n  - os.pathsep is the component separator used in $PATH etc\n  - os.linesep is the line separator in text files ('\\r' or '\\n' or '\\r\\n')\n  - os.defpath is the default search path for executables\n  - os.devnull is the file path of the null device ('/dev/null', etc.)\n\nPrograms that import and use 'os' stand a better chance of being\nportable between different platforms.  Of course, they must then\nonly use functions that are defined by all platforms (e.g., unlink\nand opendir), and leave all pathname manipulation to os.path\n(e.g., split and join)."
    ),
    _(
        "uuid.sys() \nThis module provides access to some objects used or maintained by the\ninterpreter and to functions that interact strongly with the interpreter.\n\nDynamic objects:\n\nargv -- command line arguments; argv[0] is the script pathname if known\npath -- module search path; path[0] is the script directory, else ''\nmodules -- dictionary of loaded modules\n\ndisplayhook -- called to show results in an interactive session\nexcepthook -- called to handle any uncaught exception other than SystemExit\n  To customize printing in an interactive session or to install a custom\n  top-level exception handler, assign other functions to replace these.\n\nstdin -- standard input file object; used by input()\nstdout -- standard output file object; used by print()\nstderr -- standard error object; used for error messages\n  By assigning other file objects (or objects that behave like files)\n  to these, it is possible to redirect all of the interpreter's I/O.\n\nlast_type -- type of last uncaught exception\nlast_value -- value of last uncaught exception\nlast_traceback -- traceback of last uncaught exception\n  These three are only available in an interactive session after a\n  traceback has been printed.\n\nStatic objects:\n\nbuiltin_module_names -- tuple of module names built into this interpreter\ncopyright -- copyright notice pertaining to this interpreter\nexec_prefix -- prefix used to find the machine-specific Python library\nexecutable -- absolute path of the executable binary of the Python interpreter\nfloat_info -- a struct sequence with information about the float implementation.\nfloat_repr_style -- string indicating the style of repr() output for floats\nhash_info -- a struct sequence with information about the hash algorithm.\nhexversion -- version information encoded as a single integer\nimplementation -- Python implementation information.\nint_info -- a struct sequence with information about the int implementation.\nmaxsize -- the largest supported length of containers.\nmaxunicode -- the value of the largest Unicode code point\nplatform -- platform identifier\nprefix -- prefix used to find the Python library\nthread_info -- a struct sequence with information about the thread implementation.\nversion -- the version of this interpreter as a string\nversion_info -- version information as a named tuple\n__stdin__ -- the original stdin; don't touch!\n__stdout__ -- the original stdout; don't touch!\n__stderr__ -- the original stderr; don't touch!\n__displayhook__ -- the original displayhook; don't touch!\n__excepthook__ -- the original excepthook; don't touch!\n\nFunctions:\n\ndisplayhook() -- print an object to the screen, and save it in builtins._\nexcepthook() -- print an exception and its traceback to sys.stderr\nexc_info() -- return thread-safe information about the current exception\nexit() -- exit the interpreter by raising SystemExit\ngetdlopenflags() -- returns flags to be used for dlopen() calls\ngetprofile() -- get the global profiling function\ngetrefcount() -- return the reference count for an object (plus one :-)\ngetrecursionlimit() -- return the max recursion depth for the interpreter\ngetsizeof() -- return the size of an object in bytes\ngettrace() -- get the global debug tracing function\nsetcheckinterval() -- control how often the interpreter checks for events\nsetdlopenflags() -- set the flags to be used for dlopen() calls\nsetprofile() -- set the global profiling function\nsetrecursionlimit() -- set the max recursion depth for the interpreter\nsettrace() -- set the global debug tracing function"
    ),
    _(
        "uuid.uuid1(node=None, clock_seq=None) \nGenerate a UUID from a host ID, sequence number, and the current time.\nIf 'node' is not given, getnode() is used to obtain the hardware\naddress.  If 'clock_seq' is given, it is used as the sequence number;\notherwise a random 14-bit sequence number is chosen."
    ),
    _(
        "uuid.uuid3(namespace, name) \nGenerate a UUID from the MD5 hash of a namespace UUID and a name."
    ),
    _("uuid.uuid4() \nGenerate a random UUID."),
    _(
        "uuid.uuid5(namespace, name) \nGenerate a UUID from the SHA-1 hash of a namespace UUID and a name."
    ),
]
