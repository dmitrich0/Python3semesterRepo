import unittest

from statistics import DataSet


class TestDataset(unittest.TestCase):
    def test_increment(self):
        subject, key, value = {1: 2, 2: 3}, 2, 3
        DataSet.increment(subject, key, value)
        DataSet.increment(subject, "100", value)
        self.assertEqual(subject[2], 6)
        self.assertEqual(subject['100'], 3)
