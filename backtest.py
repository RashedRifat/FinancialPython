# Testing playground for new functions 
import pandas as pd
import tqdm 
import tools, utils 
import datetime as dt
from order import order
from math import floor

def equals(o1, o2):
    '''Compares two string objects'''
    if o1 == None or o2 == None:
        raise ValueError("Expected strings, objects are null.")
    if not isinstance(o1, str):
        raise TypeError("Expected string objects.")
    if type(o1) != type(o2):
        raise TypeError("Expected two string objects")

    o1 = o1.strip().lower()
    o2 = o2.strip().lower()
    if o1 == o2:
        return True
    else:
        return False

class backtest():
    def __init__(self, stocks, start, end, api=None):
        self.api = utils.set_API(ID=None, key=None)
        self.stocks = stocks
        self.start = start
        self.end = end
        self.results = utils.analyze(stocks=self.stocks, start = self.start, end=self.end, api=self.api)
        self.id_counter = 0
        self.totalProfit = dict()
        self.capital = 0
        self.recent_log = None

    def threshold(self, date, price, current_order, trade_profit, max_drawdown, all_orders, capital, max_profit, 
                                                                                                        shares=1):
        '''Function for dealing with selling for the algorithim.'''

        current_order.sell_order(date, price)
        trade_profit += current_order.profit
        capital += (current_order.soldPrice * shares)
        all_orders.append(current_order)
        
        if current_order.profit < max_drawdown:
            max_drawdown = current_order.profit
        elif current_order.profit > max_profit:
            max_profit = current_order.profit
        
        return [current_order, trade_profit, max_drawdown, all_orders, capital, max_profit]

    
    def check_sell(self, date, price, current_order, trade_profit, max_drawdown, all_orders, capital, max_profit, 
                                                                                            shares=1, testing=False):
        if current_order == None:
            return None

        # Check and sell if price falls below stopPrice or above profitPrice
        if price <= current_order.stopPrice or price >= current_order.profitExit:
            toReturn = self.threshold(date, price, current_order, trade_profit, max_drawdown, all_orders, capital, max_profit, 
                                                                                                                shares=shares)

            if testing:
                print("Sold 1 stock due to stop losses at ", toReturn[0].soldPrice)
                print("Profit: ", toReturn[1], "Capital: ", toReturn[4], "\n") 

            toReturn[0] = None
            return toReturn
    
    def log(self):
        '''Create a set of results for a paritcular run'''
        today = str(dt.datetime.today())
        filename = str(today.replace(" ", "_").replace(".", "-").replace(":", "-"))
        f = open("results\\" + filename + ".txt", "w+")
        s = open("summary\\" + filename + ".txt", "w+")
        self.recent_log = "summary\\" + filename + ".txt"

        f.write("Summary of for [" + today + " GMT]\n")
        s.write("Summary of for [" + today + " GMT]\n")

        stockNames = list(self.totalProfit.keys())
        f.write("Results for: [" + ", ".join(stockNames) + "]\n")
        s.write("Results for: [" + ", ".join(stockNames) + "]\n")

        for key in stockNames:
            f.write("\nSummary of Trades for [" + key + "]\n")
            f.write("[----------------------------------------------------------------]\n")
            trades = self.totalProfit[key][0]
            for trade in trades:
                f.write(trade.tradeString() + "\n")
            f.write("[----------------------------------------------------------------]\n\n")


            s.write("\nSummary of Trades for [" + key + "]\n")
            s.write("[----------------------------------------------------------------]\n")
            data = self.totalProfit[key]
            # Calculate P\L 
            pl_ratio = 0
            for order in data[0]:
                if order.profitLoss > 0:
                    pl_ratio += 1

            s.write("Orders Made: " + str(len(data[0])))
            s.write("\nP\\L Ratio: " + str(pl_ratio) + "/" + str(len(data[0])) + " = " + 
                                                            str(round(100 *(1.0 * pl_ratio / len(data[0])), 2)) + "%")                                    
            s.write("\nProfit Percent: " + str(round((data[1] / self.capital) * 100, 2)) + "%")
            s.write("\nProfit: $" + str(round(data[1], 2)))
            s.write("\nMax Profit: $" + str(round(data[2], 2)))
            s.write("\nMax Drawdown: $" + str(round(data[3], 2)))
            s.write("\nEnding Balance: $" + str(round(data[4], 2)))
            s.write("\n[----------------------------------------------------------------]\n\n")

        f.close()
        s.close()
    
    def algo_1(self, risk, profit, starting_capital=500, testing=False):
        '''Generate buy and sell signals using the SuperTrend Indicator'''
        
        self.capital = starting_capital
        for stock in self.results.keys():
            all_orders = []
            current_order = None
            trade_profit = 0
            max_drawdown = 0
            max_profit = 0
            capital = self.capital
            current_shares = 0

            data = self.results[stock]   
            cash = capital
            stock = stock.upper()     
            data = data[[stock + "_date", stock+"_average", stock+"_ST", stock+"_ST_BUYSELL"]].copy(deep=True)
            data.rename(columns={stock + "_date":"date", stock+"_average":"price", 
                                        stock+"_ST_BUYSELL":"signal", stock+"_ST":"st"}, inplace=True)
            data = data.dropna()
            stopPrice = -1
            profitPrice = -1

            for i, row in data.iterrows():
                signal = data.loc[i,"signal"] 
                price = data.loc[i, "price"]
                date = data.loc[i, "date"]
            
                # Check to see if signal matches buy conditions 
                if equals(signal, "buy") and current_order == None:
                    if capital < price:
                        continue 
                    else:
                        current_shares = floor(capital / price)
                    
                    stopPrice = price * (1-risk)
                    profitPrice = price * (1+profit)
                    newOrder = order(self.id_counter, stock, date, price, profitPrice, stopPrice, shares=current_shares)
                    current_order = newOrder
                    self.id_counter += 1
                    capital -= (price * current_shares)

                    if testing:
                        print("Bought ", current_shares, " stock at ", current_order.buyPrice)
                        print("Profit: ", trade_profit, "Capital: ", capital, "\n")
                    continue

                # Check for sell conditons and threshold contions - use the new features. 
                sell = self.check_sell(date, price, current_order, trade_profit, max_drawdown, all_orders, capital, max_profit, 
                                                                                testing=testing, shares=current_shares)
                if sell != None:
                    current_order = sell[0]
                    trade_profit = sell[1]
                    max_drawdown = sell[2]
                    all_orders = sell[3]
                    capital = sell[4]
                    max_profit = sell[5]
                
                 # Check and sell if signal falls below threshold 
                if current_order != None and equals(signal, "Sell"):
                    checker = self.threshold(date, price, current_order, trade_profit, max_drawdown, all_orders, capital, 
                                                                                                max_profit, shares=current_shares)                    
                    current_order = checker[0]
                    trade_profit = checker[1]
                    max_drawdown = checker[2]
                    all_orders = checker[3]
                    capital = checker[4]
                    max_profit = checker[5]

                    if testing:
                        print("Sold ", current_shares, " stock due to siganl threshold at ", current_order.soldPrice)
                        print("Profit: ", trade_profit, "Capital: ", capital, "\n") 

                    current_order = None  
                    current_shares = 0

            # Resolution of Open Shares 
            if current_order != None:
                print("Outstanding shares: ", current_order.get_balance())
                capital += current_order.get_balance()
                current_order = None
                if all_orders[0] == None:
                    all_orders = all_orders[:-1]
            self.totalProfit[stock] = [all_orders, trade_profit, max_profit, max_drawdown, capital]
        
        self.log()
    
    def get_summary(self):
        if self.recent_log == None:
            return "Algorithims have not yet been run."

        temp = ""
        with open(self.recent_log, "r") as f:
            temp = f.read()
        
        return temp
