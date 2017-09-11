import unittest
import tsp_exhaustive

class TestTSPExhaustive(unittest.TestCase):

    def setUp(self):
        self.distance_dataset = [
            ['Barcelona', 'Belgrade', 'Berlin', 'Brussels', 'Bucharest'],
            [0, 1528.13, 1497.61, 1062.89, 1968.42],
            [1528.13, 0, 999.25, 1372.59, 447.34],
            [1497.61, 999.25, 0, 651.62, 1293.40],
            [1062.89, 1372.59, 651.62, 0, 1769.69],
            [1968.42, 447.34, 1293.40, 1769.69, 0],
        ]

    def test_shortest_path(self):
        result, duration = tsp_exhaustive.find_shortest_path_for_cities(
            self.distance_dataset, len(self.distance_dataset)
        )

        self.assertEquals(result, {
            'distance': 4983.38,
            'route': ('Barcelona', 'Belgrade', 'Bucharest', 'Berlin', 'Brussels')
        })

if __name__ == '__main__':
    unittest.main()
