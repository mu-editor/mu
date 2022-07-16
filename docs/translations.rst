Internationalisation of Mu
==========================

A really useful and relatively simple way to contribute to Mu is to translate
the user interface into a different language. The steps to do this are very
simple and there exist plenty of tools to help you.

You can contribute in three ways:

* Improve or extend an existing translation.
* Create a completely new translation for a new language.
* Make a translation of `Mu's website <https://codewith.mu/>`_ (see the
  :doc:`website` guide for how to do this).

In both cases you'll be using assets found in the ``mu/locale`` directory.

Mu uses Python's standard `gettext <https://docs.python.org/3.6/library/i18n.html>`_
based internationalization API so we can make use of standard tools to help
translators, such as `babel <https://babel.pocoo.org/en/latest/>`_ or
`Poedit <https://poedit.net/>`_.

.. admonition:: Non-technical users

    If you are not a technical user and you are not familiar with the
    tools and jargon we use in this guide,
    please reach out to us by
    `creating a new issue in GitHub <https://github.com/mu-editor/mu/issues/new>`_.

    We will help you set up a user-friendly tool that you can use to
    contribute new or improved translations, and integrate them into the next
    Mu release.

    We welcome translations from all users!



How To
------

Updating or creating a new translation for Mu's user interface requires
:doc:`setting up a development environment <setup>` beforehand and,
from there,
is a four-step process:


1. Produce an up to date ``mu.po`` file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open a CLI shell,
change the working directory to Mu's repository root,
and run::

    $ make translate_begin LANG=xx_XX

Where ``xx_XX`` is the identifier for the target language.

This creates (or updates, if it already exists) the ``mu.po`` file under the
``mu/locale/xx_XX/LC_MESSAGES/`` directory --
this is where the original British English messages
are associated with their localized translations.


2. Translate Mu user interface strings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use a tool of your choice to edit the ``mu.po`` file:

* Those looking for a GUI based tool can try out `Poedit <https://poedit.net>`__.
* Others might prefer a plain text editor, which will be sufficient.


3. Check the translation result
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As you progress,
check the translation results by launching Mu with::

    $ make translate_test LANG=xx_XX

As before,
``xx_XX`` is the identifier for the target language.

When done checking,
quit Mu,
and go back to step 2. as many times as needed.


4. Submit your translation work
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This process produced two new or updated files,
both under the ``mu/locale/xx_XX/LC_MESSAGES/`` directory:

* ``mu.po`` containing the text based source of the translation strings.
* ``mu.mo`` containing a compiled version of the above, used by Mu at runtime.

Commit your changes and create a pull request via GitHub.

Thanks!
