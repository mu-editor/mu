from mu.hybrid.repl import find_microbit


class Editor:

    def __init__(self):
        self.repl = None

    def add_repl(self):

        if self.repl is not None:
            raise RuntimeError("REPL already running")

        mb_port = find_microbit()

        if not mb_port:
            raise ResourceWarning("Could not find an attached micro:Bit")

        self.repl = REPL(port="/dev/{}".format(mb_port))
