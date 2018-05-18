# cities_ai.py
#
# Simulate a variety of uninformed and informed search algorithms for traversal between states
# For each simulation round:
#
# There will be a 2d matrix (26 x [2]) representing the "world" that the cities will be uniformly distributed across
#
# The location of each city will be chosen at random via a random number generator in python, and cities will be placed on the grid provided there is not currently another city there
#
# A random number generator will provide the starting location of the agent, and the destination
#
# A random number generator for each city will provide a number n between 1 and 4, which will determine the number of paths from the city to its closest n neighbors
#
# There will be a 26 x 26 symmetric matrix such that there is a non-negative value between cities i and j if there is a path between those cities; the cost will be determined by the value in the matrix at (i, j). The Euclidean distances will be calculated upon edge insertion

import random
import math
import numpy as np
import matplotlib.pyplot as plt

WORLD_SIZE = 5

WORLD = [[] for x in range(WORLD_SIZE)]
DISTANCES = np.zeros((WORLD_SIZE, WORLD_SIZE))
PATHS = np.zeros((WORLD_SIZE, WORLD_SIZE))

def generate_city_locations():
    for city in range(len(WORLD)):
        new_location = [random.randint(0, 99), random.randint(0, 99)]
        while new_location in WORLD:
            new_location = [random.randint(0, 99), random.randint(0, 99)]
        WORLD[city] = new_location

def compute_euclidean_distances():
    for city_number in range(len(WORLD)):
        for neighbouring_city in range(city_number+1, len(WORLD)):
            city_distance = math.sqrt((WORLD[city_number][0] - WORLD[neighbouring_city][0])**2 + (WORLD[city_number][1] - WORLD[neighbouring_city][1])**2)

            # create a symmetric matrix without doing work twice. Who likes redundancy, anyways?!
            DISTANCES[city_number][neighbouring_city] = city_distance
            DISTANCES[neighbouring_city][city_number] = city_distance

def generate_edges():
    for city in range(len(DISTANCES)):
        number_of_edges = random.randint(1, 4)
        # get closest neighbours and get rid of self-loop
        closest_neighbours = np.argsort(DISTANCES[city])[:number_of_edges + 1][1:]
        print closest_neighbours
        for neighbour in closest_neighbours:
            # print neighbour, type(neighbour)
            PATHS[city][neighbour.item()] = DISTANCES[city][neighbour.item()]
            PATHS[neighbour.item()][city] = DISTANCES[city][neighbour.item()]

def setup():
    generate_city_locations()
    compute_euclidean_distances()
    generate_edges()

def main():
    setup()

    print PATHS
    # display the city locations on a plot
    plt.plot([x[0] for x in WORLD], [y[1] for y in WORLD], 'ro')
    plt.axis([0, 99, 0, 99])
    plt.show()


if __name__ == '__main__':
    main()
