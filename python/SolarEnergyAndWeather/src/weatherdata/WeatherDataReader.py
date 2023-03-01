import pandas as pd
from meteostat import Point, Daily
from datetime import datetime


def getWeatherDataFor(latitude: float, longitude: float, altitude: int, fromDate: str, toDate: str):

    # set start and end dates
    # startDt = datetime(2022, 2, 1)
    # endDt = datetime(2023, 1, 31)
    startDt = datetime.fromisoformat(fromDate)
    endDt = datetime.fromisoformat(toDate)

    #create point - San Ramon
    #sanRamon = Point(37.7819976, -121.963481, 17)
    geoPoint = Point(latitude, longitude, altitude)

    data = Daily(geoPoint, startDt, endDt)
    data = data.fetch()
    return data
    #print("Printing csv= ", data.to_csv())

def getMockWeatherData(filePath):
    return pd.read_csv(filePath)