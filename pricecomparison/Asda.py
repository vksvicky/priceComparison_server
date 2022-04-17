from pandas import DataFrame, read_csv
from requests.exceptions import HTTPError
from collections import OrderedDict
from bs4 import BeautifulSoup
from tqdm import tqdm

import pandas as _pandas
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG, filename='asda.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

BASE_URL = "https://groceries.asda.com/api/bff/graphql"
fileName = 'pricewatch.xlsx'
priceWatchXLS = _pandas.ExcelFile(fileName)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Asda']

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

				# Get product Id from URL
				productId = str(productURL).split("/")
				# print("productId = ", productId[6])

				data_binary=json.dumps({
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

				_headers ={
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

				# _session.headers = _headers
				productDetails = requests.post(BASE_URL, headers=_headers, data=data_binary, verify=False).json()
				# print(productDetails)

				# productDetails = response.json()
				productPrice = productDetails['data']['tempo_cms_content']['zones'][0]['configs']['products']['items'][0]['price']['price_info']['price'].lstrip('£')
				# print(productPrice)

				priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
		except HTTPError as http_err:
		    logging.error("HTTTP Error: ", http_err)
		except Exception as err:
		    logging.error("Other Error: ", err)

		update_excel(fileName, eachSheet, priceWatchDataFrame)	
except Exception as general_err:
    logging.error("Error occurred: ", general_err)