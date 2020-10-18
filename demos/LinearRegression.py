#Confidence Intervals
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import quandl 
import statsmodels.formula.api as sm
from scipy import stats
quandl.read_key()

# Get Data
aapl_table = quandl.get("WIKI/AAPL")
msft_table = quandl.get("WIKI/MSFT")


# Slice Data
aapl = aapl_table.loc["2010":"2018-1", ["Close"]]
msft = msft_table.loc["2010":"2018-1", ["Close"]]


# Calculate Log Returns (and remove outliers for this demonstration)
aapl_log = np.log(aapl.Close).diff().dropna()
msft_log = np.log(msft.Close).diff().dropna() 
aapl_ZScore = np.abs(stats.zscore(aapl_log))
msft_ZScore = np.abs(stats.zscore(msft_log))
aapl_log = aapl_log[(aapl_ZScore < 3)]
msft_log = msft_log[(msft_ZScore < 3)]


# Concateneate into one table 
df = pd.concat([aapl_log, msft_log], axis=1).dropna()
df.columns = ["AAPL","MSFT"]
# print(df.head())


# Create a new plot
plt.figure(figsize=(15,10))
plt.scatter(df.AAPL, df.MSFT)
# plt.show()


# Create a Model
model = sm.ols(formula="AAPL~MSFT", data = df).fit()
print(model.summary())


# Show the fitted model
plt.figure(figsize=(15,10))
plt.scatter(df.AAPL, df.MSFT)
plt.xlabel("AAPL Return")
plt.ylabel("MSFT Return")
plt.plot(df.AAPL, model.predict(), color="red")
plt.show() 
