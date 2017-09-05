import unittest
import pmx

class TestPMX(unittest.TestCase):

    def test_range(self):
        seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        seq_2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
        cross_a = 3
        cross_b = 6
        self.assertEqual(pmx.child_from(seq_1, seq_2, cross_a, cross_b), [9, 3, 2, 4, 5, 6, 7, 1, 8])

    def test_single_element(self):
        seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        seq_2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
        cross_a = 3
        cross_b = 3
        self.assertEqual(pmx.child_from(seq_1, seq_2, cross_a, cross_b), [9, 3, 7, 4, 2, 6, 5, 1, 8])

    def test_last_boundary(self):
        seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        seq_2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
        cross_a = 8
        cross_b = 8
        self.assertEqual(pmx.child_from(seq_1, seq_2, cross_a, cross_b), [4, 3, 7, 8, 2, 6, 5, 1, 9])

    def test_start_boundary(self):
        seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        seq_2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
        cross_a = 0
        cross_b = 6
        self.assertEqual(pmx.child_from(seq_1, seq_2, cross_a, cross_b), [1, 2, 3, 4, 5, 6, 7, 9, 8])

if __name__ == '__main__':
    unittest.main()
