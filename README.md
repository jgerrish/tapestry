# tapestry minimal curses Python wrapper

This Python package provides a set of minimal wrappers around the
default curses library included with Python.

It's meant to provide an easier interface for building applications quickly.

It also provides some testing code that demonstrate some useful patterns:

* Testing curses and other code that use custom terminal calls, this
  includes duplicating stdout and other file descriptors and restoring
  them after tests run.
* Use of context managers to wrap tests and other code and ensure
  proper setup and cleanup.
* Writing callbacks as inner functions to make testing code easier to
  understand.

Some of the code closely follows code in the CPython project,
specically the test_curses.py file provides excellent examples of
duplicating file descriptors.


# Usage

First, most functions that take coordinates have the x coordinate
first, followed by the y coordinate.  This differs from the default
curses library where the y coordinate is usually first.

Example:

PYTHONPATH=. python examples/simple.py


# Development

This project uses pytest for tests.

pipenv is used to manage this project:

To install dependencies and start developing:

$ pipenv install --dev
$ pipenv shell


# Testing

$ pipenv run python -m pytest

or

$ pipenv run python -m pytest --capture=no
