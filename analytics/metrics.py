# from analytics import trend as trend
import analytics.trend as trend
import numpy_financial as npf


class Metrics:

    def __init__(self, price, quote, inc, bs, cf):
        self._price = price
        self._quote = quote
        self._inc = inc
        self._bs = bs
        self._cf = cf

    def epsGrowth(self):
        return self._trend.epsGrowth(self.eps())

    def netWorkingCapital(self):
        nc = [None, None, None, None]

        assets = self._bs.yearly().getKey("Current Assets")
        liabilities = self._bs.yearly().getKey("Current Liabilities")

        if len(assets) != len(liabilities):
            raise Exception("number of elements in assets and liabilities \
                must match")

        for i in assets.keys():
            nc.append(assets[i] - liabilities[i])

        return nc

    def roic(self):
        # Ref: https://www.thebalancesmb.com/return-on-invested-capital-393587
        inc = self._inc
        bs = self._bs
        cf = self._cf

        roic = [None, None, None, None]
        ebits = inc.yearly().getKey("EBIT")
        for i in ebits.keys():
            ebit = ebits[i]
            nopat = ebit * (1.2)  # Multiplied by marginal tax rate

            curLiab = bs.yearly().getKey("Current Liabilities")[i]
            longDebt = bs.yearly().getKey("Long-Term Debt")[i]
            commonStock = bs.yearly().getKey("Common Stock")[i]
            retainedEarnings = bs.yearly().getKey("Retained Earnings")[i]
            cashFromFin = cf.yearly().getKey("Financing Cash Flow")[i]
            cashFromInv = cf.yearly().getKey("Investing Cash Flow")[i]

            ic = curLiab + longDebt + commonStock + retainedEarnings + \
                cashFromFin + cashFromInv

            roic.append(nopat/ic)

        return roic

    # Free cash flow (Owner's Earnings)
    def fcf(self):
        # Ref: https://corporatefinanceinstitute.com/resources/knowledge/valuation/fcf-formula-free-cash-flow/
        cf = self._cf

        capExpenses = cf.yearly().getKey("Capital Expenditures")
        operationCF = cf.yearly().getKey("Operating Cash Flow")

        fcfs = []
        for i in capExpenses.keys():
            # Capital expenditures stored as negative values hence
            # the addition of the two
            fcfs.append(operationCF[i] + capExpenses[i])

        return fcfs

    # Earnings per share
    def eps(self):
        ni = self._inc.yearly().getKey("Net Income for EPS")
        cs = self._bs.yearly().getKey("Common Stock")

        allEPS = []
        for i in ni.keys():
            allEPS.append(ni[i]/cs[i])

        return allEPS

    # Book Value per share
    def bvps(self):
        se = self._bs.yearly().getKey("Shareholder Equity")
        cs = self._bs.yearly().getKey("Common Stock")

        allBVPS = []
        for i in se.keys():
            allBVPS.append(se[i]/cs[i])

        return allBVPS

    # Price to Book Value per Share Ratio
    def pbvRatio(self):
        bvps = self.bvps()

        pbv = [None, None, None, None]
        for bvp in bvps:
            if bvp is None:
                continue

            pbv.append(self._price.price/bvp)

        return pbv

    # Price to Earnings per Share Ratio
    def peRatio(self):
        allEPS = self.eps()

        pes = [None, None, None, None]
        for eps in allEPS:
            if eps is None:
                continue

            pes.append(self._price.price/eps)

        return pes

    # TODO: Monte Carlo simulation
    # https://www.youtube.com/watch?v=l-T-Vyk2txc

    def intrinsicValue(self):
        # 1. Need fcf (owner's earnings)
        # 2. Get average cash flow growth rate
        # 3. Calculate cash flow for next years based on rate from step 2
        # 4. Discount future cash flow to present
        # 5. Take last cash flow times 10 to get terminal value
        # 6. Add terminal value plus cash flows
        fcfs = self.fcf()

        fcfGrowthRate = trend.overall(fcfs)
        currentfcf = fcfs[4]

        futureCashFlows = []
        for x in range(10):
            value = currentfcf*(1+fcfGrowthRate)**(x+1)
            futureCashFlows.append(value)

        npv = npf.npv(0.15, futureCashFlows)

        terminalValue = futureCashFlows[9] * 7
        instrincValue = terminalValue + npv

        cs = self._quote.get()["sharesOutstanding"]
        ivPerStock = instrincValue / cs

        return ivPerStock

    def intrinsicValueDiscountedPerpetuity(self, fcfs, discountRate, shares):
        fcfGrowthRate = trend.overall(fcfs)
        currentfcf = fcfs[4]

        futureCashFlows = []
        for x in range(10):
            value = currentfcf*(1+fcfGrowthRate)**(x+1)
            futureCashFlows.append(value)

        discountRates = []
        for x in range(10):
            value = (1+discountRate)**(x+1)
            discountRates.append(value)

        dfcfs = []
        for x in range(10):
            dfcfs.append(futureCashFlows[x]/discountRates[x])

        dpfc = (((currentfcf*(1+fcfGrowthRate)**11)*(1+.03))/(discountRate-.03)) * (1/(1+discountRate)**11)
        iv = sum(dfcfs) + dpfc
        ivPerStock = iv / shares

        return ivPerStock
