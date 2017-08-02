Mu Icon List / Requirements
===========================

Mu is a code editor for beginner programmers. It's likely to be used by kids as
young as eight as well as beginner adults and teachers.

Mu currently has three different modes:

1. Standard Python - for regular Python development.
2. BBC micro:bit - for MicroPython development on the BBC micro:bit.
3. Adafruit - for CircuitPython development on Adafruit boards.

In addition, Mu has two themes: "day" and "night". The day theme is simply the
standard look for the application, whereas the night theme is an intentionally
high-contrast theme for those with visual impairments or for users of shonky
projectors.

I've included some screenshots:

* mu-annotated.png - A screenshot of Mu with some annotations describing the
  placement of icons within the UI. This also shows "day" mode.

* mu-high-contrast.png - An example of the "night" mode.

* mu-adafruit.png / mu-microbit.png / mu-python.png - Examples of how the icons
  change between modes.

* mu-running.png - An example of how the UI (currently) looks when Mu is
  running a script (note the "stop" icon).

* mu-mode-select.png - The dialog that pops up when you change mode.

All the screenshots are a 100% sized view of the editor.

The look of the icons should be simple, playful and friendly. The UI needs to
appeal to beginners so mustn't appear intimidating. The gold (#ffcc00) / blue
(#336699) colours currently used are those associated with the Python brand.
Since this is a Python code editor, the colours are useful to make this sort of
association.

In terms of the list of icons and their context within the application as per
the screenshots above, the requirements are as follows:

New - creates a new Python file.
Load - load an existing file from the filesystem.
Save - Save the current existing file to the filesystem.

Run - Only used in Python mode: execute the current script.

Stop - Only used in Python mode: stop the currently executing script.

Flash - Only used in micro:bit mode: copy (flash) your code onto the device.

Files - Only used in micro:bit mode: open a file explorer representing the
filesystem on the micro:bit device.

REPL - Used by all modes. A REPL (Read Evaluate Print Loop) is a way to type
Python commands directly into the computer. If you ever used an old BBC micro
before we had Windows based UI then you'll know what I mean. In any case,
here's an example of someone using a similar Python REPL:
https://youtu.be/QgaPZG_OzW0?t=2m20s

ZoomIn - to make the text in the editor pane bigger.

ZoomOut - to make the text in the editor pane smaller.

Theme (Day) - toggle to the default "day" theme.

Theme (Night) - toggle to the high-contrast "night" theme.

Check - perform a helpful check of the code in the editor window.

Help - open up online help.

Quit - stop Mu.

At the bottom-right of the editor is a small "cog" icon. If you click on it
then a window pops up containing the logs Mu has written for your coding
session. We use logs to work out what's been going on for debugging purposes
and teachers use logs to check on how learners have interacted with the editor.

In addition we need three additional icons (that don't yet exist). These are
of the debugger:

step over - step over the current line of code (moving the debugger forward one
line).

step in - step into a function that's called in the current line of code
(moving the debugger to the location of the called function).

step out - step out of a function (moving the debugger back to the original
code that called the current function).

The debug-icons.png image contains visual representations of step over, step in
and step out that are typical of many debuggers.

It would be really good to have high-contrast versions of the icons to use with
the "night" theme.

Mu is "responsive" in that the size of the icons changes as the
application is resized on the desktop. Some Pi users have very low resolution
screens and so we make this adjustment for their sake. We use three sizes of
icon to achieve this effect: 64x64, 48x48 and 32x32 (measured in pixels).

Finally, we want others to be able to create their own modes in the future. As
a result they're likely going to have to create their own icons for
as-yet-unknown functionality. The current icons are all based upon FontAwesome
for this very reason: there's a good selection of stock icons to choose from
with an existing "look" for those who need to start from scratch.

I (Nicholas) am a programmer - I can't do design, I can only describe
intentions and uses for things with perhaps some guidance on personality. I
trust you, the designer, to make something that both looks awesome yet is also
useful too. :-)

Thanks!
