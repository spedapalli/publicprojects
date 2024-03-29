import pandas as pd
import matplotlib.pyplot as plt
from statsmodels import stats
import numpy as np
from sklearn.linear_model import LinearRegression

from src.weatherdata import WeatherDataConstants as weatherConstants
from src.solarroof import SolarRoofConstants as solarConstants

def plotLinearRegressionLine(data: pd.DataFrame):
    # create arrays of data composing independent vars and dependent vars
    x = data[weatherConstants.PRECIPITATION].to_numpy()
    y = data[solarConstants.SOLAR_ENERGY_KWH].to_numpy()

    # scatter plot
    plt.plot(x, y, 'o')
    # get m(slope) and b(intercept) of linear regression line
    m, b = np.polyfit(x, y, 1)

    plt.plot(x, m*x+b)
    # plt.show()
    stats.pairplot()

def runRegression(data: pd.DataFrame):
    # create arrays of data composing independent vars and dependent vars
    x = data[[weatherConstants.TEMP_MIN, weatherConstants.TEMP_MAX, weatherConstants.PRECIPITATION]].to_numpy()
    y = data[solarConstants.SOLAR_ENERGY_KWH].to_numpy()
    print('x= ', x)
    print('y= ', y)

    # run regression
    model = LinearRegression().fit(x, y)

    # r square
    rsquare = model.score(x, y)
    print(f"Coefficient of determination aka (r**2)= {rsquare}")

    print(f"Intercept= {model.intercept_}")
    print(f"Coeffecients= {model.coef_}")

