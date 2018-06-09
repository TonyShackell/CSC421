# monopoly.py
#
# simulate a reduced game of monopoly for the purposes of probabilistic modelling
#
# Author: Anthony Shackell - June 8, 2018

import math, random, operator, numpy as np

NUM_TURNS = 100
NUM_SIMULATIONS = 1000
BOARD_SIZE = 40
# 6 chance cards deal with money, which we don't care about and thus are represented
# as zeros in the 'deck'
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
                ('Advance', [-3]), # Go back three spaces
                ('Advance', [39]), # Advance to Boardwalk
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
    #TODO: implement being locked in jail

    global_probability_matrix = [0.0 for x in range(BOARD_SIZE)]

    for simulation in range(NUM_SIMULATIONS):

        simulation_probability_matrix = [0.0 for x in range(BOARD_SIZE)]
        current_space = 0
        goj_free = 0
        num_movements = 0

        for turn in range(NUM_TURNS):
            roll, roll_again = roll_dice()
            num_rolls = 1
            current_space = (current_space + roll) % BOARD_SIZE
            num_movements += 1
            simulation_probability_matrix[current_space] += 1.0

            if current_space in CHANCE_SPACES:
                chance_card = select_chance_card()
                if chance_card[0] == None:
                    pass
                elif chance_card[0] == 'Advance':
                    #TODO: select nearest element from list of spaces to move
                    pass
                elif chance_card[0] == 'Move Directly':
                    current_space = chance_card[1][0]
                    num_movements += 1
                elif chance_card[0] == 'Get Out of Jail Free':
                    goj_free = True


            while roll_again and num_rolls < 3:
                roll, roll_again = roll_dice()
                num_rolls += 1
                # go to jail for speeding if we roll three doubles in a row
                if num_rolls == 3 and roll_again:
                    current_space = 10
                else:
                    current_space = (current_space + roll) % BOARD_SIZE
                simulation_probability_matrix[current_space] += 1.0
                num_movements += 1

        simulation_probability_matrix[:] = [x / num_movements for x in simulation_probability_matrix]
        global_probability_matrix = list(map(operator.add, global_probability_matrix, simulation_probability_matrix))

    global_probability_matrix = [x / NUM_SIMULATIONS for x in global_probability_matrix]
    print ['%.5f'%x for x in global_probability_matrix], sum(global_probability_matrix) # print average probabilities. NOTE avg will not sum to 1.

if __name__ == '__main__':
    main()
