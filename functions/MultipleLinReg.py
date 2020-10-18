# Multiple Linear Regression
import numpy as np
import pandas as pd
import quandl
import matplotlib.pyplot as plt 
import statsmodels.formula.api as sm 
quandl.read_key()

# Get Prices From Quandl
def get_prices(symbols):
    if not isinstance(symbols, list) or len(symbols) < 3:
        raise TypeError("Symbols must be an array of at least length 3!")

    symbols = [x.strip().upper() for x in symbols]
    tables = dict()
    for sym in symbols:
        tables[sym] = quandl.get(str("WIKI/" + sym))
    
    return tables

# Get Returns 
def get_returns(tables, year):
    if not isinstance(year, str) or len(year) != 4 or int(year) > 2018 or int(year) < 1986:
        raise TypeError("Year must be of type str between 1986 and 2018!")
    tables_key = tables.keys()
    closing_prices = dict()
    log_returns = dict()
    log_returns_values = []

    # Get Closing Prices 
    for key in tables_key:
        closing_prices[key] = tables[key].loc[year, ["Close"]]

    # Get Log Returns 
    for key in tables_key:
        log_returns[key] = np.log(closing_prices[key].Close).diff().dropna()
        log_returns_values.append(log_returns[key])
    
    df = pd.concat(log_returns_values, axis=1).dropna()
    df.columns = tables_key

    return df

# Create Stats Model 
def make_model(dataframe):
    keys = dataframe.columns
    formulae = str(keys[0]) + " ~ " + str(keys[1])
    for index in range(2, len(keys)):
        formulae += " + " + str(keys[index]) 
    model = sm.ols(formula=formulae, data=dataframe).fit()
    return model

# Create a main function to test and prompt for user responses 
def main(symbols, year="2016"):
    table = get_prices(symbols)
    log_returns = get_returns(table, year=year)
    model = make_model(log_returns)
    print(model.summary())

# See use case with AAPL, MSFT and EBAY from year 2016 to 2018    
# main(["aapl", "msft", "ebay"])
