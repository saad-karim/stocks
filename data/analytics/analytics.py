class Analytics:

    def __init__(self, inc, bs, cf):
        self._inc = inc
        self._bs = bs
        self._cf = cf

    def netWorkingCapital(self):
        nc = [0, 0, 0, 0]

        assets = self._bs.yearly().getKey("Current Assets")
        liabilities = self._bs.yearly().getKey("Current Liabilities")

        if len(assets) != len(liabilities):
            raise Exception("number of elements in assets and liabilities must match")

        for i in assets.keys():
            nc.append(assets[i] - liabilities[i])

        return nc

    def roic(self):
        # Ref: https://www.thebalancesmb.com/return-on-invested-capital-393587
        inc = self._inc
        bs  = self._bs
        cf  = self._cf
        
        roic = [0, 0, 0, 0]
        ebits = inc.yearly().getKey("EBIT")
        for i in ebits.keys():
            ebit = ebits[i]
            nopat = ebit * (1.2) # Multiplied by marginal tax rate
            
            curLiab = bs.yearly().getKey("Current Liabilities")[i]
            longDebt = bs.yearly().getKey("Long-Term Debt")[i]
            commonStock = bs.yearly().getKey("Common Stock")[i]
            retainedEarnings = bs.yearly().getKey("Retained Earnings")[i]
            cashFromFin = cf.yearly().getKey("Financing Cash Flow")[i]
            cashFromInv = cf.yearly().getKey("Investing Cash Flow")[i]
            
            ic = curLiab + longDebt + commonStock + retainedEarnings + cashFromFin + cashFromInv

            roic.append(nopat/ic)
        
        return roic