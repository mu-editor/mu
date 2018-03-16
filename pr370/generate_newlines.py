import os, sys

with open("newlines-rn.txt", "wb") as f:
    f.write(b"abc\r\ndef\r\nghi\rjkl\n")

for newline in (None, "", "\n", "\r\n"):
    print("Newline mode", repr(newline))
    with open("newlines-rn.txt", "r", newline=newline) as f:
        print(repr(f.readlines()))
    print()
