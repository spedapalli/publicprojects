import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from src.solarroof import SolarRoofConstants as solarConstants
from src.weatherdata import WeatherDataConstants as weatherConstants

def pairPlot(data: pd.DataFrame) :
    sns.set(style="ticks", color_codes=True)
    sns.pairplot(data=data,
                 vars=[solarConstants.SOLAR_ENERGY_KWH,
                       weatherConstants.TEMP_AVERAGE,
                       weatherConstants.TEMP_MIN,
                       weatherConstants.TEMP_MAX])
    plt.show()

