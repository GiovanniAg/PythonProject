# test_sum_function.py
import unittest
from src.sum_function import sum

class TestSumFunction(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum(2, 3), 5)

if __name__ == '__main__':
    unittest.main()