"""Tests for `pricecomparison` package."""

import pandas as pd
import pytest
import os

# Test file does not exists
STORE_NAME = "Sainsburys"
fileName = ""
realPath = ""

# @pytest.fixture(autouse=True)
# def setUp():
#     fileName = "./pricewatch.xls"
#     realPath = os.path.realpath(fileName)
#     yield
#     fileName = ""
#     realPath = ""

# class Tests(object):
def test_fileDoesNotExist():
    fileDoesNotExist = os.path.exists(fileName)
    assert fileDoesNotExist == False

#  Test if file exists
def test_fileExists():
    fileName = "./tests/pricewatch.xlsx"
    realPath = os.path.realpath(fileName)
    assert realPath

# Test Count number of sheets
def test_NumberOfSheetsInFile():
    fileName = "./pricewatch.xlsx"
    realPath = os.path.realpath(fileName)
    # numberOfSheets = len(pd.read_excel(r"./tests/pricewatch.xls", sheet_name=None))
    _excel = pd.ExcelFile(realPath)
    numberOfSheets = len(_excel.sheet_names)
    assert (numberOfSheets == 8)

# Test to check if a sheet names Sainsburys exists
def test_SheetNameHasSainsburys():
    fileName = "./pricewatch.xlsx"
    realPath = os.path.realpath(fileName)
    _excel = pd.ExcelFile(realPath)
    assert ("%s" % STORE_NAME) in _excel.sheet_names

# Test to validate we have the right amount of columns in the provided Excel sheet
def test_NumberOfColumnsInExcelSheet():
    fileName = "./pricewatch.xlsx"
    realPath = os.path.realpath(fileName)
    _excel = pd.ExcelFile(realPath)
    _excelSheet = _excel.parse("%s" % STORE_NAME)
    numberOfRowsAndColumns = _excelSheet.shape
    assert (numberOfRowsAndColumns[1] == 3)

# Test to validate the column names in the Excel sheet

# Test to throw exception if sheet does not exist

# Test to throw exception if column does not exist

