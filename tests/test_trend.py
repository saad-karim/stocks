import unittest

from analytics.trend import calcFromDict, overallFromDict


# class TestTrends(unittest.TestCase):

#     def test_netIncome(self):
#         data = {
#             2020: 100000,
#             2019: 131240,
#             2018: 98234,
#             2017: 234012,
#             2016: 123412,
#         }

#         yearly = calcFromDict(data)
#         self.assertEqual(yearly, [0, 0, 0, 0, -0.24, 0.34, -0.58, 0.9])

#         overall = overallFromDict(data)
#         self.assertEqual(overall, -0.25)


# if __name__ == '__main__':
#     unittest.main()