# -*- coding: utf-8 -*-

# Python 3 style print()
from __future__ import print_function

import sys
import token
import tokenize
import argparse
from io import BytesIO
# tokenize.tokenize exists in python 2 but actually does something
# different, import the current function for this version
if sys.version_info < (3, 0):
    from tokenize import generate_tokens as tokenizer
    # This was introduced in Python 3
    tokenize.ENCODING = None
else:
    from tokenize import tokenize as tokenizer  # pragma: no cover

_VERSION = (0, 0, 2, )


def get_version():
    return '.'.join([str(i) for i in _VERSION])


def mangle(text):
    """
    Takes a script and mangles it to fit inside 8192 bytes if necessary
    """

    text_bytes = text.encode('utf-8')

    # Wrap the input script as a byte stream
    buff = BytesIO(text_bytes)
    # Byte stream for the mangled script
    mangled = BytesIO()

    last_tok = token.INDENT
    last_line = -1
    last_col = 0
    last_line_text = ''
    open_list_dicts = 0

    # Build tokens from the script
    tokens = tokenizer(buff.readline)
    for t, text, (line_s, col_s), (line_e, col_e), line in tokens:
        # If this is a new line (except the very first)
        if line_s > last_line and last_line != -1:
            # Reset the column
            last_col = 0
            # If the last line ended in a '\' (continuation)
            if last_line_text.rstrip()[-1:] == '\\':
                # Recreate it
                mangled.write(b' \\\n')

        # We don't want to be calling the this multiple times
        striped = text.strip()

        # Tokens or charecters for opening or closing a list/dict
        list_dict_open = [token.LSQB, token.LBRACE, '[', '{']
        list_dict_close = [token.RSQB, token.RBRACE, ']', '}']

        # If this is a list or dict
        if t in list_dict_open or striped in list_dict_open:
            # Increase the dict / list level
            open_list_dicts += 1
        elif t in list_dict_close or striped in list_dict_close:
            # Decrease the dict / list level
            open_list_dicts -= 1

        # If this is a docstring comment
        if t == token.STRING and (last_tok == token.INDENT or (
            (last_tok == token.NEWLINE or last_tok == tokenize.NL)
                and open_list_dicts == 0)):
            # Output number of lines corresponding those in
            # the docstring comment
            mangled.write(b'\n' * (len(text.split('\n')) - 1))
        # Or is it a standard comment
        elif t == tokenize.COMMENT:
            # Plain comment, just don't write it
            pass
        else:
            # Recreate indentation, ideally we should use tabs
            if col_s > last_col:
                mangled.write(b' ' * (col_s - last_col))
            # On Python 3 the first token specifies the encoding
            # but we alredy know it's utf-8 and writing it just
            # gives us an invalid script
            if t != tokenize.ENCODING:
                mangled.write(text.encode('utf-8'))

        # Store the previus state
        last_tok = t
        last_col = col_e
        last_line = line_e
        last_line_text = line

    # Return a string
    return mangled.getvalue().decode('utf-8')


_HELP_TEXT = """
Strip comments from a Python script.

Please note nudatus only supports the syntax of the Python version it's running
on so nudatus running on Python 2 only supports scripts in valid Python 2 and
again for Python 3
"""


def main(argv=None):
    """
    Command line entry point
    """
    if not argv:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description=_HELP_TEXT)
    parser.add_argument('input', nargs='?', default=None)
    parser.add_argument('output', nargs='?', default=None)
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + get_version())
    args = parser.parse_args(argv)

    if not args.input:
        print("No file specified", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.input, 'r') as f:
            res = mangle(f.read())
            if not args.output:
                print(res, end='')
            else:
                with open(args.output, 'w') as o:
                    o.write(res)
    except Exception as ex:
        print("Error mangling {}: {!s}".format(args.input, ex),
              file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':  # pragma: no cover
    main(sys.argv[1:])
