# project3.py
#
# ICS 33 Fall 2022
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

from grin.simulation import Simulation
from grin.token import GrinToken
from grin.parsing import parse

def read_input_from_shell() -> list[list[GrinToken]]:
    """ Get user's input from the PowerShell, and process the input to a list of GrinToken.
    Returns:
        list: The processed input, of type GrinToken
    """
    lines = []
    while True:
        line = input().strip()
        if line == '.':
            break
        try:
            line = list(parse([line]))[0]
        except:
            print("Error input in '{}', Program exit!".format(line))
            break
        lines.append(line)
    return lines

def main():
    """do the simulation of Grin"""
    lines = read_input_from_shell()
    Sim = Simulation(lines)
    Sim.simulation()


if __name__ == '__main__':
    main()
