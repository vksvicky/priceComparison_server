"""Code to retrieve and update Aldi product prices"""
import json
import logging

import urllib3
import pandas as _pandas

from requests.exceptions import HTTPError
from tqdm import tqdm

from pricecomparison.utilities import FILENAME, update_excel, retry_session, setup_logging

urllib3.disable_warnings()
setup_logging(logging.DEBUG, "aldi")

BASE_URL = "https://groceries.aldi.co.uk/api/product/calculatePrices"
priceWatchXLS = _pandas.ExcelFile(FILENAME)
sheetNamesList = ['Aldi']

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

                # Get product Id from URL
                productId = str(productURL).split("/")

                _headers = {
                    "Content-Type": "application/json",
                    "Accept-Language": "en-GB",
                    "Host": "groceries.aldi.co.uk",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
                    "X-Requested-With": "XMLHttpRequest"
                }

                data_binary = json.dumps({
                    "products": [
                        productId[5]
                    ]
                })

                session = retry_session()

                productDetails = session.post(BASE_URL, headers=_headers, data=data_binary, verify=False)

                if productDetails.status_code == 200:
                    productDetailsContent = json.loads(productDetails.content)
                    productPrice = productDetailsContent['ProductPrices'][0]['ListPrice'].lstrip('£')
                    priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
                else:
                    logging.error("HTTP Error: %s, %s", productDetails.status_code, productDetails.reason)

        except HTTPError as http_err:
            logging.error("HTTP Error: %s", http_err)
        except Exception as err:
            logging.error("Other Error: %s", err)

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: %s", general_err)
