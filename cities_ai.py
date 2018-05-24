# cities_ai.py
#
# Simulate a variety of uninformed and informed search algorithms for traversal between states.
# Covers BFS, DFS, ID-DFS, Greedy Best-First, and A-Star searches.
#
# Author: Anthony Shackell - May 19, 2018

import random
import sys
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
	# zero the list of edges for new rounds
	global EDGES
	EDGES = np.zeros((WORLD_SIZE, WORLD_SIZE))

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
	total_nodes_added = 1
	total_nodes_visited = 0
	cities_visited = [0 for x in range(WORLD_SIZE)]

	while search_paths:
		current_path = search_paths.pop(0)
		total_nodes_visited += 1
		search_city = current_path[-1]
		cities_visited[search_city] = 1

		neighbours = [i for i, e in enumerate(EDGES[search_city]) if e != 0]
		for neighbour in neighbours:
			new_path = current_path[:]
			new_path.append(neighbour)
			if neighbour == destination_node:
				return new_path, total_nodes_added, total_nodes_visited
			else:
				if cities_visited[neighbour]:
					continue
				else:
					search_paths.append(new_path)
					total_nodes_added += 1

	return [], total_nodes_added, total_nodes_visited


def depth_first_search(start_node, destination_node):
	"""
	depth_first_search()

	@params - start_node, destination_node

	perform a depth first search from start_node to destination_node
	"""
	# start will never be destination
	search_paths = [[start_node]]
	total_nodes_added = 1
	total_nodes_visited = 0
	cities_visited = [0 for x in range(WORLD_SIZE)]

	while search_paths:
		current_path = search_paths.pop()
		total_nodes_visited += 1
		search_city = current_path[-1]
		cities_visited[search_city] = 1

		neighbours = [i for i, e in enumerate(EDGES[search_city]) if e != 0]
		for neighbour in neighbours:
			new_path = current_path[:]
			new_path.append(neighbour)
			if neighbour == destination_node:
				return new_path, total_nodes_added, total_nodes_visited
			else:
				if cities_visited[neighbour]:
					continue
				else:
					search_paths.append(new_path)
					total_nodes_added += 1

	return [], total_nodes_added, total_nodes_visited


