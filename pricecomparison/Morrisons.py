from pandas import DataFrame, read_csv
from requests.exceptions import HTTPError
from collections import OrderedDict
from bs4 import BeautifulSoup
from tqdm import tqdm

import pandas as _pandas
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG, filename='morrisons.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

fileName = 'pricewatch.xlsx'
priceWatchXLS = _pandas.ExcelFile(fileName)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Morrisons']

requests.packages.urllib3.disable_warnings()

# print(sheetNamesList)  # see all sheet names

def isNaN(string):
    return string != string

def update_excel(filename, sheetname, dataframe):
    with _pandas.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer: 
        workBook = writer.book
        dataframe.to_excel(writer, sheet_name=sheetname, index=False)
        writer.save()
        # writer.close()

try:
    for eachSheet in sheetNamesList:
        priceWatchDataFrame = _pandas.read_excel(fileName, sheet_name=eachSheet, engine="openpyxl")
        # print(priceWatchDataFrame.head(5))
        
        numberOfRows = priceWatchDataFrame.shape[0]
        # print("numberOfRows = ", numberOfRows);

        # # Reading the URL for each row in the sheet
        try:
            for eachItem in tqdm(range(0, numberOfRows, 1), "Reteriving data..."):
                productURL = priceWatchDataFrame.loc[eachItem, 'URL']
                # print("productURL = ", productURL)

                # If productURL does not exist, just move the next item in the loop
                if (isNaN(productURL)):
                    continue

                _headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Host": "groceries.morrisons.com",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
                    "Accept-Language": "en-GB,en;q=0.9",
                    "Cookie": "ai_user=MDnQn|2022-04-17T17:32:56.525Z; BP=0; LAST_REQUEST_TIME=1650216771735; W3SESSIONID=52F0A62BA27297582D8100D5DE2A61DF.MORRISONS205; COOKIE_CONSENT=y; MORRISONSSESSIONID=520AF0A6842BA27297F8582D81000ED5DE2A61DF; QueueITAccepted-SDFrts345E-V3_morrisonsshop=EventId%3Dmorrisonsshop%26QueueId%3D87226ce9-9ce9-4e7f-9e96-3af0411ac768%26RedirectType%3Dsafetynet%26IssueTime%3D1650215375%26Hash%3Dc94e818bdda75eeba1b3f13344ac41c04700082f209afb12a00d1ecaf2574446"
                }

                # _session.headers = _headers
                productDetails = requests.get(productURL, headers=_headers, verify=False)
                # print(productDetails.content)

                soup = BeautifulSoup(productDetails.text, 'html.parser')

                # Finding the price using the class name
                productPrice = (soup.find(class_='bop-price__current').text).lstrip('£')
                # print(productPrice)

                priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
        except HTTPError as http_err:
            logging.error("HTTTP Error: ", http_err)
        except Exception as err:
            logging.error("Other Error: ", err)

        update_excel(fileName, eachSheet, priceWatchDataFrame)  
except Exception as general_err:
    logging.error("Error occurred: ", general_err)