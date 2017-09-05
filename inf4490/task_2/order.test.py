import unittest
import order

class TestOrder(unittest.TestCase):

    def setUp(self):
        self.seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.seq_2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]

    def test_api(self):
        res = order.order_crossover(self.seq_1, self.seq_2)
        self.assertTrue(isinstance(res[0], list))
        self.assertTrue(isinstance(res[1], list))

    def test_range(self):
        cross_a = 3
        cross_b = 7
        self.assertEqual(
            order.child_from(self.seq_1, self.seq_2, cross_a, cross_b),
            [3, 8, 2, 4, 5, 6, 7, 1, 9]
        )

    def test_single_element(self):
        cross_a = 2
        cross_b = 3
        self.assertEqual(
            order.child_from(self.seq_1, self.seq_2, cross_a, cross_b),
            [9, 7, 3, 8, 2, 6, 5, 1, 4]
        )

    def test_last_boundary(self):
        cross_a = 8
        cross_b = 9
        self.assertEqual(
            order.child_from(self.seq_1, self.seq_2, cross_a, cross_b),
            [3, 7, 8, 2, 6, 5, 1, 4, 9]
        )

    def test_start_boundary(self):
        cross_a = 0
        cross_b = 7
        self.assertEqual(
            order.child_from(self.seq_1, self.seq_2, cross_a, cross_b),
            [1, 2, 3, 4, 5, 6, 7, 9, 8]
        )

if __name__ == '__main__':
    unittest.main()