def iterative_deepening_search(start_node, destination_node):
	"""
	iterative_deepening_search()

	@params - start_node, destination_node

	perform a iterative deepening search from start_node to destination_node
	"""
	total_nodes_added = 1
	total_nodes_visited = 0

	# because we dont allow cycles, we can have at most WORLD_SIZE-1 state transitions
	for depth in range(WORLD_SIZE):
		# start will never be destination
		search_paths = [[start_node]]

		#print "\nDepth:", depth
		while search_paths:
			cities_visited = [0 for x in range(WORLD_SIZE)]

			#print "SPs:", search_paths
			current_path = search_paths.pop()
			total_nodes_visited += 1
			search_city = current_path[-1]
			cities_visited[search_city] = 1

			neighbours = [i for i, e in enumerate(EDGES[search_city]) if e != 0]
			for neighbour in neighbours:
				new_path = current_path[:]
				new_path.append(neighbour)
				if neighbour == destination_node:
					return new_path, total_nodes_added, total_nodes_visited
				else:
					if cities_visited[neighbour]:
						continue
					else:
						if len(new_path) <= depth:
							search_paths.append(new_path)
							total_nodes_added += 1

	return [], total_nodes_added, total_nodes_visited


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
	total_nodes_added = 1
	total_nodes_visited = 0

	cities_visited = [0 for x in range(WORLD_SIZE)]

	while search_paths:
		current_path = hq.heappop(search_paths)[1]
		total_nodes_visited += 1
		search_city = current_path[-1]

		if search_city == destination_node:
				return current_path, total_nodes_added, total_nodes_visited

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
			total_nodes_added += 1
	return [], total_nodes_added, total_nodes_visited


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
	total_nodes_added = 1
	total_nodes_visited = 0

	cities_visited = [0 for x in range(WORLD_SIZE)]

	while search_paths:
		state = hq.heappop(search_paths)
		total_nodes_visited += 1
		current_path = state[2]
		search_city = current_path[-1]

		if search_city == destination_node:
				return current_path, total_nodes_added, total_nodes_visited

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
			total_nodes_added += 1
	return [], total_nodes_added, total_nodes_visited


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

	if len(sys.argv) == 1:
		print "Please specify '1' or 'many' as an argument."
		exit(1)

	setup()

	start_node = random.randint(0, 25)
	destination_node = random.randint(0, 25)

	while destination_node == start_node:
		destination_node = random.randint(0, 25)
	
	if sys.argv[1] == "1":

		BFS = breadth_first_search(start_node, destination_node)[0]
		DFS = depth_first_search(start_node, destination_node)[0]
		IDDFS = iterative_deepening_search(start_node, destination_node)[0] if BFS is not None else None
		GBFS = greedy_best_first_search(start_node, destination_node)[0]
		AS = a_star_search(start_node, destination_node)[0]

		print "Start node: " + LABELS[start_node] + "\nDestination Node: " + LABELS[destination_node]
		print "Optimal-length Path (BFS, no path cost):", [LABELS[x] for x in BFS] if BFS else None, "\n\tpath cost:", compute_path_cost(BFS)
		print "Possible non-optimal Path (DFS, no path cost):", [LABELS[x] for x in DFS] if DFS else None, "\n\tpath cost:", compute_path_cost(DFS)
		print "Optimal-length Path (ID-DFS, no path cost):", [LABELS[x] for x in IDDFS] if IDDFS else None, "\n\tpath cost:", compute_path_cost(IDDFS)
		print "Possible non-optimal Path (GBFS, path cost used):", [LABELS[x] for x in GBFS] if GBFS else None, "\n\tpath cost:", compute_path_cost(GBFS)
		print "Optimal Path (A Star, path cost used):", [LABELS[x] for x in AS] if AS else None, "\n\tpath cost:", compute_path_cost(AS)
	
	elif sys.argv[1] == "many":
		average_space_complexity_bfs = 0
		average_space_complexity_dfs = 0
		average_space_complexity_iddfs = 0
		average_space_complexity_gbfs = 0
		average_space_complexity_as = 0

		average_time_complexity_bfs = 0
		average_time_complexity_dfs = 0
		average_time_complexity_iddfs = 0
		average_time_complexity_gbfs = 0
		average_time_complexity_as = 0

		average_running_time_bfs = 0.0
		average_running_time_dfs = 0.0
		average_running_time_iddfs = 0.0
		average_running_time_gbfs = 0.0
		average_running_time_as = 0.0

		average_path_length_bfs = 0
		average_path_length_dfs = 0
		average_path_length_iddfs = 0
		average_path_length_gbfs = 0
		average_path_length_as = 0

		number_of_problems_solved_bfs = 0
		number_of_problems_solved_dfs = 0
		number_of_problems_solved_iddfs = 0
		number_of_problems_solved_gbfs = 0
		number_of_problems_solved_as = 0


		for x in range(0, 100):
			generate_edges()
			start_node = random.randint(0, 25)
			destination_node = random.randint(0, 25)

			while destination_node == start_node:
				destination_node = random.randint(0, 25)

			BFS, bfs_added, bfs_visited = breadth_first_search(start_node, destination_node)
			average_space_complexity_bfs += bfs_added
			average_time_complexity_bfs += bfs_visited
			average_path_length_bfs += len(BFS)
			if BFS:
				number_of_problems_solved_bfs += 1

			DFS, dfs_added, dfs_visited = depth_first_search(start_node, destination_node)
			average_space_complexity_dfs += dfs_added
			average_time_complexity_dfs += dfs_visited
			average_path_length_dfs += len(DFS)
			if DFS:
				number_of_problems_solved_dfs += 1

			IDDFS, iddfs_added, iddfs_visited = iterative_deepening_search(start_node, destination_node)
			average_space_complexity_iddfs += iddfs_added
			average_time_complexity_iddfs += iddfs_visited
			average_path_length_iddfs += len(IDDFS)
			if IDDFS:
				number_of_problems_solved_iddfs += 1

			GBFS, gbfs_added, gbfs_visited = greedy_best_first_search(start_node, destination_node)
			average_space_complexity_gbfs += gbfs_added
			average_time_complexity_gbfs += gbfs_visited
			average_path_length_gbfs += len(GBFS)
			if GBFS:
				number_of_problems_solved_gbfs += 1

			AS, as_added, as_visited = a_star_search(start_node, destination_node)
			average_space_complexity_as += as_added
			average_time_complexity_as += as_visited
			average_path_length_as += len(AS)
			if AS:
				number_of_problems_solved_as += 1

		average_space_complexity_bfs = average_space_complexity_bfs / 100
		average_space_complexity_dfs = average_space_complexity_dfs / 100
		average_space_complexity_iddfs = average_space_complexity_iddfs / 100
		average_space_complexity_gbfs = average_space_complexity_gbfs / 100
		average_space_complexity_as = average_space_complexity_as / 100

		average_time_complexity_bfs = average_time_complexity_bfs / 100
		average_time_complexity_dfs = average_time_complexity_dfs / 100
		average_time_complexity_iddfs = average_time_complexity_iddfs / 100
		average_time_complexity_gbfs = average_time_complexity_gbfs / 100
		average_time_complexity_as = average_time_complexity_as / 100

		average_running_time_bfs = average_running_time_bfs / 100
		average_running_time_dfs = average_running_time_dfs / 100
		average_running_time_iddfs = average_running_time_iddfs / 100
		average_running_time_gbfs = average_running_time_gbfs / 100
		average_running_time_as = average_running_time_as / 100

		average_path_length_bfs = average_path_length_bfs / 100
		average_path_length_dfs = average_path_length_dfs / 100
		average_path_length_iddfs = average_path_length_iddfs / 100
		average_path_length_gbfs = average_path_length_gbfs / 100
		average_path_length_as = average_path_length_as / 100

		print "*** BFS ***"
		print "average space complexity:", average_space_complexity_bfs
		print "average time complexity:", average_time_complexity_bfs
		print "average running time:", average_running_time_bfs
		print "average path length:", average_path_length_bfs
		print "number of problems solved:", number_of_problems_solved_bfs, "\n"

		print "*** DFS ***"
		print "average space complexity:", average_space_complexity_dfs
		print "average time complexity:", average_time_complexity_dfs
		print "average running time:", average_running_time_dfs
		print "average path length:", average_path_length_dfs
		print "number of problems solved:", number_of_problems_solved_dfs, "\n"

		print "*** IDDFS ***"
		print "average space complexity:", average_space_complexity_iddfs
		print "average time complexity:", average_time_complexity_iddfs
		print "average running time:", average_running_time_iddfs
		print "average path length:", average_path_length_iddfs
		print "number of problems solved:", number_of_problems_solved_iddfs, "\n"

		print "*** GBFS ***"
		print "average space complexity:", average_space_complexity_gbfs
		print "average time complexity:", average_time_complexity_gbfs
		print "average running time:", average_running_time_gbfs
		print "average path length:", average_path_length_gbfs
		print "number of problems solved:", number_of_problems_solved_gbfs, "\n"

		print "*** AS ***"
		print "average space complexity:", average_space_complexity_as
		print "average time complexity:", average_time_complexity_as
		print "average running time:", average_running_time_as
		print "average path length:", average_path_length_as
		print "number of problems solved:", number_of_problems_solved_as, "\n"


	# display the city locations on a plot
	# plt.plot([x[0] for x in WORLD], [y[1] for y in WORLD], 'ro')
	# plt.axis([0, 99, 0, 99])
	# plt.show()

if __name__ == '__main__':
	main()
