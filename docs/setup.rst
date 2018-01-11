Developer Setup
===============

The source code is hosted on GitHub. Fork the repository with the following
command::

  git clone https://github.com/mu-editor/mu.git

**Mu does not and never will use or support Python 2**. You should use Python
3.5 or above.

Windows, OSX, Linux
+++++++++++++++++++

On all platforms except the Raspberry Pi, to create a working development
environment install all the dependencies into your virtualenv via the
``requirements.txt`` file::

    pip install -r requirements.txt

.. warning::

    Sometimes, having several different versions of PyQt installed on your
    machine can cause problems (see
    `this issue <https://github.com/mu-editor/mu/issues/297>`_ for example).

    Using a virtualenv will ensure your development environment is safely
    isolated from such problematic version conflicts.
    
    If in doubt, throw away your virtualenv and start again with a fresh
    install from ``requirements.txt`` as per the instructions above.

Raspberry Pi
++++++++++++

If you are working on a Raspberry Pi there are three steps to create a working
development environment:

1. Install the packaged Qt related dependencies::

    apt-get install python3-pyqt5 python3-pyqt5.qsci python3-pyqt5.qtserialport python3-dev

2. Create a virtualenv that uses Python 3 and allows the virtualenv access
   to the packages installed on your system via the ``--system-site-packages``
   flag::

    virtualenv -p /usr/local/bin/python3 --system-site-packages ~/mu-venv

3. With the virtualenv enabled, pip install the Python packages for the
   Raspberry Pi via the ``requirements-pi.txt`` file::

    (mu-venv) $ pip install -r requirements-pi.txt

Running Development Mu
++++++++++++++++++++++

.. note:: From this point onwards, instructions assume that you're using
   a virtual environment.

On all platforms, to run the local development version of Mu, in the root of
the repository type::

  python run.py

Using ``make``
++++++++++++++

There is a Makefile that helps with most of the common workflows associated
with development. Typing ``make`` on its own will list the options thus::

    $ make

    There is no default Makefile target right now. Try:

    make run - run the local development version of Mu.
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

Everything should be working if you can successfully run::

  make check

(You'll see the results from various code quality tools, the test suite and
code coverage.)

.. note::

    On Windows there is a ``make.cmd`` file that works in a similar way to the
    ``make`` command on Unix-like operating systems.

Before Submitting
+++++++++++++++++

Before contributing code please make sure you've read :doc:`contributing` and
follow the checklist for contributing changes. We expect everyone participating
in the development of Mu to act in accordance with the PSF's
:doc:`code_of_conduct`.
