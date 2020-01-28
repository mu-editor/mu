Release Process 
---------------

Our continuous integration setup provides the following automation:

* Running of the unit test suite on Windows, OSX and Linux for each commit.
* Code quality checks via `LGTM.com <https://lgtm.com/projects/g/mu-editor/mu/>`_.
  Mu has an A+ rating for code quality.
* Generation of installables for Windows 32bit and Windows 64bit for each
  commit on our master branch.
* Creation of a stand-alone .app for Mac OSX for each commit on our master
  branch.

However, such automation does not make a release. What follows is a check-list
of steps needed to cut a release.

User Activity Checks
====================

To ensure nothing is broken from the user's point of view the following key
user activities should be completed on Windows, OSX and Linux (to ensure the
cross platform nature of Mu is consistent):

* Start Mu from a clean state (delete your Mu configuration file, and mu_code
  directory). *Outcome: Mu should ask for an initial mode and a fresh
  mu_code directory is created. Upon restart, Mu doesn't repeat this process.*
* Click the "Mode" button, select a new mode. *Outcome: the mode selection
  dialog should appear and you'll find yourself in a new mode.*
* Click the "New" button. *Outcome: a new blank tab will appear.*
* Click the "Load" button. *Outcome: the operating system's file selector
  dialog should appear. The selected file should open in a new tab.*
* With a new tab, click the "Save" button. *Outcome: the operating system's
  file naming dialog should appear, and the tab will be updated with the newly
  named filename.*
* While in Python mode, plug in an Adafruit board. *Outcome: Mu should
  suggest switching to Adafruit mode.*
* In Adafruit mode, load, edit and save a file on the device. *Outcome: upon
  saving the file, the device will reboot and run your code.*
* In Adafruit mode, click the "Serial" button. *Outcome: a serial connection
  to the attached device is shown in a pane at the bottom of Mu's window.
  Pressing Ctrl-C should drop you to the CircuitPython REPL.*
* In Adafruit mode, use some code `like this <https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/master/Sensor_Plotting_With_Mu_CircuitPython/light.py>`_
  on the Adafruit device (in the case of this example, a Circuit Playground
  Express) to emit tuple based data. Click the "Plotter" button
  while the code is running. *Outcome: the plotter should display the output
  as a graph.*
* While in Python mode, plug in a micro:bit board. *Outcome: Mu should
  suggest switching to micro:bit mode.*
* In micro:bit mode (from now on, assuming you have a micro:bit device
  connected), while the current tab is completely empty, click the
  "Flash" button. *Outcome: Mu should do a complete fresh flash of "vanilla"
  MicroPython.*
* In micro:bit mode, write some simple working code and click the "Flash"
  button. *Outcome: since MicroPython is already flashed on the device, only
  the file will be copied over and the device will soft-reboot.*
* In micro:bit mode, click on the "Files" button. *Outcome: the files pane
  will appear and contain a true reflection of the current state of the file
  system on the device and in your mu_code directory.*
* In micro:bit mode, while the "Files" pane is active, copy to/from the device,
  delete a file on the device and open files listed on your computer by
  right-clicking them. *Outcome: the file pane state should update and no 
  error message appear.*
* In micro:bit mode, click on the "REPL" button. *Outcome: you should see and
  be able to interact with the REPL of MicroPython running on the connected
  device.*
* In micro:bit mode, use some code to emit tuple based data. Click on the
  "Plotter" button while the code is running. *Outcome: the plotter should
  display the output as a graph.*
* In PyGameZero mode, with an empty file, click the "Play" button. *Outcome:
  a blank Pygame window will appear.*
* In PyGameZero mode, with correctly working code, click the "Play" button.
  *Outcome: the game runs.*
* In PyGameZero mode, click each of the "Images", "Fonts", "Sounds" and "Music"
  buttons. *Outcome: the operating system's file manager should open in the
  correct directory for each of these types of game asset.*
* In Python mode, enter a simple script and click "Run". *Outcome: the script
  should run with input/output being handled by a pane at the bottom of the
  Mu window.*
* In Python mode, add a new breakpoint to your code, click "Debug". *Outcome:
  the visual debugger should start and stop at your breakpoint.*
* In Python mode, with no breakpoints present, click "Debug". *Outcome: the
  visual debugger will start and stop at the first valid line of code.*
* While the visual debugger is active, add and remove breakpoints. *Outcome:
  the UI will update (red dots will appear etc) and the debugger will respect
  such changes (stopping at new breakpoint, ignoring removed breakpoints).*
* While in the visual debugger click the "Stop", "Continue", "Step Over", "Step
  In", "Step Out" buttons. *Outcome: the conventional behaviour for each button
  should happen. "Stop" will stop the script. "Continue" will run to the next
  break or end of script. "Step Over" will move to the next valid line of
  code. "Step In" will move into the called funtion. "Step Out" will move out
  of the current function. As all this happens, the input/output pane and
  object inspector should update as the code progresses.*
