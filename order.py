import datetime as dt

class order():
    '''A class that represents an order on the stock market.'''

    def __init__(self, ID, stock, startDate, buyPrice, profitExit, stopPrice, shares=1):
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
        self.profitLoss = 0
        self.current_shares = shares
    
    def sell_order(self, endDate, soldPrice):
        endArray = endDate.split(" ")[0].split("-")
        self.endDate = endArray[1] + "-" + endArray[2] + "-" + endArray[0]
        self.soldPrice = float(soldPrice)
        self.profit = float(self.soldPrice - self.buyPrice) * self.current_shares
        self.profitPercent = float(self.profit / self.buyPrice) * 100 
        if self.profit > 0:
            self.profitLoss = 1
        else:
            self.profitLoss = -1

    def tradeString(self):
        toString = ""
        toString += f"ID: {self.ID:>26}\n"
        toString += f"Shares: {self.current_shares:>22}   ||   Stock: {self.stock:>26}\n"
        startdate = self.startDate.strftime("%m-%d-%Y")
        toString += f"Buy Date: {startdate:>20}   ||   Sell Date: {self.endDate:>22}\n"
        toString += f"Buy Price: {round(self.buyPrice,2):>19}   ||   Sell Price: {(round(self.soldPrice,2)):>21}\n"
        toString += f"Stop Order: {round(self.stopPrice,2):>18}   ||   Profit Exit: {round(self.profitExit,2):>20}\n"
        toString += f"Profit: {round(self.profit,2):>22}   ||   Profit Percent: {round(self.profitPercent, 2):>17}\n"
        return toString
    
    def get_balance(self):
        return self.buyPrice * self.current_shares