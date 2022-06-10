import logging
import pandas as _pandas

from tqdm import tqdm
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from pricecomparison.Utilities import FILENAME, update_excel, retry_session

logging.basicConfig(level=logging.DEBUG, filename='ocado_mands.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

priceWatchXLS = _pandas.ExcelFile(FILENAME)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Ocado']

# print(sheetNamesList)  # see all sheet names

try:
    for eachSheet in sheetNamesList:
        priceWatchDataFrame = _pandas.read_excel(FILENAME, sheet_name=eachSheet, engine="openpyxl")

        # Printing top 10 rows
        # print(priceWatchDataFrame.head(10))
        numberOfRows = priceWatchDataFrame.shape[0]

        # Reading the URL for each row in the sheet
        try:
            for eachItem in tqdm(range(0, numberOfRows, 1)):
                productURL = priceWatchDataFrame.loc[eachItem, 'URL']
                # print(productURL)

                # If productURL does not exist, just move the next item in the loop
                if _pandas.isna(productURL):
                    continue

                session = retry_session()
                productDetails = session.get(productURL)
                # print(productDetails.text)

                soup = BeautifulSoup(productDetails.text, 'html.parser')

                # Finding the price using the class name
                productPrice = (soup.find(class_='bop-price__current').text).lstrip('£')
                # print(productPrice)

                # Update the cell in the sheet with the price
                priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
        except HTTPError as http_err:
            logging.error("HTTTP Error: ", http_err)
        except Exception as err:
            logging.error("Other Error: ", err)

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: ", general_err)
