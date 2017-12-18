Developer Setup
===============

.. Much of this information is also in the README.rst file at the top level.
   If you are updating one, remember to update the other.

The source code is hosted on GitHub. Fork the repository with the following
command::

  git clone https://github.com/mu-editor/mu.git

For Mu to work you'll need to have Qt5 and Python 3. **Mu does not and never
will use or support Python 2**. The requirements for the project should be met
by using Python's ``pip`` command with the ``requirements.txt`` file::

    pip install -r requirements.txt

.. warning:: This will only work on Windows, OSX and Linux (x86, amd64).
  
    The binary wheels for Raspberry Pi's arm platform don't exist for PyQt.
    However, you can meet the required dependencies by installing:
    ``python3-pyqt5``, ``python3-pyqt5.qsci`` and
    ``python3-pyqt5.qtserialport`` packages with ``apt-get``. If you're using
    a virtual environment on the Raspberry Pi remember to use the
    ``--system-site-packages`` flag.

To run the local development version of Mu, in the root of the repository
type::

  python3 run.py

There is a Makefile that helps with most of the common workflows associated
with development. Typing ``make`` on its own will list the options thus::

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

Everything should be working if you can successfully run::

  make check

(You'll see the results from various code quality tools, the test suite and
code coverage.)