* In Python mode, click on the "REPL" button. *Outcome: an iPython based REPL
  should appear in a new pane at the bottom of Mu's window. Clicking the
  button again toggles the REPL off.*
* In Python mode, use some code to emit tuple based data. Click on the
  "Plotter" button while the code is running. *Outcome: the plotter should
  display the output as a graph.*
* Click "Zoom-In". *Outcome: the font size should increase.*
* Click "Zoom-out". *Outcome: the font size should decrease.*
* Click "Theme" several times. *Outcome: the theme/look should toggle.*
* With incorrect code in the current tab, click "Check". *Outcome: problems
  like syntax errors or undefined names should be highlighted with
  annotations on the correct line. If appropriate, they will be underlined.*
* Click the "Help" button. *Outcome: the operating system's default browser
  should open at the help page for the current version of Mu.*
* With unsaved code in the current tab, click "Quit". *Outcome: Mu should warn
  you may lose unsaved work and prompt you to confirm.*
* With all work saved, click "Quit". *Outcome: Mu should quit.*
* Click on the "cog" icon in the bottom right of Mu's Window. *Outcome: the
  "admin" dialog should open with the "logs" tab in focus.*
* In the editor panel, type CTRL-K while code is selected. *Outcome: the
  selected code should toggle between commented and uncommented.*
* Type CTRL-F. *Outcome: the find/replace dialog should appear.*

Pre-Packaging Checklist
=======================

* All autogenerated API information used by Mu for auto-completion and call 
  tips should be regenerated.
* The developer documentation should be checked, re-read and regenerated
  locally to ensure everything is presented correctly.
* The CHANGELOG.rst file should be updated to reflect the differences since the
  last officially packaged release.
* If this is a major release make sure the resources for the old version of
  Mu on the `project website <https://codewith.mu/>`_ are archived under the
  correctly versioned URL scheme.
* Make sure the current resources in the source for the project website
  reference the new version of Mu.

Packaging Processes
===================

Official final releases will be signed by Nicholas H.Tollervey (the creator and
current maintainer of Mu). This is a manual step only Nicholas can do (since
only he has the cryptographic keys to make this work). Once the release
packages for Windows (32bit and 64bit) and OSX have been created and signed
they should be checked so no warning messages appear about untrusted sources
during the installation process.

The instructions for signing the Windows installers are explain in
`this wonderful article on Adafruit's website <https://learn.adafruit.com/how-to-sign-windows-drivers-installer/making-an-installer>_`.
But the essence is that the command issued should look something like::

    "C:\Program Files (x86)\Windows Kits\10\bin\10.0.17134.0\x86\signtool" sign /v /n "Nicholas H.Tollervey" /tr http://timestamp.globalsign.com/?signature=sha2 /td sha256 mu-editor_1.0.1_win32.exe

Signing the Mac app involves issuing the following two commands::

    codesign --deep --force --verbose --sign "CERT_ID" mu-editor.app
    dmgbuild -s package/dmg_settings.py "Mu Editor" dist/mu-editor.dmg

The appropriate installer should be checked on the following operating systems:

* Windows 7 (32bit)
* Windows 10 (64bit)
* Latest OSX.

For native Python packaging, ensure Mu is installable via ``pip install .`` run
in the root of the source repository in a virtualenv.

Pre-Release Checklist
=====================

* Create an announcement blog post for `MadeWithMu <https://madewith.mu/>`_.
* Tweet an announcement for the timing of the upcoming release.
* Compose (but do not publish) a tweet to announce Mu's release.
* Ensure the source code for the developer docs, the project website and
  MadeWithMu is all ready to be published.
* Prepare a press release and circulation list.
* Check other possible channels for announcements, community websites etc.

Release Process
===============

* Build the developer documentation on ReadTheDocs. Make a note of the link to
  the latest release in the resulting page on the CHANGELOG.
* Create a new release on GitHub and attach the signed 32bit and 64bit Windows
  installers and OSX dmg. Reference the changelog from step 1 in the release
  notes.
* Update the download page on the project website to the URLs for the
  installers added to the release in step 2. Update the live version of the
  website.
* Push the latest version to PyPI (``make publish-test`` then
  ``make publish-live``).
* Publish the blog post announcement to MadeWithMu.
* Tweet with link to the announcement blog post and changelog.
* Mention release in Gitter, Adafruit's CircuitPython Discord.
* Send out press release / news item to circulation list / friends.
* Hit other possible announcement channels.

Post-Release Tasks
==================

* Monitor Gitter chat channel for problems.
* Clean up fixed issues in GitHub.
* Update Roadmap.rst with reference to the next release.
* Send out thanks / gifts where appropriate.
