import unittest

from analytics.ratio import Ratio

class TestRatios(unittest.TestCase):

    def test_exception(self):
        with self.assertRaises(Exception) as context:
            Ratio().calc({}, {2020: 10000})

        self.assertTrue("number of elements in upper and lower must match" in str(context.exception))

    def test_ratios(self):
        upper = {
            2020: 100000,
            2019: 131240,
            2018: 98234,
            2017: 234012,
            2016: 123412,
        }

        lower = {
            2020: 10000,
            2019: 13124,
            2018: 9823,
            2017: 23401,
            2016: 12341,
        }

        ratios = Ratio().calc(upper, lower)
        self.assertEqual(ratios, [None, None, None, None, 10.0, 10.0, 10.0, 10.0, 10.0])

if __name__ == '__main__':
    unittest.main()
