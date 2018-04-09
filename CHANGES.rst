Release History
---------------

1.0.0.beta.16
=============

* Updated flashing in micro:bit mode so it is more robust and doesn't block
  on Windows. Thank you to Carlos Pereira Atencio for issue #350 and the polite
  reminder.
* Updated the mu-debug runner so if the required filename for the target isn't
  passed into the command, a helpful message is displayed to the user.
* Developer documentation updates.
* Updated to the latest version of uflash, which contains the latest stable
  release of MicroPython for the micro:bit. Many thanks to Damien George for
  all his continuing hard work on MicroPython for the micro:bit.
* Inclusion of tkinter, turtle, gpiozero, guizero, pigpio, pillow and requests
  libraries as built-in modules.

1.0.0.beta.15
=============

* A new plotter works with CircuitPython and micro:bit modes. If you emit
  tuples of numbers via the serial connection (e.g. ``print((1, 2, 3))`` as
  three arbitrary values) over time these will be plotted as line graphs.
  Many thanks to Limor "ladyada" Fried for contributing code for this feature.
* Major refactoring of how Mu interacts with connected MicroPython based boards
  in order to enable the plotter and REPL to work independently.
* Mu has a new mode for Pygame Zero (version 1.1). Thanks to Dan Pope for
  Pygame Zero and Rene Dudfield for being Pygame maintainer.
* It's now possible to run mu "python3 -m mu". Thanks to Cefn Hoile for the
  contribution.
* Add support for pirkey Adafruit board. Thanks again Adafruit.
* Updated all the dependencies to the latest upstream versions.
* Various minor bug fixes and guards to make Mu more robust (although this will
  always be bugs!).

1.0.0.beta.14
=============

* Add new PythonProcessPanel to better handle interactions with child
  Python3 processes. Includes basic command history and command editing.
* Move the old "run" functionality in Python3 mode into a new "Debug" button.
* Create a new "Run" button in Python3 mode that uses the new
  PythonProcessPanel.
* Automation of 32bit and 64bit Windows installers (thanks to Thomas Kluyver
  for his fantastic pynsist tool).
* Add / revise developer documentation in light of changes above.
* (All the changes mentioned above were supported by the Raspberry Pi
  Foundation -- Thank you!)
* Update / add USB PIDs for Adafruit boards (thanks Adafruit for the heads up).
* Minor cosmetic changes.
* Additional test cases.

1.0.0.beta.13
=============

* Fix to solve problem when restoring CircuitPython session when device is not
  connected.
* Fix to solve "data terminal ready" (DTR) problem when CircuitPython expects
  DTR to be set (and it isn't by default in Qt).
* Added initial work on developer documentation found here: http://mu.rtfd.io/
* Updates to USB PIDs for Adafruit boards.
* Added functionally equivalent "make.py" for Windows based developers.
* Major refactor of the micro:bit related "files" UI pane: it no longer blocks
  the main UI thread.

1.0.0.beta.12
=============

* Update "save" related behaviour so "save as" pops up when the filename in the tab is double clicked.
* Update the debugger so the process stops at the end of the run.
* Ensure the current working directory for the REPL is set to mu_mode.
* Add additional documentation about Raspberry Pi related API.
* Update micro:bit runtime to lates MicroPython beta.
* Make a start on developer documentation.

1.0.0.beta.11
=============

* Updated Python 3 REPL to make use of an out of process iPython kernel (to avoid problems with blocking Mu's UI).
* Reverted Save related functionality to prior behaviour.
* The "Save As" dialog for re-naming a file is launched when you click the filename in the tab associated with the code.

1.0.0.beta.10
=============

* Ensured "Save" button prompts user to confirm (or replace) the filename of an existing file. Allows Mu to have something like "Save As".
* Updated to latest microfs library for working with the micro:bit's filesystem.
* Fixed three code quality warnings found by https://lgtm.com/projects/g/mu-editor/mu/alerts/?mode=list
* Updated API generation so the output is ordered (helps when diffing the generated files).
* Updated Makefile to create Python packages/wheels and deploy to PyPI.
* Explicit versions for packages found within install_requires in setup.py. 
* Minor documentation changes.

1.0.0.beta.9
============

* Debian related packaging updates.
* Fixed a problem relating to how Windows stops the debug runner.
* Fixed a problem relating to how Windows paths are expressed that was stopping the debug runner from starting.

1.0.0.beta.8
============

* Updated splash image to reflect trademark usage of logos.
* Refactored the way the Python runner executes so that it drops into the Python shell when it completes.
* The debug runner now reports when it has finished running a script.

1.0.0.beta.7
============

* Update PyInstaller icons.
* Fix some tests that fail on older version of Python 3.
* Add scripts to extract API information from Adafruit and Python 3.
* Add generated API documentation to Mu so autosuggest and call tips have data.
* Ensure translation files are distributed.

1.0.0.beta.6
============

* Pip installable.
* Updated theme handling: day, night and high-contrast (as per user feedback).
* Keyboard shortcuts.

1.0.0.beta.*
============

* Added modes to allow Mu to be a general Python editor. (Python3, Adafruit and micro:bit.)
* Added simple visual debugger.
* Added iPython based REPL for Python3 mode.
* Many minor UI changes based on UX feedback.
* Many bug fixes.

0.9.13
======

* Add ability to change default Python directory in the settings file. Thanks to Zander Brown for the contribution. See #179.

0.9.12
======

* Change the default Python directory from ``~/python`` to ``~/mu_code``. This fixes issue #126.
* Add instructions for installing PyQt5 and QScintilla on Mac OS.
* Update to latest version of uFlash.
* Add highlighting of search mathes.
* Check if the script produced is > 8k.
* Use a settings file local to the Mu executable if available.
* Fix bug with highlighting code errors in Windows.
* Check to overwrite an existing file on the micro:bit FS.
* Start changelog
