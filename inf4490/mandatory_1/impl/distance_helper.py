def get_distance(distance_dataset, from_city, to_city):
    cities = distance_dataset[0]
    from_index = cities.index(from_city)
    to_index = cities.index(to_city)

    return distance_dataset[to_index + 1][from_index] # Add one since first row is the name of cities
