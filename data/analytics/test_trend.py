import unittest

from trend import Trend

class TestTrends(unittest.TestCase):

    def test_netIncome(self):
        trend = Trend().netIncome({
            2020: 100000,
            2019: 131240,
            2018: 98234,
            2017: 234012,
            2016: 123412,
        })
        self.assertEqual(trend["yearlyTrend"], [0, 0, 0, 0, -0.24, 0.34, -0.58, 0.9])
        self.assertEqual(trend["overallTrend"], -0.25)

if __name__ == '__main__':
    unittest.main()