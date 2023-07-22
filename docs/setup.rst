Developer Setup
===============

The source code is hosted on GitHub. Fork the repository with the following
command::

  git clone https://github.com/mu-editor/mu.git

**Mu does not and never will use or support Python 2**. You should use Python
3.5 or above.

Windows, OSX, Linux
+++++++++++++++++++

Create a working development environment by installing all the dependencies
into your virtualenv with::

    pip install -e ".[dev]"

.. note::

    The Mu package distribution, as specified in ``setup.py``, declares
    both runtime and extra dependencies.

    The above mentioned ``pip install -e ".[dev]"`` installs all runtime
    dependencies and most development ones: it should serve nearly everyone.

    For the sake of completeness, however, here are a few additional details.
    The ``[dev]`` extra is actually the aggregation of the following extras:

    * ``[tests]`` specifies the testing dependencies, needed by ``make test``.
    * ``[docs]`` specifies the doc building dependencies, needed by ``make docs``.
    * ``[i18n]`` specifies the translation dependencies, needed by ``make translate_*``.
    * ``[package]`` specifies the packaging dependencies needed by ``make win32``,
      ``make win64``, ``make macos``, or ``make dist``.

    Additionally, the following extras are defined:

    * ``[utils]`` specifies the dependencies needed to run the utilities
      under the ``utils`` directory. It has been specifically excluded from
      the ``[dev]`` extra for two reasons: i) on the Windows platform, it
      requires a C compiler to be installed (as of this writing), and
      ii) running such utilities is seldom needed in Mu's development process.
    * ``[all]`` includes all the dependencies in all extras.


.. warning::

    Sometimes, having several different versions of PyQt installed on your
    machine can cause problems (see
    `this issue <https://github.com/mu-editor/mu/issues/297>`_ for example).

    Using a virtualenv will ensure your development environment is safely
    isolated from such problematic version conflicts.

    If in doubt, throw away your virtualenv and start again with a fresh
    install as per the instructions above.

    On Windows, use the venv module from the standard library to avoid an
    issue with the Qt modules missing a DLL::

        py -3 -mvenv .venv

    Virtual environment setup can vary depending on your operating system.
    To learn more about virtual environments, see this `in-depth guide from Real Python <https://realpython.com/python-virtual-environments-a-primer/>`_.


Running Development Mu
++++++++++++++++++++++

.. note:: From this point onwards, instructions assume that you're using
   a virtual environment.

To run the local development version of Mu, in the root of the repository type::

  python run.py

An alternative form is to type::

  python -m mu

Yet another one is typing::

  mu-editor


Running Development Mu on Newer MacBook Machines
++++++++++++

If you are working on a newer Apple computers using ARM architecture, an error regarding PyQt may occur due to system incompatibility.

In this case, switch to the pyqt6 branch and make a few changes to the setup.py file before installing the dependencies and run Mu again locally.

In the setup.py file on the pyqt6 branch, you'll find the following lines::
  
  "PyQt6==6.3.1"
  + ';"arm" not in platform_machine and "aarch" not in platform_machine',
  "PyQt6-QScintilla==2.13.3"
  + ';"arm" not in platform_machine and "aarch" not in platform_machine',
  "PyQt6-Charts==6.3.1"
  + ';"arm" not in platform_machine and "aarch" not in platform_machine',

Remove the lines for Rasberry Pi and leave only the following lines:

  "PyQt6==6.3.1",
  "PyQt6-QScintilla==2.13.3",
  "PyQt6-Charts==6.3.1",

Once the changes are saved, install the dependencies and Mu should be up and running.

Since this workaround is only for newer Mac users, when you are committing your changes, be careful to not commit it. 

And when you are making pull request, merge it to main or master instead of pyqt6. 


Raspberry Pi
++++++++++++

If you are working on a Raspberry Pi there are additional steps to create a
working development environment:

1. Install required dependencies from Raspbian repository::

    sudo apt-get install python3-pyqt5 python3-pyqt5.qsci python3-pyqt5.qtserialport python3-pyqt5.qtsvg python3-dev python3-gpiozero python3-pgzero libxmlsec1-dev libxml2 libxml2-dev

2. If you are running Raspbian Buster or newer you can also install this
   optional package::
   
    sudo apt-get install python3-pyqt5.qtchart

3. Create a virtualenv that uses Python 3 and allows the virtualenv access
   to the packages installed on your system via the ``--system-site-packages``
   flag::

    sudo pip3 install virtualenv
    virtualenv -p /usr/bin/python3 --system-site-packages ~/mu-venv

4. Activate the virtual environment ::

    source ~/mu-venv/bin/activate

5. Clone mu::

    (mu-venv) $ git clone https://github.com/mu-editor/mu.git ~/mu-source

6. With the virtualenv enabled, pip install the Python packages for the
   Raspberry Pi with::

    (mu-venv) $ cd ~/mu-source
    (mu-venv) $ pip install -e ".[dev]"

7. Run mu::

     python run.py

   An alternative form is to type::

     python -m mu

   Or even::

     mu-editor

.. warning::

    These instructions for Raspberry Pi only work with Raspbian version
    "Stretch".

    If you use ``pip`` to install Mu on a Raspberry Pi, then the PyQt related
    packages will not be automatically installed from PyPI. This is why you
    need to use ``apt-get`` to install them instead, as described in step 1,
    above.

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
    make win32 - create a 32bit Windows installer for Mu.
    make win64 - create a 64bit Windows installer for Mu.
    make macos - create a macOS native application for Mu.
    make video - create an mp4 video representing code commits.

Everything should be working if you can successfully run::

  make check

(You'll see the results from various code quality tools, the test suite and
code coverage.)

.. note::

    On Windows there is a ``make.cmd`` file that works in a similar way to the
    ``make`` command on Unix-like operating systems.

.. warning::

    In order to use the MicroPython REPL via USB serial you may need to add
    yourself to the ``dialout`` group on Linux.

Before Submitting
+++++++++++++++++

Before contributing code please make sure you've read :doc:`contributing` and
follow the checklist for contributing changes. We expect everyone participating
in the development of Mu to act in accordance with the PSF's
:doc:`code_of_conduct`.
