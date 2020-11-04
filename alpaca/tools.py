# File of Finacial Instruments To Be Used
import pandas as pd


def get_MA(stock, data, n, method=None):
    '''Calculates the moving average for a stock
    
    Args: 
        stock (str): name of stock to be analyzed 
        data (Pandas Dataframe): data frame object containing data for stock 
        n (int): number of days for which to calculate MA for 
        method (string): value by which to calculate MA for (ex: by closing price, daily low, etc)
    
    Returns:
        ma: a pands Series with the moving average of the stock 
    '''

    # Basic Error Checking
    if not isinstance(stock, str):
        raise TypeError(stock, " must be a string!")
    if not isinstance(method, str):
        raise TypeError(method, " must be a string!")
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a dataframe!")
    if not isinstance(n, int):
        raise TypeError("n must be a int")

    method = method.strip().lower() 
    stock = stock.strip().upper()
    methods = ["high", "low", "close", "open", "average"]
    if method not in methods:
        raise ValueError("method must be in ", methods)
    
    # If avergae, create avergae data
    price_name = stock + "_" + method
    if method == "average":
        data[price_name] = (data[stock + "_high"].apply(float) + data[stock + "_low"].apply(float)) / 2.0

    # Check for correct stock data 
    if price_name not in data.columns:
        raise AttributeError("data does not contain " + method + " data")

    prices = data[price_name]
    ma = prices.ewm(span=n, adjust=False).mean()
    return ma

def get_MACD(stock, data, n=[12, 26], method=None):
    '''Calculates the MACD for a stock
    
    Args: 
        stock (str): name of stock to be analyzed 
        data (Pandas Dataframe): data frame object containing data for stock 
        n (list): list of days for which to calculate MACD for 
        method (string): value by which to calculate MACD for (ex: by closing price, daily low, etc)
    
    Returns:
        macd: a pands Series for the MACD of the stock 
    '''

    if not isinstance(n, list) or len(n) != 2:
        raise TypeError("n must be a list of two days (spans)")
    
    macd_1 = get_MA(stock, data, n[0], method)
    macd_2 = get_MA(stock, data, n[1], method)
    macd = macd_1 - macd_2
    return macd

def get_MACD_Signal(stock, data, n=[12, 26], method=None):
    '''Calculates the MACD Signal line from a stock
    
    Args: 
        stock (str): name of stock to be analyzed 
        data (Pandas Dataframe): data frame object containing data for stock 
        n (list): list of days for which to calculate MACD Signal Line for 
        method (string): value by which to calculate MACD Singal Line for (ex: by closing price, daily low, etc)
    
    Returns:
        macd: a pands Series for the MACD Signal line of the stock 
    '''

    macd = get_MACD(stock, data, n, method)
    macd_signal = macd.ewm(span=n[0], adjust=False).mean()
    return macd_signal

def get_SuperTrend(stock, data):
    '''Calculates the Supertrend tool for a stock'''
    
    
    
    return None 

def get_ValueZone():
    return None

def get_ADX():
    return None

def get_LongImpulse():
    return None

def get_ShortImpulse():
    return None