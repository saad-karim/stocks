import loader.date as loader

def generate(data, key):
    currentYear = loader.currentYear()
    return [
        data.quarterly().quarter(currentYear, 4).get(key),
        data.quarterly().quarter(currentYear, 3).get(key),
        data.quarterly().quarter(currentYear, 2).get(key),
        data.quarterly().quarter(currentYear, 1).get(key),
        data.yearly().year(currentYear-1).get(key),
        data.yearly().year(currentYear-2).get(key),
        data.yearly().year(currentYear-3).get(key),
        data.yearly().year(currentYear-4).get(key),
        data.yearly().year(currentYear-5).get(key),
    ]

def price(price):
    return {
        'Price Used for Calculations': [[price.resp.get("Price")], "money"],
    }

def dividend(dividend):
    return {
        'Dividend Amount': [generate(dividend, "Amount"), "money"],
    }

def income(income):
    return {
        'Interest Expense': [generate(income, "Interest Expense"), "ratio"],
        'Total Revenue': [generate(income, "Total Revenue"), "money"],
        'EBITDA': [generate(income, "EBITDA"), "money"], 
        'Net Income': [generate(income, "Net Income"), "money"],
        'Net Income Ratio': [generate(income, "Net Income Ratio"), "ratio"],
        'Gross Profit': [generate(income, "Gross Profit"), "money"],
        'Gross Profit Ratio': [generate(income, "Gross Profit Ratio"), "ratio"],
        'Operating Income': [generate(income, "Operating Income"), "money"],
        'Operating Income Ratio': [generate(income, "Operating Income Ratio"), "ratio"],
        'EPS': [generate(income, "EPS"), "money"],
    }

def balanceSheet(balancesheet):
    return {
        'Cash': [generate(balancesheet, "Cash"), "money"],
        'Current Assets': [generate(balancesheet, "Current Assets"), "money"],
        'Current Liabilities': [generate(balancesheet, "Current Liabilities"), "money"],
        'Shareholder Equity': [generate(balancesheet, "Shareholder Equity"), "money"],
    }

def cashFlow(cashFlow):
        return {
            'Free Cash Flow': [generate(cashFlow, "Free Cash Flow"), "money"],
            'Acquisitions': [generate(cashFlow, "Acquisitions"), "money"],
            'Stock BuyBack': [generate(cashFlow, "Stock Buyback"), "money"],
            'Net Change in Cash': [generate(cashFlow, "Net Change in Cash"), "money"],
            'Operating Cash Flow': [generate(cashFlow, "Operating Cash Flow"), "money"],
            'Investing Cash Flow': [generate(cashFlow, "Investing Cash Flow"), "money"],
            'Financing Cash Flow': [generate(cashFlow, "Financing Cash Flow"), "money"],
        }