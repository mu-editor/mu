Development
===========

.. Much of this information is also in the README.rst file at the top level.
   If you are updating one, remember to update the other.

If you only want to use Mu as a code editor then ignore this section. If you'd
like to contribute to the development of Mu, please read on...

The source code is hosted on GitHub. Please feel free to fork the repository.
Assuming you have Git installed, you do it like this from the command line::

    git clone https://github.com/mu-editor/mu.git

For Mu to work you'll need to have Qt5 and Python 3 installed.

* On Debian based systems this is covered by installing: ``python3-pyqt5``,
  ``python3-pyqt5.qsci``, ``python3-pyqt5.qtserialport`` and ``python3-pyqt5.qtwebkit``.

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

    pip install -r requirements.txt

To run the local development version of Mu, in the root of this repository
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
    make docs - run sphinx to create project documentation.

.. include:: ../CONTRIBUTING.rst
