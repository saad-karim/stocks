from data.analytics.trend import Trend
import numpy_financial as npf


class Analytics:

    def __init__(self, price, inc, bs, cf):
        self._price = price
        self._inc = inc
        self._bs = bs
        self._cf = cf
        self._trend = Trend(inc, bs, cf)

    def epsGrowth(self):
        return self._trend.epsGrowth(self.eps())

    def netWorkingCapital(self):
        nc = [0, 0, 0, 0]

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

        roic = [0, 0, 0, 0]
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

        fcfs = [0, 0, 0, 0]
        for i in capExpenses.keys():
            # Capital expenditures stored as negative values hence
            # the addition of the two
            fcfs.append(operationCF[i] + capExpenses[i])

        return fcfs

    # Earnings per share
    def eps(self):
        ni = self._inc.yearly().getKey("Net Income for EPS")
        cs = self._bs.yearly().getKey("Common Stock")

        allEPS = [0, 0, 0, 0]
        for i in ni.keys():
            allEPS.append(ni[i]/cs[i])

        return allEPS

    # Book Value per share
    def bvps(self):
        se = self._bs.yearly().getKey("Shareholder Equity")
        cs = self._bs.yearly().getKey("Common Stock")

        allBVPS = [0, 0, 0, 0]
        for i in se.keys():
            allBVPS.append(se[i]/cs[i])

        return allBVPS

    # Price to Book Value per Share Ratio
    def pbvRatio(self):
        bvps = self.bvps()

        pbv = [0, 0, 0, 0]
        for bvp in bvps:
            if bvp == 0:
                continue

            pbv.append(self._price.price/bvp)

        return pbv

    # Price to Earnings per Share Ratio
    def peRatio(self):
        allEPS = self.eps()

        pes = [0, 0, 0, 0]
        for eps in allEPS:
            if eps == 0:
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
        print("fcfs: ", fcfs)

        fcfGrowthRate = self._trend.fcfGrowth(fcfs)["overallTrend"]
        print("fcf growth rate: ", fcfGrowthRate)

        currentfcf = fcfs[4]
        print("current fcf", currentfcf)

        firstYear = currentfcf * (1 + fcfGrowthRate)
        print("first year", firstYear)

        futureCashFlows = [firstYear]
        for x in range(9):
            futureCashFlows.append(futureCashFlows[x]*(1 + fcfGrowthRate))

        print("future cash flows", futureCashFlows)
        npv = npf.npv(0.15, futureCashFlows)

        terminalValue = pvs[9] * 10
        value = terminalValue + npv

        cs = self._bs.yearly().getKey("Common Stock")
        print("cs: ", cs)
        ivPerStock = npv / cs[2020]  # TODO: Get number of shares as real time data

        print("iv per stock", ivPerStock)

        return ivPerStock
