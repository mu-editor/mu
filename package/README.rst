Packing Mu
==========

Install dependencies
--------------------

Windows
+++++++

Please ensure you use the specified versions in the instructions below. We've
found the latest versions of some of these packages are not always backwards
compatible with each other.

* Install the 32bit version of Python 3.4 from the `official website <https://www.python.org/downloads/>`_.
* Install the PyQt5 binary package from `riverbankcomputing <https://riverbankcomputing.com/software/pyqt/download>`_ (specifically, `this one <https://riverbankcomputing.com/software/pyqt/download5>`_).
* Install PyInstaller using pip or pip3 (includes pypiwin32)::

    $ pip install pyinstaller==3.1.1

If in doubt, look in the details of the ``appveyor.yml`` file in the root of
this repository.

Mac OS X
++++++++

Assuming you have the `Homebrew <http://brew.sh/>`_ package manager installed:

* Install Python 3::

    $ brew update
    $ brew install python3

* Install the PyQt5 binary package::

    $ pip3 install PyQt5

* Install the QScintilla2 package using the formula in the `extras` directory::

    $ pip3 install QScintilla

* Install PyInstaller::

    $ pip3 install pyinstaller

Linux
-----

Assuming you are running a Linux distribution with apt.

* Install Python 3::

    $ sudo apt-get update
    $ sudo apt-get install python3

* Install PyQt5::

    $ sudo apt-get install python3-pyqt5 python3-pyqt5.qsci python3-pyqt5.qtserialport

* Install PyInstaller::

    $ pip3 install pyinstaller


Package Mu
----------

From the project root directory, run::

    $ pyinstaller package/pyinstaller.spec

The single file executable should be saved in `/dist/mu`, `/dist/mu.exe`, or `/dist/mu.app`.

The spec file `package/pyinstaller.spec` can be edited to simplify packaging debugging.


Run the executable
------------------

On Windows you can simply double-click the `mu.exe` file.

On Linux ensure the file permissions are set to executable and, from the file location, run::

    $ ./mu

On OS X double click on the `mu.app`, if trying to run the downloadable version, right click on the file and select `open`.


Download the Mu executable
--------------------------

.. image:: https://ci.appveyor.com/api/projects/status/agr9wmestx3t1tcl/branch/master?svg=true
    :target: https://ci.appveyor.com/project/carlosperate/mu

.. image:: https://travis-ci.org/mu-editor/mu.svg?branch=master
    :target: https://travis-ci.org/mu-editor/mu

You can download the latest executable build of Mu for your respective operating system from the following links:

* `Windows <http://mu-builds.s3-website.eu-west-2.amazonaws.com/?prefix=windows/>`_
* `Mac OS X <http://mu-builds.s3-website.eu-west-2.amazonaws.com/?prefix=osx/>`_
* `Linux <http://mu-builds.s3-website.eu-west-2.amazonaws.com/?prefix=linux/>`_
