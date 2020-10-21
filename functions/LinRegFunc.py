# Linear Regression Function
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import quandl 
import statsmodels.formula.api as sm
from scipy import stats
quandl.read_key()

# Get data for tickers 
def get_data(tickers, year="2016"):
    if not isinstance(tickers, list) or len(tickers) != 2:
        raise ValueError("Should be a list of two tickers.")
    if not isinstance(year, str) or int(year) < 2010 or int(year) > 2018:
        raise ValueError("Year should be a string between [2010,2018]")

    value_table = dict()
    for symbol in tickers:
        if not isinstance(symbol, str):
            raise ValueError("Tickers Must be Strings!")
        try:
            temp = quandl.get(str("WIKI/" + symbol.upper()))
            temp = temp.loc[year:"2018-1", ["Close"]]
            value_table[symbol] = temp
        except:
            raise ValueError(symbol + " not in Quandl WIKI dataset.")
    
    return value_table


# Get log returns 
def get_returns(value_table, deviation=3):
    keys = value_table.keys()
    values = []
    for key in keys:
        temp = np.log(value_table[key].Close).diff().dropna()
        temp_Zscore = np.abs(stats.zscore(temp))
        temp = temp[(temp_Zscore < deviation)]
        values.append(temp)
    
    df = pd.concat(values, axis=1).dropna()
    df.columns = keys
    return df

# Create and return a OLS model
def make_model(dataframe):
    tickers = dataframe.columns
    formulae = str(tickers[0] + "~" + tickers[1])
    model = sm.ols(formula=formulae, data=dataframe).fit()
    return model

# Return a visulization 
def make_scatterplot(dataframe, figsize=(15,20)):
    model = make_model(dataframe)
    plt.figure(0, figsize=figsize)
    plt.scatter(dataframe[dataframe.columns[0]], dataframe[dataframe.columns[1]])
    plt.xlabel(str(dataframe.columns[0] + " Returns"))
    plt.ylabel(str(dataframe.columns[1] + " Returns"))
    plt.title("Return Association Graph")
    #plt.plot(dataframe[dataframe.columns[0]], model.predict(), color="red")
    plt.show()  


# Main Class for testing 
def main():
    tickers = ["AAPL", "MSFT"]
    value_dict = get_data(tickers)
    dataframe = get_returns(value_dict)
    model = make_model(dataframe)
    print(model.summary())
    make_scatterplot(dataframe)

main()