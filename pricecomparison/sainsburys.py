"""Main module."""
import logging
import pandas as _pandas

from tqdm import tqdm
from requests.exceptions import HTTPError

from pricecomparison.Utilities import FILENAME, update_excel, retry_session

logging.basicConfig(level=logging.DEBUG, filename='sainsburys.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

priceWatchXLS = _pandas.ExcelFile(FILENAME)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Sainsburys']

# print(sheetNamesList)  # see all sheet names

try:
    for eachSheet in sheetNamesList:
        priceWatchDataFrame = _pandas.read_excel(FILENAME, sheet_name=eachSheet, engine="openpyxl")

        # Printing top 10 rows
        # print(priceWatchDataFrame.head(10))
        numberOfRows = priceWatchDataFrame.shape[0]

        # Reading the URL for each row in the sheet
        try:
            for eachItem in tqdm(range(0, numberOfRows, 1), "Retrieving data..."):
                productURL = priceWatchDataFrame.loc[eachItem, 'URL']
                # print(productURL)

                # If productURL does not exist, just move the next item in the loop
                if _pandas.isna(productURL):
                    continue

                session = retry_session()
                response = session.get(productURL)
                productDetails = response.json()
                productPrice = productDetails['products'][0]['retail_price']['price']
                # print(productPrice)
                priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
        except HTTPError as http_err: \
                logging.error("HTTTP Error: ", http_err)
        except Exception as err:
            logging.error("Other Error: ", err)
        # # priceWatchDataFrame.to_excel("./pricewatch.xlsx",index=False);

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: ", general_err)
