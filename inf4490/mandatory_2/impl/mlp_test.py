import unittest
from mlp import Mlp
import numpy as np

BIAS = -1 # Must be the same as mlp.py

class TestMlp(unittest.TestCase):

    def setUp(self):
        self.mlp = Mlp(np.array([[1], [2]]), np.array([[1], [2]]), 12)

    def test_weighted_sum_with_one_input(self):
        # shape(1, 2) -> (1, 3) with bias added
        inputs = np.array([
            [4, -3]
        ])
        # shape (3, 2) with added bias
        weights = np.array([
            [-1, 5], # Added bias weights
            [1, 3],
            [2, 4],
        ])
        np.testing.assert_array_equal(self.mlp._weighted_sum(inputs, weights), np.array([
            [
                (BIAS * -1) + (4 * 1) + (-3 * 2),
                (BIAS * 5) + (4 * 3) + (-3 * 4)
            ]
        ]))

    def test_weighted_sum_with_two_inputs(self):
        # shape(2, 3) -> (2, 4) with bias added
        inputs = np.array([
            [4, -3, 1],
            [2, -1, 2]
        ])
        # shape (4, 2) with added bias
        weights = np.array([
            [-1, 5], # Added bias weights
            [1, 3],
            [2, 4],
            [1, 2],
        ])
        np.testing.assert_array_equal(self.mlp._weighted_sum(inputs, weights), np.array([
            [
                (BIAS * -1) + (4 * 1) + (-3 * 2) + (1 * 1),
                (BIAS * 5) + (4 * 3) + (-3 * 4) + (1 * 2)
            ],
            [
                (BIAS * -1) + (2 * 1) + (-1 * 2) + (2 * 1),
                (BIAS * 5) + (2 * 3) + (-1 * 4) + (2 * 2)
            ],
        ]))

if __name__ == '__main__':
    unittest.main()
