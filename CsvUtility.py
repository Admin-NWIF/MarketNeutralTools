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

    def readCsvToList(self, path):
        with open(path, 'r', encoding='UTF8') as file:
            reader = csv.reader(file)
            headers = next(reader)

            resultsDictionary = {}
            for num, line in enumerate(reader):
                if line[3] == "NASDAQ.NMS":
                    line[3] = "SMART"
                resultsDictionary[num] = line

            return [headers, resultsDictionary]