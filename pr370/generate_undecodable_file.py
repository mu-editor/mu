#
# This will generate a file containing a cp1252-encoded pound sign
# which won't decide in utf-8 because the same byte sequence
# represents a continuation byte
#
f = open("t.py", "w", encoding="cp1252")
f.write("# -*- coding: utf-8 -*-\n")
f.write("£")
f.close()

