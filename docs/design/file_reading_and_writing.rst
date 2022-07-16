Reading and writing code files
==============================

Decision
--------

By default Mu will save files encoded as UTF-8 without a PEP 263 encoding cookie.
However, if the file as loaded started with an encoding cookie, then the file
will be saved again with that encoding.

When reading files, Mu will detect UTF8/16 BOMs and encoding cookies.
In their absence, UTF-8 will be attempted. If that fails, the OS default will
be used (ie locale.getpreferredencoding()).

If the file cannot be decoded according to these rules, refuse to guess. Instead,
produce an informative error popup.

Background
----------

Originally Mu used the built-in open() function for reading and writing its
files without specifying an encoding. In that situation Python would request
the preferred encoding for the locale and use that. If the user then used
a character in their code which had no mapping in that encoding, the save/autosave
functionality would raise an uncaught exception and the user would lose their
code.

Discussion and Implementation
-----------------------------

It was initially suggested that we simply read/write everything as UTF-8
which can encode the entire universe of Unicode codepoints. However, files
which had previously been saved by Mu under a different encoding might
produce mojibake or simply raise UnicodeDecodeError.

To overcome the difficulty of using UTF-8 going forwards without losing backwards
compatibility, the compromise was adopted of *writing* UTF-8 with an encoding
cookie, while *reading* according to the rules above.

It will still possible for a file to fail decoding on the way in
(eg because the locale-default encoding is used, but the file is encoded otherwise).
In that situation we might have attempted to reload using, eg, latin-1 which
can decode every byte to *something*. But the result would have been mojibake
and -- crucially -- the autosave mechanism would have kicked in 30 seconds
later, overwriting the user's original file for good.

Instead it was decided to offer an informative message box which could explain
the situation in enough terms to offer the user a way forward without risking
the integrity of their code.

UPDATE: After initial implementation of the encoding cookie, it was thought
that it was too arcane for beginner coders. It was decided then to save as
UTF-8 by default, although without a cookie. But if a file already has an
encoding cookie, that should be preserved and the encoding honoured.

Implemented via:
~~~~~~~~~~~~~~~~

* https://github.com/mu-editor/mu/pull/390
* https://github.com/mu-editor/mu/pull/399
* https://github.com/mu-editor/mu/pull/418

Discussion in:
~~~~~~~~~~~~~~

(Initial)

* https://github.com/mu-editor/mu/issues/370
* https://github.com/mu-editor/mu/pull/364
* https://github.com/mu-editor/mu/pull/371

(Later)

* https://github.com/mu-editor/mu/issues/402
* https://github.com/mu-editor/mu/issues/696
