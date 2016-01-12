Mu - a "micro" editor
=====================

**This project works with Python 3 and the Qt UI library.**

Currently, the latest builds for Windows, OSX and Linux x86 can be found here:

http://ardublockly-builds.s3-website-us-west-2.amazonaws.com/?prefix=microbit

What?
-----

Mu is a a very simple code editor for kids. It's written in Python and uses the
Qt GUI framework. This means it'll work on Windows, OSX and Linux. It should
also work on a Raspberry Pi.

Why?
----

The BBC's micro:bit project is aimed at 11-year old children. It consists of a
small and simple programmable device. One option is the remarkable work of
Damien George in the form of MicroPython, a full re-implementation of Python 3
for microcontrollers including the BBC micro:bit.

The BBC's "blessed" solution for programming tools is web-based. However, we
have observed that this doesn't provide the optimum experience:

* It requires you to be connected to the internet to get the tools you need.
* You need to download the .hex file to flash onto the device and then drag it to the device's mount point on the filesystem. A rather clunky multi-part process.
* It doesn't allow you to connect to the device in order to live code in Python via the REPL.

The Mu editor addresses each of these problems: it is a native application so
does not need to be connected to the internet to work. It makes it easy to
flash your code onto the device (it's only a click of a button). It has a built
in REPL client that automatically connects to the device.

How?
----

This is very much a first draft, brain dump work in progress just to "spike"
out code to see if it can be done (it appears it can). Much of the work has
been adapted from previous work done with Damien George and Dan Pope on the
"Puppy" editor for kids. "Mu" is an ultra-slimmed down version of Puppy - an
MVP of sorts.

The code is also simple and monolithic - it's commented and mostly found in a
a few obviously named Python files. This has been done on purpose: we want
teachers and kids to take ownership of this project and organising the code in
this way aids the first steps required to get involved (everything you need to
know is in three obvious files).

In terms of features - it's a case of less is more with regard to the following features:

* Create a new Python script.
* Load an existing Python script.
* Save the existing Python script.
* Use code snippets (both via a menu and hotkey).
* Flash the device with the current script.
* Connect to the device via the REPL (will only work if a device is connected).
* Zoom in/out.
* Quit.

That's it!
