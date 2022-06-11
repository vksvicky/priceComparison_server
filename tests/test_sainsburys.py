"""Tests for `pricecomparison` package."""

import pandas as pd
import requests
import pytest
import os
import re

from pathlib import Path

# Test file does not exists from requests import ConnectTimeout

from pricecomparison.utilities import retry_session

STORE_NAME = "Sainsburys"
absolutePath = Path().absolute()
doesAbsolutePathStartWith: bool = bool(re.findall("/home/runner/work/", str(absolutePath)))

@pytest.fixture(autouse=True)
def pytest_setup():
    file_name: str = "./pricewatch.xlsx"

    file_object: dict[str: str] = {
        "fileName": file_name,
        "realPath": os.path.realpath(file_name),
        "absolutePath": os.path.abspath(file_name)
    }
    yield file_object

@pytest.mark.skipif(doesAbsolutePathStartWith, reason="Cannot run in CI environment")
def test_file_does_not_exist(pytest_setup):
    file_name = "./pricewatch.xls"
    file_does_not_exist = os.path.exists(file_name)

    assert file_does_not_exist == False

#  Test if file exists
@pytest.mark.skipif(doesAbsolutePathStartWith, reason="Cannot run in CI environment")
def test_file_exists(pytest_setup):
    assert pytest_setup["absolutePath"]

# Test Count number of sheets
def test_number_of_sheets_in_file(pytest_setup):
    excel_file = pd.ExcelFile(pytest_setup['absolutePath'])
    number_of_sheets = len(excel_file.sheet_names)
    assert (number_of_sheets == 8)

# Test to check if a sheet names Sainsbury's exists
@pytest.mark.skipif(doesAbsolutePathStartWith, reason="Cannot run in CI environment")
def test_sheet_name_has_sheet_named_sainsburys(pytest_setup):
    excel_file = pd.ExcelFile(pytest_setup["absolutePath"])
    assert ("%s" % STORE_NAME) in excel_file.sheet_names

# Test to validate we have the right amount of columns in the provided Excel sheet
@pytest.mark.skipif(doesAbsolutePathStartWith, reason="Cannot run in CI environment")
def test_number_of_columns_in_excel_sheet(pytest_setup):
    excel_file = pd.ExcelFile(pytest_setup["absolutePath"])
    excel_sheet = excel_file.parse("%s" % STORE_NAME)
    number_of_rows_and_columns = excel_sheet.shape
    assert (number_of_rows_and_columns[1] == 3)

# Test to validate the number of column in an Excel sheet
@pytest.mark.skipif(doesAbsolutePathStartWith, reason="Cannot run in CI environment")
def test_validate_number_of_columns_in_excel_sheet(pytest_setup):
    excel_file = pd.ExcelFile(pytest_setup["absolutePath"])
    dataframe = excel_file.parse(STORE_NAME)
    col_names = list(dataframe.columns.values)
    assert (len(col_names) == 3)

# Test to validate the column names in an Excel sheet
def test_validate_column_names_in_an_excel_sheet(pytest_setup):
    excel_file = pd.ExcelFile(pytest_setup["absolutePath"])
    dataframe = excel_file.parse(STORE_NAME)
    col_names = list(dataframe.columns.values)
    columns_to_validate = ['Product Name', 'URL', 'Price']
    assert col_names == columns_to_validate

# Test to throw exception if sheet does not exist
# @pytest.mark.xfail
# def test_get_with_timeout():
#
#     raise ConnectTimeout("Unable to connect server")
#
#     with pytest.raises(ConnectTimeout) as _error:
#          # and now we inject the fake get method:
#          return requests.get(_URL).json()
#     assert _error.value == "Unable to connect server"

# def test_get_with_timeout():
#     _URL = "https://google.com"
#     try:
#         # ADD EXCEPTION HERE
#         raise requests.exceptions.HTTPError('Unable to connect server')
#         response = requests.get(_URL, verify=False, stream=True)
#         response.raise_for_status()
#     except (requests.exceptions.HTTPError,
#             requests.exceptions.ConnectionError,
#             requests.exceptions.Timeout) as err:
#         # err will now be 'Unable to connect server'
#         msg = f'Failure: {err}' # Here err is always empty
#         raise SystemExit(msg)
# # Test to throw exception if column does not exist

def test_request_a_url_with_infinite_timeout():
    response = requests.get('https://postman-echo.com/delay/10', timeout=None)
    assert response.status_code == 200

def test_request_a_url_with_a_very_short_timeout_and_fails():
    with pytest.raises(requests.exceptions.Timeout):
        requests.get('https://postman-echo.com/status/200', timeout=0.001)

def test_retry_session_a_successful_url_and_success():
    session = retry_session()
    response = session.get("https://postman-echo.com/status/200")
    assert response.status_code == 200

def test_retry_session_a_non_existing_url_n_times_and_fails(caplog):
    session = retry_session()
    with pytest.raises(requests.exceptions.ConnectionError):
        session.get("http://this-url-does-not-exist.throw_error")

    assert "Retry(total=0, " in caplog.records[2].message
    assert "Retry(total=1, " in caplog.records[1].message
    assert "Retry(total=2, " in caplog.records[0].message