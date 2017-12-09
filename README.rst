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

* IDLE - the educationally problematic editor that comes bundled with Python.
* A third party IDE (integrated development environment) for teaching. If "IDE" sounds complicated for beginner programmers, that's because it is.
* An intimidating professional programmer's editor such as vi or emacs.

Such tools are fiddly, complicated and full of distracting "features". They
are usually inappropriate for teaching and learning ~ complexity impedes a
novice programmer's first steps.

How?
----

Mu's philosophy is:

* Less is more (remove all unnecessary distractions);
* Keep it simple (so Mu is easy to understand);
* Walk the path of least resistance (Mu should be easy to use);
* Have fun (learning should be a positive experience).

Mu is modal. It works as a general purpose Python 3 editor, as a MicroPython
editor for the BBC's micro:bit device, or as a CircuitPython editor for
Adafruit boards.

Mu's code is simple - it's commented and mostly found in a few obviously named
Python files. This has been done on purpose: we want teachers and kids to take
ownership of this project and organising the code in this way aids the first
steps required to get involved (everything you need to know is in obviously
named files).

Development
-----------

If you only want to use Mu then please ignore this section. If you'd like to
contribute to the development of Mu read on...

The source code is hosted on GitHub. Please feel free to fork the repository.
Assuming you have Git installed you can download the code from the canonical
repository with the following command::

    $ git clone https://github.com/mu-editor/mu.git

Ensure you have the correct dependencies for development installed.

First, create a virtualenv.

Dependency installation for the Raspberry Pi is described below, for all other
platforms, run::

    $ pip install -r requirements.txt

If you are building for the Pi there are two steps::

    $ apt-get install python3-pyqt5 python3-pyqt5.qsci and python3-pyqt5.qtserialport python3-pyqt5.qtsvg python3-dev
    $ pip install -r requirements_pi.txt

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
    make dist - make a dist/wheel for the project.
    make publish-test - publish the project to PyPI test instance.
    make publish-live - publish the project to PyPI production.
    make docs - run sphinx to create project documentation.
    make translate - create a messages.pot file for translations.
    make translateall - as with translate but for all API strings.


Before contributing code please make sure you've read CONTRIBUTING.rst. We
expect everyone participating in the development of Mu to act in accordance
with the PSF's code of conduct found in the CODE_OF_CONDUCT.rst file.
