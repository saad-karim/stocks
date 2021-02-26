class IntrinsicValue:

    def __init__(self):
        return


    def freeCashFlow(self, baseCashFlow, growthRate, n):
        fcf = (baseCashFlow * (1 + growthRate)**n)
        return round(fcf)

    def discountFactor(self, discountRate, n):
        df = (1 + discountRate)**n
        return round(df, 2)

    def discountedFreeCashFlow(self, baseCashFlow, growthRate, discountRate, n):
        totalCF = 0
        for i in range(1,n+1):
            DFCF = self.freeCashFlow(baseCashFlow, growthRate, i) / self.discountFactor(discountRate, i)
            totalCF = totalCF + DFCF
        return round(totalCF)

    def discountedPerpetuityCashFlow(self, baseCashFlow, longGrowthRate, growthRate, discountRate):
        DPCF = ((baseCashFlow*(1+growthRate)**11 * (1 + longGrowthRate))/(discountRate - longGrowthRate)) * (1/(1 + discountRate)**11)
        return round(DPCF)

    def calc(self, baseCashFlow, longGrowthRate, growthRate, discountRate, keyStats, n):
        iv = round(((self.discountedFreeCashFlow(baseCashFlow, growthRate, discountRate, n)
                        + self.discountedPerpetuityCashFlow(baseCashFlow, longGrowthRate, growthRate, discountRate))
                        / keyStats["Shares Outstanding"]), 2)
        return iv
