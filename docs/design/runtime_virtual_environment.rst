Run the user's code inside its own virtual environment
======================================================

Decision
--------

Mu, whether pip-installed or via installer will maintain a separate virtual
environment for running the user's code. Initially this will contain all
the dependencies used by any of our modes, plus any packages the user
installs in addition.

The dependencies needed for the running of the editor itself (mostly PyQt
stuff but currently including some serial packages which have "leaked" from
the modes) will be kept in a separate environment, virtual or otherwise.

The installers will have to support this approach by bundling wheels (as
our assumption is that some schools at least will have restricted or no
internet access).

For now we're not breaking out modes into plugins or separate environments
although that's a natural extension of this work. If that were done later,
each mode could specify its own dependencies which could be installed on
demand.

Background
----------

* Getting Mu to unpack and run out of the box on the three main platforms:
  Windows, OS X & Linux has always proven challenging.
* In addition, within the Mu codebase, the code to run the user's code is
  scattered and contains a fragile re-implementation of a virtual environment.
* Installing 3rd-party modules was also a little fragile as we had to run
  `pip` with a `--target` parameter
* There are other issues, especially around the Jupyter console and, on
  Windows, its use of the pywin32 packages which have slightly odd path
  handling.

Discussion and Implementation
-----------------------------

This started off with work by @ntoll to have the 3rd-party apps installed
into a virtual environment rather than with the `--target` parameter which
would try to force them into a directory where Mu could find them. This
stalled somewhat, especially on Windows, and I (@tjguk) took over that
branch.

Having focused on the getting a virtual environment running for the 3rd-party
installs, I realised that having a venv for the whole of the code runtime
might help solve some of the other issues. After a few merges to get some
changes in, especially those by @tmontes to the installer, we started PR#1072
https://github.com/mu-editor/mu/pull/1072.

There is now a `virtual_environment.py` module which initially brings together
various pieces of code which were scattered around the codebase and adds
support for creating and installing into a virtual environment. The various
places where the user code is run (mostly within the `modes` package, but including
inside `panes.py`) have been updated to use this virtual environment logic.
Possible future work might involve adding a "run process" method to the class
itself.

As far as possible this should remove the need to hack up special `PYTHONPATH`,
`*.pth` and `site.py` logic.

Implemented via:
~~~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/pull/1068
* https://github.com/mu-editor/mu/pull/1072
* https://github.com/mu-editor/mu/pull/1056
* https://github.com/mu-editor/mu/pull/1058

Discussion in:
~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/issues/1061
* https://github.com/mu-editor/mu/issues/1070
