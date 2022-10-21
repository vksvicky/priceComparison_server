"""Code to retrieve and update ASDA product prices"""
import json
import logging
import urllib3
import pandas as _pandas

from requests.exceptions import HTTPError
from tqdm import tqdm

from pricecomparison.utilities import FILENAME, update_excel, retry_session, SuperMarkets, setup_logging

urllib3.disable_warnings()
setup_logging(logging.DEBUG, f"{SuperMarkets.Asda.lower()}")

BASE_URL = "https://groceries.asda.com/api/bff/graphql"
sheetNamesList = [SuperMarkets.Asda]

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

                data_binary = json.dumps({
                    "variables": {
                        "is_eat_and_collect": False,
                        "payload": {
                            "page_id": productId[6],
                            "page_meta_info": True,
                            "page_type": "productDetailsPage"
                        },
                        "store_id": "4565"
                    },
                    "contract": "web/cms/product-details-page",
                    "requestorigin": "gi"
                })

                _headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "en-GB,en;q=0.9",
                    "Cache-Control": "max-age=0",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Origin": "https://groceries.asda.com",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
                    "Referer": productURL,
                    "Host": "groceries.asda.com",
                    "Request-Origin": "gi"
                }

                session = retry_session()
                productDetails = session.post(BASE_URL, headers=_headers, data=data_binary, verify=False).json()

                productPrice = productDetails['data']['tempo_cms_content']['zones'][0]['configs']['products']['items'][0]['price'][
                    'price_info']['price'].lstrip('£')

                priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
        except HTTPError as http_err:
            logging.error(f"HTTP Error: {http_err}")
        except Exception as err:
            logging.error(f"Other Error: {err}")

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error(f"Error occurred: {general_err}")
