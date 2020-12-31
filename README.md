# FinancialPython
FinancialPython uses the Alpaca Trading API to save market data and backtest recent stock patterns based on a custom trading algorithim. While FinacialPython could be adapted into an algorthimic trading function, it's purpose is to aid clients in performing analysis using their own strategies based on technical analysis. FinancialPython allows for efficent scaling of simple to complex trading rules to many stocks. Decisons can then be made on the results of these tradinf rules. This is not meant as a replacement for traditional stock picking and should not be regarded as a sole alternative method of a analysis. 

Custom indicators have been built to aid in analysis, including commonly found indicators such as the moving average and MACD indicators. FinancialPython is highly flexible and allows for granular control of timeframes and methods by which indicators are calculated. 

## Using the program
As an example of using the program, please refer to the main.py file. 
To begin, we create an array of stocks to test an algorithim. We then create a backtest obejct, with our array of stocks as well as range of times on which the algorithim should perform. We then execute an algorithim (a simple algorithim based on the SuperTrend has been provided as an example). To see the results of the algorithim, we can call get_summary or take a look at the log files generated in the results or summary folders, which provide different levels of information for each individual placed trade. 

Note that all portions of this library are highly customizable. You are free to create your own algorithim and test it with the tools provided. Sufficent explantions of input parameters and output variables are included with every function, which you can peruse through the files located within this repo. If you have any questions, please reach out to me or open an issue. 

## Disclaimer 
This program or the author is not responsible for any investment failure or loss due to the use of this program. The program is provided as is, without any other warranty or support. 
