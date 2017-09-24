import data.csv_reader
import math
import sys
import random
import statistics
from hill_climber.hill_climb import hill_climb
from time import time

MAX_ITERATIONS = 5000

def hill_climber(num_cities):
    distance_dataset = data.csv_reader.read_file('european_cities.csv')
    return find_shortest_path_for_cities(distance_dataset, num_cities)

def find_shortest_path_for_cities(distance_dataset, num_cities):
    current_route = list(distance_dataset[0][0:num_cities])
    random.shuffle(current_route)
    num_permutations = len(current_route)
    start = time()
    shortest = hill_climb(distance_dataset, current_route, MAX_ITERATIONS)
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
    total_duration = 0
    print('Hill climber search using first ' + str(num_cities) + ' cities. Running in total ' + str(num_executions) + ' executions.')
    for i in range(num_executions):
        shortest, duration = hill_climber(num_cities)
        if shortest['route_distance'] < best:
            best = shortest['route_distance']
        if shortest['route_distance'] > worst:
            worst = shortest['route_distance']

        distances.append(shortest['route_distance'])
        total_duration = total_duration + duration

    print('Best     ' + str(best))
    print('Worst    ' + str(worst))
    print('Mean     ' + str(sum(distances) / num_executions))
    print('stdev    ' + str(statistics.stdev(distances)))
    print('duration ' + str(total_duration))
