# Testing the Alpaca API
import alpaca_trade_api as tradeapi
import pandas as pd 

# Set up API
api = tradeapi.REST("PKK0OEAG0UQRP9KN9IYD", "NXkfAhVf8kGluaXMji73RiaAuyzLQzc3ykhcUBHR", base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below
account = api.get_account()

def check_for_data(stocks, start, end):
    '''Checks if stock data is already in the data file.'''

    f = open("runs.txt", "a+")
    f.seek(0)
    lines = f.readlines()
    returnStocks = list()

    for stock in stocks:
        search_text = stock.upper() + start + end + "\n"
        if search_text in lines:
            continue
        else:
            f.seek(2)
            f.write(search_text)
            returnStocks.append(stock.upper())
    f.close()

    return returnStocks


def make_data_csv(stocks=["AAPL", "MSFT"], start="2020-10-01", end="2020-10-31", reset=False):
    '''Make new csv's if needed'''

    # Basic Error Checking
    if not isinstance(stocks, list):
        raise TypeError("make_data_csv: must have an input of type list with string values!")
    if len(stocks) == 0 or not start or not end:
        raise TypeError("make)data_csv: incorrect parameters")

    #Check for previous runs 
    if not reset:
        stocks = check_for_data(stocks, start, end)
        if len(stocks) == 0 and reset == False:
            print("Data saved from previous runs, new csv('s) not needed.\n") 
            return

    # Get Data from API
    NY = 'America/New_York'
    start = pd.Timestamp(start, tz=NY).isoformat()
    end = pd.Timestamp(end, tz=NY).isoformat()
    data = api.get_barset(stocks, 'day', start=start, end=end).df

    # Save Data in CSV for later use
    stop_index = len(data.columns)
    if stop_index % 5 != 0:
        raise TypeError("API did not return expected number of columns")
    start_index = 0
    end_index = 5

    # Save Data    
    while (start_index < stop_index):
        stock_data = data[data.columns[start_index:end_index]]
        filename = "data\\" + stocks[0].lower() + "_data.csv"
        stocks.pop(0)
        stock_data.to_csv(filename)
        start_index += 5
        end_index += 5
        print("Saved file: " + filename)


def get_data(stocks=["AAPL"]):
    if not isinstance(stocks, list):
        raise TypeError("get_data must have an input of type list!")

    stock_dict = dict()
    for stock in stocks:
        stock = stock.lower()
        filename = "data\\" + stock + "_data.csv"
        stock_data = pd.read_csv(filename).dropna()
        columns = ["date", stock + "_open", stock + "_high", stock + "_low", stock + "_close", stock + "_volume"]
        stock_data.columns = columns
        stock_dict[stock.upper()] = stock_data
    
    return stock_dict


def run(stocks, start, end):
    '''Psudo Main Class for running the File'''
    make_data_csv(stocks, start, end)
    stock_dict = get_data(stocks)

# Test Methods
run(stocks=["AAPL", "MSFT", "TSLA"], start="2020-10-01", end="2020-10-31")