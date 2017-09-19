import unittest
import distance.distance_helper as distance_helper

class TestDistanceHelper(unittest.TestCase):

    def setUp(self):
        self.distances = [
            ['Barcelona', 'Belgrade', 'Berlin'],
            [0, 1528.13, 1497.61],
            [1528.13, 0, 999.25],
            [1497.61, 999.25, 0]
        ]

    def test_get_distance_from_barcelona_to_belgrade(self):
        self.assertEqual(
            distance_helper.get_distance(self.distances, 'Barcelona', 'Belgrade'),
            1528.13
        )

    def test_get_distance_from_berlin_to_belgrade(self):
        self.assertEqual(
            distance_helper.get_distance(self.distances, 'Berlin', 'Belgrade'),
            999.25
        )

    def test_get_distance_from_berlin_to_berlin(self):
        self.assertEqual(
            distance_helper.get_distance(self.distances, 'Berlin', 'Berlin'),
            0
        )

    def test_get_route_distance(self):
        self.assertEqual(
            distance_helper.get_route_distance(self.distances, self.distances[0]),
            1528.13 + 999.25 + 1497.61
        )

if __name__ == '__main__':
    unittest.main()
