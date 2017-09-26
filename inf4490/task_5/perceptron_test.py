import unittest
import perceptron

class TestPerceptron(unittest.TestCase):

    def setUp(self):
        self.weights = [1, -0.4, 0.6]
        self.perceptron = perceptron.Perceptron(self.weights)

    def test_get_activation(self):
        self.assertEqual(self.perceptron.get_activation([-1.5, 1, 2]), 0)
        self.assertEqual(self.perceptron.get_activation([-1.5, 1, 4]), 1)

if __name__ == '__main__':
    unittest.main()
