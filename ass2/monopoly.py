# monopoly.py
#
# simulate a reduced game of monopoly for the purposes of probabilistic modelling
#
# Author: Anthony Shackell - June 8, 2018

import math, random, operator

NUM_TURNS = 100
NUM_SIMULATIONS = 1000
BOARD_SIZE = 40
# 6 chance cards deal with money, which we don't care about and thus are represented
# as (None, 0) in the 'deck'
CHANCE_CARDS = [(None, 0),
                (None, 0),
                (None, 0),
                (None, 0),
                (None, 0),
                (None, 0),
                ('Advance', [0]), # Advance to GO
                ('Advance', [24]), # Advance to Illinois Ave.
                ('Advance', [11]), # Advance to St. Charles Place
                ('Advance', [12, 28]), # Advance to nearest utility
                ('Advance', [5, 15, 25, 35]), # Advance to nearest railroad
                ('Advance', [5]), # Take a ride on the reading railroad
                ('Advance', [39]), # Advance to Boardwalk
                ('Go Back', [3]), # Go back three spaces
                ('Move Directly', [10]), # Go directly to jail
                ('Get Out of Jail Free', None)] # GoJ Free
CHANCE_SPACES = [7, 22, 36]

def roll_dice():
    """
    roll_dice()

    simulate a roll of two dice.

    @params - None

    @returns - sum of the two dice, boolean of whether to roll again or not.
    """
    roll_again = False

    # di rolls are independent events
    di_1 = random.randint(1, 6)
    di_2 = random.randint(1, 6)

    # if we roll doubles we get to roll again in the same turn
    if di_1 == di_2:
        roll_again = True

    return di_1 + di_2, roll_again


def select_chance_card():
    """
    select_chance_card()

    select a chance card at random from the available deck.

    @params - None

    @returns - number indicating the chance card picked from the deck.
    """
    chance_card_index = random.randint(0,15)
    return CHANCE_CARDS[chance_card_index]


def main():

    global_probability_matrix = [0.0 for x in range(BOARD_SIZE)]

    for simulation in range(NUM_SIMULATIONS):

        simulation_probability_matrix = [0.0 for x in range(BOARD_SIZE)]
        current_space = 0
        goj_free = False
        in_jail = False
        num_movements = 0

        for turn in range(NUM_TURNS):
            # simulate being 'in jail'
            if in_jail:
                roll, roll_again = roll_dice()
                num_jail_rolls = 1

                # normally we'd have to pay money to get out of jail after three
                # non-double rolls, but here we just leave after three consecutive
                # non-double rolls, or one double roll.
                while not roll_again and num_jail_rolls < 3:
                    roll, roll_again = roll_dice()
                    # if we roll doubles
                    if roll_again:
                        break
                    num_jail_rolls += 1
                    simulation_probability_matrix[current_space] += 1.0

                current_space = (current_space + roll) % BOARD_SIZE
                simulation_probability_matrix[current_space] += 1.0
                in_jail = False
                continue

            roll, roll_again = roll_dice()
            num_rolls = 1
            current_space = (current_space + roll) % BOARD_SIZE
            num_movements += 1
            simulation_probability_matrix[current_space] += 1.0

            if current_space in CHANCE_SPACES:
                chance_card = select_chance_card()
                if chance_card[0] == None:
                    pass
                elif chance_card[0] == 'Go Back':
                    current_space = current_space - chance_card[1][0]
                    # Python's mod operator misbehaves with negative numbers
                    # always renturns a positive member of the same congruence class
                    if current_space < 0:
                        current_space += 40
                    num_movements += 1
                    simulation_probability_matrix[current_space] += 1.0
                elif chance_card[0] == 'Advance':
                    # advance to nearest element from list of spaces to move
                    # not the most elegant solution, but it works.
                    while current_space not in chance_card[1]:
                        current_space = (current_space + 1) % BOARD_SIZE
                    num_movements += 1
                    simulation_probability_matrix[current_space] += 1.0
                elif chance_card[0] == 'Move Directly':
                    current_space = chance_card[1][0]
                    num_movements += 1
                    simulation_probability_matrix[current_space] += 1.0
                    # allow room for expansion with other 'Move Directly' cards
                    if chance_card[1][0] == 10 and not goj_free:
                        in_jail = True
                        continue
                    elif chance_card[1][0] == 10 and goj_free:
                        goj_free = False
                        continue
                elif chance_card[0] == 'Get Out of Jail Free':
                    goj_free = True

            while roll_again and num_rolls < 3:
                roll, roll_again = roll_dice()
                num_rolls += 1
                # go to jail for speeding if we roll three doubles in a row
                if num_rolls == 3 and roll_again:
                    current_space = 10
                    in_jail = True
                else:
                    current_space = (current_space + roll) % BOARD_SIZE
                simulation_probability_matrix[current_space] += 1.0
                num_movements += 1

        simulation_probability_matrix[:] = [x / num_movements for x in simulation_probability_matrix]
        global_probability_matrix = list(map(operator.add, global_probability_matrix, simulation_probability_matrix))

    global_probability_matrix = [x / NUM_SIMULATIONS for x in global_probability_matrix]
    # print average probabilities.
    for x in range(BOARD_SIZE):
        print 'Space', x, 'probability:', '%.5f'%global_probability_matrix[x]

if __name__ == '__main__':
    main()
