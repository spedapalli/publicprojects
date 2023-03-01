import unittest
import src.main as main
import pandas as pd

# https://docs.python.org/3/library/unittest.html

class MainTest(unittest.TestCase):

    def mergeWeatherAndKwhData(self):
        filePath = "../data/tesla"

        # to test pd.concat and dropping of index
        # df1 = pd.DataFrame([['a', 1], ['b', 2]], columns=['letter', 'number'])
        # df4 = pd.DataFrame([['bird', 'polly'], ['monkey', 'george']], columns=['animal', 'name'])
        df1 = pd.read_csv(filePath + "/../sanramon_weather.csv")
        df4 = pd.read_csv(filePath + "/../solar_consolidated.csv")
        print(df1)
        print(df4)
        data = main.mergeWeatherAndKwhData(df1, df4)


if __name__ == '__main__':
    unittest.main