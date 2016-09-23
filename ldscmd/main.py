#!/usr/bin/env python

import sys
from os.path import abspath, dirname

# Hack to put this package and ldstools into the python path
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from ldscmd.htvtcmd import htvtCmd

def Run():
    htvt = htvtCmd()
    htvt.cmdloop()

if __name__ == "__main__":
    Run()
