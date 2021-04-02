class Price:

    resp = {}

    def __init__(self):
        return

    def parse(self, raw):
        resp = self.genResp(raw)
        self.resp = resp
        return self

    def genResp(self, price):
        return {
            "Price": price,
        }

    def output(self):
        return self.resp

