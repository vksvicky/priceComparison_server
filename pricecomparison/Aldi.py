from requests.exceptions import HTTPError
from urllib.request import Request, urlopen
from tqdm import tqdm

import pandas as _pandas
import requests
import logging
import json
import urllib3

from pricecomparison.Utilities import isNaN, retry_session

urllib3.disable_warnings()
logging.basicConfig(level=logging.DEBUG, filename='aldi.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')

BASE_URL = "https://groceries.aldi.co.uk/api/product/calculatePrices"
fileName = 'pricewatch.xlsx'
priceWatchXLS = _pandas.ExcelFile(fileName)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Aldi']

# print(sheetNamesList)  # see all sheet names

def update_excel(filename, sheetname, dataframe):
    with _pandas.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        writer.book
        dataframe.to_excel(writer, sheet_name=sheetname, index=False)
        writer.save()
    # writer.close()

try:
    for eachSheet in sheetNamesList:
        priceWatchDataFrame = _pandas.read_excel(fileName, sheet_name=eachSheet, engine="openpyxl")
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
                if (isNaN(productURL)):
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
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest"
                }

                data_binary = json.dumps({
                    "products": [
                        productId[5]
                    ]
                })

                # _session.headers = _headers
                session = retry_session()
                for_cookies = session.get("https://groceries.aldi.co.uk")
                cookies = for_cookies.cookies

                productDetails = session.post(BASE_URL, headers=_headers, cookies=cookies, data=data_binary, verify=False)
                # print(productDetails.content)

                if (productDetails.status_code == 200):
                    try:
                        productDetailsContent = json.loads(productDetails.content)
                    except:
                        productDetailsContent = ""
                    if (productDetailsContent != ''):
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

        update_excel(fileName, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: ", general_err)