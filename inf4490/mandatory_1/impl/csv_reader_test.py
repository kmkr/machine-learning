import unittest
import csv_reader

class TestCSVReader(unittest.TestCase):

    def test_read_and_convert_file(self):
        result = csv_reader.read_file('european_cities.csv')
        self.assertEqual(len(result), 25)
        self.assertEqual(len(result[0]), 24)
        self.assertEqual(len(result[1]), 24)
        self.assertIsInstance(result[1][0], float)

if __name__ == '__main__':
    unittest.main()
