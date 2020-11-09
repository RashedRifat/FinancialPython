# Testing the Alpaca API
import alpaca_trade_api as tradeapi
import pandas as pd 
import os 
import tools

# Set up API and check to see that it is working 
def set_API(ID=None, key=None, paperMode=True, ask=False):
    
    if ID == None or key == None:
        ask = True
    if ask:
        ID = str(input("Enter Alpaca Account ID: "))
        key = str(input("Enter Alpaca Account Key: "))

    url = ""
    if paperMode:
        url = 'https://paper-api.alpaca.markets'
    else:
        raise ConnectionRefusedError("Live mode not Enabled!")

    api = tradeapi.REST(ID, key, base_url=url) # or use ENV Vars shown below
    try:
        account = api.get_account()
    except Exception:
        raise ConnectionError("Unable to get account for keys.")
    
    return api


def check_for_data(stocks, start, end, timeframe):
    '''Checks if stock data is already in the data directory by using the runs.txt file.
    
    Args:
        stocks (list): list of stocks to check for
        start (str): string representation of the start date 
        end (str): string reprsentation of the end date
        timeframe (str): timeframe for which the data should be checked

    Returns:
        returnStocks (list): list of stocks for which data has not been found
    '''
    # Implement further validation here - check if the stock name is within the list of directories 
    # Check if the start and end dates match the dates within the file  
    # Create a clear function that removes all of the files within the data file and use it for reset=True

    if not isinstance(stocks, list):
        raise TypeError("stocks must be a list!")
    if not isinstance(start, str):
        raise TypeError("start must be a string formatted YYYY-MM-DD!")
    if not isinstance(end, str):
        raise TypeError("end must be a string formatted YYYY-MM-DD!")

    f = open("bin\\runs.txt", "a+")
    f.seek(0)
    lines = f.readlines()
    returnStocks = list()
    all_files = os.listdir("data")

    # Check that stocks are in the directory
    for stock in stocks:
        search_text = stock.upper() + start + end + timeframe + "\n"
        file_text = stock.upper() + "_" + timeframe + "_data.csv"
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


def make_data_csv(stocks, start, end, api=None, timeframe="day", reset=False):
    '''Find data for the specificed stocks and create csv's in the data directory
    
    Args:
        stocks (list): list of stocks to find data for 
        start (str): string representation of the start date 
        end (str): string reprsentation of the end date
        timeframe (str): timeframe for getting data; can be minute, 1Min, 5Min, 15Min, day or 1D
        reset (bool): if True, create new csv files regardless if data is already present 
                      if False, create csv files for only missing stocks 

    Returns:
        None
    '''
    if api == None:
        api = set_API(ask=True)
    else:
        pass
    timeframe_list = ["minute", "1Min", "5Min", "15Min", "day", "1D"]
    # Basic Error Checking
    if not isinstance(stocks, list):
        raise TypeError("stocks musbt be of type list with string values!")
    if len(stocks) == 0:
        raise ValueError("list of stocks musbt be greater than 0!")
    if not isinstance(start, str):
        raise TypeError("start must be a string formatted YYYY-MM-DD!")
    if not isinstance(end, str):
        raise TypeError("end must be a string formatted YYYY-MM-DD!")
    if not isinstance(timeframe, str):
        raise TypeError("timeframe must be of type str and be minute, 1Min, 5Min, 15Min, day or 1D")
    if timeframe not in timeframe_list:
        timeframe_str = ", ".join([elem for elem in timeframe_list])
        raise ValueError("timeframe must be of: " + timeframe_str + ", not " + timeframe)

    #Check for previous runs 
    if reset:
        all_files = os.listdir("data")
        for nfile in all_files:
            os.remove("data\\" + nfile)
        new_runs = open("bin\\runs.txt", "w+")
        for stock in stocks:
            search_text = stock.upper() + start + end + timeframe + "\n"
            new_runs.write(search_text)
        new_runs.close()

    else:
        stocks = check_for_data(stocks, start, end, timeframe)
        if len(stocks) == 0 and reset == False:
            print("Data saved from previous runs, new csv('s) not needed.\nPlease check that old csv's have the correct time ranges.\n") 
            return

    # Get Data from API
    NY = 'America/New_York'
    start = pd.Timestamp(start, tz=NY).isoformat()
    end = pd.Timestamp(end, tz=NY).isoformat()

    try:
        data = api.get_barset(stocks, timeframe, start=start, end=end).df
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
        filename = "data\\" + stock_name + "_" + timeframe + "_data.csv"
        stock_data.to_csv(filename)
        start_index += 5
        end_index += 5
        print("Saved file: " + filename)
    if not reset:
        print("\nPlease ensure previous files in \\data has the correct time ranges.\nOtherwise, delete all files in \\data and run this program again.\n")

def get_data(stocks, timeframe):
    '''Get data from the data directory for the stocks given.
    
    Args:
        stocks (list): list of stocks for which to get data for 
        timeframe (str): timeframe for stock data; can be minute, 1Min, 5Min, 15Min, day or 1D

    Returns:
        stock_dict (dict): dictonary of stocks and the associated data 
    '''

    if not isinstance(stocks, list):
        raise TypeError("get_data must have an input of type list!")
    if not isinstance(timeframe, str):
        raise TypeError("timeframe must be of type str and be minute, 1Min, 5Min, 15Min, day or 1D")
    timeframe_list = ["minute", "1Min", "5Min", "15Min", "day", "1D"]
    if timeframe not in timeframe_list:
        timeframe_str = ", ".join([elem for elem in timeframe_list])
        raise ValueError("timeframe must be of: " + timeframe_str + ", not " + timeframe)

    stock_dict = dict()
    for stock in stocks:
        stock = stock.upper()
        filename = "data\\" + stock + "_" + timeframe + "_data.csv"
        
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


def run(stocks, start, end, reset=False, timeframe="day"):
    '''Pesudo Main Class for testing programs'''

    make_data_csv(stocks, start, end, reset=reset, timeframe=timeframe)
    stock_dict = get_data(stocks, timeframe)
    GOOG_data = stock_dict["GOOG"]
    value_zone = tools.get_ValueZone(stock="GOOG", data=GOOG_data, method="average", n=[2,5])
    MACD = tools.get_MACD(stock="GOOG", data=GOOG_data, n=[1,2], method="average")
    supertrend = tools.get_SuperTrend(stock="GOOG", data=GOOG_data)
    print(GOOG_data.head())
    exit()
