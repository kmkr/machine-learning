import csv_reader
import math
import distance_helper;
import sys
import random
import statistics
from time import time

max_iterations = 5000
max_iterations_without_change = 50
change_threshold = 300

def hill_climber(num_cities):
    distance_dataset = csv_reader.read_file('european_cities.csv')
    return find_shortest_path_for_cities(distance_dataset, num_cities)

def find_shortest_path_for_cities(distance_dataset, num_cities):
    current_route = list(distance_dataset[0][0:num_cities])
    random.shuffle(current_route)
    num_permutations = len(current_route)

    shortest = {
        'distance': distance_helper.get_route_distance(distance_dataset, current_route),
        'route': current_route
    }

    start = time()

    num_iterations = 0
    num_iterations_without_change = 0

    # print 'Iteration 0: ' + str(current_route)

    while num_iterations < max_iterations and num_iterations_without_change < max_iterations_without_change:
        candidate_route = distance_helper.swap_random(current_route[:])
        distance = distance_helper.get_route_distance(distance_dataset, candidate_route)
        change = distance - shortest['distance']
        if change > 0 and change <= change_threshold:
            num_iterations_without_change = num_iterations_without_change + 1
        else:
            num_iterations_without_change = 0

        num_iterations = num_iterations + 1

        if shortest['distance'] > distance:
            shortest = {
                'distance': distance,
                'route': candidate_route
            }
            current_route = candidate_route

    end = time()
    return shortest, end-start

if __name__ == '__main__':
    num_cities = 12
    if len(sys.argv) > 1:
        num_cities = int(sys.argv[1])

    best = float('inf')
    worst = 0
    distances = []
    num_executions = 20
    print('Hill climber search using first ' + str(num_cities) + ' cities. Running in total ' + str(num_executions) + ' executions.')
    for i in range(num_executions):
        shortest, duration = hill_climber(num_cities)
        if shortest['distance'] < best:
            best = shortest['distance']
        if shortest['distance'] > worst:
            worst = shortest['distance']

        distances.append(shortest['distance'])

    print('Best   ' + str(best))
    print('Worst  ' + str(worst))
    print('Mean   ' + str(sum(distances) / num_executions))
    print('stdev  ' + str(statistics.stdev(distances)))
