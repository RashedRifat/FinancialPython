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
        self.profit = float(self.buyPrice - self.soldPrice)
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
        self.api = utils.set_API(ID="PKTCO6SLSQRIGROJLNHR", key="4z0sJl647VMSqM4FoLbfelMjDhy3aigz6OXlKor9")
        self.stocks = stocks
        self.start = start
        self.end = end
        self.results = utils.analyze(stocks=self.stocks, start = self.start, end=self.end, api=self.api)
        self.id_counter = 0
        self.totalProfit = dict()
        self.capital = 0
    
    def begin(self, risk, profit, capital=500, threshold=7):

        print("\n\nBegin Testing...")
        self.capital = capital

        # Begin by iterating through the list of stocks and generating a profit/loss for each
        for stock in self.results.keys():
            all_orders = []
            current_order = None
            trade_profit = 0
            max_drawdown = 0
            max_profit = 0
            capital = self.capital

            data = self.results[stock]   
            cash = capital
            stock = stock.upper()     
            data = data[[stock + "_date", stock+"_average", stock+"_FINAL_SIGNAL"]].copy(deep=True)
            data.rename(columns={stock + "_date":"date", stock+"_average":"price", stock+"_FINAL_SIGNAL":"signal"}, inplace=True)
            stopPrice = -1
            profitPrice = -1

            # Iterate through the list 
            for i, row in data.iterrows():
                signal = data.loc[i,"signal"] 
                price = data.loc[i, "price"]
                date = data.loc[i, "date"]

                # Start a new order
                if signal >= threshold and current_order == None:
                    stopPrice = price*(1-risk)
                    profitPrice = price*(1+profit)
                    
                    if capital - price < 0:
                        continue
                    
                    newOrder = order(ID=self.id_counter, stock=stock, startDate=date, 
                                        buyPrice=price, profitExit=price*(1+profit), stopPrice=stopPrice)
                    current_order = newOrder
                    self.id_counter += 1
                    capital -= price
                    continue
                
                # Check and sell if price falls below stopPrice
                if current_order != None and price <= stopPrice:

                    current_order.sell_order(endDate=date, soldPrice=price)
                    trade_profit += current_order.profit
                    if current_order.profit < max_drawdown:
                        max_drawdown = current_order.profit
                    all_orders.append(current_order)
                    capital += current_order.soldPrice
                    current_order = None
            

                # Check and sell if price rises above profitPrice 
                if current_order != None and price >= profitPrice:
                    current_order.sell_order(endDate=date, soldPrice=price)
                    trade_profit += current_order.profit

                    if current_order.profit > max_profit:
                        capital += current_order.soldPrice

                    capital += current_order.profit
                    all_orders.append(current_order)
                    current_order = None
                

                # Check and sell if signal falls below threshold 
                if current_order != None and signal < threshold:
                    current_order.sell_order(endDate=date, soldPrice=price)
                    trade_profit += current_order.profit

                    if current_order.profit < max_drawdown:
                        max_drawdown = current_order.profit
                    if current_order.profit > max_profit:
                        max_profit = current_order.profit

                    all_orders.append(current_order)
                    capital += current_order.soldPrice
                    current_order = None

                print("Profit: ", trade_profit, "Capital: ", capital)  
                    
            self.totalProfit[stock] = [all_orders, trade_profit, max_profit, max_drawdown]
        return self.totalProfit



newTest = backtest(["GOOG"], start="2019-01-01", end="2019-12-31")
toReturn = newTest.begin(risk=0.05, profit=0.10, threshold=6, capital=2000)
print("\nOrders Made: ", len(toReturn["GOOG"][0]))
print("Profit: $", round(toReturn["GOOG"][1], 2))
print("Max Profit: $", round(toReturn["GOOG"][2], 2))
print("Max Drawdown: $", round(toReturn["GOOG"][3], 2))

# Create a backtest.set() to easily set paraeters for the analyze function 
# Create a backtest.results() to get a readable set of results 
#    Make sure to add all of the orders and their to string to a txt file