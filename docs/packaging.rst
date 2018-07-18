Packaging Mu
------------

Because our target users (beginner programmers and those who support them) may
not be confident with the technical requirements for installing packages,
we need to make obtaining and setting up Mu as simple and easy as possible. 

Furthermore, we aim to make the creation of packages automatic and as simple
as possible. By automating this process we ensure that the knowledge and steps
needed to package Mu is stored in software (so everyone can see how we do it)
and we don't rely on a volunteer to take time and effort to make things happen.
If you submit code and it is accepted into our master branch, within minutes
you should have a set of packages for different platforms that includes your
changes. Such builds can be
`found here <http://mu-builds.s3-website.eu-west-2.amazonaws.com/>`_. 

Of course, such builds are not "official" releases. We'll only do that every
so often when major updates land. These will take the form of
`releases found in our GitHub repository <https://github.com/mu-editor/mu/releases>`_.
Such releases will include the "official" installers for supported platforms.
The installers referenced on `Mu's website <http://codewith.mu/>`_ will always
be the latest stable release of Mu on GitHub.

.. note::

    Huge thanks to `Carlos Pereira Atencio <https://twitter.com/carlosperate>`_
    who made considerable efforts to automate and configure the packaging of
    Mu. Without the contributions of volunteers like Carlos, projects like Mu
    simply wouldn't exist. If you find Mu useful why not say thank you to
    Carlos via Twitter..?

    Thank you Carlos! :-)

We package Mu in various different ways so it is as widely available as
possible. What follows is a brief description of how each package is generated
(some of them require the manual intervention of others outside the Mu
project).

Python Package
++++++++++++++

If you have Python 3.5 or later installed on Windows, OSX or 64-bit Linux and
you are familiar with Python's built-in packaging system, you can install Mu
into a virtual environment with ``pip``::

    $ pip install mu-editor

.. note::

    By design, ``pip`` will not create any shortcuts for applications that it
    installs.

    If you want to add a shortcut for Mu to your desktop/start menu you can
    use Martin O'Hanlon's amazingly useful
    `Shortcut tool <https://shortcut.readthedocs.io/en/latest/>`_ like this::

        $ pip install shortcut
        $ shortcut mu

As per conventions, the ``setup.py`` file contains all the details used by
``pip`` to install it. We use `twine <https://github.com/pypa/twine>`_ to push
releases to PyPI and I (Nicholas - maintainer) simply use a Makefile to
automate this::

    $ make publish-test
    $ make publish-live

The ``make publish-live`` command is what updates PyPI. The
``make publish-test`` command uses the test instance of PyPI so we can confirm
the release looks, behaves and works as expected before pushing to live.

Raspberry Pi
++++++++++++

When asked, Serge Schneider, a maintainer of Raspbian at the Raspberry Pi
Foundation takes our latest release and updates the Raspbian package
repositories. It means that all you need to do to install Mu on Raspbian is
type::

    $ sudo apt-get install mu

.. warning::

    Since Mu for Raspberry Pi is packaged by a third party, our latest releases
    may not be immediately available.

Windows Installer
+++++++++++++++++

Packaging for Windows is essential for the widespread use of Mu since most
computers in schools run this operating system. Furthermore, feedback from
school network administrators tells us that they prefer installers since these
are easier to install "in bulk" to computing labs.

There are two versions of the installer: one for 32bit Windows and the other
for 64bit Windows. The 32bit version has been tested on Windows 7 and the 64bit
version has been tested on Windows 10. Support for anything other than Windows
10 is important, but a "best effort" affair. If you find you're having problems
please `submit a bug report <https://github.com/mu-editor/mu/issues/new>`_.

The latest *unsigned* builds for Mu on Windows
`can be found here <http://mu-builds.s3-website.eu-west-2.amazonaws.com/?prefix=windows/>`_.

Mu for Windows contains its own version of Python packaged in such a way that
makes it only usable within the context of Mu (Python's so-called 
`isolated mode <https://docs.python.org/3.4/whatsnew/3.4.html#whatsnew-isolated-mode>`_).
Of course, the version of Python in Mu will have as much or little
access to computing resources as the host operating system will allow.

Packaging is automated using the `Appveyor <https://www.appveyor.com/>`_ cloud
based continuous integration solution for Windows. The 
`.appveyor.yml <https://github.com/mu-editor/mu/blob/master/.appveyor.yml>`_
file found in the root of Mu's repository, configures and describes this
process. You can see the history of such builds
`here <https://ci.appveyor.com/project/carlosperate/mu/history>`_.

