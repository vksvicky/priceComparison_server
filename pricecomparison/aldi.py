"""Code to retrieve and update Aldi product prices"""
import json
import logging

import urllib3
import pandas as _pandas

from requests.exceptions import HTTPError
from tqdm import tqdm

from pricecomparison.utilities import FILENAME, update_excel, retry_session, setup_logging, SuperMarkets

urllib3.disable_warnings()
setup_logging(logging.DEBUG, "%s" % SuperMarkets.Aldi.lower())

BASE_URL = "https://groceries.aldi.co.uk/api/product/calculatePrices"
sheetNamesList = [SuperMarkets.Aldi]

try:
    for eachSheet in sheetNamesList:
        priceWatchDataFrame = _pandas.read_excel(FILENAME, sheet_name=eachSheet, engine="openpyxl")

        numberOfRows = priceWatchDataFrame.shape[0]
        index = -1

        # Reading the URL for each row in the sheet
        try:
            # create a process pool that uses all cpus
            # with multiprocessing.Pool() as pool:
            for eachItem in tqdm(range(0, numberOfRows, 1), "Retrieving data..."):

                productURL = priceWatchDataFrame.loc[eachItem, 'URL']

                # # If productURL does not exist, just move the next item in the loop
                # if _pandas.isna(productURL):
                #     continue
                index += 1
                # Get product Id from URL
                productId = str(productURL).rsplit("/")

                _headers = {
                    "Authority": "groceries.aldi.co.uk",
                    "Content-Type": "application/json",
                    "Accept-Language": "en-GB",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
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
                    if len(productDetailsContent['ProductPrices']) > 0:
                        productPrice = productDetailsContent['ProductPrices'][0]['ListPrice'].lstrip('£')
                    else:
                        productPrice = 0
                else:
                    logging.error("HTTP Error: %s, %s", productDetails.status_code, productDetails.reason)

                priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
        except HTTPError as http_err:
            logging.error("HTTP Error: %s", http_err)
        except Exception as err:
            logging.error("Other Error: %s", err)

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: %s", general_err)
