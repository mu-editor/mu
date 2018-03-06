import os, sys
import codecs
import locale
import re

encoding_cookie = re.compile("^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")

boms = [
    (codecs.BOM_UTF8, ("utf-8-sig", "")),
    (codecs.BOM_UTF16_BE, ("utf-16-be", "\ufeff")),
    (codecs.BOM_UTF16_LE, ("utf-16-le", "\ufeff")),
]

#
# Try to determine the encoding of an input file:
#
# * If there is a UTF-8 BOM, decode as UTF-8
# * If there is a UTF-16 BOM, decode as UTF-16
# * If there is a PEP 263 encoding cookie, decode from that
# * Otherwise re-open without an encoding
#
def determine_encoding(filepath):
    """Determine the encoding of a file:

    * If there is a BOM, return the appropriate encoding and any prefix to strip
    * If there is a PEP 263 encoding cookie, return the appropriate encoding
    * Return the locale default encoding
    """
    #
    # Try for a BOM
    # The UTF16BE/LE codecs
    #
    with open(filepath, "rb") as f:
        line = f.readline()
    for bom, (encoding, prefix) in boms:
        if line.startswith(bom):
            return encoding, prefix

    #
    # Look for a PEP 263 encoding cookie
    #
    default_encoding = locale.getpreferredencoding()
    uline = line.decode(default_encoding)
    match = encoding_cookie.match(uline)
    if match:
        return match.group(1), ""

    #
    # Fall back to the locale default
    #
    return default_encoding, ""

def open_and_decode(filepath):
    #
    # Read one line with the default encoding
    #
    encoding, prefix = determine_encoding(filepath)
    print("Encoding:", encoding)
    return open(filepath, encoding=encoding).read().lstrip(prefix)

if __name__ == '__main__':
    import glob
    for filepath in glob.glob("*.txt"):
        print(filepath)
        print(repr(open_and_decode(filepath)))
