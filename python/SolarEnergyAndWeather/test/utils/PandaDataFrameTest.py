import datetime
import glob
import unittest
import pandas as pd
from src.solarroof import CSVReader as csvReader

class PandaDataFrameTest(unittest.TestCase):
    def tes_DataFrameColumnFormat(self):
        # filePath = "../../data/tesla"
        filePath = "data/"
        # kwhDateFrame = csvReader.getKwhForDateFromCsv(filePath)
        #
        # timeCharIndex = (kwhDateFrame.iloc[1]['Date time']).find('T')
        # kwhDateFrame['Date time'] = pd.to_datetime(kwhDateFrame['Date time']).dt.date
        # print(kwhDateFrame)

    def test_ReadCsvDataFrameColumnFormat(self):
        # -- read individual file and merge
        filePath = "../../data/tesla"
        csv_files = glob.glob('{}/*.{}'.format(filePath, 'csv'))
        print(csv_files)

        dfAllCsvData = pd.DataFrame()

        for file in csv_files:
           csvData = pd.read_csv(file)
           csvData['Date time'] = pd.to_datetime(csvData['Date time']).dt.date
           dfAllCsvData = dfAllCsvData.append(csvData, ignore_index=True)

        print(dfAllCsvData)



