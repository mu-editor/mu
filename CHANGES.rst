Release History
===============

1.0.0.beta.11
-------------

* Updated Python 3 REPL to make use of an out of process iPython kernel (to avoid problems with blocking Mu's UI).
* Reverted Save related functionality to prior behaviour.
* The "Save As" dialog for re-naming a file is launched when you click the filename in the tab associated with the code.

1.0.0.beta.10
-------------

* Ensured "Save" button prompts user to confirm (or replace) the filename of an existing file. Allows Mu to have something like "Save As".
* Updated to latest microfs library for working with the micro:bit's filesystem.
* Fixed three code quality warnings found by https://lgtm.com/projects/g/mu-editor/mu/alerts/?mode=list
* Updated API generation so the output is ordered (helps when diffing the generated files).
* Updated Makefile to create Python packages/wheels and deploy to PyPI.
* Explicit versions for packages found within install_requires in setup.py. 
* Minor documentation changes.

1.0.0.beta.9
------------

* Debian related packaging updates.
* Fixed a problem relating to how Windows stops the debug runner.
* Fixed a problem relating to how Windows paths are expressed that was stopping the debug runner from starting.

1.0.0.beta.8
------------

* Updated splash image to reflect trademark usage of logos.
* Refactored the way the Python runner executes so that it drops into the Python shell when it completes.
* The debug runner now reports when it has finished running a script.

1.0.0.beta.7
------------

* Update PyInstaller icons.
* Fix some tests that fail on older version of Python 3.
* Add scripts to extract API information from Adafruit and Python 3.
* Add generated API documentation to Mu so autosuggest and call tips have data.
* Ensure translation files are distributed.

1.0.0.beta.6
------------

* Pip installable.
* Updated theme handling: day, night and high-contrast (as per user feedback).
* Keyboard shortcuts.

1.0.0.beta.*
------------

* Added modes to allow Mu to be a general Python editor. (Python3, Adafruit and micro:bit.)
* Added simple visual debugger.
* Added iPython based REPL for Python3 mode.
* Many minor UI changes based on UX feedback.
* Many bug fixes.

0.9.13
------

* Add ability to change default Python directory in the settings file. Thanks to Zander Brown for the contribution. See #179.

0.9.12
------

* Change the default Python directory from ``~/python`` to ``~/mu_code``. This fixes issue #126.
* Add instructions for installing PyQt5 and QScintilla on Mac OS.
* Update to latest version of uFlash.
* Add highlighting of search mathes.
* Check if the script produced is > 8k.
* Use a settings file local to the Mu executable if available.
* Fix bug with highlighting code errors in Windows.
* Check to overwrite an existing file on the micro:bit FS.
* Start changelog
