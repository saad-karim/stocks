from aggregator import Aggregator
from decimal import Decimal

aggregator = Aggregator()
aggregator.metrics = [{'Ticker': 'jpm', 'Dividend Year 2020': Decimal('0.9'), 'Dividend Year 2019': Decimal('3.4'), 'Dividend Year 2018': Decimal('2.75'), 'Dividend Year 2017': Decimal('2.16'), 'Dividend Year 2016': Decimal('2.35'), 'Dividend Year 2015': Decimal('0.90')}]


def test_genCSV():
    aggregator.genCSV("test.csv")

if __name__ == "__main__":
    test_genCSV()
    print("Everything passed")
