"""Code to retrieve and update Ocado and 'Marks & Spencers' product prices"""
import logging
import pandas as _pandas

from tqdm import tqdm
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from pricecomparison.utilities import FILENAME, retry_session, update_excel, setup_logging, SuperMarkets

setup_logging(logging.DEBUG, "%s" % SuperMarkets.Ocado.lower())

priceWatchXLS = _pandas.ExcelFile(FILENAME)
sheetNamesList = [SuperMarkets.Ocado]

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
                productDetails = session.get(productURL)

                soup = BeautifulSoup(productDetails.text, 'html.parser')

                # Finding the price using the class name
                productPrice = (soup.find(class_='bop-price__current').text).lstrip('£')

                # Update the cell in the sheet with the price
                priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
        except HTTPError as http_err:
            logging.error("HTTP Error: %s", http_err)
        except Exception as err:
            logging.error("Other Error: %s", err)

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: %s", general_err)
