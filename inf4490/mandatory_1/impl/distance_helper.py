def get_distance(distance_dataset, from_city, to_city):
    cities = distance_dataset[0]
    from_index = cities.index(from_city)
    to_index = cities.index(to_city)

    return distance_dataset[to_index + 1][from_index] # Add one since first row is the name of cities

def get_route_distance(distance_dataset, route):
    distance = 0
    for index, from_city in enumerate(route):
        to_city = route[index + 1] if index < len(route) - 1 else route[0]
        distance = distance + get_distance(distance_dataset, from_city, to_city)

    return distance
