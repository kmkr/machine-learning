import mutation.mutation_helper as mutation_helper
import distance.distance_helper as distance_helper

MAX_ITERATIONS_WITHOUT_CHANGE = 50
CHANGE_THRESHOLD = 300

def hill_climb(distance_dataset, route, max_iterations):
    num_iterations = 0
    num_iterations_without_change = 0

    shortest = {
        'route_distance': distance_helper.get_route_distance(distance_dataset, route),
        'route': route
    }

    while num_iterations < max_iterations and num_iterations_without_change < MAX_ITERATIONS_WITHOUT_CHANGE:
        candidate_route = mutation_helper.swap_random(route[:])
        distance = distance_helper.get_route_distance(distance_dataset, candidate_route)
        change = distance - shortest['route_distance']
        if change > 0 and change <= CHANGE_THRESHOLD:
            num_iterations_without_change = num_iterations_without_change + 1
        else:
            num_iterations_without_change = 0

        num_iterations = num_iterations + 1

        if shortest['route_distance'] > distance:
            shortest = {
                'route_distance': distance,
                'route': candidate_route
            }
            route = candidate_route

    return shortest
