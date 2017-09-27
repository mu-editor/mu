Mu - an editor for beginner programmers
=======================================

What?
-----

Mu is a simple code editor for beginner programmers based on the feedback given
to and experiences of the Raspberry Pi Foundation's education team.

It's written in Python and works on Windows, OSX, Linux and Raspberry Pi.

Why?
----

There isn't a cross platform Python code editor that is:

* Easy to use;
* Available on all major platforms;
* Well documented (even for beginners);
* Simply coded;
* Easily translated;
* Currently maintained; and,
* Thoroughly tested.

Mu addresses these needs.

In the Python world, teachers, students and other beginner programmers are
forced to use one of the following options:

* IDLE - the editor that comes bundled with Python.
* A third party IDE (integrated development environment) for teaching. If "IDE" sounds complicated for beginner programmers, that's because it is.
* A professional programmer's editor such as vi or emacs.

Such tools are fiddly, complicated and full of distracting "features". They
are usually inappropriate for teaching and learning ~ complexity impedes a
novice programmer's first steps.

How?
----

Mu's philosophy is:

* Less is more (remove all unnecessary distractions);
* Keep it simple (so Mu is easy to understand);
* Walk the path of least resistance (Mu should be easy);
* Have fun (learning should be a positive experience).

Mu is modal. It works as a general purpose Python 3 editor, as a MicroPython
editor for the BBC's micro:bit device, or as a CircuitPython editor for
Adafruit boards.

Mu's code is simple - it's commented and mostly found in a few obviously named
Python files. This has been done on purpose: we want teachers and kids to take
ownership of this project and organising the code in this way aids the first
steps required to get involved (everything you need to know is in obviously
named files).

History
-------

Mu was created as a PSF contribution to the BBC's micro:bit project, aimed at
11-year old children.

The micro:bit consists of a small and simple programmable device. One option is
the remarkable work of Damien George in the form of MicroPython, a full
re-implementation of Python 3 for microcontrollers including the BBC micro:bit.

The BBC's "blessed" solution for programming this device is web-based. However,
we observed this doesn't provide the optimum experience for Python:

* It requires you to use a web-browser as a text based code editor.
* You need to download the .hex file to flash onto the device and then drag it to the device's mount point on the filesystem. A rather clunky multi-part process.
* It doesn't allow you to connect to the device in order to live code in Python via the REPL.

Mu was created to address each of these problems: it is a native application
specifically designed as a text based coding environment. It makes it easy to
flash your code onto the device (it's only a click of a button). It has a built
in REPL client that automatically connects to the device.

Mu was adapted from my previous work done with Damien George and Dan Pope
on the "Puppy" editor for kids. Mu is an ultra-slimmed down version of Puppy.

Mu has since become quite popular and the most requested feature has been to
make it into a generic Python code editor for beginners. Thanks to the support
of the Raspberry Pi Foundation I've been able to make it into the modal editor
that exists today.

Installation
------------

** THESE INSTALLATION INSTRUCTIONS ARE OUT OF DATE **

Currently, the latest builds for Windows, OSX and Linux x86 can be found here:

http://mu-builds.s3-website.eu-west-2.amazonaws.com

For our project roadmap see the ``ROADMAP.rst`` file.

You could run Mu from source. Alternatively, go to the link above, choose the
directory for your platform and download the latest build of the editor (HINT:
they're ordered by date).

Windows
+++++++

You only need to copy the downloaded .exe file somewhere handy and double-click
it to launch. Once you've got past all the Windows induced warnings and
privilege requests you'll see the editor. Unfortunately, due to Windows more
than anything else, to be able to use the REPL you'll need to install a driver
for USB/serial connectivity to the BBC micro:bit. You can find the required
driver and detailed instructions for installing it on ARM's website:

https://developer.mbed.org/handbook/Windows-serial-configuration

We're trying to find a way around this problem via Windows packaging.

OS X
++++

OSX will probably ask you to confirm you want to run a program downloaded from
the internet. You may need to right-click on the file and select `open` to make
it work first time. You do not need to install any drivers.

Linux
+++++

Just make the file executable and run it! :-)

We're in the process of creating official packages for both Debian and Fedora
based flavours of Linux.

Raspberry Pi (Raspbian)
+++++++++++++++++++++++

A package is available for Raspbian for mu can be installed using the following commands.

Open a Terminal (Menu > Accessories > Terminal):

    sudo apt-get update

    sudo apt-get install mu


Development
-----------

If you only want to use Mu then please ignore this section. If you'd like to
contribute to the development of Mu read on...

The source code is hosted on GitHub. Please feel free to fork the repository.
Assuming you have Git installed you can download the code from the canonical
repository with the following command::

    $ git clone https://github.com/mu-editor/mu.git

For this to work you'll need to have Qt5 and Python 3 installed.

* On Debian based systems this is covered by installing: python3-pyqt5,
  python3-pyqt5.qsci, python3-pyqt5.qtserialport, python3-pyqt5.qtsvg

* On Mac OS, first install PyQT5::

    brew install pyqt5 --with-python3

  Then install QScintilla using the recipe from the mu repository::

    brew install https://raw.githubusercontent.com/mu-editor/mu/master/package/extras/qscintilla2.rb

  .. note:: If you have an existing virtual environment it will not have
     changed to add the new packages. The simplest thing to do is to create a
     new virtual environment, remembering to use the
     ``--system-site-packages`` switch so that installed libraries are
     included. For instance::

        $ virtualenv -p /usr/local/bin/python3 --system-site-packages ~/env/py3

     or::

        $ mkvirtualenv -p /usr/local/bin/python3 --system-site-packages py3

Ensure you have the correct dependencies for development installed by creating
a virtualenv and running::

    $ pip install -r requirements.txt

To run the local development version of "mu", in the root of this repository
type::

    $ python3 run.py

There is a Makefile that helps with most of the common workflows associated
with development. Typing "make" on its own will list the options thus::

    $ make

    There is no default Makefile target right now. Try:

    make clean - reset the project and remove auto-generated assets.
    make pyflakes - run the PyFlakes code checker.
    make pep8 - run the PEP8 style checker.
    make test - run the test suite.
    make coverage - view a report on test coverage.
    make check - run all the checkers and tests.
    make docs - run sphinx to create project documentation.

Before contributing code please make sure you've read CONTRIBUTING.rst.
