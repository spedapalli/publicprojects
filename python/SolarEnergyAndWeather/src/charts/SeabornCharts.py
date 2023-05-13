import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def pairPlot(data: pd.DataFrame) :
    sns.set(style="ticks", color_codes=True)
    sns.pairplot(data=data, vars=['Solar Energy (kWh)', 'tavg', 'tmin', 'tmax'])
    plt.show()

