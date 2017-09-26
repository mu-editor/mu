Release History
===============

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
