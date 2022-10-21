"""Code to retrieve and update Sainsburys product prices"""
import logging
import pandas as _pandas

from tqdm import tqdm
from requests.exceptions import HTTPError

from pricecomparison.utilities import FILENAME, update_excel, retry_session, setup_logging, SuperMarkets

setup_logging(logging.DEBUG, "%s" % SuperMarkets.Sainsburys.lower())

sheetNamesList = [SuperMarkets.Sainsburys]

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
                response = session.get(productURL)
                productDetails = response.json()
                productPrice = productDetails['products'][0]['retail_price']['price']
                priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
        except HTTPError as http_err:
            logging.error("HTTP Error: %s", http_err)
        except Exception as err:
            logging.error("Other Error: %s", err)

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: %s", general_err)
