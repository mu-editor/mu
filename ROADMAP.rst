Mu Roadmap (Mappa MUndi)
------------------------

(Apologies for the pun: https://en.wikipedia.org/wiki/Mappa_mundi)

Mu started as a shonky hack. Now many people are interested in our small editor
for educational use and we owe it to them to be clear what our plans are, how
we work together and how *anyone* can get involved (see ``CONTRIBUTING.rst``).

This is not so much a roadmap as a cartographic exercise to pull together all
the different areas of Mu that people have been working on. By doing so
*everyone* can see what's going in the project and find something to which
they can contribute if they so wish.

This is a first draft. It's a straw man. It will contain mistakes and overlook
important stuff. In the spirit of open collaboration, cooperation and community
focussed development please feel free to annotate comments, suggest changes and
point out omissions.

I believe it worth repeating the Mu philosophy we have followed so far:

* Less is More: Mu has only the most essential features, so users are not intimidated by a baffling interface.
* Path of Least Resistance: Whatever the task, there is always only one obvious way to do it with Mu.
* Keep it Simple: It's quick and easy to learn Mu ~ complexity impedes a novice programmer's first steps.
* Have fun: Learning should inspire fun ~ Mu helps learners quickly create and test working code.

With this in mind, the following features are collected in no particular order
under a bunch of headings so we can see related effort. Let's revise and find a
consensus (it'll be fun!).

:-)

Internationalisation
====================

* Python, like music, is an international language. Beginners must not be excluded from learning to program because their tools work in an unfamiliar (human) language. While Python uses English keywords, the UI should reflect the learner's written language, locale and culture.
* Our documentation should also respect our user's written language, locale and culture without implication that English is the only way to go.
* We should have a clear infrastructure, documentation and well organised code such that anyone can contribute translation and localisation effort to the project.

Accessibility
=============

* Mu should make beginners think "this is somewhere I belong". It must help everyone given the diverse range of abilities our users may have. To do this we should make it easy for assistive technology such as screen readers and braille devices to work with Mu.
* To ensure we make Mu easy to grok by developers there should be a clear and obvious description of our accessibility related design decisions.
* Accessibility also includes addressing special educational needs (at both ends of the spectrum).
* For learners working towards basic programming competence Mu should feel safe, encouraging and guide them towards fulfilling the basic skills needed to learn to program. This may include context sensitive help, walk-throughs, and adaptive UI elements (for example, as a simple feature is repeatedly used, it becomes more powerful as more subtle features are revealed).
* For learners working beyond basic programming skills it should be simple to switch to "I know what I'm doing" mode. Furthermore, it should be possible to customise Mu to some extent and/or surface more advanced features through editing a settings file.
* We should encourage and engage with UX specialists. Computing is not just about programming and it would be wonderful if Mu led people to HCI related aspects of our field.

Code Refactor
=============

* Mu is designed to be simple to code: our hope is that advanced learners will know enough to be able to understand how it works. We want our users to take ownership of the tool. Despite such simplicity there are aspects of the logic and interface code that are not cleanly separated. These should be disentangled (for example, use of Qt serial in the interface layer rather than PySerial in the logic layer).
* A clean separation of logic and interface means other UI libraries could be used. For example, BeeWare have expressed an interest in helping to port Mu. It also means others have the freedom to change the look and feel of their version of Mu without having to disentangle the logical features.
* Furthermore, not all the features implemented in the logic layer need be exposed by Mu. Discussion of MegaMu (a more featureful version of Mu) has taken place and providing a selection of features for UI designers to pick'n'mix depending on the needs of their users would make Mu a compelling solution for editor designers.
* How the logic and interface layers interact should be clearly documented.

Generic Editor
==============

* The RPi Foundation have asked that we support other Python contexts. For example, having the ability to create / write PyGameZero, GPIOZero and NetworkZero based projects with the UI automatically updating as the context changes. I have an old branch that provides a model for this in the logic layer that reaches into the interface layer. It's an exploratory spike that I believe could bear fruit.
* To help in the user's graduation to a "real" editor we should ensure generic editor behaviours work as per the conventions: shortcut keys are the same, editing activities (e.g. selecting and acting upon blocks of code) should work as expected and helpful features (like code completion and call tips) should work in "the usual way".

Multi Device Support
====================

* Adafruit, Calliope and others have expressed an interest in Mu supporting their devices. It should, and do so automagically. It should be possible to use USB's manufacturer and device ID's to work out what's plugged in and adapt accordingly.
* It should be obvious from the source code how to add newly supported devices. This may be related to the "Python contexts" work mentioned in the Generic Editor section above. Such work should at least encompass adding flashing a device with the appropriate version of MicroPython, copying / flashing scripts to the device and connecting to an on-board file-system and connecting to the REPL.

New Features
============

* Carlos has a spike proof of concept for Blockly integration (i.e. visual programming a la Scratch - move blocks around to create a program and it emits Python). Should we implement this (and I believe many teachers would love to see this) we *must* address the problem of migrating beginners from a visual style of programming to text based programming. This could be addressed by some of the UI related points from above.
* The REPL, while an amzingly powerful feature, can appear a little unfriendly to beginners. Jupyter notebooks are a replacement for the REPL but also allow additional annotations and images to interweave with the code to be evaluated. That they can be shared and are fully editable also means they're a great way to share a "movement of thought" in words, code and pictures. I'd like to explore how these could be used to deliver lesson plans, exercises and "follow-along" resources for teachers and learners.

Documentation
=============

* We need some.
* Read the Docs looks like a good place to start - especially since they appear to support internationalisation and can watch our repos for update.

Website
=======

* Is currently a bootstrap based affair cobbled together one afternoon by me and improved at PyCon UK.
* Installation instructions / videos.
* "How do I?" instructions / videos.
* I guess we need design work and a logo (I know just the person to ask: Steve Hawkes does the amazing design work for PyCon UK).

Releases
========

* We should investigate packaging for Windows and OSX. Perhaps the PSF could fund the necessary developer keys needed to sign such packages.
* We should also engage with Debian and Ubuntu (Fedora is already in hand thanks to Kushal) for packaging. Mu is already packaged in Raspbian although it's unclear who or how to update the package.
* We should be fearless in making releases. Everything should be automated with tests at the appropriate points in the process to ensure we don't release a dud.
* How could we get an already installed executable to auto-update itself?
