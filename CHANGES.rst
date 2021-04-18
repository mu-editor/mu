Release History
---------------

1.1.0-beta.4
============

This is a beta release and may contain bugs or unfinished features. Please
provide bug reports or feedback via: https://github.com/mu-editor/mu/issues/new

* During the beta phase, we're moving to a fortnightly release cadence. Since
  this release is a week late, expect the next one in a week's time - 26th
  April.
* Carlos made many changes to clean up the specification for required modules
  used by the installer. This will make supporting and tracking Mu's
  dependencies MUCH easier. Thank you Carlos!
* Huge thanks to Dan Halbert of Adafruit who contributed a significant amount
  of refactoring to the CircuitPython mode. As a result Mu now uses the
  `adafruit-board-toolkit` module for device identification, among many other
  helpful changes
  [described in Dan's pull request](https://github.com/mu-editor/mu/pull/1371).
  Thank you Dan..!
* Carlos was on fire... he also fixed a bug in the file-copy dialog when the
  context menu was opened with an empty list of files.
* Carlos (again), fixed some outstanding documentation issues for supporting
  Raspbian Buster (and newer). These are now at https://mu.rtfd.io/.
* Carlos (again, again) tidied up various aspects of the Makefile so there is
  only a single source of truth for running various utilities and commands.
* Logging was another focus for this release. Now that we have a few weeks
  worth of crash reports we've been able to look at the parts of the
  application that cause most grief and add extra-logging in various locations.
  Tim put in a great effort to make sure the "first run" and other virtual
  environment based aspects of Mu now have clearer and more useful logging and
  throw more useful exceptions, closer to the source of the problem, for the
  resulting crash report. Carlos ensured the IPython kernel installation was
  properly logged.
* We ensured various key packages were pinned to particular versions to
  maximise compatibility with older versions of Python still found in schools.

There are many pull requests and work items currently in flight and they'll be
landing very soon as the overall quality and robustness of Mu significantly
improves. Many thanks to everyone who continues to help, support and contribute
to the ongoing development of Mu.

1.1.0-beta.3
============

This is a beta release and may contain bugs or unfinished features. Please
provide bug reports or feedback via: https://github.com/mu-editor/mu/issues/new

* During beta phase, we're moving to a fortnightly release cadence. Expect beta
  4 on the 12th April.
* The final version of the Mu splash screen was delivered. Huge thanks to the
  extraordinarily talented Steve Hawkes ([@hawkz](https://github.com/hawkz)) of
  [The Developer Society](https://www.dev.ngo/) for his generous artistic
  support, patience and humorous approach.
* Thanks to a recent update in [PyGame Zero](https://pypi.org/project/pgzero/),
  we're back to using the official package from PyPI, rather than our patched
  fork, in the installer.
* Both Tim and Carlos have contributed updates, fixes and tests to address a
  bug affecting Windows users who may have a space in the file path upon which
  Mu is found. This was a difficult bug to reproduce but Tim did a lot of
  digging to isolate the cause with as much confidence as is possible when it
  comes to such things. Carlos did a bunch of thankless and fiddly test related
  work so testing with spaces in the path is part of our test suite. Work on
  this is ongoing so expect further improvements in upcoming releases. As
  always, many thanks for these efforts.
* Tim addressed a `wheel`/`sdist` related problem that was causing odd side
  effects with regard to dependancies.
* A strange bug, where it was not possible to install third-party packages on
  first run of Mu, opened up a deep rabbit hole of investigation. In the end
  Tim was able to fix this AND address the source of a warning message from Qt
  when Mu was starting for the first time.
* The splash screen code was rewritten in such a way that objects relating to
  the splash screen will always be garbage-collected by Python and destroyed by
  Qt5. Previously, they existed for the full duration of the application, not
  really causing any problems, but "in limbo" nonetheless.
* The crash reporting tool has had a minor update so the user is reminded to
  attach their log file to the bug report, along with an indication of where to
  find the log file.

1.1.0-beta.2
============

This is a beta release and may contain bugs or unfinished features. Please
provide bug reports or feedback via: https://github.com/mu-editor/mu/issues/new

* This is the first public beta release (beta 1 was created for testing by the
  core development team).
* Many minor bug fixes to the existing new features found in beta 1
  (see below).
* Many thanks to Martin Dybdal for his work on improving the admin panel.
* Carlos made significant changes so Mu can be packaged with very recent
  versions of Python. Carlos also made various changes relating to the status
  of Python packages contained within the official installer.
* Many thanks to Dan Pope for assistance with an upgraded version of PyGameZero
  (which uses the latest version of PyGame - kudos to René and the other
  developers of PyGame for the recent improvements).
* Various fixes to the UI so that panes are easier to resize and the themes are
  correctly applied to the REPL (thanks again to Martin for these fixes).
* Carlos also contributed fixes relating to the micro:bit mode (compatibility
  with versions 1 and 2).
* Tim has made herculean efforts to ensure the creation and checking of Mu's
  virtual environment is robust and easy to maintain.
* A new crash reporting feature has been added. If Mu breaks the user will be
  redirected to the endpoint codewith.mu/crash with details of the crash and an
  option to create a bug report. This ensures Mu crashes are handled more
  gracefully, and the user is able to see the error that caused the crash.
* A new animated splash screen has been added so the initial creation of Mu's
  virtual environment happens in such a way that the user can see progress is
  being made, and updates are logged on the splash screen for the user. If Mu
  encounters a problem at this early stage, the splash screen recovers and the
  new crash reporting feature kicks in. The current animation was created by
  Steve Hawkes (thank you) with a much more polished version promised very
  soon..!
* Behind the scenes, Tiago has continued to make outstanding work on the `pup`
  tool we use to create the installers for Windows 64/32 bit and MacOS X. This
  beta release will be the first to use installers created with `pup`.
* **Known bug** - on first ever start of Mu, if in Python3 mode the package
  manager will not work. Re-starting Mu fixes this (i.e. from second and
  subsequent starts). We're tracking this problem via
  [this issue](https://github.com/mu-editor/mu/issues/1358).

1.1.0-beta.1
============

This is a beta release and may contain bugs or unfinished features. Please
provide bug reports or feedback via: https://github.com/mu-editor/mu/issues/new

* A new mode for ESP8266/ESP32 devices running MicroPython. This work and a
  significant amount of related refactoring was contributed with Viking like
  energy and efficiency by Martin Dybdal. This work has meant it was relatively
  easy to create two further new modes...
* New mode for Lego Spike devices (thanks to Chris and Ethan at Tufts
  University for the help and support).
* New mode for Raspberry Pi Pico (thanks to Zander, Martin and Carlos for the
  extensive testing).
* Updates to the Microbit mode made by Spanish source-code wrangler
  extraordinaire (and resident Microbit expert) Carlos Pereira Atencio. The
  Microbit mode now supports versions 1 and 2 of the board.
* Various bits of artwork used in the application have been updated (including
  a new [temporary] animated splash screen). Thanks to devdanzin for
  choreographing the initial work on the splash screen at short notice.
* A complete re-write of the virtualenv and third party package handlers by the
  hugely talented Tim Golden. This was a long term and difficult refactoring
  project which Tim has delivered with great aplomb. This should make package
  handling much smoother and simpler.
* Various smallish UI fixes, enhancements and smoothing by devdanzin. Thank you
  for these contributions - they really make a difference to the ease of use
  and friendly feel of Mu.
* This version of Mu is packaged with stand-alone installers for Windows and
  OSX by the wonder that is PUP - a new packaging tool by our very own Tiago
  Montes ~ Portugal's Premier Python Packager Par-excellence. We have big plans
  for PUP... watch this space. :-)
* Many many many minor bug fixes contributed by many many many people to whom
  we are eternally grateful.

We hope to release beta.2 very soon.

1.0.3
=====

Bugfix.

* Updated to the latest version of Qt to fix syntax highlighting issues in OSX.
* Ensure CWD is set to the directory containing the script to be run in Python3
  mode.
* Updated website with instructions in light of OSX changes.

1.1.0-alpha.2
=============

The second alpha release of 1.1. This version may contain bugs and is
unfinished (more new features will be arriving in alpha 3). Please provide bug
reports or feedback via: https://github.com/mu-editor/mu/issues/new

* **NEW FEATURE** A brand new web mode for creating simple dynamic web
  applications with the Flask web framework. Currently users are able to edit
  Python, HTML and CSS files, run a local server and view their website in
  thier browser. We expect to add a deployment option thanks to PythonAnywhere
  by the time alpha 3 is released.
* **NEW FEATURE** A new Slovak translation of Mu thanks to Miroslav Biňas
  (GitHub user `bletvaska <https://github.com/bletvaska>`_).
* **ACHIEVEMENT UNLOCKED** Fixed a problematic bug where students got into a
  seemingly impossible loop because the auto-save feature encountered errors
  and got in the way of renaming a file. We are THRILLED TO BITS that the fix
  for this problem was contributed by
  `Sean Tibor <http://teachingpython.fm>`_, a teacher from
  Fort Lauderdale, Florida. **Teachers coding the tools they use to teach has
  been a core aim for Mu, and Sean gets the gold medal (or perhaps a beer when
  I next see him) for unlocking this achievement.**
* **RENAME** At the suggestion of Adafruit's Dan Halbert, the "Adafruit" mode
  has been renamed to "CircuitPython" mode to reflect the growing number of
  manufacturers who support CircuitPython. Many thanks to
  `Benjamin Shockley <http://benjaminshockley.com/>`_ for putting the work in
  to make this happen.
* **NEW DEVICES** Several new non-Adafruit boards have been added to the
  renamed CircuitPython mode. Many thanks to
  `Shawn Hymel <http://shawnhymel.com>`_ (SparkFun) and
  `Gustavo Reynaga <http://www.gustavoreynaga.com/>`_ (Electronic Cats) for
  contributing these valuable changes.
* Add some new free-to-reuse image and sound assets for use in PyGameZero
  example games.
* Middle mouse wheel scrolling with the CTRL or CMD (on Mac) keys will zoom the
  UI in a consistent manner across all platforms.
* Minor documentation updates / corrections thanks to
  `Luke Slevinsky <https://lukeslev.github.io/>`_.
* Refinement of the built-in educational libraries as we start to unbundle a
  slew of software from Mu's installer so users can install such packages from
  within Mu. Many thanks to the formidably talented
  `Martin O'Hanlon <https://www.stuffaboutcode.com/>`_ for his help.
* PyGameZero mode will look for game assets relative to the location of the
  game file, rather than just within the user's workspace. Thanks to the
  evergreen `Tim Golden <http://timgolden.me.uk/>`_ for this helpful update.
* Minor corrections to the French localisation by GitHub user
  `ogoletti <https://github.com/ogoletti>`_.
* UI related convenience in the new ESP mode so that the current / most recent
  filesystem path is used when using the file copy pane. Many thanks (as
  always) to `Martin Dybdal <http://dybber.dk/>`_ for his continued work on all
  things ESP related in Mu.
* A tidy up of the file save dialog so it uses Qt's built in dialog features.
  Thanks to `Tiago Montes <https://tmont.es/>`_ for being his usual awesome
  self.
* Tabs are restored on startup in the correct order. Once again, this is the
  work of Tiago Montes.
* The mechanism for generating the various installers and packages for Mu has
  been significantly refactored so that there is, if possible, always a single
  source for configuration information. The significant amount of effort to
  make this happen was, once again (again), contributed by Tiago Montes.
* Window size and location is also restored on startup. Tiago Montes, who
  implemented this change, has been **ON FIRE** during this development phase.
* A small (but important) change to the tool-tip for the sleep function found
  in MicroPython on the micro:bit has been submitted to the pedagogical legend
  and friend of Mu that is `Dave Ames <https://dave-ames.net/>`_.
* A helpful message is now sent to the output pane when the graphical
  debugger starts in Python 3 mode. The Shakespeare like talents of
  long term Mu-tineer `Steve Stagg <https://sta.gg/>`_  are behind this
  Nobel-prize-worthy literary contribution.
* Re-add support for user defined syntax check overrides. Many thanks to
  `Leroy Levin <https://github.com/leroyle>`_ for making this happen..!
* Ensure that ``pip`` is updated while creating the Windows installers. Thanks
  to `Yu Wang <https://github.com/bigeyex>`_ for making this change.
* Various minor updates and fixes to aid code readibility.

1.1.0-alpha.1
=============

The first alpha release of 1.1. This version may contain bugs and is unfinished
(more new features will be added in later alpha releases or, depending on
feedback, we may change the behaviour of existing features). Please provide bug
reports or feedback via: https://github.com/mu-editor/mu/issues/new

* **NEW FEATURE** Installation of third party packages from PyPI. Click on the
  cog icon to open the admin dialog and select the "Third Party Packages" tab.
* **NEW FEATURE** Code tidy via the wonderful code formatter
  `Black <https://black.readthedocs.io/en/stable/>`_. Click the new "Tidy"
  button to reformat and tidy your code so it looks more readable. If your code
  has errors, these will be pointed out. Many thanks to Black's creator and
  maintainer, Łukasz Langa, for this contribution.
* **NEW FEATURE** A new ESP8266 / ESP32 mode for working with these WiFi
  enabled cheap IoT boards. Many thanks to Martin Dybdal for driving this
  work forward and doing the heavy lifting. Thanks also to Murilo Polese for
  testing and very constructive input in the review stage of this feature.
* **OS CHANGE** Due to Qt's and Travis's lack of support, Mu will only run on
  Mac OS 10.12 and above.
* Ensure line-number margin is not too sensitive to inaccurate clicking from
  young coders trying to position the cursor at the beginning of the line.
  Thanks to Tiago Montes for this enhancement.
* Fix some typos in the French translation. Thank you to GitHub user
  @camillem.
* Fix a bug relating to Adafruit boards when a file on a board which is then
  unplugged is saved, Mu used to crash. Thanks to Melissa LeBlanc-Williams for
  the report of this problem.
* Fix problem with a missing newline at the end of a file. Thanks to Melissa
  LeBlanc-Williams for the eagle-eyes and fix.
* Fix for PYTHONPATH related problems on Windows (the current directory is now
  on the path when a script is run). Thanks to Tim Golden for this fix.
* Update to locale detection (use Qt's QLocale class). Thanks to Tiago Montes
  for making this happen.
* Fix bug relating to match selection of non-ASCII characters. Thank you to
  Tiago Montes for this work.
* Fixed various encoding related issues on OSX.
* Various minor / trivial bug fixes and tidy ups.

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
