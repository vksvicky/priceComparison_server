"""Tests for `pricecomparison` package."""

import pandas as pd
import pytest
import os

# Test file does not exists
STORE_NAME = "Sainsburys"

@pytest.fixture(autouse=True)
def setUp():
    _fileName: str = "pricewatch.xlsx"

    fileObject: dict[str : str] = {
        "fileName": _fileName,
        "realPath": os.path.realpath(_fileName),
        "absolutePath": os.path.abspath(_fileName)
    }
    yield fileObject

def test_fileDoesNotExist(setUp):
    fileName = "./pricewatch.xls"
    fileDoesNotExist = os.path.exists(fileName)
    assert fileDoesNotExist == False

#  Test if file exists
def test_fileExists(setUp):
    assert setUp["absolutePath"]

# Test Count number of sheets
def test_NumberOfSheetsInFile(setUp):
    _excel = pd.ExcelFile(setUp['absolutePath'])
    numberOfSheets = len(_excel.sheet_names)
    assert (numberOfSheets == 8)

# Test to check if a sheet names Sainsburys exists
def test_SheetNameHasSainsburys(setUp):
    _excel = pd.ExcelFile(setUp["absolutePath"])
    assert ("%s" % STORE_NAME) in _excel.sheet_names

# Test to validate we have the right amount of columns in the provided Excel sheet
def test_NumberOfColumnsInExcelSheet(setUp):
    _excel = pd.ExcelFile(setUp["absolutePath"])
    _excelSheet = _excel.parse("%s" % STORE_NAME)
    numberOfRowsAndColumns = _excelSheet.shape
    assert (numberOfRowsAndColumns[1] == 3)

# Test to validate the column names in the Excel sheet

# Test to throw exception if sheet does not exist

# Test to throw exception if column does not exist
