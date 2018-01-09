Mu - a simple editor 
====================

What?
-----

Mu is a simple code editor for beginner programmers based on the feedback given
to and experiences of the Raspberry Pi Foundation's education team. Having said
that, Mu is for anyone who wants to use a simple "no frills" editor.

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

* IDLE - the educationally problematic  editor that comes with Python.
* A third party IDE (integrated development environment) for teaching. If "IDE"
  sounds complicated for beginner programmers, that's because it is.
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

The instructions below assume that you're working within a Python
virtual environment (aka "venv").

For this to work you'll need to have Qt5, all the other dependencies and at
least Python 3.5 installed.

On all platforms except the Raspberry Pi, this can be achieved by installing
all the dependencies into your virtualenv via the ``requirements.txt`` file::

    $ pip install -r requirements.txt

If you are developing on the Raspberry Pi there are three steps. First install
the packaged Qt related dependencies::

    $ apt-get install python3-pyqt5 python3-pyqt5.qsci and python3-pyqt5.qtserialport python3-dev

Next create  a virtualenv that uses Python 3 and allows the virtualenv access
to the packages installed on your system via the ``--system-site-packages``
flag::

    virtualenv -p /usr/local/bin/python3 --system-site-packages ~/mu-venv

Finally, with the virtualenv enabled, pip install the Python packages for the
Raspberry Pi via the ``requirements-pi.txt`` file::

    (mu-venv) $ pip install -r requirements-pi.txt

.. note:: From this point onwards, the instructions assume that you're
   using a virtual environment.

On all platforms, if you are using a virtualenv, to run the local development
version of Mu you should run the following command in the root of this
project::

    (mu-venv) $ python run.py

There is a Makefile that helps with most of the common workflows associated
with development. Typing "make" on its own will list the options thus::

    $ make

    There is no default Makefile target right now. Try:

    make clean - reset the project and remove auto-generated assets.
    make pyflakes - run the PyFlakes code checker.
    make pycodestyle - run the PEP8 style checker.
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
with the PSF's code of conduct found in the CODE_OF_CONDUCT.rst file in this
repository.
