Session & Settings Data
=======================

Decision
--------

*(Draft - to be discussed / agreed)*

Mu maintains two files, automatically saved on exit, to hold user settings
and session data. The former contains critical parameters without which the
editor probably won't function. The latter contains more or less cosmetic
items which can be cleared (eg by a "Reset" button) without losing functionality.


Background
----------

Historically access to these files has been somewhat scattered around the
codebase, making it difficult for modules to access them coherently. The
first aim of the re-implementation is to create globally-accessible singletons,
much as is conventional for logging. Those "settings" objects would offer
a dictionary-like interface so that code could easily do::

    import settings

    def set_new_theme(theme):
        ...
        settings.session['theme'] = theme.name

The second aim is, possibly, to reconsider the use of the settings, or their
structures, or which / how many files they are and where they're situated.
Any such refactoring or restructuring should be a lot easier with a newer
implementation.


Discussion and Implementation
-----------------------------

Open questions:

* How many / which files do we need?
* Should we combine both settings / sessions into one file? Is there a meaningful difference which we want to maintain? [+0.5]
* Should we register exit handlers so the files are always saved on closedown? [+1]
* Should we write files to disc as soon as they are updated? [-0]
* Should we re-read files to allow users to update them mid-session? [-1]
* Should we implement read-only mode (ie the existing file is loaded but not written back)? [+0]
* Should we implement amnesia mode (ie the file is neither loaded nor written back)? [+1]
* Should we implement reset mode (ie the file is not loaded but is written back)? [+0]
* Should we break out the virtual environment settings (venv location, baseline packages) into its own file? [+1]
* What levels of config do we need? Defaults? One/multiple settings files? Override at instance level?
* Do we still need to look in the application directory as well as the data directory? [-0]

Exit Handlers
~~~~~~~~~~~~~

Registered exit handlers to ensure that files are saved when Mu exits. (This
could probably be alternatively achieved within the Qt app). The advantage of
this is that the save is automatic; the disadvantage is that it's a little
hidden.

Not currently writing to disc as soon as updated: having an exit handler ensures
the settings will be written, even in the event of an unhandled exception.
And it's not clear what advantage an "autosave" would offer.


Levels of Config
~~~~~~~~~~~~~~~~

Allowing three levels of data: the defaults for each setting type, held in
a class dictionary; possible overrides at class instantiation [I'm not clear
where this would be used; it can probably go]; and the .json files.

The ``load`` function merges into the existing settings. Most commonly this means
it'll be preceded by a call to ``reset``. But it could be used to implement a
cascade of settings, eg where an admin sets site-wide settings which are then
overridden by user settings.

Amnesia / Read-only / Reset modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To support the possible "modes" above -- amnesia, read-only etc. there is a
``readonly`` flag on each settings object, preventing it from being written to
disc; and a ``reset`` method which will return to default settings. This last
can be used either to "forget" any loaded or set settings; or before reloading
from a different file.

So *amnesia mode* is implemented by calling ``reset`` without ``load`` and settings ``readonly``.
*Read-only mode* is implemented by calling ``reset`` followed by ``load`` and setting ``readonly``
And *reset mode* is implemented by calling ``reset`` without ``load`` and *not* setting ``readonly``

Failure modes
~~~~~~~~~~~~~

It's critical that we should recover well from not being able to read or to
write settings files, whether that's a file system failure or invalid JSON.
Regardless of the approach we should definitely log any exception, or log a
warning where there's no exception as such but, say, a missing file.

Reading
+++++++

* A failure to find/open a settings file is considered usual: it's expected
  that, the first time around, a user settings file won't exist to be read.
  The loader will log a warning and carry on as though it had found it empty
* A failure to read the JSON from a settings file is more complicated. For
  pragmatic purposes, the intention is here is: log a warning; quarantine the
  file; and carry on as though it had been found empty. That way the editor
  continues to work, albeit in "reset" mode, and the failing file is available
  for debugging.

  Not quite clear: should we automatically enter read-only mode in this situation?

Writing
+++++++

* A failure to open a settings file to write to is more problematic, and there's
  not very much we can do. Log the exception (eg AccessDenied or whatever).
  Perhaps -- given that the text won't be great -- pushign the JSON output to
  the logs as debug might give some manual fallback.
* A failure to *write* JSON is less probable -- although it does happen during
  testing where the JSON lib attempts to serialise a Mock object. Here, we can't
  really do more than log the exception and fail gracefully.

Implemented via:
~~~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/pull/1200

Discussion in:
~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/issues/1184