We use the `NSIS <http://nsis.sourceforge.net/Main%5FPage>`_ tool to build the
installers. This process if coordinated by the amazing
`pynsist <https://pynsist.readthedocs.io/en/latest/>`_ utility.

.. note::

    Pynsist is the creation of
    `Thomas Kluyver <https://twitter.com/takluyver>`_, who has done an amazing
    job creating many useful tools and utilities for the wider Python
    community (for example, Thomas is also responsible for the Jupyter
    widget Mu uses for the REPL in Python 3 mode).

    On several occasions Thomas has volunteered his time to help Mu. Like
    Carlos, Thomas is another example of the invaluable efforts that go into
    making Mu. Once again, if you find Mu useful, please don't hesitate to
    thank Thomas via Twitter.

    Thank you Thomas!

The configuration for ``pynsist`` are the ``win_installer32.cfg`` and
``win_installer64.cfg`` files (one each for 32bit and 64bit installers) in the
root of the repository. Please check out the
`specification for configuration files <https://pynsist.readthedocs.io/en/latest/cfgfile.html>`_
for more information.

The automated builds are unsigned, so Windows will complain about the software
coming from an untrusted source. The official releases will be signed by
me (Nicholas Tollervey - the current maintainer) on my local machine using
a private key and uploaded to GitHub and associated with the relevant release.
`The instructions for cyrptographically signing installers <https://pynsist.readthedocs.io/en/latest/faq.html#code-signing>`_
explain this process more fully
(the details of which are described
`by Mozilla <https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Build_Instructions/Signing_an_executable_with_Authenticode>`_).

Use the ``make`` command to build your own installers::

    $ make win32
    $ make win64

This will clean the repository before running the ``win_installer.py`` command
for the requested bitness.

Because Mu depends on the availability of tkinter, part of the build process is
to download the appropriate tkinter-related resources from
`Mu's tkinter assets repository <https://github.com/mu-editor/mu_tkinter>`_.

If asked, the command for automatically installing Mu, system wide, should use
the following flags::

    mu-editor_win64.exe /S /AllUsers

The ``/S`` flag tells the installer to work in "silent" mode (i.e. you won't
see the windows shown in the screenshots above) and the ``/AllUsers`` flag
makes Mu available to all users of the system (i.e. it's installed "system
wide").

OSX App Installer
+++++++++++++++++

We use Travis to automate the building of the .app and .dmg installer (see the
``.travis`` file in the root of Mu's GIT repository for the steps involved). 
This process is controlled by
`Briefcase (part of the BeeWare suite of tools <https://briefcase.readthedocs.io/en/latest/>`_
which piggy-backs onto the ``setup.py`` script to build the necessary assets.
To ensure Mu has Python 3 available for it to both run and use for evaluating
users' scripts, we have created a portable/embeddable Python runtime whose
automated build scripts can be found
`in this repository <https://github.com/mu-editor/mu_portable_python_macos>`_.
This (not the version of Python on the user's machine) the version of Python
used by Mu.

The end result of submitting a commit to Mu's master branch is an
automatically generated installable for OSX. These assets are un-signed, so OSX
will complain about Mu coming from an unknown developer. However, for full
releases we sign the .app with our Apple developer key (a manual process).

Linux Packages
++++++++++++++

We don't automatically create packages for Linux distros. However, we liaise
with upstream developers to ensure that Mu finds its way into both Debian and
Fedora based distributions.

Debian
======

Work on packaging for Debian is at an advanced stage and ongoing. You can
track progress at `this ticket <https://github.com/mu-editor/mu/issues/58>`_.

Fedora
======

Mu was packaged by `Kushal Das <https://twitter.com/kushaldas>`_ for Fedora.
However this is an old version of Mu and, as with the Raspberry Pi version,
relies on a third party to package it so may lag behind the latest version.

.. note::

    Last, but not least, Kushal does a huge amount of work for both the
    Fedora and Python communities and is passionate about sustaining our
    Python community through education outreach. With people like Kushal
    putting in the time and effort to package tools like Mu and mentor
    beginner programmers who use Mu our community would flourish less. If you
    find Mu useful, please don't hesitate to thank Kushal via Twitter.

    Thank you Kushal.
