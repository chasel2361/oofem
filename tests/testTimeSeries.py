import unittest

from TimeSeries import *
from math import isclose

class TimeSeriesTest(unittest.TestCase):
    def setUp(self):
        self.series = TimeSeries(1, 0.01, [1, -1, 3, -2, 5])

    def tearDown(self):
        self.series = None
    
    def test_at(self):
        true = self.assertTrue
        series = self.series
        true(isclose(series.at(1.007), -0.4))
        true(isclose(series.at(1.039), 4.3))

if __name__ == '__main__':
    unittest.main()