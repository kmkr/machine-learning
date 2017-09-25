import data.csv_reader
import itertools;
import math
import distance.distance_helper as distance_helper
import sys
from time import time

def exhaustive_search(num_cities):
    distance_dataset = data.csv_reader.read_file('european_cities.csv')
    return find_shortest_path_for_cities(distance_dataset, num_cities)

def find_shortest_path_for_cities(distance_dataset, num_cities):
    cities = distance_dataset[0][0:num_cities]
    permutations = itertools.permutations(cities)

    shortest = {
        'route_distance': float('inf')
    }

    start = time()
    for _, candidate_route in enumerate(permutations):
        distance = distance_helper.get_route_distance(distance_dataset, candidate_route)

        if shortest['route_distance'] > distance:
            shortest = {
                'route_distance': distance,
                'route': candidate_route
            }

    end = time()
    return shortest, end-start

if __name__ == '__main__':
    num_cities = 5
    if len(sys.argv) > 1:
        num_cities = int(sys.argv[1])

    print('Exhaustive search using ' + str(num_cities) + ' first cities')
    shortest, duration = exhaustive_search(num_cities)
    print('Found shortest ' + str(shortest) + ' in ' + str(duration) + ' seconds')
