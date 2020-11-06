# Testing playground for new functions 
import pandas as pd
from utils import get_data
from tools import get_SuperTrend
import tools


#print(get_SuperTrend(stock, data))
stock = "GOOG"
data = get_data(stocks=["GOOG"], timeframe="day")["GOOG"]
print(tools.get_impulse(stock="GOOG", data=data, n=9, method="average"))