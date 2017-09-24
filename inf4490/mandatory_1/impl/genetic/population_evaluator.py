import distance.distance_helper as distance_helper;

def evaluate_population(distance_dataset, population):
    return [{
        'route_distance': distance_helper.get_route_distance(distance_dataset, individual),
        'route': individual
    } for individual in population]
