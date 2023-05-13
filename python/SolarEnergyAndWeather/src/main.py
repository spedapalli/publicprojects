import os
import pandas as pd

from src.solarroof import SolarRoofConstants as solarConstants
from src import CommonConstants as commonConstants
from src.solarroof import CSVReader as cvsReader
from src.weatherdata import WeatherDataReader as weatherData
from src.charts import SeabornCharts as seabcharts

#NOTE: the dir path provided here is
#print('current working dir', os.getcwd())
csvDir = os.path.abspath(solarConstants.TESLA_SOLAR_DATA_DIR)

def trimTimestampFromDate(dateTime: str):
    return dateTime[:dateTime.index('T')]

def run(csvDir:str):
    """This method is the entry point to this module. It calls the underlying solarroof module to retrieve Solar Energey data stored in CSV files
    within the data folder; calls the Weather API to retrieve weather data from the starting date to End Date in the combined CSV data.
    
    Returns: DataFrame of CSV data composing the headers - Date time, Solar Energy (kWh), tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun."""

    # get DateTime and Kwh from csv files -
    # First column is DateTime, second is Kwh (Tesla data). Data is sorted in asc by Date
    kwhCsvDataFrame = cvsReader.getKwhForDateFromCsv(csvDir)
    kwhCsvDataFrame[solarConstants.DATE_TIME] = pd.to_datetime(kwhCsvDataFrame[solarConstants.DATE_TIME]).dt.date

    # print(kwhCsvDataFrame.index)

    # get the first start date of the data
    startDate = kwhCsvDataFrame.iloc[0, 0]
    endDate = kwhCsvDataFrame.iloc[-1, 0]
    # startDate = trimTimestampFromDate(startDateTime)
    # endDate = trimTimestampFromDate(endDateTime)
    print("Getting weather data from {0} date to {1} date".format(startDate, endDate))

    startDateStr = startDate.strftime("%Y-%m-%d")
    endDateStr = endDate.strftime("%Y-%m-%d")

    #get weather data - note by default the underlying API does not return the date and sorts data by date
    data = weatherData.getWeatherDataFor(
        commonConstants.LOCATION_LATITUDE,
        commonConstants.LOCATION_LONGITUDE,
        commonConstants.LOCATION_ALTITUDE, startDateStr, endDateStr)

    # If need to use static data to avoid API limits. @TODO: Replace with proper mock
    # data = weatherData.getMockWeatherData(filePath + "/../" + "sanramon_weather.csv");

    # Merge the 2 data sets
    kwhAndWeatherDataFrame = mergeWeatherAndKwhDataUsingRowNumAsIndex(kwhCsvDataFrame, data)
    return kwhAndWeatherDataFrame


def mergeWeatherAndKwhDataUsingDateAsIndex(kwhData: pd.DataFrame, weatherData: pd.DataFrame):
    """ Merges the Solar energy generated data and the weather data into one DataFrame. This function
    uses the Date that exists in both DataFrames as the index to merge the records from the 2 DataFrames
    Inputs : 
        kwhData : Solar Energy generated data sorted by date in ascending order. Please see the CSV files in data/tesla directory on the expected CSV format
        weatherData : Weather data sorted by date in ascending order

    Returns : DataFrame of the merged data - Date time, Solar Energy (kWh), tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun.
    """
    # make sure the index is the date column
    kwhData.set_index('Date time', inplace=True)

    # Make sure index is date column in Date format
    weatherData.index = weatherData.index.date

    #concat - https://pandas.pydata.org/docs/reference/api/pandas.concat.html
    # Ref: https://sparkbyexamples.com/pandas/pandas-concat-dataframes-explained/
    consolidatedCsv = pd.concat([kwhData, weatherData], axis=1, join='inner')

    consolidatedCsv.to_csv(commonConstants.DATA_ROOT_DIR + commonConstants.CONSOLIDATED_FILENAME)
    return consolidatedCsv

def mergeWeatherAndKwhDataUsingRowNumAsIndex(kwhData: pd.DataFrame, weatherData: pd.DataFrame):
    """ Merges the Solar energy generated data and the weather data into one DataFrame. This function
    uses the Row number as the index to merge the records from the 2 DataFrames
    Inputs :
        kwhData : Solar Energy generated data sorted by date in ascending order. Please see the CSV files in data/tesla directory on the expected CSV format
        weatherData : Weather data sorted by date in ascending order

    Returns : DataFrame of the merged data - Date time, Solar Energy (kWh), tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun.
    """
    #TODO : TRIM datetime stamp from kwhData. Also, with no call to reset, not sure where Date shows up for WeatherData.
    kwhData.reset_index(inplace=True, drop=True)

    weatherData.reset_index(inplace=True, drop=True)
    # print("weather data index, after reset= ", weatherData.index.values)

    # concat - https://pandas.pydata.org/docs/reference/api/pandas.concat.html
    # Ref: https://sparkbyexamples.com/pandas/pandas-concat-dataframes-explained/
    consolidatedCsv = pd.concat([kwhData, weatherData], axis=1, join='inner')

    consolidatedCsv.to_csv(commonConstants.DATA_ROOT_DIR + commonConstants.CONSOLIDATED_FILENAME)
    return consolidatedCsv

print(os.path.abspath(os.curdir))
print("Tesla data dir= ", commonConstants.DATA_ROOT_DIR + solarConstants.TESLA_SOLAR_DATA_DIR)
data = run(commonConstants.DATA_ROOT_DIR + solarConstants.TESLA_SOLAR_DATA_DIR)
# plotTempAndKwh(data)
# plotLinearRegressionLine(data)
# plotPrecipitationAndKwn() #Not working. Throws error on args to the method. Need to check on the method
seabcharts.pairPlot(data)
# runRegression(data)
