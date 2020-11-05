# MultipleLinearRegression
import numpy as np
import pandas as pd
import quandl
import matplotlib.pyplot as plt 
import statsmodels.formula.api as sm 
quandl.read_key()

# Get Prices 
aapl_table = quandl.get("WIKI/AAPL")
amzn_table = quandl.get("WIKI/AMZN")
msft_table = quandl.get("WIKI/MSFT")
wal_table = quandl.get("WIKI/WMT")
ebay_table = quandl.get("WIKI/EBAY")

# Get Closing Prices 
aapl = aapl_table.loc["2016", ["Close"]]
amzn = amzn_table.loc["2016", ["Close"]]
msft = msft_table.loc["2016", ["Close"]]
wal = wal_table.loc["2016", ["Close"]]
ebay = ebay_table.loc["2016", ["Close"]]


# Get Log Returns 
aapl_log = np.log(aapl.Close).diff().dropna()
amzn_log = np.log(amzn.Close).diff().dropna()
msft_log = np.log(msft.Close).diff().dropna()
wal_log = np.log(wal.Close).diff().dropna()
ebay_log = np.log(ebay.Close).diff().dropna()
df  = pd.concat([aapl_log, amzn_log, msft_log, wal_log, ebay_log], axis = 1).dropna()
df.columns = ["AAPL", "AMZN", "MSFT", "WMT", "EBAY"]
# print(df.tail())

# Create Stats Model 
model = sm.ols(formula="AAPL ~ AMZN + MSFT + WMT + EBAY", data=df).fit()
print(model.summary())
