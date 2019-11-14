Roadmap (Mappa MUndi)
---------------------

(Apologies for the pun: https://en.wikipedia.org/wiki/Mappa_mundi)

Mu started as a shonky hack. Now many people are interested in our small editor
for educational use and we owe it to them to be clear what our plans are, how
we work together and how *anyone* can get involved (see ``CONTRIBUTING.rst``).

I believe it worth repeating the Mu philosophy we have followed so far:

* Less is More: Mu has only the most essential features, so users are not
  intimidated by a baffling interface.
* Path of Least Resistance: Whatever the task, there is always only one obvious
  way to do it with Mu.
* Keep it Simple: It's quick and easy to learn Mu ~ complexity impedes a novice
  programmer's first steps.
* Have fun: Learning should inspire fun ~ Mu helps learners quickly create and
  test working code.

Python aims to make code readable, Mu aims to make it writeable.

With this in mind:

Next Point Release
==================

1.0.1 is a bug fix / translations release and will only include:

* Update to Adafruit boards and future proofing for as-yet-unknown boards.
* Swedish translation.
* Updated and complete Chinese translation.
* Blocking IO from Python 3 sub-process flooding data is fixed.
* New MicroPython runtime for micro:bit (bug fixes).
* Improvements to the stability of micro:bit flashing.

Expected delivery: mid-September 2018.

Next Minor Release
==================

1.1.0 will introduce some new "beta" modes:

* ESP mode for embedded devices from ESP.
* Web mode for creating simple dynamic websites.

It will also add some new features:

* Use of "black" for code style / quality checking.
* Configuration of UI for purposes of better presentation:

  - Change size of buttons.
  - Tool-tips and auto-complete toggle.
  - Colour configuration for "Custom" theme (help dyslexic users via colour).
  - Transparent background (makes screen-casting easier).

* Update minifier.
* More translations.
* Cleanups to the documentation.
* Bug fix release of MicroPython for micro:bit.

Expected delivery: late-November 2018.
