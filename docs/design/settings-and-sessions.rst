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

The `load` function merges into the existing settings. Most commonly this means
it'll be preceded by a call to `reset`. But it could be used to implement a
cascade of settings, eg where an admin sets site-wide settings which are then
overridden by user settings.

Amnesia / Read-only / Reset modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To support the possible "modes" above -- amnesia, read-only etc. there is a
`readonly` flag on each settings object, preventing it from being written to
disc; and a `reset` method which will return to default settings. This last
can be used either to "forget" any loaded or set settings; or before reloading
from a different file.

So *amnesia mode* is implemented by calling `reset` without `load` and settings `readonly`.
*Read-only mode* is implemented by calling `reset` followed by `load` and setting `readonly`
And *reset mode* is implemented by calling `reset` without `load` and *not* setting `readonly`

Implemented via:
~~~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/pull/1200

Discussion in:
~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/issues/1184
