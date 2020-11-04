# Testing the Alpaca API
import alpaca_trade_api as tradeapi
import pandas as pd 
import os 
#import tqdm 
import tools

# Set up API and check to see that it is working 
api = tradeapi.REST("hidden", "hidden", base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below
try:
    account = api.get_account()
except Exception:
    raise ConnectionError("Unable to get account for keys.")

def check_for_data(stocks, start, end):
    '''Checks if stock data is already in the data directory by using the runs.txt file.'''
    # Implement further validation here - check if the stock name is within the list of directories 
    # Check if the start and end dates match the dates within the file  
    # Create a clear function that removes all of the files within the data file and use it for reset=True

    f = open("bin\\runs.txt", "a+")
    f.seek(0)
    lines = f.readlines()
    returnStocks = list()
    all_files = os.listdir("data")

    # Check that stocks are in the directory
    for stock in stocks:
        search_text = stock.upper() + start + end + "\n"
        file_text = stock.upper() + "_data.csv"
        if search_text in lines and file_text in all_files:
            continue
        else:
            if search_text in lines and file_text not in all_files:
                print(stock + " data has been deleted, re-getting data.")
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
        raise ValueError("make_data_csv: incorrect parameters")

    #Check for previous runs 
    if not reset:
        stocks = check_for_data(stocks, start, end)
        if len(stocks) == 0 and reset == False:
            print("Data saved from previous runs, new csv('s) not needed.\nPlease check that old csv's have the correct time ranges.\n") 
            return

    # Get Data from API
    NY = 'America/New_York'
    start = pd.Timestamp(start, tz=NY).isoformat()
    end = pd.Timestamp(end, tz=NY).isoformat()

    try:
        data = api.get_barset(stocks, 'day', start=start, end=end).df
    except Exception as e:
        print("Alpaca API Error: Unable to get data for: ", stocks, "\n", e)
        return 

    # Save Data in CSV for later use
    stop_index = len(data.columns)
    if stop_index % 5 != 0:
        raise TypeError("API did not return expected number of columns")
    start_index = 0
    end_index = 5

    # Save Data    
    while (start_index < stop_index):
        stock_data = data[data.columns[start_index:end_index]]
        stock_name = stock_data.columns[0][0].upper()
        filename = "data\\" + stock_name + "_data.csv"
        stock_data.to_csv(filename)
        start_index += 5
        end_index += 5
        print("Saved file: " + filename)
    print("\nPlease ensure previous files in \\data has the correct time ranges.\nOtherwise, delete all files in \\data and run this program again.\n")

def get_data(stocks=["AAPL"]):
    '''Get data from the data directory for the stocks given.'''
    if not isinstance(stocks, list):
        raise TypeError("get_data must have an input of type list!")

    stock_dict = dict()
    for stock in stocks:
        stock = stock.upper()
        filename = "data\\" + stock + "_data.csv"
        
        # Check if data exsists 
        try:
            stock_data = pd.read_csv(filename).dropna()
        except:
            print("Unable to find data for: ", stock, " skipping for now.")
            continue

        columns = ["date", stock + "_open", stock + "_high", stock + "_low", stock + "_close", stock + "_volume"]
        stock_data.columns = columns
        stock_dict[stock.upper()] = stock_data
    
    return stock_dict


def run(stocks, start, end, reset=False):
    '''Psudo Main Class for running the File'''
    make_data_csv(stocks, start, end, reset=reset)
    stock_dict = get_data(stocks)
    

# Test Methods
run(stocks=["VYM", "GOOG", "T"], start="2020-10-01", end="2020-10-31")
run(stocks=["AAPL", "MSFT", "TSLA"], start="2020-10-01", end="2020-10-31")