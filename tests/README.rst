Mu Tests
========

We aim for 100% test coverage - it means someone has expressed an opinion about
how all the code paths for the application should behave. THIS DOES NOT MEAN
THE CODE IS BUG FREE!

The tests are organised to mirror the structure of the application itself.

To run the test suite, ensure you're in the *root* directory of the repository
and run the following command::

    $ make check

This will run the code style analysis, code quality analysis, test suite and
coverage check. To just run each of these use the following commands:

* Coding style::

    $ make pep8

* Code quality::

    $ make pyflakes

* Test suite only::

    $ make test

* Code coverage::

    $ make coverage
