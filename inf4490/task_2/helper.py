import random

def get_crossover_points(total_length):
    cross_a = random.randint(0, total_length - 2)
    cross_b = random.randint(cross_a, total_length - 1)

    return cross_a, cross_b
