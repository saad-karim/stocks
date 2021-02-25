import requests
import logging
import json
import os

log = logging.getLogger("fmp_prod")

baseURL = "https://financialmodelingprep.com/api/v3"

headers = {
    'User-Agent': 'user-agent',
}

class Prod:

    session = requests.Session()
    session.headers.update(headers)

    def __init__(self, token, cacheLocation, refresh):
        self.token = token
        self.cacheLocation = cacheLocation
        self.refresh = refresh

    def dividend(self, symbol):
        log.info("Getting dividend information for: %s", symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "dividendquarter")
            if cachedResponse != None:
                return cachedResponse

        url = baseURL+"/historical-price-full/stock_dividend/"+symbol+"?apikey=" + self.token
        log.info("Dividend URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "dividendquarter", response.json())

        return response.json()

    def income(self, symbol, period):
        log.info("Getting %s income information for: %s", period, symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "income"+period)
            if cachedResponse != None:
                return cachedResponse

        url = baseURL+"/income-statement/"+symbol+"?period="+period+"&apikey=" + self.token
        log.info("Income URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "income"+period, response.json())

        return response.json()

    def balanceSheet(self, symbol, period):
        log.info("Getting %s balance sheet information for: %s", period, symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "balancesheet"+period)
            if cachedResponse != None:
                return cachedResponse

        url = baseURL+"/balance-sheet-statement/"+symbol+"?period="+period+"&apikey=" + self.token
        log.info("Balance Sheet URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "balancesheet"+period, response.json())

        return response.json()

    def financialRatios(self, symbol, period):
        log.info("Getting %s financial information for: %s", period, symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "ratios"+period)
            if cachedResponse != None:
                return cachedResponse

        url = baseURL+"/ratios/"+symbol+"?period="+period+"&apikey=" + self.token
        log.info("Financial ratios URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "ratios"+period, response.json())

        return response.json()

    def keyMetrics(self, symbol, period):
        log.info("Getting %s key metrics: %s", period, symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "keymetrics"+period)
            if cachedResponse != None:
                return cachedResponse

        url = baseURL+"/key-metrics/"+symbol+"?period="+period+"&apikey=" + self.token
        log.info("Key Metrics URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "keymetrics"+period, response.json())

        return response.json()

    def cashFlow(self, symbol, period):
        log.info("Getting %s cash flow: %s", period, symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "cashflow"+period)
            if cachedResponse != None:
                return cachedResponse

        url = baseURL+"/cash-flow-statement/"+symbol+"?period="+period+"&apikey=" + self.token
        log.info("Cash Flow URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "cashflow"+period, response.json())

        return response.json()

    def enterpriseValues(self, symbol, period):
        log.info("Getting %s cash flow: %s", period, symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "enterprisevalues"+period)
            if cachedResponse != None:
                return cachedResponse

        url = baseURL+"/enterprise-values/"+symbol+"?period="+period+"&apikey=" + self.token
        log.info("Cash Flow URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "enterprisevalues"+period, response.json())

        return response.json()

    def financialGrowth(self, symbol, period):
        log.info("Getting %s financial growth info: %s", period, symbol)

        if not bool(self.refresh):
            cachedResponse = self.readCache(symbol, "financialgrowth"+period)
            if cachedResponse != None:
                return cachedResponse

        url = baseURL+"/financial-growth/"+symbol+"?period="+period+"&apikey=" + self.token
        log.info("Financial Growth URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "financialgrowth"+period, response.json())

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
