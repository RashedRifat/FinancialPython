import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from scipy.stats import norm
import quandl

quandl.ApiConfig.api_key = ""

# Rolling Dice simulation 
def dice():
    return random.choice(range(1,7))
series = np.array([dice() for x in range(10000)])

# Create a histogram
plt.figure(figsize=(20,10))
plt.hist(series, bins=11, align="mid")
plt.xlabel("Dice Number")
plt.ylabel("Occurences ")
plt.grid()
# plt.show()

# Print the percentage of occurences less than three 
print(len([x for x in series if x <=3])/float(len(series)))
print(np.mean(series))

# Simulate a binomial distribution 
def trial():
    anum = random.choice(range(1,11))
    if anum <= 7:
        return 1
    else:
        return 0

# Simulate the possiblity 10 times 
results = [trial() for x in range(10)]

# For an approximation reaching the bionomial distribution, we need many trials 
# Here, simulate the possibility of succedding number times out of 10 trials 
def bionomial(number):
    l = []
    for i in range(10000):
        results = [trial() for x in range(10)]
        l.append(sum(results))
    return len([x for x in l if x == number])/float(len(l))

prob = []
for i in range(1,11):
    prob.append(bionomial(i))
prob_s = pd.Series(prob, index=range(1,11))
# print(prob_s)

# Print out a chart of the results of the binomial distribution 
plt.figure(figsize=(20,10))
plt.bar(range(1,11), prob)
plt.grid()
# plt.show()

# Get the logarithimic daily return of the SP500, and see the time-series data 
spy_table = quandl.get("BCIW/_SPXT")
spy = spy_table.loc["2015":"2020", ["Open", "Close"]]
spy["log_return"] = np.log(spy.Close).diff()
spy = spy.dropna()

spy_plot = plt.figure()
spy_plot.log_return.plot()
spy_plot.show()

