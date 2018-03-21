Line-endings
============

Decision
--------

Use \n internally in Mu. Detect the majority line-ending when loading a file
and store it on the tab object within the editor. Then use that newline
convention when saving. By default, eg for a new / empty file, use the
platform line-ending.


Background
----------

Mu is designed to run on any platform which supports Python / Qt. This includes
Windows and any *nix variant, including OS/X. Windows traditionally uses \r\n
(ASCII 13 + ASCII 10) for line-endings while *nix usually recognises a single \n
(ASCII 10). Although many editors now detect and adapt to either convention,
it's common enough for beginners to use, eg, Windows notepad which only honours
and only generates the \r\n convention.

When reading / writing files, Python offers several forms of line-ending
manipulation via the newline= parameter in the built-in open() function.
Mu originally used Universal newlines (newline=None; the default), but then switched
to retaining newlines (newline="") in PR #133

The effect of this last change is to retain whatever convention or mix of
conventions is present in the source file. In effect it is overriding any newline
manipulation to present to the editor control the characters originally present
in the file. When the file is saved, the same characters are written out.

However this creates a quandary when programatically manipulating the editor
text: do we use the most widespread \n as a line-ending; or do we use the
platform convention `os.linesep`; or do we use the convention used in the
file itself, which may or may not follow the platform convention?


Discussion and Implementation
-----------------------------

My proposal here is that Mu operate its own line-ending manipulation.

When reading the file, note the majority line-ending convention but
convert wholly to \n. When writing the file, use the convention noted
on the way in. This is essentially the same as we would do when reading
encoded Unicode from a file.

This way the line-endings are honoured so that, eg, a file can be read/written
in Notepad without problems. And the Mu code can be sure of using
\n as a line-ending convention when manipulating the text.

In terms of the current implementation, the convention from the incoming
file could presumably be stored on the tab object.

Implemented via:
~~~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/pull/390
* https://github.com/mu-editor/mu/pull/399

Discussion in:
~~~~~~~~~~~~~~

* (original change) https://github.com/mu-editor/mu/pull/133
* https://github.com/mu-editor/mu/pull/371
* https://github.com/mu-editor/mu/issues/380
