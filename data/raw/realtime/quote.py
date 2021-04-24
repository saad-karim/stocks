class Quote:

    def __init__(self):
        return

    def load(self, quote):
        self._resp = quote[0]

    def get(self):
        return self._resp
