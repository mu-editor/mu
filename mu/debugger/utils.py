"""
Debug related utility functions for the Mu editor.

Copyright (c) Nicholas H.Tollervey and others (see the AUTHORS file).

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


def is_breakpoint_line(code):
    """
    Return a boolean indication if the specified code from a single line can
    have a breakpoint added to it.

    Based entirely on simple but effective heuristics (see comments).
    """
    code = code.strip()
    if not code:
        return False
    # Can't set breakpoints on blank lines or comments.
    # TODO: Make this more robust.
    if code[0] == "#" or code[:3] == '"""' or code[:3] == "'''":
        return False
    # Can't set breakpoints on lines that end with opening (, { or [
    if code[-1] in ("(", "{", "["):
        return False
    # Can't set breakpoints on lines that contain only closing ), } or ]
    if len(code) == 1 and code in (")", "}", "]"):
        return False
    return True
