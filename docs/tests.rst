Mu's Test Suite
---------------

We have tests so we can make changes with confidence.

We use several different sorts of test:

* `PyFlakes <https://github.com/PyCQA/pyflakes>`_ for checking for errors in
  our code.
* `pycodestyle <http://pycodestyle.pycqa.org/en/latest/intro.html>`_ for
  making sure our coding style conforms with most of the conventions of
  `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.
* `PyTest <https://pytest.readthedocs.io/en/latest/>`_ as a framework for
  writing our unit tests.
* `Coverage <https://coverage.readthedocs.io/en/coverage-4.5/>`_ for checking
  the coverage of our unit tests.

.. warning::

    We currently have 100% test coverage.

    It means **every line of code in Mu has been exercised by at least one
    unit test**. We would like to keep it this way!

    We can't claim that Mu is bug-free, but we can claim that we've expressed
    an opinion about how every line of code should behave. Furthermore, our
    opinion of how such code behaves may **NOT** be accurate or even
    desirable. ;-)

In addition, we regularly make use of the excellent
`LGTM <https://lgtm.com/projects/g/mu-editor/mu/>`_ online code quality service
written, in part, by friend-of-Mu,
`Dr.Mark Shannon <https://sites.google.com/site/makingcpythonfast/>`_.

Running the Tests
+++++++++++++++++

Running the tests couldn't be simpler: just use the ``make`` command::

    $ make check

This will run **ALL** the tests of each type.

To run specific types of test please try: ``make pyflakes``,
``make pycodestyle``, ``make test`` or ``make coverage``.

.. warning::
    
    The test suite will only work if you have installed all the requirements
    for developing Mu.

    Please see :doc:`setup` for more information on how to achieve this.

Writing a New Test
++++++++++++++++++

All the unit tests are in the ``tests`` subdirectory in the root of Mu's
repository. The tests are organised to mirror the code structure of the
application itself. For example, the tests for the ``mu.modes.base``
namespace are in the ``tests.modes.test_base.py`` file.

As mentioned above, we use PyTest as a framework for writing our unit tests.
Please refer to their
`extensive documentation <https://pytest.readthedocs.io/en/latest/>`_ for more
details.

In terms of our expectation for writing a test, we expect it to look something
like the following::

    def test_MyClass_function_name_extra_info():
        """
        This is a description of the INTENTION of the test. For
        example, we may want to know why this test is important,
        any special context information and even a reference to a
        bug report if required.
        """
        assert True  # As per PyTest conventions, use simple asserts.

We also expect your test code to pass PyFlakes and PEP checks. If in doubt,
don't hesitate to get in touch and ask.
