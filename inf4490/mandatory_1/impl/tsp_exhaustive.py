import csv_reader
import itertools;
import math
import distance_helper;
import sys
from time import time

def exhaustive_search(num_cities):
    distance_dataset = csv_reader.read_file('european_cities.csv')
    return find_shortest_path_for_cities(distance_dataset, num_cities)

def find_shortest_path_for_cities(distance_dataset, num_cities):
    cities = distance_dataset[0][0:num_cities]
    permutations = itertools.permutations(cities)

    shortest = {
        'distance': float('inf')
    }

    start = time()
    for _, candidate_route in enumerate(permutations):
        distance = 0
        for index, from_city in enumerate(candidate_route):
            to_city = candidate_route[index + 1] if index < len(candidate_route) - 1 else candidate_route[0]
            distance = distance + distance_helper.get_distance(distance_dataset, from_city, to_city)

        if shortest['distance'] > distance:
            shortest = {
                'distance': distance,
                'route': candidate_route
            }

    end = time()
    return shortest, end-start



if __name__ == '__main__':
    num_cities = 5
    if len(sys.argv) > 1:
        num_cities = int(sys.argv[1])

    print('Exhastive search using ' + str(num_cities) + ' first cities')
    shortest, duration = exhaustive_search(num_cities)
    print('Found shortest ' + str(shortest) + ' in time ' + str(duration))

