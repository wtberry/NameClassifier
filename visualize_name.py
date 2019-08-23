import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

names = pd.read_csv('data/last_names.csv')

#df = names.head(8000)

fig, ax = plt.subplots()
ax.bar(names.ranking, names.population, color='b', width=1.0)
ax2 = ax.twinx() # create new ax instance with separate y ticker on the other side
ax2.plot(names.cumpercentage, color='r')
ax2.yaxis.set_major_formatter(PercentFormatter())

ax.tick_params(axis='y', colors='b')
ax2.tick_params(axis='y', colors='r')

ax.set_xlabel("Ranking of Last Names in Japan")
ax.set_ylabel("Population")
ax2.set_ylabel("Cumulative Percentage")

plt.show()
