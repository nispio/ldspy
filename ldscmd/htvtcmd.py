
from __future__ import print_function

from cmd import Cmd

# This will be a command-line interface for dealing with the htvt database.
# Eventually, I would like to get a GUI running

class htvtCmd(Cmd, object):
    """Simple command processor example."""
    def __init__(self):
        super(htvtCmd, self).__init__()
        self.prompt = 'htvt> '

    def do_greet(self, line):
        print("Hello World!")

    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        print()
        return True

    do_quit = do_exit
    do_q = do_quit

if __name__ == '__main__':
    htvtCmd().cmdloop()
