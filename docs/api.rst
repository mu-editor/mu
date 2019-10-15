Mu API Reference
----------------

This API reference is automatically generated from the docstrings found within
the source code. It's meant as an easy to use and easy to share window into the
code base.

Take a look around! The code is simple and short.

``mu.app``
==========

The Mu application is created and configured in this module.

.. automodule:: mu.app
    :members:

``mu.logic``
============

Most of the fundamental logic for Mu is in this module.

.. automodule:: mu.logic
    :members:

``mu.debugger``
===============

The debugger consists of two parts:

* Client - used by Mu to process messages from the process being debugged.
* Runner - created in a new process to run the code to be debugged.

Messages are passed via inter-process communication.

``mu.debugger.client``
++++++++++++++++++++++

Code used by the Mu application to communicate with the process being debugged.

.. automodule:: mu.debugger.client
    :members:

``mu.debugger.runner``
++++++++++++++++++++++

The runner code controls the debug process.

.. automodule:: mu.debugger.runner
    :members:

``mu.interface``
================

This module contains all the PyQt related code needed to create the user
interface for Mu. All interaction with the user interface is done via the
``Window`` class in ``mu.interface.main``.

All the other sub-modules contain different bespoke aspects of the user
interface.

``mu.interface.main``
+++++++++++++++++++++

Contains the core user interface assets used by other parts of the application.

.. automodule:: mu.interface.main
    :members:

``mu.interface.dialogs``
++++++++++++++++++++++++

Bespoke modal dialogs required by Mu.

.. automodule:: mu.interface.dialogs
    :members:

``mu.interface.editor``
+++++++++++++++++++++++

Contains the customised Scintilla based editor used for textual display and
entry.

.. automodule:: mu.interface.editor
    :members:

``mu.interface.panes``
++++++++++++++++++++++

Contains code used to populate the various panes found in the user interface
(REPL, file list, debug inspector etc...).

.. automodule:: mu.interface.panes
    :members:

``mu.interface.themes``
+++++++++++++++++++++++

Theme related code so Qt changes for each pre-defined theme.

.. automodule:: mu.interface.themes
    :members:

``mu.modes``
============

Contains the definitions of the various modes Mu into which Mu can be put. All
the core functionality is in the ``mu.modes.base`` module.

``mu.modes.base``
+++++++++++++++++

Core functionality and base classes for all Mu's modes. The definitions of
API autocomplete and call tips can be found in the ``mu.modes.api`` namespace.

.. automodule:: mu.modes.base
    :members:

``mu.modes.circuitpython``
++++++++++++++++++++++++++

CircuitPython mode for Adafruit boards (and others).

.. automodule:: mu.modes.circuitpython
    :members:

``mu.modes.debugger``
+++++++++++++++++++++

The Python 3 debugger mode.

.. automodule:: mu.modes.debugger
    :members:

``mu.modes.microbit``
+++++++++++++++++++++

The original BBC micro:bit mode.

.. automodule:: mu.modes.microbit
    :members:

``mu.modes.pygamezero``
+++++++++++++++++++++++

The Pygame Zero / pygame mode.

.. automodule:: mu.modes.pygamezero
    :members:

``mu.modes.python3``
++++++++++++++++++++

The Python 3 editing mode.

.. automodule:: mu.modes.python3
    :members:

``mu.resources``
================

Contains utility functions for working with binary assets used by Mu (mainly
images).

.. automodule:: mu.resources
    :members:
