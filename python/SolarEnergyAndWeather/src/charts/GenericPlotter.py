import matplotlib.pyplot as plt
import pandas as pd


def plotTempAndKwh(data: pd.DataFrame):
    data.plot(x='Date time', y=['tmax', 'tmin', 'Solar Energy (kWh)'])
    #data.plot(y=['tavg'])
    plt.show()

def plotPrecipitationAndKwn(data: pd.DataFrame):
    data.plot(x='Date time', y=['prcp', 'Solar Energy (kWh)'])
    plt.show()

