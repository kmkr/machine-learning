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

def genetic(num_cities, population_size):
    distance_dataset = csv_reader.read_file('european_cities.csv')
    return find_shortest_path_for_cities(distance_dataset, num_cities, population_size)

def generate_population(cities, population_size):
    population = []
    for i in range(population_size):
        random.shuffle(cities)
        population.append(list(cities))

    return population

# Problemet ligger her tror jeg. Jeg tror det er for tidlig å kalkulere fitness.
def evaluate_population(distance_dataset, population):
    distances = []
    for i, individual in enumerate(population):
        distances.append((distance_helper.get_route_distance(distance_dataset, individual), individual ))

    longest_distance = 0
    for distance in distances:
        if distance[0] > longest_distance:
            longest_distance = distance[0]

    result = []
    for distance in distances:
        result.append((distance[0], longest_distance - distance[0], distance[1]))

    return result

def get_probability_distribution(sorted_population):
    total_distance = 0

    for elem in sorted_population:
        total_distance = total_distance + elem[0]

    result = []
    for elem in sorted_population:
        result.append(elem[1] / total_distance)

    return result;


def select_parents(sorted_population, num_parents):
    # Stochastic universal sampling
    probability_distribution = get_probability_distribution(sorted_population)
    # Fitness blir feil siden man tar utgangspunkt i feil tall (basert på hele population)

    r = random.random() * (1 / num_parents)
    i = 0
    mating_pool = []
    while len(mating_pool) < num_parents:
        while r <= probability_distribution[i]:
            mating_pool.append(sorted_population[i])
            r = r + (1 / num_parents)
        i = i + 1

    return mating_pool

def find_shortest_path_for_cities(distance_dataset, num_cities, population_size):
    cities = list(distance_dataset[0][0:num_cities])
    population = generate_population(cities, population_size)
    # Her evalueres fitness
    evaluated_population = evaluate_population(distance_dataset, population)
    sorted_population = list(reversed(sorted(evaluated_population, key=lambda elem: elem[1])))

    # Problemet nå er at fitness er allerede satt
    parents = select_parents(sorted_population[0:4], 4)

    start = time()

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
