import csv
import os
import glob

import pandas as pd


def getCsvFiles(filePath: str) :
    #csvFileList = glob.glob(filePath+'*.{}'.format('.csv'))
    csvFileList = os.listdir(filePath)
    print("No of files found=== ", len(csvFileList))

    return csvFileList

def mergeCsvFiles(csvFileDirPath: str, csvFileList: str):
    consolidatedCsv = pd.concat(
        [pd.read_csv(csvFileDirPath + "/" + file) for file in csvFileList])

    # for file in csvFileList :
    #     print("File in current process= ", file)
    #     consolidatedCsv = consolidatedCsv.append(file, ignore_index=True)
    return consolidatedCsv

def getPowerGeneratedForDate(consolidatedCsv: pd.DataFrame) :
    # get the datetime and Kwh columns only
    # columns = consolidatedCsv.iloc[:, lambda consolidatedCsv: [0, 2]]
    columns = consolidatedCsv.iloc[:,[0, 2]]
    # print("Columns: \n", columns)
    return columns


def getKwhForDateFromCsv(csvFileDirPath: str):
    """Given a directory containing list of CSV files, this function merges the CSV and returns a pd.DataFrame composing DateTime and Kwh energy generated.
    Input : Absolute path to the directory containing CVS files. PLEASE see the CSV files in data/tesla dir to see the format expected.
    Output : DataFrame containing DateTime and Kwh """
    
    csvFileList = getCsvFiles(csvFileDirPath)
    # Merge all CSV files and get DataFrame object
    consolidatedCsv = mergeCsvFiles(csvFileDirPath, csvFileList)
    consolidatedCsv.sort_values(["Date time"], axis=0, inplace=True)
    outputFilePath = csvFileDirPath + "/../" + "solar_consolidated.csv"
    consolidatedCsv.to_csv(outputFilePath, index=False, encoding="utf-8-sig")
    return getPowerGeneratedForDate(consolidatedCsv)
