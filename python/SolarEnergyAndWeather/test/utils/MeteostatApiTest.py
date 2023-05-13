
from datetime import datetime
from meteostat import Point, Hourly
import unittest

class PandaDataFrameTest(unittest.TestCase):
    latitude = 37.7819976
    longitude = -121.963481
    altitude = 17

    filePath = "data/"

    def test_GetHourlyData(self):
        startDt = datetime(2022, 9, 1)
        endDt = datetime(2023, 9, 30)

        # create point - San Ramon
        # sanRamon = Point(37.7819976, -121.963481, 17)
        geoPoint = Point(self.latitude, self.longitude, self.altitude)

        data = Hourly(geoPoint, startDt, endDt)
        data.normalize()
        # data.coverage('time')

        data = data.fetch()
        weatherOutFilePath = self.filePath + "/../" + "sanramon_weather_202209.csv"
        data.to_csv(weatherOutFilePath, index=True, encoding="utf-8-sig")

