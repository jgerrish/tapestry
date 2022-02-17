import curses
from curses.textpad import rectangle
from dataclasses import dataclass

from tapestry.screen import Screen


@dataclass
class Window:
    """
    A Curses Window

    The Window class creates both a window and a surrounding rectangle
    that surrounds the window.
    """
    screen: Screen

    width: int
    "The width of the window"

    height: int
    "The height of the window"

    x_location: int
    "The left-up corner x location"

    y_location: int
    "The left-up corner y location"

    def __post_init__(self):
        """
        Create the curses window and rectangle object as a border for
        the window.
        """
        # curses.newwin(nlines, ncols, begin_y, begin_x)
        self.window = curses.newwin(self.height - 2,
                                    self.width - 3,
                                    self.y_location + 1,
                                    self.x_location + 1)

        # curses.textpad.rectangle(win, uly, ulx, lry, lrx)
        self.border = rectangle(self.screen.stdscr,
                                self.y_location, self.x_location,
                                self.height + self.y_location - 1,
                                self.width + self.x_location - 2)

    def addstr(self, *args):
        """
        Add a string to the window
        This method takes one or three arguments:
          addstr(str): Adds a string to the current cursor location
          addstr(x, y, str): Adds a string to the location (x, y)
        """
        if len(args) == 1:
            return self.window.addstr(args[0])
        elif len(args) == 3:
            return self.window.addstr(args[1], args[0], args[2])
        else:
            raise Exception

    def write(self):
        ""
        pass

    def keypad(self, arg):
        return self.window.keypad(arg)
