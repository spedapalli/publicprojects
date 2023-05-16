import matplotlib.pyplot as plt
import pandas as pd

from src import CommonConstants as commonConstants
from src.solarroof import SolarRoofConstants as solarConstants
from src.weatherdata import WeatherDataConstants as weatherConstants

def plotTempAndKwh(data: pd.DataFrame):
    data.plot(x=solarConstants.DATE_TIME,
              y=[weatherConstants.TEMP_MAX, weatherConstants.TEMP_MIN, solarConstants.SOLAR_ENERGY_KWH])
    #data.plot(y=['tavg'])
    plt.show()

def plotPrecipitationAndKwn(data: pd.DataFrame):
    data.plot(x=solarConstants.DATE_TIME, y=[weatherConstants.PRECIPITATION, solarConstants.SOLAR_ENERGY_KWH])
    plt.show()

