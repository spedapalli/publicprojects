import pandas as pd
from meteostat import Point, Daily
from datetime import datetime

from src.weatherdata import WeatherDataConstants as weatherConstants
from src import CommonConstants as commonConstants

def getWeatherDataFor(latitude: float, longitude: float, altitude: int, fromDate: str, toDate: str):
    """This function calls a 3rd party API to retrieve weather data for the given parameters.
    NOTE that the returned Data Frame has "time" column as the index and it does not show up when you print
    columns. The default format is as a string 'yyyy-mm-dd' and when output may include the Timestamp with 0s
    as the value eg: '2023-01-26T00:00:00.000000000'. If you need only date, you may explicitly set the index using `df.index = df.index.date`.
    Ref : https://github.com/meteostat/meteostat-python/issues/97
    https://stackoverflow.com/questions/67243861/converting-datetime-formatted-index-to-date-only-python-pandas
    """
    # set start and end dates
    # startDt = datetime(2022, 2, 1)
    # endDt = datetime(2023, 1, 31)
    startDt = datetime.fromisoformat(fromDate)
    endDt = datetime.fromisoformat(toDate)

    #create point - San Ramon
    #sanRamon = Point(37.7819976, -121.963481, 17)
    geoPoint = Point(latitude, longitude, altitude)

    data = Daily(geoPoint, startDt, endDt)
    data.normalize()
    #data.coverage('time')

    data = data.fetch()
    # print(data.columns)
    weatherOutFilePath = commonConstants.DATA_ROOT_DIR + weatherConstants.WEATHER_DATA_OUTPUT_FILENAME
    data.to_csv(weatherOutFilePath, index=True, encoding=commonConstants.UTF_8)

    return data
    #print("Printing csv= ", data.to_csv())

def getMockWeatherData(filePath):
    return pd.read_csv(filePath)