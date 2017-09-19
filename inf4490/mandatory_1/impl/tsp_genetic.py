import csv_reader
import math
import distance_helper;
import sys
import random
import statistics
from time import time
from functools import reduce
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
    return [{
        'route_distance': distance_helper.get_route_distance(distance_dataset, individual),
        'route': individual
    } for individual in population]

def get_probability_distribution(population):
    # Stochastic universal sampling
    worst = max(map((lambda x: x['route_distance']), population))
    fitness_list = list(map((lambda x: worst - x['route_distance']), population))
    total_fitness = reduce((lambda x, y: x + y), fitness_list, 0)

    if total_fitness == 0:
        # Convergence
        print('Convergence')
        return [0] * len(population)

    return [(fitness / total_fitness) for fitness in fitness_list]

def get_index_at_point(probability_distribution, point):
    cur_val = 0
    for index, elem in enumerate(probability_distribution):
        cur_val = cur_val + elem
        if cur_val >= point:
            return index

    return 0

def generate_mating_pool(population, num_parents):
    probability_distribution = get_probability_distribution(population)

    pointer = random.random() * (1 / num_parents)
    mating_pool = []
    while len(mating_pool) < num_parents:
        index = get_index_at_point(probability_distribution, pointer)
        mating_pool.append(population[index])
        pointer = pointer + (1 / num_parents)

    return mating_pool

def generate_offspring(parents, num_offspring):
    offspring = []

    while len(offspring) < num_offspring:
        parent_1 = parents[random.randint(0, len(parents) - 1)]
        parent_2 = parents[random.randint(0, len(parents) - 1)]

        child_1, child_2 = task_2.pmx.partial_mapped_crossover(parent_1, parent_2)
        offspring.append(child_1)
        if len(offspring) < num_offspring:
            offspring.append(child_2)

    return offspring

def get_shortest_route(distance_dataset, population):
    shortest = { 'distance': float('inf') }
    for individual in population:
        route_distance = distance_helper.get_route_distance(distance_dataset, individual)
        if route_distance < shortest['distance']:
            shortest = {
                'distance': route_distance,
                'individual': individual
            }

    return shortest

def find_shortest_path_for_cities(distance_dataset, num_cities, population_size):
    start = time()

    cities = list(distance_dataset[0][0:num_cities])
    population = generate_population(cities, population_size)
    stop_at_iter = 200
    num_iter = 0

    while num_iter < stop_at_iter:
        evaluated_population = evaluate_population(distance_dataset, population)
        num_parents = population_size / 2
        num_offspring = population_size - num_parents
        mating_pool = generate_mating_pool(evaluated_population, num_parents)
        parents = list(map((lambda x: x['route']), mating_pool))

        offspring = generate_offspring(parents, num_offspring)
        population = parents + offspring
        num_iter = num_iter + 1

    shortest = get_shortest_route(distance_dataset, population)
    end = time()
    print(distance_helper.get_route_distance(distance_dataset, shortest['individual']))
    return shortest, end-start

if __name__ == '__main__':
    num_cities = 12
    population_size = 20
    if len(sys.argv) > 1:
        num_cities = int(sys.argv[1])

    best = float('inf')
    best_route = None
    worst = 0
    distances = []
    num_executions = 20
    print('Genetic algorithm using first ' + str(num_cities) + ' cities')
    for i in range(num_executions):
        shortest, duration = genetic(num_cities, population_size)
        if shortest['distance'] < best:
            best = shortest['distance']
            best_route = shortest['individual']
        if shortest['distance'] > worst:
            worst = shortest['distance']

        distances.append(shortest['distance'])

    print('Best   ' + str(best))
    print(best_route)
    print('Worst  ' + str(worst))
    print('Mean   ' + str(sum(distances) / num_executions))
    print('stdev  ' + str(statistics.stdev(distances)))
