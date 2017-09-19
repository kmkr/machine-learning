import random

def swap_random(route):
    idx_1 = 0
    idx_2 = 0
    while idx_1 == idx_2:
        idx_1 = random.randint(0, len(route) - 1)
        idx_2 = random.randint(0, len(route) - 1)

    route[idx_1], route[idx_2] = route[idx_2], route[idx_1]
    return route
