Release History
---------------

1.0.2
=====

Another bugfix and translation release. No new features were added. Unless
there are show-stoppers, the next release will be 1.1 with new features.

* Updated OSX to macOS, as per Apple's usage of the terms. Thanks Craig Steele.
* Updates and improvements to the Chinese translation. Thank John Guan.
* Improved locale detection on macOS. Many thanks to Tiago Montes.
* Cosmetic stripping of trailing spaces on save. Thanks to Tim Golden.
* Update PyQt version so pip installed Mu works with Python 3.5. Thanks to
  Carlos Pereira Atencio.
* Fix incorrect setting of dataTerminalReady flag. Thanks to GitHub user
  @wu6692776.
* Spanish language improvements and fixes by Juan Biondi, @yeyeto2788 and
  Carlos Pereira Atencio.
* Improvements and fixes to the German translation by Eberhard Fahle.
* Fix encoding bug on Windows which caused crashes and lost files. Many thanks
  to Tim Golden for this work.
* Keyboard focus loss when closing REPL is now fixed. Thanks again Tim Golden.
* More devices for Adafruit mode along with a capability to work with future
  devices which have the Adafruit vendor ID. Thanks to Limor Friend for this
  contribution.
* Fix a bug introduced in 1.0.1 where output from a child Python process was
  being truncated.
* Fix an off-by-one error when reading bytes from UART on MicroPython devices.
* Ensure zoom is consistent and remembered between panes and sessions.
* Ensure mu_code and/or current directory of current script are on Python path
  in Mu installed from the installer on Windows. Thanks to Tim Golden and Tim
  McCurrach for helping to test the fix.
* Added Argon, Boron and Xenon boards to Adafruit mode since they're also
  supported by Adafruit's CircuitPython.
* The directory used to start a load/save dialog is either what the user last
  selected, the current directory of the current file or the mode's working
  directory (in order of precedence). This is reset when the mode is changed.
* Various minor typo and bug fixes.

1.0.1
=====

This is a bugfix and new translation release. No new features were added. The
next release will be 1.1.0 with some new features.

* Added a German translation by René Raab.
* Added various new Adafruit boards, thanks Limor!
* Added a Vietnamese translation by GitHub user @doanminhdang.
* Fix bug in MicroPython REPL when dealing with colour escape sequences, thanks
  Martin Dybdal of Coding Pirates! Arrr.
* Ensured anyone trying to setup on an incompatible version of Python is given
  a friendly message explaining the problem. Thanks to the hugely talented
  René Dudfield for migrating this helpful function from PyGame!
* Added a Brasilian translation by Marco A L Barbosa.
* Added missing API docs for PyGameZero. Thanks to Justin Riley.
* Added a Swedish translation by Filip Korling.
* Fixes to various metadata configuration entries by Nick Morrott.
* Updated to a revised Chinese translation. Thanks to John Guan.
* Added the Mappa MUndi (roadmap) to the developer documentation.
* Added a Polish translation by Filip Kłębczyk.
* Fixes and enhancements to the UI to aid dyslexic users by Tim McCurrach.
* Updated to version 1.0.0.final for MicroPython on the BBC micro:bit. Many
  thanks to Damien George of the MicroPython project for his amazing work.
* Many other minor bugs caught and fixed by the likes of Zander and Carlos!

1.0.0
=====

* Fix for font related issues in OSX Mojave. Thanks to Steve Stagg for spotting
  and fixing.
* Fix for encoding issue encountered during code checking. Thanks to Tim
  Golden for a swift fix.
* Fix for orphaned modal dialog. Thanks for spotting this Zander Brown.
* Minor revisions to hot-key sequences to avoid duplications. All documented
  at https://codewith.mu/en/tutorials/1.0/shortcuts.
* Update to latest version of uflash and MicroPython 1.0.0-rc.2 for micro:bit.
* Updated to latest GuiZero in Windows installers.
* Update third party API documentation used by QScintilla for code completion
  and call tips. Includes CircuitPython 3 and PyGame Zero 1.2.
* Added swag related graphics to the repository (non-functional change).

1.0.0.rc.1
==========

