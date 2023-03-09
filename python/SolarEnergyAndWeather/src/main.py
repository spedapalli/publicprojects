from solarroof import CSVReader as cvsReader
from weatherdata import WeatherDataReader as weatherData
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

#NOTE: the dir path provided here is
#print('current working dir', os.getcwd())
filePath = "../data/tesla"
csvDir = os.path.abspath(filePath)
latitude = 37.7819976
longitude = -121.963481
altitude = 17

def trimTimestampFromDate(dateTime: str):
    return dateTime[:dateTime.index('T')]

def run():
    """This method is the entry point to this module. It calls the underlying solarroof module to retrieve Solar Energey data stored in CSV files
    within the data folder; calls the Weather API to retrieve weather data from the starting date to End Date in the combined CSV data.
    
    Returns: DataFrame of CSV data composing the headers - Date time, Solar Energy (kWh), tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun."""

    # get DateTime and Kwh from csv files -
    # First column is DateTime, second is Kwh (Tesla data). Data is sorted in asc by Date
    kwhCsvDataFrame = cvsReader.getKwhForDateFromCsv(csvDir)

    # get the first start date of the data
    startDateTime = kwhCsvDataFrame.iloc[0, 0]
    endDateTime = kwhCsvDataFrame.iloc[-1, 0]
    startDate = trimTimestampFromDate(startDateTime)
    endDate = trimTimestampFromDate(endDateTime)
    print("Getting weather data from {0} date to {1} date".format(startDate, endDate))

    #get weather data - note by default the underlying API does not return the date and sorts data by date
    data = weatherData.getWeatherDataFor(latitude, longitude, altitude, startDate, endDate)
    #weatherOutFilePath = filePath + "/../" + "sanramon_weather.csv"
    #data.to_csv(weatherOutFilePath, index=False, encoding="utf-8-sig")

    # If need to use static data to avoid API limits. @TODO: Replace with proper mock
    data = weatherData.getMockWeatherData(filePath + "/../" + "sanramon_weather.csv");

    # Merge the 2 data sets
    kwhAndWeatherDataFrame = mergeWeatherAndKwhData(kwhCsvDataFrame, data)
    return kwhAndWeatherDataFrame


def mergeWeatherAndKwhData(kwhData: pd.DataFrame, weatherData: pd.DataFrame):
    """ Merges the Solar energy generated data and the weather data into one DataFrame.
    Inputs : 
        kwhData : Solar Energy generated data sorted by date in ascending order. Please see the CSV files in data/tesla directory on the expected CSV format
        weatherData : Weather data sorted by date in ascending order


    Returns : DataFrame of the merged data - Date time, Solar Energy (kWh), tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun.
    """
    weatherData.reset_index()
    print(kwhData)
    print(weatherData)
    # index needs to be reset. 
    # for future ref: https://stackoverflow.com/questions/35084071/concat-dataframe-reindexing-only-valid-with-uniquely-valued-index-objects
    kwhData.reset_index(inplace=True, drop=True)
    #concat - https://pandas.pydata.org/docs/reference/api/pandas.concat.html
    consolidatedCsv = pd.concat([kwhData, weatherData], axis=1)

    consolidatedCsv.to_csv(filePath + "/../consolidated/SolarKwhWithWeather.csv")
    return consolidatedCsv


def plotTempAndKwh(data: pd.DataFrame):
    data.plot(x='Date time', y=['tmax', 'tmin', 'Solar Energy (kWh)'])
    #data.plot(y=['tavg'])
    plt.show()

def plotPrecipitationAndKwn(data: pd.DataFrame):
    data.plot(x='Date time', y=['prcp', 'Solar Energy (kWh)'])
    plt.show()

def runRegression(data: pd.DataFrame):
    x = data[['tmin', 'tmax', 'prcp']].to_numpy()
    y = data['Solar Energy (kWh)'].to_numpy()
    print('x= ', x)
    print('y= ', y)

data = run()
plotTempAndKwh(data)
# runRegression(data)



