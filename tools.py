# File of Finacial Instruments To Be Used
import pandas as pd


def get_MA(stock, data, n, method=None):
    '''Calculates the moving average for a stock
    
    Args: 
        stock (str): name of stock to be analyzed 
        data (Pandas.DataFrame): data frame object containing data for stock 
        n (int): number of days for which to calculate MA for 
        method (str): value by which to calculate MA for (ex: by closing price, daily low, etc)
    
    Returns:
        ma: a pands Series with the moving average of the stock 
    '''

    # Basic Error Checking
    if not isinstance(stock, str) or not stock:
        raise TypeError(stock, " must be a string!")
    if not isinstance(method, str) or not method:
        raise TypeError(method, " must be a string!")
    if not isinstance(data, pd.DataFrame) or data.empty:
        raise TypeError("data must be a Pandas.DataFrame!")
    if not isinstance(n, int) or not n > 0:
        raise TypeError("n must be a int")

    data = data.copy(deep=True)
    stock = stock.strip().upper()
    method = method.strip().lower() 
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
        data (Pandas.DataFrame): data frame object containing data for stock 
        n (list): list of days for which to calculate MACD for 
        method (str): value by which to calculate MACD for (ex: by closing price, daily low, etc)
    
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
        data (Pandas.DataFrame): data frame object containing data for stock 
        n (list): list of days for which to calculate MACD Signal Line for 
        method (str): value by which to calculate MACD Singal Line for (ex: by closing price, daily low, etc)
    
    Returns:
        macd: a pands Series for the MACD Signal line of the stock 
    '''

    macd = get_MACD(stock, data, n, method)
    macd_signal = macd.ewm(span=n[0], adjust=False).mean()
    return macd_signal

def get_SuperTrend(stock, data):
    '''Calculates the Supertrend tool for a stock
    
    Args:
        stock (str): name of stock for calculating the SuperTrend
        data (Pandas.DataFrame): dataframe of prices for SuperTrend Calculations

    Returns:
        data (Pandas.DataFrame): dataframe of prices, the SuperTrend and SuperTrend buy and sell signals 
    '''
    
    # Basic Error Checking 
    if not isinstance(stock, str) or not stock:
        raise TypeError("stock must be of type str")
    if not isinstance(data, pd.DataFrame) or data.empty:
        raise TypeError("data must be of type Pandas.DataFrame")

    data = data.copy(deep=True)
    old_columns = data.columns.tolist()
    old_columns.append("ST")
    old_columns.append( "ST_SIGNAL")

    data.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    data.reset_index(drop=True, inplace=True)
    for col in data.columns:
        if col == "Date":
            continue
        data[col] = data[col].apply(float)
    
    data['tr0'] = abs(data["High"] - data["Low"])
    data['tr1'] = abs(data["High"] - data["Close"].shift(1))
    data['tr2'] = abs(data["Low"]- data["Close"].shift(1))
    data["TR"] = round(data[['tr0', 'tr1', 'tr2']].max(axis=1),2)
    data["ATR"]=0.00
    data['BUB']=0.00
    data["BLB"]=0.00
    data["FUB"]=0.00
    data["FLB"]=0.00
    data["ST"]=0.00

    # Calculating ATR 
    for i, row in data.iterrows():
        if i == 0:
            data.loc[i,'ATR'] = 0.00#data['ATR'].iat[0]
        else:
            data.loc[i,'ATR'] = ((data.loc[i-1,'ATR'] * 13)+data.loc[i,'TR'])/14

    data['BUB'] = round(((data["High"] + data["Low"]) / 2) + (2 * data["ATR"]),2)
    data['BLB'] = round(((data["High"] + data["Low"]) / 2) - (2 * data["ATR"]),2)


    # FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
    #                     THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)


    for i, row in data.iterrows():
        if i==0:
            data.loc[i,"FUB"]=0.00
        else:
            if (data.loc[i,"BUB"]<data.loc[i-1,"FUB"])|(data.loc[i-1,"Close"]>data.loc[i-1,"FUB"]):
                data.loc[i,"FUB"]=data.loc[i,"BUB"]
            else:
                data.loc[i,"FUB"]=data.loc[i-1,"FUB"]

    # FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND)) 
    #                     THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)

    for i, row in data.iterrows():
        if i==0:
            data.loc[i,"FLB"]=0.00
        else:
            if (data.loc[i,"BLB"]>data.loc[i-1,"FLB"])|(data.loc[i-1,"Close"]<data.loc[i-1,"FLB"]):
                data.loc[i,"FLB"]=data.loc[i,"BLB"]
            else:
                data.loc[i,"FLB"]=data.loc[i-1,"FLB"]



    # SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
    #                 Current FINAL UPPERBAND
    #             ELSE
    #                 IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
    #                     Current FINAL LOWERBAND
    #                 ELSE
    #                     IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
    #                         Current FINAL LOWERBAND
    #                     ELSE
    #                         IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
    #                             Current FINAL UPPERBAND


    for i, row in data.iterrows():
        if i==0:
            data.loc[i,"ST"]=0.00
        elif (data.loc[i-1,"ST"]==data.loc[i-1,"FUB"]) & (data.loc[i,"Close"]<=data.loc[i,"FUB"]):
            data.loc[i,"ST"]=data.loc[i,"FUB"]
        elif (data.loc[i-1,"ST"]==data.loc[i-1,"FUB"])&(data.loc[i,"Close"]>data.loc[i,"FUB"]):
            data.loc[i,"ST"]=data.loc[i,"FLB"]
        elif (data.loc[i-1,"ST"]==data.loc[i-1,"FLB"])&(data.loc[i,"Close"]>=data.loc[i,"FLB"]):
            data.loc[i,"ST"]=data.loc[i,"FLB"]
        elif (data.loc[i-1,"ST"]==data.loc[i-1,"FLB"])&(data.loc[i,"Close"]<data.loc[i,"FLB"]):
            data.loc[i,"ST"]=data.loc[i,"FUB"]

    # Buy Sell Indicator
    for i, row in data.iterrows():
        if i==0:
            data["ST_BUY_SELL"]="NA"
        elif (data.loc[i,"ST"]<data.loc[i,"Close"]) :
            data.loc[i,"ST_BUY_SELL"]="BUY"
        else:
            data.loc[i,"ST_BUY_SELL"]="SELL"
   
    data = data[["Date", "Open", "High", "Low", "Close", "Volume", "ST", "ST_BUY_SELL"]] 
    data.columns = old_columns 
    return data
    
def get_ValueZone(stock, data, method="average", n=[9,50]):
    '''Calculates if the stock is within the value zone. The value zone is defined as the difference between 
       a short moving average and a long moving average.
       
       Args:
            stock (str): name of stock to be evaluated 
            data (pd.DataFrame): dataframe of stock data 
            method (str): value by which to calculate valueZone for (ex: by closing price, daily low, etc)
            n (list): list of length 2 of days to calculate valueZone by 

       Retruns:
            new_data (Pandas.DataFrame): dataframe containing upper and lower bounds of the Value Zone as well as 
                                         as Value Zone indicator
       '''
    # Basic Error Checking 
    if not isinstance(stock, str) or not stock:
        raise TypeError("stock must be of type str!")
    stock = stock.upper()
    if not isinstance(data, pd.DataFrame) or data.empty:
        raise TypeError("data must be of type Pandas.DataFrame!")
    if not isinstance(n, list) or len(n) != 2:
        raise TypeError("n must be a list of two elements!")
    if n[0] > n[1]:
        raise ValueError("n must in sorted ascending order!")

    method = method.strip().lower() 
    methods = ["high", "low", "close", "open", "average"]
    if method not in methods:
        raise ValueError("method must be in ", methods)
    
    # If avergae, create average data
    new_data = data.copy(deep=True)
    price_name = stock + "_" + method
    if method == "average":
        new_data[price_name] = (new_data[stock + "_high"].apply(float) + new_data[stock + "_low"].apply(float)) / 2.0

    # Create upper and lower boundary of stocks
    upper_boundary = get_MA(stock=stock, data=new_data, n=n[0], method=method)
    lower_boundary = get_MA(stock=stock, data=new_data, n=n[1], method=method)
    new_data["upper"] = upper_boundary
    new_data["lower"] = lower_boundary
    new_data["value_zone"] = "NA"
    
    # Iterate through and create zone designations for each observation
    for i, row in new_data.iterrows():
        if i == 0:
            new_data["value_zone"] = "0" 

        current_price = new_data.loc[i, price_name]
        upper = new_data.loc[i, "upper"]
        lower = new_data.loc[i, "lower"]
      
        if current_price > lower and current_price < upper:
            new_data.loc[i, "value_zone"] = 1
        elif current_price < lower and current_price < upper:
            new_data.loc[i, "value_zone"] = 2
        elif current_price > lower and current_price > upper:
            new_data.loc[i, "value_zone"] = 0
        else:
            new_data.loc[i, "value_zone"] = "0"
    
    new_data = new_data[["upper", "lower", "value_zone"]]
    return new_data

def get_ADX():
    return None

def get_LongImpulse():
    return None

def get_ShortImpulse():
    return None