import csv_reader
import math
import distance_helper;
import sys
import random
import statistics
from time import time
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', '..'))
sys.path.append(os.path.join(dir_path, '..', '..', 'task_2'))
import task_2.pmx

def genetic(num_cities, population_size):
    distance_dataset = csv_reader.read_file('european_cities.csv')
    return find_shortest_path_for_cities(distance_dataset, num_cities, population_size)

def generate_population(cities, population_size):
    population = []
    for _ in range(population_size):
        random.shuffle(cities)
        population.append(list(cities))

    return population

def evaluate_population(distance_dataset, population):
    result = []
    for individual in population:
        result.append({
            'route_distance': distance_helper.get_route_distance(distance_dataset, individual),
            'route': individual
        })

    return result

def get_probability_distribution(population):
    total_distance = 0

    for individual in population:
        total_distance = total_distance + individual['route_distance']

    result = []
    for individual in population:
        result.append(individual['route_distance'] / total_distance)

    return result;

def get_index_at_point(probability_distribution, point):
    cur_val = 0
    for index, elem in enumerate(probability_distribution):
        cur_val = cur_val + elem
        if cur_val >= point:
            return index

def select_parents(population, num_parents):
    # Stochastic universal sampling
    probability_distribution = get_probability_distribution(population)

    pointer = random.random() * (1 / num_parents)
    mating_pool = []
    while len(mating_pool) < num_parents:
        index = get_index_at_point(probability_distribution, pointer)
        mating_pool.append(population[index])
        pointer = pointer + (1 / num_parents)

    return mating_pool

def find_shortest_path_for_cities(distance_dataset, num_cities, population_size):
    start = time()

    cities = list(distance_dataset[0][0:num_cities])
    population = generate_population(cities, population_size)
    evaluated_population = evaluate_population(distance_dataset, population)
    num_parents = population_size / 2
    parents = select_parents(evaluated_population, num_parents)
    task_2.pmx.partial_mapped_crossover(parents[0], parents[1])

    end = time()
    return shortest, end-start

if __name__ == '__main__':
    num_cities = 12
    population_size = 20
    if len(sys.argv) > 1:
        num_cities = int(sys.argv[1])

    best = float('inf')
    worst = 0
    distances = []
    num_executions = 20
    print('Genetic algorithm using first ' + str(num_cities) + ' cities')
    for i in range(num_executions):
        shortest, duration = genetic(num_cities, population_size)
        if shortest['distance'] < best:
            best = shortest['distance']
        if shortest['distance'] > worst:
            worst = shortest['distance']

        distances.append(shortest['distance'])

    print('Best   ' + str(best))
    print('Worst  ' + str(worst))
    print('Mean   ' + str(sum(distances) / num_executions))
    print('stdev  ' + str(statistics.stdev(distances)))
