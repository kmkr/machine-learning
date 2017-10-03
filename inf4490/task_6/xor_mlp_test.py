import unittest
from xor_mlp import XorMlp
import numpy as np

BIAS = -1 # Must be the same as xor_mlp.py

class TestXorMlp(unittest.TestCase):

    def setUp(self):
        self.inputs = np.array([
            [0, 0], # BIAS i første col (ikke synlig), i_1 i andre col, i_2 i andre col
            [0, 1], # samme her
            [1, 1], # samme her
            [1, 0]  # samme her
        ])
        self.targets = np.array([
            [0],
            [1],
            [0],
            [1]
        ])
        num_hidden = 2
        self.mlp = XorMlp(self.inputs, self.targets, num_hidden)

    def test_correct_shape_for_weights(self):
        self.assertEqual(self.mlp.weights_hidden_layer.shape, (3,2))
        self.assertEqual(self.mlp.weights_output_layer.shape, (3,1))

    def test_activation(self):
        np.testing.assert_array_equal(
            self.mlp.activation(np.array([[-1, 0], [0, 1]])),
            np.array([[0, 0], [0, 1]])
        )

    def test_weighted_sum_with_one_input(self):
        weights = np.array([
            # vh1, vh2
            [-3, 2],
            [1, 3],
            [4, 5],
        ])
        np.testing.assert_array_equal(self.mlp._weighted_sum(self.inputs, weights), np.array([
            [ (BIAS * -3) + (0 * 1) + (0 * 4), (BIAS * 2) + (0 * 3) + (0 * 5) ], # weighted sum input (0, 0)
            [ (BIAS * -3) + (0 * 1) + (1 * 4), (BIAS * 2) + (0 * 3) + (1 * 5) ], # weighted sum input (0, 1)
            [ (BIAS * -3) + (1 * 1) + (1 * 4), (BIAS * 2) + (1 * 3) + (1 * 5) ], # weighted sum input (1, 1)
            [ (BIAS * -3) + (1 * 1) + (0 * 4), (BIAS * 2) + (1 * 3) + (0 * 5) ] # weighted sum input (1, 0)
        ]))

if __name__ == '__main__':
    unittest.main()