* Various UI style clean ups to make sure the look of Mu is more consistent
  between platforms. Thanks to Zander Brown for this valuable work.
* Added French translation of the user interface. Thanks to Gerald Quintana.
* Added Japanese translation of the user interface. Thanks to @MinoruInachi.
* Added Spanish translation of the user interface. Thanks to Carlos Pereira
  Atencio with help from Oier Echaniz.
* Added Portuguese translation of the user interface. Thanks to Tiago Montes.
* Fixed various edge cases relating to the new-style flashing of micro:bits.
* Fixed off-by-one error in the visual debugger highlighting of code (caused
  by Windows newlines not correctly handled).
* Fixed shadow module related problem relating to Adafruit mode. It's now
  possible to save "code.py" files onto boards.
* Updated to latest version of uflash and MicroPython 1.0.0-rc.1 for micro:bit.
* Various minor bugs and niggles have been fixed.

1.0.0.beta.17
=============

* Update to the latest version of uflash with the latest version of MicroPython
  for the BBC micro:bit.
* Change flashing the BBC micro:bit to become more efficient (based on the
  copying of files to the boards small "fake" filesystem, rather than
  re-flashing the whole device in one go).
* Ensure user agrees to GPL3 license when installing on OSX.
* Fix Windows "make" file to correctly report errors thanks to Tim Golden.
* The debugger in Python mode now correctly handles user-generated exceptions.
* The debugger in Python mode updates the stack when no breakpoints are set.
* Major update of the OSX based automated build system.
* Modal dialog boxes should behave better on GTK based desktops thanks to
  Zander Brown.
* Right click to access context menu in file panes in micro:bit mode so local
  files can be opened in Mu.
* Fix bug where REPL, Files and Plotter buttons got into a bad state on
  mode change.
* Update to use PyQt 5.11.
* On save, check for shadow modules (i.e. user's are not allowed to save
  code whose filename would override an existing module name).
* Automatic comment toggling via Ctrl-K shortcut.
* A simple find and replace diaolog is now available via the Ctrl-F shortcut.
* Various minor bugs and niggles have been squashed.

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
* Update to latest version of Pygame Zero.
* Fix plotter axis label bug which wouldn't display numbers if value was a
  float.
* Separate session and settings into two different files. Session includes
  user defined changes to configuration whereas settings contains sys-admin-y
  configuration.
* Update the CSS for the three themes so they display consistently on all
  supported platforms. Thanks to Zander Brown for his efforts on this.
* Move the mode selection to the "Mode" button in the top left of the window.
* Support for different encodings and default to UTF-8 where possible. Many
  thanks to Tim Golden for all the hard work on this rather involved fix.
* Consistent end of line support on all platforms. Once again, many thanks to
  Tim Golden for his work on this difficult problem.
* Use ``mu-editor`` instead of ``mu`` to launch the editor from the command
  line.
* More sanity when dealing with cross platform paths and ensure filetypes are
  treated in a case insensitive manner.
* Add support for minification of Python scripts to be flashed onto a micro:bit
  thanks to Zander Brown's nudatus module.
* Clean up logging about device discovery (it's much less verbose).
* Drag and drop files onto Mu to open them. Thanks to Zander Brown for this
  *really useful* feature.
* The old logs dialog is now an admin dialog which allows users to inspect the
  logs, but also make various user defined configuration changes to Mu.
* Plotter now works in Python 3 mode.
* Fix problem in OSX with the ``mount`` command when detecting Circuit Python
  boards. Thanks to Frank Morton for finding and fixing this.
* Add data flood avoidance to the plotter.
* OSX automated packaging. Thanks to Russell Keith-Magee and the team at
  BeeWare for their invaluable help with this problematic task.
* Refactoring and bug fixing of the visual debugger's user interface. Thank you
  to Martin O'Hanlon and Carlos Pereira Atencio for their invaluable bug
  reports and testing.
* Various fixes to the way the UI and themes are displayed (crisper icons on
  HiDPI displays and various other fixes). Thanks to Steve Stagg for putting
  lipstick on the pig. ;-)
* A huge number of minor bug fixes, UI clean-ups and simplifications.

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
