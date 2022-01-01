from ibapi.client import EClient
from ibapi.wrapper import EWrapper 
from ContractSamples import *
from ibapi.common import * # @UnusedWildImport
from ibapi.utils import * # @UnusedWildImport
from ibapi.contract import (Contract, ContractDetails, DeltaNeutralContract)
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.execution import Execution
from ibapi.ticktype import * # @UnusedWildImport
from ibapi.commission_report import CommissionReport
from CsvUtility import CsvUtility

import datetime
import time
import threading
import os

class IBAPI(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        headers = ['conId', 'symbol', 'secType', 'primExchange', 'currency', 'derivativeSecTypes']
        self.csvClient = CsvUtility(headers)

    def historicalData(self, reqId:int, bar: BarData):
        # print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        #rowData = str(bar.date) + "," + str(bar.open) + "," +  str(bar.high) + "," +  str(bar.low) + "," +  str(bar.close) + "," +  str(bar.volume) + "," +  str(bar.average) + "," +  str(bar.barCount)
        barData = [bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume, bar.average, bar.barCount]
        self.csvClient.insertRow(barData)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)

    def symbolSamples(self, reqId: int, contractDescriptions: ListOfContractDescription):
        super().symbolSamples(reqId, contractDescriptions)
        print("Symbol Samples. Request Id: ", reqId)
        
        headers = ['conId', 'symbol', 'secType', 'primExchange', 'currency', 'derivativeSecTypes']
        csvUtility = CsvUtility(path=os.getcwd()+"\\choices.csv", headers=headers)

        for contractDescription in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += derivSecType
            derivSecTypes += " "
            currentRow = [
                contractDescription.contract.conId,
                contractDescription.contract.symbol,
                contractDescription.contract.secType,
                contractDescription.contract.primaryExchange,
                contractDescription.contract.currency, derivSecTypes
            ]
            csvUtility.insertRow(currentRow)
            # print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, "
            #         "currency:%s, derivativeSecTypes:%s" % (
            #     contractDescription.contract.conId,
            #     contractDescription.contract.symbol,
            #     contractDescription.contract.secType,
            #     contractDescription.contract.primaryExchange,
            #     contractDescription.contract.currency, derivSecTypes))

class Operations():
    def __init__(self, host, port, clientId):
        self.client = IBAPI()
        self.client.connect(host, port, clientId)
        self.api_thread = threading.Thread(target = self.runLoop, daemon=True)
        self.api_thread.start()
        time.sleep(1)

    def runLoop(self):
        self.client.run()
    
    def getHistoricalMarketData(self, reqId, contract, queryTime, durationString, barSize, historicalDataType):
        self.client.reqHistoricalData(reqId, contract, queryTime, durationString, barSize, historicalDataType, 1, 1, False, [])

    def stockSearch(self, symbol):
        self.client.reqMatchingSymbols(1, symbol)
        
# x.getHistoricalMarketData("symbol")

# time.sleep(100) #Sleep interval to allow time for incoming price data