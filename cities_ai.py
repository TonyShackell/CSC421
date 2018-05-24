# cities_ai.py
#
# Simulate a variety of uninformed and informed search algorithms for traversal between states.
# Covers BFS, DFS, ID-DFS, Greedy Best-First, and A-Star searches.
#
# Author: Anthony Shackell - May 19, 2018

import random
import math
import numpy as np
import string
import matplotlib.pyplot as plt
import heapq as hq

WORLD_SIZE = 26

WORLD = [[] for x in range(WORLD_SIZE)]
DISTANCES = np.zeros((WORLD_SIZE, WORLD_SIZE))
EDGES = np.zeros((WORLD_SIZE, WORLD_SIZE))
LABELS = dict(zip(range(0,26), string.ascii_uppercase))


def generate_city_locations():
	"""
	generate_city_locations()

	@params - none

	disperse WORLD_SIZE cities across the map with uniform randomness.
	"""
	for city in range(len(WORLD)):
		new_location = [random.randint(0, 99), random.randint(0, 99)]
		while new_location in WORLD:
			new_location = [random.randint(0, 99), random.randint(0, 99)]
		WORLD[city] = new_location


def compute_euclidean_distances():
	"""
	compute_euclidean_distances()

	@params - none

	compute the euclidean distance from all cities to all other cities and store in DISTANCES.
	"""
	for city_number in range(len(WORLD)):
		for neighbouring_city in range(city_number+1, len(WORLD)):
			city_distance = math.sqrt((WORLD[city_number][0] - WORLD[neighbouring_city][0])**2 + (WORLD[city_number][1] - WORLD[neighbouring_city][1])**2)

			# create a symmetric matrix without doing work twice. Who likes redundancy, anyways?!
			DISTANCES[city_number][neighbouring_city] = city_distance
			DISTANCES[neighbouring_city][city_number] = city_distance


def generate_edges():
	"""
	generate_edges()

	@params - none

	randomly choose between 1 and 4 of each cities closest neighbours and create an edge between them, with the euclidean distance between the cities as the path cost.
	"""
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
	"""
	breadth_first_search()

	@params - start_node, destination_node

	perform a breadth first search from start_node to destination_node
	"""
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
	"""
	depth_first_search()

	@params - start_node, destination_node

	perform a depth first search from start_node to destination_node
	"""
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
	"""
	iterative_deepening_search()

	@params - start_node, destination_node

	perform a iterative deepening search from start_node to destination_node
	"""

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


def greedy_best_first_search(start_node, destination_node):
	"""
	greedy_best_first_search()

	@params - start_node, destination_node

	perform a greedy best-first search from start_node to destination_node
	"""
	# start will never be destination
	# use a min queue with distance from last node in path to destination as index value
	# that way the popped node will always be the closest node to the dest and we can still retain the path
	# do not add a path to the queue if the last node on the path has already been visited (non-optimal, but complete)
	search_paths = []
	hq.heappush(search_paths, (DISTANCES[start_node][destination_node], [start_node]))

	cities_visited = [0 for x in range(WORLD_SIZE)]

	while search_paths:
		current_path = hq.heappop(search_paths)[1]
		search_city = current_path[-1]

		if search_city == destination_node:
				return current_path

		cities_visited[search_city] = 1

		# get ordered list of neighbours by distance
		closest_neighbours = np.argsort(EDGES[search_city])[-np.count_nonzero(EDGES[search_city]):]

		for neighbour in closest_neighbours:
			new_path = current_path[:]
			new_path.append(neighbour)
			distance_to_destination = DISTANCES[neighbour][destination_node]
			if cities_visited[neighbour]:
				continue
			hq.heappush(search_paths, (distance_to_destination, new_path))
	return None


def a_star_search(start_node, destination_node):
	"""
	a_star_search()

	@params - start_node, destination_node

	perform an a-star search from start_node to destination_node
	"""
	# start will never be destination
	# use a min queue with (distance from last node in path to destination + past cost to date) as index value
	# that way the popped node will always be the closest node to the dest and we can still retain the path
	# do not add a path to the queue if the last node on the path has already been visited
	search_paths = []
	hq.heappush(search_paths, (DISTANCES[start_node][destination_node], 0, [start_node]))

	cities_visited = [0 for x in range(WORLD_SIZE)]

	while search_paths:
		state = hq.heappop(search_paths)
		current_path = state[2]
		search_city = current_path[-1]

		if search_city == destination_node:
				return current_path

		cities_visited[search_city] = 1

		# get ordered list of neighbours by distance
		closest_neighbours = np.argsort(EDGES[search_city])[-np.count_nonzero(EDGES[search_city]):]

		for neighbour in closest_neighbours:
			new_path = current_path[:]
			new_path.append(neighbour)
			distance_to_destination = DISTANCES[neighbour][destination_node]
			total_cost_to_date = state[1] + EDGES[search_city][neighbour]


			if cities_visited[neighbour]:
				continue
			hq.heappush(search_paths, (distance_to_destination + total_cost_to_date, total_cost_to_date, new_path))
	return None


def compute_path_cost(path):
	"""
	compute_path_cost()

	@params - path: path to have cost evaluated

	return the total cost of a path from start to end
	"""

	if not path:
		return None

	current_node = path.pop(0)
	total_cost = 0

	while path:
		next_node = path.pop(0)
		total_cost += EDGES[current_node][next_node]
		current_node = next_node

	return total_cost


def setup():
	"""
	setup()

	@params - none

	setup the world by calling auxiliary functions
	"""
	generate_city_locations()
	compute_euclidean_distances()
	generate_edges()


def main():
	setup()

	start_node = random.randint(0, 25)
	destination_node = random.randint(0, 25)

	while destination_node == start_node:
		destination_node = random.randint(0, 25)

	BFS = breadth_first_search(start_node, destination_node)
	DFS = depth_first_search(start_node, destination_node)
	IDDFS = iterative_deepening_search(start_node, destination_node) if BFS is not None else None
	GBFS = greedy_best_first_search(start_node, destination_node)
	AS = a_star_search(start_node, destination_node)

	print "Start node: " + LABELS[start_node] + "\nDestination Node: " + LABELS[destination_node]
	print "Optimal-length Path (BFS, no path cost):", [LABELS[x] for x in BFS] if BFS is not None else None, "\n\tpath cost:", compute_path_cost(BFS)
	print "Possible non-optimal Path (DFS, no path cost):", [LABELS[x] for x in DFS] if DFS is not None else None, "\n\tpath cost:", compute_path_cost(DFS)
	print "Optimal-length Path (ID-DFS, no path cost):", [LABELS[x] for x in IDDFS] if IDDFS is not None else None, "\n\tpath cost:", compute_path_cost(IDDFS)
	print "Possible non-optimal Path (GBFS, path cost used):", [LABELS[x] for x in GBFS] if GBFS is not None else None, "\n\tpath cost:", compute_path_cost(GBFS)
	print "Optimal Path (A Star, path cost used):", [LABELS[x] for x in AS] if AS is not None else None, "\n\tpath cost:", compute_path_cost(AS)

	# display the city locations on a plot
	# plt.plot([x[0] for x in WORLD], [y[1] for y in WORLD], 'ro')
	# plt.axis([0, 99, 0, 99])
	# plt.show()

if __name__ == '__main__':
	main()
