import quandl
import pandas as pd
quandl.ApiConfig.api_key  = ""


# Get Data for adjusted close in 2017
aapl_table = quandl.get("WIKI/AAPL")
aapl = aapl_table['Adj. Close']['2017']

# Resample and aggregrate into monthly data and weekly data 
by_month = aapl.resample('M').mean()
by_week = aapl.resample("W").mean()

# Use the format 'nf'
three_day = aapl.resample('3D').mean()
two_week = aapl.resample("2W").mean()
two_months = aapl.resample("2M").mean()

# Use other methods using the resampler 
std = aapl.resample("W").std()
max_price = aapl.resample("W").max()
min_price = aapl.resample("W").min()

# Get the last day of the month using lambda 
last_day = aapl.resample("M").agg(lambda x: x[-1])
monthly_return = aapl.resample('M').agg(lambda x: x[-1]/x[1] - 1)

# Combine with previous methods for easy stats 
mean_return = monthly_return.mean()
std_return = monthly_return.std()
max_return = monthly_return.max()
print(max_return)

# Use .diff() and .pct() change 
# The former calculates the difference between consecutive elements.
# The latter calculates the percentage change.
diff = last_day.diff()
pct_change = last_day.pct_change()

# Remove null values by using .dropna() or fill them using .fillna()
# More options such as backword and forward fill using .bfill and .ffill
pct_change.fillna(method = 'ffill')
pct_change.fillna(method = 'bfill')
pct_change.dropna()

