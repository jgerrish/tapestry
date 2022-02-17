from curses import textpad


class Textbox:
    "Create a Textbox that allows user editing"
    def __init__(self, window):
        "Create a Textbox with an already created Window"
        self.textbox = textpad.Textbox(window.window)

    def edit(self):
        "Activate editing mode, until the user presses CTRL-C or CTRL-G"
        return self.textbox.edit()

    def gather(self):
        "Get the contents of the Textbox"
        return self.textbox.gather()
