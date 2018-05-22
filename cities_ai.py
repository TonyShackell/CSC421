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

WORLD_SIZE = 26

WORLD = [[] for x in range(WORLD_SIZE)]
DISTANCES = np.zeros((WORLD_SIZE, WORLD_SIZE))
EDGES = np.zeros((WORLD_SIZE, WORLD_SIZE))


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
    # TODO: possibly - if the edge exists between two nodes already, do we want to discard
    # and take the next closest neighbour?
    total_edges = 0.0

    for city in range(len(DISTANCES)):
        number_of_edges = random.randint(1, 4)
        total_edges += number_of_edges
        # get closest neighbours and get rid of self-loop (will always be at start of closest neighbour list)
        closest_neighbours = np.argsort(DISTANCES[city])[:number_of_edges + 1][1:]
        for neighbour in closest_neighbours:
            EDGES[city][neighbour.item()] = DISTANCES[city][neighbour.item()]
            EDGES[neighbour.item()][city] = DISTANCES[city][neighbour.item()]

    print "average number of edges for simulation round:" + str(total_edges / WORLD_SIZE)


def breadth_first_search(start_node, destination_node):
    # start will never be destination
    search_paths = [[start_node]]
    cities_visited = [0 for x in range(WORLD_SIZE)]

    while search_paths:
        current_path = search_paths.pop(0)
        search_city = current_path[-1]
        cities_visited[search_city] = 1

        neighbours = [i for i, e in enumerate(EDGES[search_city]) if e != 0]
        for neighbour in neighbours:
            new_path = current_path[:]
            new_path.append(neighbour)
            if neighbour == destination_node:
                return new_path
            else:
                if cities_visited[neighbour]:
                    continue
                else:
                    search_paths.append(new_path)

    return None


def depth_first_search(start_node, destination_node):
    # start will never be destination
    search_paths = [[start_node]]
    cities_visited = [0 for x in range(WORLD_SIZE)]

    while search_paths:
        current_path = search_paths.pop()
        search_city = current_path[-1]
        cities_visited[search_city] = 1

        neighbours = [i for i, e in enumerate(EDGES[search_city]) if e != 0]
        for neighbour in neighbours:
            new_path = current_path[:]
            new_path.append(neighbour)
            if neighbour == destination_node:
                return new_path
            else:
                if cities_visited[neighbour]:
                    continue
                else:
                    search_paths.append(new_path)

    return None


def iterative_deepening_search(start_node, destination_node):
    #TODO: make this efficient. Currently regenerates up to depth-1 paths
    #also why is it not returning the shortest length?

    # because we dont allow cycles, we can have at most WORLD_SIZE-1 state transitions
    for depth in range(WORLD_SIZE):
        # start will never be destination
        search_paths = [[start_node]]

        #print "\nDepth:", depth
        while search_paths:
            cities_visited = [0 for x in range(WORLD_SIZE)]

            #print "SPs:", search_paths
            current_path = search_paths.pop()
            search_city = current_path[-1]
            cities_visited[search_city] = 1

            neighbours = [i for i, e in enumerate(EDGES[search_city]) if e != 0]
            for neighbour in neighbours:
                new_path = current_path[:]
                new_path.append(neighbour)
                if neighbour == destination_node:
                    return new_path
                else:
                    if cities_visited[neighbour]:
                        continue
                    else:
                        if len(new_path) <= depth:
                            search_paths.append(new_path)

    return None


def best_first_search():
    pass


def a_star():
    pass


def setup():
    generate_city_locations()
    compute_euclidean_distances()
    generate_edges()


def main():
    setup()

    start_node = random.randint(0, 25)
    destination_node = random.randint(0, 25)

    while destination_node == start_node:
        destination_node = random.randint(0, 25)

    # for x in range(WORLD_SIZE):
    #     print str(x) + ":", [(i, e) for i, e in enumerate(EDGES[x]) if e != 0]

    print "Start node: " + str(start_node) + "\nDestination Node: " + str(destination_node)
    print "Optimal Path (BFS):", breadth_first_search(start_node, destination_node)
    print "Possible non-optimal Path (DFS):", depth_first_search(start_node, destination_node)
    print "Optimal Path (ID-DFS):", iterative_deepening_search(start_node, destination_node)

    # display the city locations on a plot
    # plt.plot([x[0] for x in WORLD], [y[1] for y in WORLD], 'ro')
    # plt.axis([0, 99, 0, 99])
    # plt.show()

if __name__ == '__main__':
    main()
