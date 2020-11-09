# Testing playground for new functions 
import pandas as pd
import tqdm 
import tools, utils 

# TO-DO:
# Create a backtesting file that predicts stock movements and takes position as required 
# For the purpose of this test, no shorts will be allowed  


class backtest():
    def __init__(self, stock, start, end):
        self.api = utils.set_API(ask=True)
        self.stock = stock
        self.start = start
        self.end = end

    def funcname(self, parameter_list):
        return None



backtest(0,0,0)