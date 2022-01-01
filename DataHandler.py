from IBAPI import *
from HistoricalDataEnums import HistoricalDataEnums
from random import randint, randrange

import time
import statistics
import math

class DataHandler():
    def __init__(self, headers: list, data, operations: Operations):
        self.headers = headers
        self.data = data
        self.operations = operations
    
    def getBetaAgainstMarketIndex2Yr(self):
        sp500Contract = Contract()
        sp500Contract.symbol = "SPY"
        sp500Contract.secType = "STK"
        sp500Contract.exchange = "ARCA"
        sp500Contract.currency = "USD"

        headers = ['date', 'open', 'high', 'low', 'close', 'volume', 'average', 'barCount']

        sp500SymbolPath = os.getcwd() + "//{}.csv".format(sp500Contract.symbol)
        self.operations.client.csvClient.setPath(headers, sp500SymbolPath)
        self.operations.getHistoricalMarketData(
            randint(200, 900),
            sp500Contract, 
            HistoricalDataEnums.QUERY_TIME.value, 
            HistoricalDataEnums.DURATION_FIVEYEARS.value, 
            HistoricalDataEnums.BAR_SIZE_ONEMONTH.value, 
            HistoricalDataEnums.HISTORICAL_DATA_TYPE_MIDPOINT.value)
        time.sleep(2)

        sp500Data = self.operations.client.csvClient.readCsvToList(sp500SymbolPath, HistoricalDataEnums.RAW_EQUITY_DATA.value)
        firstDataClose, marketDataClose = self.operations.client.csvClient.validateTwoDatasetDatesAndReturnCloseValues(self.data, sp500Data[1], 4)
        betaValue = self.calculateBetaHelper(firstDataClose, marketDataClose)
        return betaValue

    def calculateBetaHelper(self, Ri, Rm):
        covar = self.calculateCovariance(Ri, Rm)
        var = self.calculateVariance(Rm)  
        return covar/var
    
    def calculateCovariance(self, Ri, Rm):
        return self.covariance(Ri, Rm)

    def calculateVariance(self, Rm):
        return self.variance(Rm)
    
    def getCapitalAllocation(self, firstBeta, secondBeta, capitalAmount):
        capitalAmount = float(capitalAmount)/2
        capitalNeededOne = capitalAmount//firstBeta
        print("Desired Market Exposure, Asset One: ", capitalAmount)
        print("Asset One Beta: ", firstBeta)
        print(capitalAmount, "/", firstBeta, " = Long allocation needed: $", capitalNeededOne)
        print("\n")

        capitalNeededTwo = capitalAmount//secondBeta
        print("Desired Market Exposure, Asset Two: ", capitalAmount)
        print("Asset Two Beta: ", secondBeta)
        print(capitalAmount, "/", secondBeta, " = Short allocation needed: $", capitalNeededTwo)
        print("\n")

        print("Total cash allocation: $", capitalNeededOne+capitalNeededTwo)
        print("Exposure: ", "100% Market Neutral")
    
        return

    def variance(self, data):
        # Number of observations
        n = len(data)
        # Mean of the data
        mean = sum(data) / n
        # Square deviations
        deviations = [(x - mean) ** 2 for x in data]
        # Variance
        variance = sum(deviations) / n
        return variance

    def covariance(self, x, y, /):
        """Covariance
        Return the sample covariance of two inputs *x* and *y*. Covariance
        is a measure of the joint variability of two inputs.
        >>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> y = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        >>> covariance(x, y)
        0.75
        >>> z = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        >>> covariance(x, z)
        -7.5
        >>> covariance(z, x)
        -7.5
        """
        n = len(x)
        if len(y) != n:
            raise StatisticsError('covariance requires that both inputs have same number of data points')
        if n < 2:
            raise StatisticsError('covariance requires at least two data points')
        xbar = math.fsum(x) / n
        ybar = math.fsum(y) / n
        sxy = math.fsum((xi - xbar) * (yi - ybar) for xi, yi in zip(x, y))
        return sxy / (n - 1)