import sys

from tapestry.screen import Screen
from tapestry.textbox import Textbox
from tapestry.window import Window


class Simple:
    def __init__(self):
        "Create the example Screen"
        Screen(self.event_loop)

    def event_loop(self, screen):
        "The main event_loop for the application"

        vert_split = int((screen.num_cols() / 4) * 3)
        vert_size = int(screen.num_cols() / 4)

        # The main window
        Window(screen, vert_split, screen.num_lines() - 5, 0, 0)

        # The sidebar
        Window(screen, vert_size, screen.num_lines() - 5, vert_split, 0)

        # The edit or command window
        editwin = Window(screen, screen.num_cols(), 5, 0,
                         screen.num_lines() - 5)

        screen.refresh()

        box = Textbox(editwin)

        # Let the user edit until CTRL-G or CTRL-C is struck.
        box.edit()

        # Get resulting contents
        message = box.gather()
        sys.stderr.write("message: {}\n".format(message))


if __name__ == "__main__":
    simple = Simple()
