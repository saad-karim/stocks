import requests
import logging
import json
import os

log = logging.getLogger("iex_sandbox")

baseURL = "https://sandbox.iexapis.com/stable/stock/"

headers = {
    'User-Agent': 'user-agent',
}


class Sandbox:

    session = requests.Session()
    session.headers.update(headers)

    def __init__(self, token, cacheLocation, refresh):
        self.token = token
        self.cacheLocation = cacheLocation
        self.refresh = refresh

    def dividend(self, symbol, range):
        log.info("Getting dividend information for: %s", symbol)
        cacheName = "dividends-{}".format(range)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, cacheName)
            if cachedResponse is not None:
                return cachedResponse

        resource = "/dividends/{range}?token={token}". \
            format(range=range, token=self.token)

        url = baseURL+symbol+resource
        log.info("Dividend URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, cacheName, response.json())

        return response.json()

    def cashFlow(self, symbol, period, last):
        log.info("Getting %s cash flow information for: %s", period, symbol)
        cacheName = "cashflow-{}".format(period)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, cacheName)
            if cachedResponse is not None:
                return cachedResponse

        resource = "/cash-flow?period={period}&last={last}&token={token}". \
            format(period=period, last=last, token=self.token)

        url = baseURL+symbol+resource
        log.info("Cash-Flow URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, cacheName, response.json())

        return response.json()

    def income(self, symbol, period, last):
        log.info("Getting %s income information for: %s", period, symbol)
        cacheName = "income-{}".format(period)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, cacheName)
            if cachedResponse is not None:
                return cachedResponse

        resource = "/income?period={period}&last={last}&token={token}". \
            format(period=period, last=last, token=self.token)

        url = baseURL+symbol+resource
        log.info("Income URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, cacheName, response.json())

        return response.json()

    def balanceSheet(self, symbol, period, last):
        log.info("Getting %s balance sheet information for: %s", period, symbol)
        cacheName = "balancesheet-{}".format(period)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, cacheName)
            if cachedResponse is not None:
                return cachedResponse

        resource = "/balance-sheet?period={period}&last={last}&token={token}". \
            format(period=period, last=last, token=self.token)

        url = baseURL+symbol+resource
        log.info("Balance Sheet URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, cacheName, response.json())

        return response.json()

    def keyStats(self, symbol):
        log.info("Getting key stats information for: %s", symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "keystats")
            if cachedResponse is not None:
                return cachedResponse

        url = baseURL+symbol+"/stats?token=" + self.token
        log.info("Key Stats URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "keystats", response.json())

        return response.json()

    def advancedKeyStats(self, symbol):
        log.info("Getting advanced stats information for: %s", symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "advancedkeystats")
            if cachedResponse is not None:
                return cachedResponse

        url = baseURL+symbol+"/advanced-stats?token=" + self.token
        log.info("Advance Stats URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "advancedkeystats", response.json())

        return response.json()

    def price(self, symbol):
        log.info("Getting price information for: %s", symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "price")
            if cachedResponse is not None:
                return cachedResponse

        url = baseURL+symbol+"/price?token=" + self.token
        log.info("Price URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "price", response.json())

        return response.json()

    def advanceFundamentals(self, symbol, period, last):
        log.info("Getting advance fundamentals  for: %s", symbol)
        cacheName = "advancefundamentals-{}".format(period)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, cacheName)
            if cachedResponse is not None:
                return cachedResponse

        base = "https://sandbox.iexapis.com/stable"
        resource = "/time-series/fundamentals/{symbol}/{period}?last={last}&token={token}". \
            format(symbol=symbol, period=period, last=last, token=self.token)

        url = base+resource
        log.info("Price URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, cacheName, response.json())

        return response.json()

    def writeCache(self, symbol, api, data):
        cacheDir = os.path.join(self.cacheLocation, symbol)
        path = os.path.join(cacheDir, api + ".json")

        os.makedirs(os.path.dirname(path), exist_ok=True)

        log.info("Writing cache of %s for api %s", symbol, api)

        with open(path, "w") as outfile:
            json.dump(data, outfile)

    def readCache(self, symbol, api):
        cacheDir = os.path.join(self.cacheLocation, symbol)
        path = os.path.join(cacheDir, api + ".json")

        if not os.path.exists(path):
            log.info("No cached information of %s for api %s", symbol, api)
            return None

        log.info("Found cached information of %s for api %s", symbol, api)
        with open(path) as json_file:
            json_data = json_file.read()

        data = json.loads(json_data)
        return data
