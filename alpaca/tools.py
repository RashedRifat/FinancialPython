# File of Finacial Instruments To Be Used
import pandas as pd

'''
Conidtions

Long Impulse: [0, Decreasing], [1, Stable], [2, Increasing]
Short Impulse: [0, Decreasing], [,1 Stable], [2, Increasing]
Value Zone: [0, Above], [1, Below], [2, At]
MACD: [0, Decreasing], [1, Stable], [2, Increasing]
ADX Spread: [0, Increasing], [1, Stable], [2, Decreasing]

'''

def get_MA(stock, data, n, method=None):
    '''Calculates the MACD for a stock'''

    # Basic Error Checking
    method = method.strip().lower() 
    stock = stock.strip().upper()
    methods = ["high", "low", "close", "open", "average"]
    if not isinstance(data, pd.DataFrame):
        raise ValueError("data must be a dataframe!")
    if method not in methods or method == False:
        raise ValueError("method must be in ", methods)
    
    # If avergae, create avergae data
    price_name = stock + "_" + method
    if method == "average":
        data[price_name] = (data[stock + "_high"].apply(float) + data[stock + "_low"].apply(float)) / 2.0

    # Check for correct stock data 
    if price_name not in data.columns:
        raise AttributeError("data does not contain " + method + " data")

    prices = data[price_name]
    to_return = prices.ewm(span=n, adjust=False).mean()
    return to_return

def get_MACD(stock, data, n=[12, 26], method=None):
    if not isinstance(n, list) or len(n) != 2:
        raise TypeError("n must be a list of two days (spans)")
    
    macd_1 = get_MA(stock, data, n[0], method)
    macd_2 = get_MA(stock, data, n[1], method)
    return macd_1 - macd_2

def get_MACD_Signal(stock, data, n=[12, 26], method=None):
    macd = get_MACD(stock, data, n, method)
    return macd.ewm(span=n[0], adjust=False).mean()