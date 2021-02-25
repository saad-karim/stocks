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

    def __init__(self, token, cacheLocation):
        self.token = token
        self.cacheLocation = cacheLocation

    def dividend(self, symbol):
        log.info("Getting dividend information for: %s", symbol)

        cachedResponse = self.readCache(symbol, "dividend")
        if cachedResponse != None:
            return cachedResponse

        url = baseURL+symbol+"/dividends/5y?token=" + self.token
        log.info("Dividend URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "dividend", response.json())

        return response.json()

    def income(self, symbol):
        log.info("Getting income information for: %s", symbol)

        cachedResponse = self.readCache(symbol, "income")
        if cachedResponse != None:
            return cachedResponse

        url = baseURL+symbol+"/income?period=annual&last=5&token=" + self.token
        log.info("Income URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "income", response.json())

        return response.json()

    def balanceSheet(self, symbol):
        log.info("Getting balance sheet information for: %s", symbol)

        cachedResponse = self.readCache(symbol, "balancesheet")
        if cachedResponse != None:
            return cachedResponse

        url = baseURL+symbol+"/balance-sheet?period=annual&last=5&token=" + self.token
        log.info("Balance Sheet URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "balancesheet", response.json())

        return response.json()

    def keyStats(self, symbol):
        log.info("Getting key stats information for: %s", symbol)

        cachedResponse = self.readCache(symbol, "keystats")
        if cachedResponse != None:
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

        cachedResponse = self.readCache(symbol, "advancedkeystats")
        if cachedResponse != None:
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

        cachedResponse = self.readCache(symbol, "price")
        if cachedResponse != None:
            return cachedResponse

        url = baseURL+symbol+"/price?token=" + self.token
        log.info("Price URL: %s", url)

        response = self.session.get(url)

        log.info("Status Code: %s", response.status_code)
        log.debug("Response: %s", response.json())

        self.writeCache(symbol, "price", response.json())

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
