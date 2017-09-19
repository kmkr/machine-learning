import unittest
import tsp_genetic

class TestGenetic(unittest.TestCase):

    def setUp(self):
        self.cities = ['Barcelona', 'Belgrade', 'Berlin', 'Brussels', 'Bucharest'];

    def test_population_generation(self):
        population = tsp_genetic.generate_population(self.cities, 5)
        self.assertTrue(len(population), 5)
        self.assertTrue(len(population[0]), 5)
        self.assertTrue(population[0][0] in self.cities)

    def test_probability_distribution(self):
        population = [
            {'route_distance': 6},
            {'route_distance': 9},
            {'route_distance': 7}
        ]
        probability_distribution = tsp_genetic.get_probability_distribution(population)
        self.assertTrue(len(probability_distribution), len(population))
        total_fitness = (9 - 6) + (9 - 9) + (9 - 7)
        self.assertEqual(probability_distribution[0], (9 - 6) / total_fitness)
        self.assertEqual(probability_distribution[1], (9 - 9) / total_fitness)
        self.assertEqual(probability_distribution[2], (9 - 7) / total_fitness)

if __name__ == '__main__':
    unittest.main()
