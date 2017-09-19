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
sys.path.append(os.path.join(dir_path, '..', '..')) # To import modules from task_2 folder
sys.path.append(os.path.join(dir_path, '..', '..', 'task_2')) # Setting task_2 as path will avoid having to re-write module imports in task_2 files
import task_2.pmx

NUM_GENERATIONS = 1000
POPULATION_SIZE = 100
NUM_EXECUTIONS = 20

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

def get_probability_distribution(distances):
    worst = max(distances)
    fitness_list = [worst - distance for distance in distances]
    total_fitness = sum(fitness_list)

    if total_fitness == 0:
        # Convergence
        # Fikses med fitness sharing / crowding ?
        return [0] * len(distances)

    return [(fitness / total_fitness) for fitness in fitness_list]

def get_index_at_point(probability_distribution, point):
    cur_val = 0
    for index, elem in enumerate(probability_distribution):
        cur_val = cur_val + elem
        if cur_val >= point:
            return index

    return 0

def stochastic_universal_sampling(evaluated_population, num_individuals):
    distances = list(map((lambda x: x['route_distance']), evaluated_population))
    probability_distribution = get_probability_distribution(distances)

    pointer = random.random() * (1 / num_individuals)
    mating_pool = []
    while len(mating_pool) < num_individuals:
        index = get_index_at_point(probability_distribution, pointer)
        mating_pool.append(evaluated_population[index]['route'])
        pointer = pointer + (1 / num_individuals)

    return mating_pool

def mutate(route):
    return distance_helper.swap_random(route)

def generate_offspring(parents, num_offspring):
    offspring = []

    while len(offspring) < num_offspring:
        parent_1 = parents[random.randint(0, len(parents) - 1)]
        parent_2 = parents[random.randint(0, len(parents) - 1)]

        child_1, child_2 = task_2.pmx.partial_mapped_crossover(parent_1, parent_2)
        if random.random() < 0.5:
            child_1 = mutate(child_1)
        if random.random() < 0.5:
            child_2 = mutate(child_2)

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

def select_survivors(distance_dataset, parents, offspring, population_size):
    # Discard parents ((μ,λ) selection) and select best-fit offspring
    evaluated_offspring = evaluate_population(distance_dataset, offspring)
    sorted_offspring = sorted(evaluated_offspring, key=lambda offspring: offspring['route_distance'])
    return map((lambda x: x['route']), sorted_offspring[0:population_size])

def find_shortest_path_for_cities(distance_dataset, num_cities, population_size):
    start = time()

    cities = list(distance_dataset[0][0:num_cities])
    population = generate_population(cities, population_size)
    num_generation = 0

    while num_generation < NUM_GENERATIONS:
        evaluated_population = evaluate_population(distance_dataset, population)
        num_parents = population_size / 2
        parents = stochastic_universal_sampling(evaluated_population, num_parents)
        num_offspring = population_size * 2
        offspring = generate_offspring(parents, num_offspring)
        population = select_survivors(distance_dataset, parents, offspring, population_size)
        num_generation = num_generation + 1

    shortest = get_shortest_route(distance_dataset, population)
    end = time()
    print(distance_helper.get_route_distance(distance_dataset, shortest['individual']))
    return shortest, end-start

def run(num_cities):
    best = float('inf')
    best_route = None
    worst = 0
    distances = []

    print('Genetic algorithm using first ' + str(num_cities) + ' cities')
    for _ in range(NUM_EXECUTIONS):
        shortest, duration = genetic(num_cities, POPULATION_SIZE)
        if shortest['distance'] < best:
            best = shortest['distance']
            best_route = shortest['individual']
        if shortest['distance'] > worst:
            worst = shortest['distance']

        distances.append(shortest['distance'])

    print('Best   ' + str(best))
    print(best_route)
    print('Worst  ' + str(worst))
    print('Mean   ' + str(sum(distances) / NUM_EXECUTIONS))
    print('stdev  ' + str(statistics.stdev(distances)))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run(int(sys.argv[1]))
    else:
        run(5)
