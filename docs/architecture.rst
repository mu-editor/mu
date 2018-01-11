Mu's Architecture
-----------------

This section provides a high level overview of how the various parts of Mu
fit together.

Key Concepts
============

The key concepts you should know are:

* Mu uses the `PyQT5 framework <https://riverbankcomputing.com/software/pyqt/intro>`_ (that makes the `Qt <https://www.qt.io/>`_ GUI toolkit available to Python) for making its user interface.
* Mu is a modal editor: the behaviour of Mu changes, depending on mode.
* There are a number of core features and behaviours that are always available and never vary, no matter the mode.
* The text area into which users type code is based on a `Scintilla <http://www.scintilla.org/>`_ based widget.
* Mu is easy to internationalise using Python's standard ``gettext`` based modules and tools.
* Mu's code base is small, well documented and has 100% unit test coverage.

Code Structure
==============

The code is found in the ``mu`` directory and organised in the following way:

* The application is created and configured in ``app.py``.
* Most of the fundamental logic for Mu is in ``logic.py``.
* Un-packaged third party code used by Mu is found in ``contrib``.
* The Python3 debugger consists of a debug client and debug runner found in the ``debugger`` namespace. A description of how the debugger works can be found in :doc:`debugger`.
* Interacting with the UI layer is done via the ``Window`` class in the ``interface.main`` module. Mu specific UI code used by the ``Window`` class found in the other modules in the namespace.
* Internationalization (I18n) related assets are found under ``locale``. Learn how this works via :doc:`translations`.
* Modes are found under the ``modes`` namespace. They all inherit from a ``BaseMode`` class and there's a tutorial for :doc:`modes`. 
* Graphical assets, fonts and CSS descriptions for the themes are all found under ``resources``.

All classes, methods and functions have documentation *written for humans*.
These are extracted into the :doc:`api`.

:doc:`tests` is in the ``test`` directory and filenames for tests relate
directly to the file they test in the Mu code base. The module / directory
structure mirrors the organisation of the Mu code base. We use PyTest's assert
based unit testing. All tests have a comment describing their intent.

The documentation you're reading right now (i.e. that written for developers)
is found in the ``docs`` directory. We use `Sphinx <http://www.sphinx-doc.org/en/stable/>`_
to write our docs and host them on `ReadTheDocs <https://mu.readthedocs.io/en/latest/>`_.
Other documentation (tutorials, user help and so on) is on :doc:`website`.

The ``utils`` directory contains various scripts used to scrape and / or build
the API documentation used by Mu's autocomplete and call tip functionality.

The other assets in the root directory of the project are mainly for
documentation (such as our Code of Conduct), configuration (for testing) or
packaging for various platforms (see :doc:`packaging`).

If you want to make changes please read :doc:`contributing`.
