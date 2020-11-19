# Testing playground for new functions 
import pandas as pd
import tqdm 
import tools, utils 
import datetime as dt

# TO-DO:
# Create a backtesting file that predicts stock movements and takes position as required 
# For the purpose of this test, no shorts will be allowed  

class order():
    def __init__(self, ID, stock, startDate, buyPrice, profitExit, stopPrice):
        startArray = startDate.split(" ")[0].split("-")
        self.ID = ID
        self.stock = stock
        self.startDate = dt.datetime(int(startArray[0]), int(startArray[1]), int(startArray[2]))
        self.buyPrice = float(buyPrice)
        self.profitExit = float(profitExit)
        self.stopPrice = float(stopPrice)
        self.soldPrice = " Open Position"
        self.endDate = " Open Postion"
        self.profit = " Open Position"
        self.profitPercent = " Open Postion"
    
    def sell_order(self, endDate, soldPrice):
        endArray = endDate.split(" ")[0].split("-")
        self.endDate = dt.datetime(int(endArray[0]), int(endArray[1]), int(endArray[2]))
        self.soldPrice = float(soldPrice)
        self.profit = float(self.soldPrice - self.buyPrice)
        self.profitPercent = float(self.profit / self.buyPrice) * 100 

    def __str__(self):
        toString = ""
        toString += f"ID: {self.ID:>26}   ||   Stock: {self.stock:>26}\n"
        startdate = self.startDate.strftime("%m-%d-%Y")
        toString += f"Buy Date: {startdate:>20}   ||   End Date: {self.endDate:>23}\n"
        toString += f"Buy Price: {self.buyPrice:>19}   ||   Sell Price: {self.soldPrice:>21}\n"
        toString += f"Stop Order: {self.stopPrice:>18}   ||   Profit Exit: {self.profitExit:>20}\n"
        toString += f"Profit: {self.profit:>22}   ||   Profit Percent: {self.profitPercent:>17}\n"
        return toString
        

class backtest():
    def __init__(self, stocks, start, end, api=None):
        self.api = utils.set_API(ID="", key="")
        self.stocks = stocks
        self.start = start
        self.end = end
        self.results = utils.analyze(stocks=self.stocks, start = self.start, end=self.end, api=self.api)
        self.id_counter = 0
        self.totalProfit = dict()
        self.capital = 0
    
    def begin(self):
        pass
    # create your own backtest here
