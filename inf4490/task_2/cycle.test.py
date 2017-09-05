import unittest
import cycle

class TestCycle(unittest.TestCase):

    def setUp(self):
        self.seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.seq_2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]

    def test_get_idxes_from_start(self):
        self.assertEqual(
            cycle.get_idxes(self.seq_1, self.seq_2, 0),
            [0, 8, 3, 7]
        )

    def test_get_idxes_from_idx_1(self):
        self.assertEqual(
            cycle.get_idxes(self.seq_1, self.seq_2, 1),
            [1, 2, 6, 4]
        )

    def test_get_idxes_from_idx_1(self):
        child_1, child_2 = cycle.cycle_crossover(self.seq_1, self.seq_2);
        self.assertEqual(child_1, [1, 3, 7, 4, 2, 6, 5, 8, 9])
        self.assertEqual(child_2, [9, 2, 3, 8, 5, 6, 7, 1, 4])

if __name__ == '__main__':
    unittest.main()
