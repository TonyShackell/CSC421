# csp.py
#
# Solve a cryptarithmetic puzzle in figure 6.2 of the AIMA textbook.
#
# Author: Anthony Shackell - June 15, 2018

from constraint import *
import pprint


def cryptarithmetic():
    """
    Solve the cryptarithmetic puzzle described in figure 6.2 of the AIMA text.
    @params - None
    """
    problem = Problem()
    pp = pprint.PrettyPrinter(indent=2)

    problem.addVariables(['T', 'W', 'O', 'F', 'U', 'R'], range(10))
    problem.addVariables(['C1', 'C2', 'C3'], [0, 1])

    problem.addConstraint(AllDifferentConstraint(), ['T', 'W', 'O', 'F', 'U', 'R'])
    problem.addConstraint(lambda O, R, C1: (2 * O) == R + (10 * C1), ('O', 'R', 'C1'))
    problem.addConstraint(lambda W, U, C1, C2: C1 + (2 * W) == U + (10 * C2), ('W', 'U', 'C1', 'C2'))
    problem.addConstraint(lambda T, O, C2, C3: C2 + (2 * T) == O + (10 * C3), ('T', 'O', 'C2', 'C3'))
    problem.addConstraint(lambda F, C3: C3 == F, ('F', 'C3'))

    pp.pprint(problem.getSolutions())


def waltz_filtering():
    pass


def main():
    cryptarithmetic()

if __name__ == '__main__':
    main()
