import data.csv_reader
import math

import mutation.mutation_helper as mutation_helper;
import random
import statistics
from time import time
from functools import reduce
import numpy as np
import genetic.pmx as pmx
import genetic.population_evaluator as population_evaluator
import genetic.survivor_selector as survivor_selector

MAX_GENERATIONS = 100
MAX_WITHOUT_CHANGE = 10
NUM_EXECUTIONS = 20
SINGLE_SWAP_MUTATION_PROBABILITY = 0.6
DOUBLE_SWAP_MUTATION_PROBABILITY = 0.4

def genetic(num_cities, population_size, survivor_selector_strategy):
    distance_dataset = data.csv_reader.read_file('european_cities.csv')
    return find_shortest_path_for_cities(distance_dataset, num_cities, population_size, survivor_selector_strategy)

def generate_population(cities, population_size):
    population = []
    for _ in range(population_size):
        random.shuffle(cities)
        population.append(list(cities))

    return population

def get_probability_distribution(distances):
    worst = max(distances)
    fitness_list = [worst - distance for distance in distances]
    total_fitness = sum(fitness_list)

    if total_fitness == 0:
        # Convergence (the entire population has the same fitness value)
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
    rnd = random.random()
    if rnd < DOUBLE_SWAP_MUTATION_PROBABILITY:
        route = mutation_helper.swap_random(route)
    if rnd < SINGLE_SWAP_MUTATION_PROBABILITY:
        route = mutation_helper.swap_random(route)

    return route

def generate_offspring(parents, num_offspring):
    offspring = []

    while len(offspring) < num_offspring:
        parent_1 = parents[random.randint(0, len(parents) - 1)]
        parent_2 = parents[random.randint(0, len(parents) - 1)]

        child_1, child_2 = pmx.partial_mapped_crossover(parent_1, parent_2)
        child_1 = mutate(child_1)
        child_2 = mutate(child_2)

        offspring.append(child_1)
        if len(offspring) < num_offspring:
            offspring.append(child_2)

    return offspring

def get_shortest_route(distance_dataset, population):
    shortest = { 'route_distance': float('inf') }
    evaluated_population = population_evaluator.evaluate_population(distance_dataset, population)
    for individual in evaluated_population:
        if individual['route_distance'] < shortest['route_distance']:
            shortest = individual

    return shortest


def find_shortest_path_for_cities(distance_dataset, num_cities, population_size, survivor_selector_strategy):
    start = time()

    cities = list(distance_dataset[0][0:num_cities])
    population = generate_population(cities, population_size)
    num_generation = 0
    shortest_per_generation = []

    while num_generation < MAX_GENERATIONS:
        evaluated_population = population_evaluator.evaluate_population(distance_dataset, population)
        num_parents = population_size / 2
        parents = stochastic_universal_sampling(evaluated_population, num_parents)
        num_offspring = population_size * 2
        offspring = generate_offspring(parents, num_offspring)
        population, shortest = survivor_selector.select_survivors(distance_dataset, parents, offspring, population_size, survivor_selector_strategy)
        shortest_per_generation.append(shortest['route_distance'])
        num_generation = num_generation + 1

    shortest = get_shortest_route(distance_dataset, population)
    end = time()
    return shortest, end-start, shortest_per_generation

def run(num_cities, population_size, survivor_selector_strategy):
    best = float('inf')
    best_route = None
    worst = 0
    distances = []
    total_duration = 0

    print('Genetic algorithm using population size ' + str(population_size) + ' with ' + str(MAX_GENERATIONS) + ' generations on first ' + str(num_cities) + ' cities ')
    for num_execution in range(NUM_EXECUTIONS):
        shortest, duration, shortest_per_generation = genetic(num_cities, population_size, survivor_selector_strategy)
        print('Execution ' + str(num_execution) + ': ' + str(shortest['route_distance']) + ' km (' + str(duration) + ' s)')
        if shortest['route_distance'] < best:
            best = shortest['route_distance']
            best_route = shortest['route']
        if shortest['route_distance'] > worst:
            worst = shortest['route_distance']

        distances.append(shortest['route_distance'])
        total_duration = total_duration + duration

    print('Best     ' + str(best))
    print(best_route)
    print('Worst    ' + str(worst))
    print('Mean     ' + str(sum(distances) / NUM_EXECUTIONS))
    print('stdev    ' + str(statistics.stdev(distances)))
    print('duration ' + str(total_duration))
    print('\n\n')

    return shortest_per_generation

def run_three_variants(num_cities, survivor_selector_strategy):
    shortest_per_generation_50 = run(num_cities, 50, survivor_selector_strategy)
    shortest_per_generation_100 = run(num_cities, 100, survivor_selector_strategy)
    shortest_per_generation_200 = run(num_cities, 200, survivor_selector_strategy)

    shortest_per_generation_average = np.mean(np.array([shortest_per_generation_50, shortest_per_generation_100, shortest_per_generation_200]), axis=0)
    return {
        '50': shortest_per_generation_50,
        '100': shortest_per_generation_100,
        '200': shortest_per_generation_200,
        'avg': shortest_per_generation_average
    }
