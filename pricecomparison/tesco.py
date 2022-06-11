"""Code to retrieve and update Tesco product prices"""
import logging

from collections import OrderedDict
import urllib3
import pandas as _pandas

from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from tqdm import tqdm

from pricecomparison.utilities import FILENAME, update_excel, retry_session, setup_logging, SuperMarkets

urllib3.disable_warnings()
setup_logging(logging.DEBUG, "%s" % SuperMarkets.Tesco.lower())

priceWatchXLS = _pandas.ExcelFile(FILENAME)
sheetNamesList = [SuperMarkets.Tesco]

_headers = OrderedDict({
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': 'www.tesco.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
})

try:
    for eachSheet in sheetNamesList:
        priceWatchDataFrame = _pandas.read_excel(FILENAME, sheet_name=eachSheet, engine="openpyxl")

        numberOfRows = priceWatchDataFrame.shape[0]

        # Reading the URL for each row in the sheet
        try:
            for eachItem in tqdm(range(0, numberOfRows, 1), "Retrieving data..."):
                productURL = priceWatchDataFrame.loc[eachItem, 'URL']

                # If productURL does not exist, just move the next item in the loop
                if _pandas.isna(productURL):
                    continue

                session = retry_session()
                response = session.get(productURL, headers=_headers, verify=False).text

                soup = BeautifulSoup(response, 'html.parser')

                # Identifying the Div which contains the price
                productPriceDiv = soup.find("div", {"class": "price-control-wrapper"})

                # Using the identified div that contains the price, find the span with the price
                productPrice = productPriceDiv.find("span", {"class": "value"})

                # Update the cell in the sheet with the price
                priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice.text
        except HTTPError as http_err:
            logging.error("HTTP Error: %s", http_err)
        except Exception as err:
            logging.error("Other Error: %s", err)

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: %s", general_err)
