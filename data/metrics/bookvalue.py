class BookValue:

    def __init__(self):
        return

    def calc(self, price, advKeyStats, keyStats):
        bookValue = float(price["Price"]) / float(advKeyStats["Price/BookValue Ratio"])
        return {
            "Book Value": bookValue,
        }
