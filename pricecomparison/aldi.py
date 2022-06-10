import json
import logging

import requests
import urllib3
import pandas as _pandas

from requests.exceptions import HTTPError
from tqdm import tqdm

from pricecomparison.Utilities import FILENAME, update_excel, retry_session

urllib3.disable_warnings()
logging.basicConfig(level=logging.DEBUG, filename='aldi.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

BASE_URL = "https://groceries.aldi.co.uk/api/product/calculatePrices"
priceWatchXLS = _pandas.ExcelFile(FILENAME)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Aldi']

# print(sheetNamesList)  # see all sheet names

try:
    for eachSheet in sheetNamesList:
        priceWatchDataFrame = _pandas.read_excel(FILENAME, sheet_name=eachSheet, engine="openpyxl")
        # print(priceWatchDataFrame.head(5))

        numberOfRows = priceWatchDataFrame.shape[0]
        # numberOfRows = 1
        # print("numberOfRows = ", numberOfRows);

        # # Reading the URL for each row in the sheet
        try:
            for eachItem in tqdm(range(0, numberOfRows, 1), "Reteriving data..."):
                productURL = priceWatchDataFrame.loc[eachItem, 'URL']
                # print("productURL = ", productURL)

                # If productURL does not exist, just move the next item in the loop
                if _pandas.isna(productURL):
                    continue

                # Get product Id from URL
                productId = str(productURL).split("/")
                # print("productId = ", productId[5])

                _headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-GB",
                    "Host": "groceries.aldi.co.uk",
                    "Origin": "https://groceries.aldi.co.uk",
                    "User-Accept": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
                    "X-Requested-With": "XMLHttpRequest"
                }

                data_binary = json.dumps({
                    "products": [
                        productId[5]
                    ]
                })

                session = retry_session()
                for_cookies = session.get("https://groceries.aldi.co.uk")
                _cookies = for_cookies.cookies

                productDetails = session.post(BASE_URL, headers=_headers, cookies=_cookies, data=data_binary, verify=False)
                # print(productDetails.content)

                if productDetails.status_code == 200:
                    try:
                        productDetailsContent = json.loads(productDetails.content)
                    except:
                        productDetailsContent = ""

                    if productDetailsContent != '':
                        # print(productDetailsContent)
                        productPrice = productDetailsContent['ProductPrices'][0]['ListPrice'].lstrip('£')
                        # print(productPrice)
                        priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
                else:
                    logging.error("HTTP Error: %s, %s", productDetails.status_code, productDetails.reason)

        except HTTPError as http_err:
            logging.error("HTTTP Error: ", http_err)
        except Exception as err:
            logging.error("Other Error: ", err)

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: ", general_err)