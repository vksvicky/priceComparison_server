"""Tests for `pricecomparison` package."""

import pandas as pd
import pytest
import os

# Test file does not exists
STORE_NAME = "Sainsburys"

@pytest.fixture(autouse=True)
def pytest_setup():
    file_name: str = "pricewatch.xlsx"

    file_object : dict[str : str] = {
        "fileName": file_name,
        "realPath": os.path.realpath(file_name),
        "absolutePath": os.path.abspath(file_name)
    }
    yield file_object

def test_file_does_not_exist(pytest_setup):
    file_name = "./pricewatch.xls"
    file_does_not_exist = os.path.exists(file_name)
    assert file_does_not_exist == False

#  Test if file exists
def test_file_exists(pytest_setup):
    assert pytest_setup["absolutePath"]

# Test Count number of sheets
def test_number_of_sheets_in_file(pytest_setup):
    excel_file = pd.ExcelFile(pytest_setup['absolutePath'])
    number_of_sheets = len(excel_file.sheet_names)
    assert (number_of_sheets == 8)

# Test to check if a sheet names Sainsburys exists
def test_sheet_name_has_sheet_named_sainsburys(pytest_setup):
    excel_file = pd.ExcelFile(pytest_setup["absolutePath"])
    assert ("%s" % STORE_NAME) in excel_file.sheet_names

# Test to validate we have the right amount of columns in the provided Excel sheet
def test_number_of_columns_in_excel_sheet(pytest_setup):
    excel_file = pd.ExcelFile(pytest_setup["absolutePath"])
    excel_sheet = excel_file.parse("%s" % STORE_NAME)
    number_of_rows_and_columns = excel_sheet.shape
    assert (number_of_rows_and_columns[1] == 3)

# Test to validate the column names in the Excel sheet

# Test to throw exception if sheet does not exist

# Test to throw exception if column does not exist
