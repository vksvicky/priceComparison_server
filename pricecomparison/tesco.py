import logging

from collections import OrderedDict
import urllib3
import pandas as _pandas

from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from tqdm import tqdm

from pricecomparison.Utilities import FILENAME, update_excel, retry_session

urllib3.disable_warnings()
logging.basicConfig(level=logging.DEBUG, filename='tesco.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

priceWatchXLS = _pandas.ExcelFile(FILENAME)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Tesco']

_headers = OrderedDict({
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': 'www.tesco.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
})

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
            for eachItem in tqdm(range(0, numberOfRows, 1), "Retrieving data..."):
                productURL = priceWatchDataFrame.loc[eachItem, 'URL']
                # print("productURL = ", productURL)

                # If productURL does not exist, just move the next item in the loop
                if _pandas.isna(productURL):
                    continue

                session = retry_session()
                response = session.get(productURL, headers=_headers, verify=False).text
                # print(response)

                # response = requests.get(productURL)
                # print("response = ", response)

                # htmldoc = html.fromstring(response)
                soup = BeautifulSoup(response, 'html.parser')

                # print("price = ", soup.find_all("span", class_="value"))
                # print("price = ", soup.findAll("span", {"class": "value"}))

                # Identifiying the Div which contains the price
                productPriceDiv = soup.find("div", {"class": "price-control-wrapper"})

                # Using the idenfified div that contains the price, find the span with the price
                productPrice = productPriceDiv.find("span", {"class": "value"})

                # Update the cell in the sheet with the price
                # print("price = ", productPrice.text)
                priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice.text

            # for span in soup.find_all('form'):
            # 	print(span.get('span'))

            # productDetails = response.json()
            # print("productDetails = ", productDetails);

            # productPrice = productDetails['products'][0]['retail_price']['price']
            # # print(productPrice)
            # priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
        except HTTPError as http_err:
            logging.error("HTTTP Error: ", http_err)
        except Exception as err:
            logging.error("Other Error: ", err)
        # # priceWatchDataFrame.to_excel("./pricewatch.xlsx",index=False);

        update_excel(FILENAME, eachSheet, priceWatchDataFrame)
except Exception as general_err:
    logging.error("Error occurred: ", general_err)
