"""Code to retrieve and update Morrisons product prices"""
import logging
import urllib3
import pandas as _pandas

from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from tqdm import tqdm

from pricecomparison.utilities import FILENAME, update_excel, retry_session, setup_logging, SuperMarkets

urllib3.disable_warnings()
setup_logging(logging.DEBUG, "%s" % SuperMarkets.Morrisons.lower())

priceWatchXLS = _pandas.ExcelFile(FILENAME)
sheetNamesList = [SuperMarkets.Morrisons]

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

                _headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Encoding": "gzip",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,hi-IN;q=0.7,hi;q=0.6,de-DE;q=0.5,de;q=0.4",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                }

                session = retry_session()
                for_cookies = session.get("https://groceries.morrisons.com")
                cookies = for_cookies.cookies

                productDetails = session.get(productURL, headers=_headers, cookies=cookies, verify=False)

                if productDetails.status_code == 200:
                    soup = BeautifulSoup(productDetails.text, 'html.parser')

                    # Finding the price using the class name
                    priceElement = soup.find(class_='bop-price__current').text
                    productPrice = priceElement.lstrip('£')
                    priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
        except HTTPError as http_err:
            logging.error("HTTP Error: %s", http_err)
        except Exception as err:
            logging.error("Other Error: %s", err)

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: %s", general_err)
