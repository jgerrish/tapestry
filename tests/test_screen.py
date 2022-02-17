from contextlib import contextmanager
import curses
import os
import sys
import tempfile

from test.support import (verbose, SaveSignals)

from tapestry.screen import Screen


class TestCurses:
    """
    A class that tests the curses library This sets the standard
    output stream to go to a temporary file, so that test output
    isn't corrupted.

    Based on test_curses.py in CPython
    """
    @classmethod
    def setUpClass(cls):
        term = os.environ.get('TERM')
        if verbose:
            print(f'TERM={term}', file=sys.stderr, flush=True)
        # testing setupterm() inside initscr/endwin
        # causes terminal breakage
        stdout_fd = sys.__stdout__.fileno()
        curses.setupterm(fd=stdout_fd)

    def setUp(self):
        term = os.environ.get('TERM')
        if verbose:
            print(f'TERM={term}', file=sys.stderr, flush=True)
        if (term is None) or (term == "None"):
            return
        # TODO: re-introduce more condtional setup
        self.stack = []
        self.isatty = True
        self.output = sys.__stdout__
        stdout_fd = sys.__stdout__.fileno()
        stdin_fd = sys.__stdin__.fileno()

        self.stdout_fd = stdout_fd
        self.stdin_fd = stdin_fd

        # initstr() unconditionally uses C stdout.
        # If it is redirected to file or pipe, try to attach it
        # to terminal.
        # First, save a copy of the file descriptor of stdout, so it
        # can be restored after finishing the test.
        stdout_dup_fd = os.dup(stdout_fd)
        self.stdout_dup_fd = stdout_dup_fd

        self.addCustomCleanup(os.close, stdout_dup_fd)
        self.addCustomCleanup(os.dup2, stdout_dup_fd, stdout_fd)

        # duplicate stdin
        stdin_dup_fd = os.dup(stdin_fd)
        self.stdin_dup_fd = stdin_dup_fd

        self.addCustomCleanup(os.close, stdin_dup_fd)
        self.addCustomCleanup(os.dup2, stdin_dup_fd, stdin_fd)
        # if not sys.__stdout__.isatty():
        tmp = tempfile.TemporaryFile(mode='wb', buffering=0)
        self.tmp = tmp
        self.isatty = False
        self.addCustomCleanup(tmp.close)
        self.output = None

        # swap out stdout for the temp file
        os.dup2(tmp.fileno(), stdout_fd)

        self.save_signals = SaveSignals()
        self.save_signals.save()
        self.addCustomCleanup(self.save_signals.restore)
        if verbose and self.output is not None:
            # just to make the test output a little more readable
            sys.stderr.flush()
            sys.stdout.flush()
            print(file=self.output, flush=True)
        self.stdscr = curses.initscr()

        try:
            curses.savetty()
            self.addCustomCleanup(curses.endwin)
            self.addCustomCleanup(curses.resetty)
        except Exception as e:
            sys.stderr.write("Caught exception: {}\n".format(e))

        self.stdscr.erase()

    def addCustomCleanup(self, func, *args):
        try:
            self.stack.append((func, *args))
        except Exception as e:
            sys.stderr.write("Couldn't add cleanup function: {}\n".format(e))

    def cleanUp(self):
        try:
            for i in range(len(self.stack) - 1, -1, -1):
                (func, *args) = self.stack[i]
                func(*args)
        except Exception as e:
            sys.stderr.write("Caught exception in cleanUp: {}\n".format(e))

    # This is a context manager for running curses tests
    # It wraps the test in a try except finally block that automatically cleans
    # up and restores stdin / stdout
    @contextmanager
    def curses_test(self, mocker):
        if not sys.__stdout__.isatty():
            mocker.patch('curses.cbreak')
            mocker.patch('curses.nocbreak')
            mocker.patch('curses.endwin')
        term = os.environ.get('TERM')

        # This is for headless environments like GitHub Actions use, we'll have
        # to create some other kind of fake "framebuffer"
        # curses probably provides a test for this, we'll use this for now
        if (term == "unknown") or (term == "dumb") or (term == "None") or Term is None:
            mocker.patch('curses.setupterm')
            # This may not be the proper pattern for context managers, but it works
            # Pressure is constraining me from working on this
            yield False
        else:
            self.setUp()
            try:
                yield True
            except Exception as e:
                sys.stderr.write("Caught exception in curses_test: {}\n".format(e))
                self.cleanUp()
                raise e
            finally:
                self.cleanUp()

    def test_create_windows(self, mocker):
        "Test creating base curses windows"
        with self.curses_test(mocker) as valid_term:
            if valid_term:
                win = curses.newwin(5, 10)
                assert win.getbegyx() == (0, 0)
                assert win.getparyx() == (-1, -1)
                assert win.getmaxyx() == (5, 10)

    def test_screen_addstr(self, mocker):
        "Test adding a string to the screen"
        def event_loop(screen):
            screen.addstr(0, 0, "test")
            assert screen.instr(0, 0, 4) == b"test"

        with self.curses_test(mocker) as valid_term:
            if valid_term:
                Screen(event_loop)
