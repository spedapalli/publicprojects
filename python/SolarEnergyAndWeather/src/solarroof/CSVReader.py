import csv
import os
import glob
import deprecation
import pandas as pd
import src.CommonConstants as commonConstants
import src.solarroof.SolarRoofConstants as solarConstants

@deprecation.deprecated(details=
        """by reading files using getCsvFilesList and merging below, using one command, if any of the columns",
        need to be formatted, we run into challenges if list of rows is greater than 240 or so. Hence, this 
        function is not being used.""")
def getCsvFilesList(filePath: str) :
    """Returns all the files in the given Directory as parameter to this method.
    NOTE: This reads all files, not just CSV. If you have a dot (.) file in the directory even that will be read."""
    #csvFileList = glob.glob(filePath+'*.{}'.format('.csv'))
    csvFileList = os.listdir(filePath)
    print("No of files found=== ", len(csvFileList))

    return csvFileList

def getCsvDataFromFiles(fileDirPath: str):
    """Lists only CSV files. Formats the DateTime to Date and returns all the data from all the CSV files in
    the given Directory parameter to this function."""
    csv_files = glob.glob('{}/*.{}'.format(fileDirPath, 'csv'))

    # append
    appendedCsv = []
    dfAllCsvData = pd.DataFrame()

    for file in csv_files:
        csvData = pd.read_csv(file)
        csvData[solarConstants.DATE_TIME] = pd.to_datetime(csvData[solarConstants.DATE_TIME]).dt.date
        appendedCsv.append(csvData)

    dfAllCsvData = pd.concat(appendedCsv, ignore_index=True)
    return dfAllCsvData


@deprecation.deprecated(details="By doing one merge, operating aka formatting columns makes it challenging if rows are more than 240 or so")
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
    
    consolidatedCsv = getCsvDataFromFiles(csvFileDirPath)
    # Merge all CSV files and get DataFrame object
    #consolidatedCsv = mergeCsvFiles(csvFileDirPath, csvFileList)
    consolidatedCsv.sort_values([solarConstants.DATE_TIME], axis=0, inplace=True)
    outputFilePath = csvFileDirPath + "/../" + solarConstants.SOLAR_CONSOLIDATED_FILE
    consolidatedCsv.to_csv(outputFilePath, index=False, encoding=commonConstants.UTF_8)
    return getPowerGeneratedForDate(consolidatedCsv)
