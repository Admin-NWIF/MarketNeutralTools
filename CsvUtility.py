from HistoricalDataEnums import *

import csv
import time

class CsvUtility:
    def __init__(self, headers, path=None):
        self.path = path
        self.headers = headers

        if path is not None:
            with open(path, 'w', encoding='UTF8', newline='') as file:
                csv.writer(file).writerow(self.headers)

    def insertRow(self, row):
        with open(self.path, 'a', encoding='UTF8', newline='') as file:
            csv.writer(file).writerow(row)
    
    def setPath(self, headers, path):
        with open(path, 'w', encoding='UTF8', newline='') as file:
                csv.writer(file).writerow(headers)
        self.path = path

    def readCsvToList(self, path, type):
        with open(path, 'r', encoding='UTF8') as file:
            reader = csv.reader(file)
            headers = next(reader)

            resultsDictionary = {}
            
            if type == HistoricalDataEnums.SYMBOL_LOOKUP_DATA.value:
                for num, line in enumerate(reader):
                    if line[3] == "NASDAQ.NMS":
                        line[3] = "SMART"
                    resultsDictionary[num] = line
            elif type == HistoricalDataEnums.RAW_EQUITY_DATA.value:
                for num, line in enumerate(reader):
                    resultsDictionary[num] = line

            return [headers, resultsDictionary]
    
    def validateTwoDatasetDatesAndReturnCloseValues(self, dataSetOne, dataSetTwo, closeIdx):
        dataSetOneCloses = []
        dataSetTwoCloses = []

        lastDataOneValue = None
        lastDataTwoValue = None

        if len(dataSetOne) != len(dataSetTwo):
            return [None, None]
        for key in dataSetOne:
            if dataSetOne[key][0] != dataSetTwo[key][0]:
                return [None, None]
            if lastDataOneValue is None and lastDataTwoValue is None:
                lastDataOneValue = float(dataSetOne[key][closeIdx])
                lastDataTwoValue = float(dataSetTwo[key][closeIdx])
            else:
                currentValue = float(dataSetOne[key][closeIdx])
                percentChange = self.percentChangeTwoValues(lastDataOneValue, currentValue)
                dataSetOneCloses.append(percentChange)
                lastDataOneValue = currentValue

                currentValue = float(dataSetTwo[key][closeIdx])
                percentChange = self.percentChangeTwoValues(lastDataTwoValue, currentValue)
                dataSetTwoCloses.append(percentChange)
                lastDataTwoValue = currentValue

        return [dataSetOneCloses, dataSetTwoCloses]
    
    def percentChangeTwoValues(self, valueOne, valueTwo):
        return (valueTwo-valueOne)/valueOne