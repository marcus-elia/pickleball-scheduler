#!/usr/bin/env python3

import unittest
from recursive_backtracking import is_valid

class TestScheduling(unittest.TestCase):
    def test_is_valid(self):
        self.assertTrue(is_valid([[1, 2, 3, 4, 5, 6]], 6))
        self.assertFalse(is_valid([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]], 6))
        self.assertTrue(is_valid([[1, 2, 3, 4, 5, 6], [1, 3, 2, 5, 4, 6]], 6))
        self.assertTrue(is_valid([[1, 2, 3, 4, 5, 6], [1, 3, 2, 5, 4, 6], [1, 4, 2, 6, 3, 5]], 6))
        self.assertTrue(is_valid([[1, 2, 3, 4, 5, 6], [1, 3, 2, 5, 4, 6], [1, 4, 2, 6, 3, 5], [1, 5, 2, 4, 3, 6]], 6))
        self.assertTrue(is_valid([[1, 2, 3, 4, 5, 6], [1, 3, 2, 5, 4, 6], [1, 4, 2, 6, 3, 5], [1, 5, 2, 4, 3, 6], [1, 6, 2, 3, 4, 5]], 6))
        self.assertTrue(is_valid([[1, 2, 3, 4, 5, 6], [1, 3, 2, 5, 4, 6], [1, 4, 2, 6, 3, 5], [1, 5, 2, 4, 3, 6], [1, 6, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]], 6))
        self.assertFalse(is_valid([[1, 2, 3, 4, 5, 6], [1, 3, 2, 5, 4, 6], [1, 4, 2, 6, 3, 5], [1, 5, 2, 4, 3, 6], [1, 6, 2, 3, 4, 5], [1, 5, 2, 4, 5, 6]], 6))

if __name__ == '__main__':
    unittest.main()
