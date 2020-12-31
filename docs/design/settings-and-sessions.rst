Session & Settings Data
=======================

Decision
--------

Centralise access to settings inside a standalone module offering a
dictalike-interface. The settings can be loaded from and saved to files.
This currently uses JSON (as we have historically) but https://github.com/mu-editor/mu/issues/1203
is tracking the possibility of using TOML or some other format.

Settings objects have defaults which are overridden by values loaded from file
or set programatically. When the settings are saved, only values overriding
the defaults are saved.

The ``load`` method can be called several times for the same settings; values in
each one override any corresponding existing values. The last loaded filename
is the file which the settings will be saved to. Both load and save attempt to
be robust, carrying on with warnings in the log if files can't be found, open,
read etc.

The existing files (session.json, settings.json) are implemented as singletons
in the settings module, and settings.json is autosaved. New settings to support
venv functionality -- in particular, baseline packages -- is also added.

At its simplest https://github.com/mu-editor/mu/pull/1200 does no more than
implement this set of functionality. The few places in existing code where
settings were used or altered have been updated to use the new objects and
functionality.

Not Implemented / Hooks
-----------------------

During the design and/or based on previous discussions, several ideas were
floated which are at least supported by the new implementation.

* Safe mode / Readonly mode / Reset mode

  As described below, there are situations where teachers or admins would
  like to reset settings for use in a club or classroom setting. The new
  implementation supports this idea via the ``reset`` method and ``readonly``
  flags without actually implementing it as such.

  Such functionality might, in the future, be managed by means of command-line
  switches or some other flag.

* File format: JSON, YAML, TOML...

  The implementation tries to be agnostic as to file format. At present it
  uses the historically-implemented JSON format. But the choice of serialiser
  is centralised towards the top of the module and shouldn't be hard to change,
  especially for any serialiser which uses the conventional ``.dumps``, ``.loads``
  API.

  cf https://github.com/mu-editor/mu/issues/1203

* One file / Two files?

  The new settings implementation facilitates any number of files each of
  which can have an arbitrary hierarchy. Whether we end up with one settings
  file containing, eg, session settings and board settings, or several files
  each specific to an area can be decided later. Nothing in this implementation
  precludes either approach.

* Interpolation

  Because it is easy to implement and doesn't seem risky, this implementation
  applies ``os.path.expandvars`` to any values retrieved. This will do
  platform-sensitive env var expansion so admins can specify, eg, a workspace
  directory of %USERPROFILE%\mu_code or $HOME/.mu/mu_code.

  Value interpolation (where one settings value can rely on another) has *not*
  been implemented. It's potentially quite an involved piece of work, and the
  benefit is not so clear.

* Indicating failure to users

  This is obviously a wider issue, but while this implementation tries to be
  robust when loading / saving settings, it only writes to the standard logs
  and then fails quietly. The problem here is that we're possibly not operating
  within the UI. At the least, we don't have a good overall story for a UI
  which isn't part of the central editor itself.

Background
----------

Mu maintains two files, automatically saved on exit, to hold user settings
and session data. The former contains critical parameters without which the
editor probably won't function. The latter contains more or less cosmetic
items which can be cleared (eg by a "Reset" button) without losing functionality.

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
* Should we combine both settings / sessions into one file? Is there a meaningful difference which we want to maintain? [+1]
* Should we register exit handlers so the files are always saved on closedown? [+1]
* Should we write files to disc as soon as they are updated? [-0]
* Should we re-read files to allow users to update them mid-session? [-1]
* Should we implement read-only mode (ie the existing file is loaded but not written back)? [+0]
* Should we implement safe mode (ie the file is neither loaded nor written back)? [+1]
* Should we implement reset mode (ie the file is not loaded but is written back)? [+0]
* Should we break out the virtual environment settings (venv location, baseline packages) into its own file? [+1]
* Could we add a boards.json file to allow users to add new/variant configurations? [+0]
* What levels of config do we need? Defaults? One/multiple settings files? Override at instance level?
* Do we still need to look in the application directory as well as the data directory? [-0]
* What format should the files use? [cf https://github.com/mu-editor/mu/issues/1203]
* Should we save everything every time? [-0.5]
* Do we need interpolation of other settings? (eg ROOT_DIR = abc; WORK_DIR = %(ROOT_DIR)/xyz)
* Do we need interpolation of env vars? (eg ROOT_DIR = %USERPROFILE%\mu_code) [+0.5]
* Should we merge ``settings.py`` into ``config.py`` [+0]
* Should settings (as opposed to sessions) be read-only? [+1]

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

So *Safe mode* is implemented by calling ``reset`` without ``load`` and setting ``readonly``.
*Read-only mode* is implemented by calling ``reset`` followed by ``load`` and setting ``readonly``
And *Reset mode* is implemented by calling ``reset`` without ``load`` and *not* setting ``readonly``

The use cases here would be mostly for admins or leaders who needed, eg,
to ensure that new sessions were started for every user, or who needed to debug
or recover from a corrupt settings file.

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

Levels of Config & Defaults
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The thrust of this proposal expects the `Settings` subclass to hold a dictionary
of defaults at class level. These are applied first before any file is loaded.
Any information from a loaded file is overlaid, so the file data "wins". Any
values not present in the file remain per the default.

Although not implemented in any way at present, the mechanism allows for several
files to be loaded in succession, typically for a site-wide file, set up by
an administrator, followed by a user-specific file. In this scenario, the data
would be read: Defaults < Site settings < User settings with later data
replacing earlier data.

The presence of the defaults in the `Settings` subclass should also make for
a more consistent use of defaults across the codebase. Eg if in general device
timeouts should be 2 seconds but can be changed, one piece of code might do::

    timeout_s = settings.user.get('timeout_s', 2)

while another piece elsewhere might do::

    timeout_s = settings.user.get('timeout_s', 3)

If the defaults are present in the class, the `.get` method could be implemented
so the default, instead of `None` as conventional, returns the class default::

    timeout_s = settings.user.get('timeout_s')
    # with no explicit timeout_s setting, timeout_s is now the default value

Taking this further, it's not clear that we even need to load the defaults as
such; we could always just fall back to them in the event of a .get KeyError
or even a __getitem__ KeyError. Taking that approach would also means we wouldn't
need the "dirty data" mechanism because anything in the ``_Settings`` object's own
``_dict`` should be saved out at the end.

Saving Everything?
~~~~~~~~~~~~~~~~~~

Implicit in the new design is the idea that settings are saved out to file(s) at
the end of every session.

Originally, the effect of the defaults was that, say, a workspace directory would
inherit the default which will then be written out to the settings file at the
end of the session. Even if that file had not originally had a settings for the
workspace directory.

On reflection, I've re-implemented for now a "dirty" setting for each attribute.
Only "dirty" attributes are written out to file. Anything loaded from a file
is considered "dirty" even if it remains unchanged for the duration of the
session. Anything updated during the session -- and this will typically be
user-configurable items like Zoom level, Theme &c. -- is also tagged as "dirty"
and will be written out to file.


Implemented via:
~~~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/pull/1200

Discussion in:
~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/issues/1184
* https://github.com/mu-editor/mu/issues/1203
