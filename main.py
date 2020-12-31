import backtest


if __name__ == "__main__":
    testStock = ["AAPL"]
    newTest = backtest.backtest(testStock, start="2020-05-30", end="2020-12-30")
    newTest.algo_1(risk=0.05, profit=0.10, starting_capital=500, testing=False)
    print("\n\n" + newTest.get_summary())