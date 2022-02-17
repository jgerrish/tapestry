import curses
import re


class NewlineError(Exception):
    """
    Raise an exception if a newline is in a string
    This is due to an old bug:


    A bug in ncurses, the backend for this Python module, can cause
    SegFaults when resizing windows. This is fixed in
    ncurses-6.1-20190511. If you are stuck with an earlier ncurses,
    you can avoid triggering this if you do not call addstr() with a
    str that has embedded newlines. Instead, call addstr() separately
    for each line.

    A lot of old systems won't have updated curses libraries
    """
    pass


class Screen:
    """
    Screen acts as a wrapper and RAII object
    Pass your main TUI event loop into the initializer
    When your event loop exits, the Screen will be cleaned up
    """
    def __init__(self, tui_event_loop):
        """
        Initialize the Screen object
        Pass in your TUI event loop
        When the event loop exits, the screen will be cleaned up
        """
        self.nl_search = re.compile("\n")
        curses.wrapper(self.run, tui_event_loop)

    def run(self, stdscr, tui_event_loop):
        "Run the event loop with the Screen object as the main parameter"
        self.stdscr = stdscr
        return tui_event_loop(self)

    def refresh(self):
        "Refresh the window, drawing any objects to screen"
        return self.stdscr.refresh()

    def num_cols(self):
        "Number of columns in the screen"
        return curses.COLS

    def num_lines(self):
        "Number of lines in the screen"
        return curses.LINES

    def addstr(self, *args):
        """
        Add a string to the screen
        This method takes one or three arguments:
          addstr(str): Adds a string to the current cursor location
          addstr(x, y, str): Adds a string to the location (x, y)
        """
        if len(args) == 1:
            return self.stdscr.addstr(args[0])
        elif len(args) == 3:
            return self.stdscr.addstr(args[1], args[0], args[2])
        else:
            raise Exception

    def instr(self, *args):
        """
        Get a string at position (x_location, y_location)
        This expects zero, one, two or three arguments:
          instr(): get the string at the current cursor location
          instr(n): get a string of length n at the current cursor location
          instr(x, y): get a string at location (x, y)
          instr(x, y, n): get a string of length n at location (x, y)
        """
        if len(args) == 0:
            return self.stdscr.instr()
        elif len(args) == 1:
            return self.stdscr.instr(args[0])
        elif len(args) == 2:
            return self.stdscr.instr(args[1], args[0])
        elif len(args) == 3:
            return self.stdscr.instr(args[1], args[0], args[2])
        else:
            raise Exception
