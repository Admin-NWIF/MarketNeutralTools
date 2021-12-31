from IBAPI import *
from consolemenu import *
from consolemenu.items import *
from prompt_toolkit import *
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from HistoricalDataEnums import *

import os
import time
import click

class Program():
    def __init__(self):
        self.operations = Operations("127.0.0.1", 4001, 21)
        # self.operations.stockSearch("TSLA")
        self.menu = ConsoleMenu("Market Neutral Tool", "Beta")
        self.menuRender(self.menu)

    def menuRender(self, menu):
        # Create the menu
        menu = ConsoleMenu("Title", "Subtitle")

        # MenuItem is the base class for all items, it doesn't do anything when selected
        menu_item = MenuItem("Menu Item")

        # A FunctionItem runs a Python function when selected
        function_item = FunctionItem("Symbol Searcher", self.userInput)
        function_item = FunctionItem("Neutral Trade Creator", self.neutralTradeMaker)

        menu.append_item(menu_item)
        menu.append_item(function_item)
        menu.show()

    def userInput(self):
        user_input = prompt('Symbol>', history=FileHistory('history.txt'), auto_suggest=AutoSuggestFromHistory())
        click.echo_via_pager(user_input)
        self.operations.stockSearch(user_input)

        selection_menu = SelectionMenu(["item1", "item2", "item3"])
        submenu_item = SubmenuItem("Submenu item", selection_menu, self.menu)
        self.menu.append_item(submenu_item)
        self.menu.show()

        while True:
            return
    
    def neutralTradeMaker(self):
        firstSelection, secondSelection = -1, -1

        # First Symbol Selection
        user_input = prompt('First Symbol>', history=FileHistory('history.txt'), auto_suggest=AutoSuggestFromHistory())
        self.operations.stockSearch(user_input)

        time.sleep(1)
        path = os.getcwd()+"\\choices.csv"
        headers = ['conId', 'symbol', 'secType', 'primExchange', 'currency', 'derivativeSecTypes']
        csvUtility = CsvUtility(headers)
        headers, resultsDictionary = csvUtility.readCsvToList(path)

        print("Select from an option below. (For example: Option 4 -> Type 4 and Press ENTER")
        print("")
        print("")
        print("  ", headers)
        for key in resultsDictionary:
            print(key, " ", resultsDictionary[key])
        user_selection = prompt('Selection>')
        firstSelection = int(user_selection)
        firstContract = Contract()
        # firstContract.conId = resultsDictionary[firstSelection][0]
        firstContract.symbol = resultsDictionary[firstSelection][1]
        firstContract.secType = resultsDictionary[firstSelection][2]
        firstContract.exchange = resultsDictionary[firstSelection][3] if resultsDictionary[firstSelection][3] is not "NASDAQ.NMS" else "NASDAQ"
        firstContract.currency = resultsDictionary[firstSelection][4]

        os.system('cls' if os.name == 'nt' else 'clear')

        # Second Symbol Selection
        user_input = prompt('Second Symbol>', history=FileHistory('history.txt'), auto_suggest=AutoSuggestFromHistory())
        self.operations.stockSearch(user_input)

        time.sleep(1)
        headers, resultsDictionary = csvUtility.readCsvToList(path)

        print("Select from an option below. (For example: Option 4 -> Type 4 and Press ENTER")
        print("")
        print("")
        print("  ", headers)
        for key in resultsDictionary:
            print(key, " ", resultsDictionary[key])
        user_selection = prompt('Selection>')
        secondSelection = int(user_selection)
        secondContract = Contract()
        # secondContract.conId = resultsDictionary[secondSelection][0]
        secondContract.symbol = resultsDictionary[secondSelection][1]
        secondContract.secType = resultsDictionary[secondSelection][2]
        secondContract.exchange = resultsDictionary[secondSelection][3] if resultsDictionary[firstSelection][3] is not "NASDAQ.NMS" else "NASDAQ"
        secondContract.currency = resultsDictionary[secondSelection][4]

        os.system('cls' if os.name == 'nt' else 'clear')

        print("Symbols Selected: [", firstContract.symbol, ", ", secondContract.symbol, "]")
        capital_allocation = prompt('Capital Allocation (ex: 10500)>', history=FileHistory('capitalallocationhistory.txt'), auto_suggest=AutoSuggestFromHistory())
        
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
        headers = ['date', 'open', 'high', 'low', 'close', 'volume', 'average', 'barCount']
        self.operations.client.csvClient.setPath(headers, os.getcwd() + "//{}.csv".format(firstContract.symbol))
        firstSymbolDataSet = self.operations.getHistoricalMarketData(
            100,
            firstContract, 
            queryTime, 
            HistoricaDataEnums.DURATION_ONEMONTH.value, 
            HistoricaDataEnums.BAR_SIZE_ONEDAY.value, 
            HistoricaDataEnums.HISTORICAL_DATA_TYPE_MIDPOINT.value)
        time.sleep(1)
        self.operations.client.csvClient.setPath(headers, os.getcwd() + "//{}.csv".format(secondContract.symbol))
        secondSymbolDataSet = self.operations.getHistoricalMarketData(
            101,
            secondContract, 
            queryTime, 
            HistoricaDataEnums.DURATION_ONEMONTH.value, 
            HistoricaDataEnums.BAR_SIZE_ONEDAY.value, 
            HistoricaDataEnums.HISTORICAL_DATA_TYPE_MIDPOINT.value)

        time.sleep(100)

        
        

x = Program()