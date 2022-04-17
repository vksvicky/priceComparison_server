from pandas import DataFrame, read_csv
from requests.exceptions import HTTPError
from collections import OrderedDict
from bs4 import BeautifulSoup
from requests import Session
from lxml import html
from tqdm import tqdm

import pandas as _pandas
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG, filename='tesco.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')


fileName = 'pricewatch.xlsx'
priceWatchXLS = _pandas.ExcelFile(fileName)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Tesco']

_session = Session()
_headers = OrderedDict({
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Host': 'www.tesco.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
	'Accept-Language': 'en-GB,en;q=0.9',
	'Accept-Encoding': 'gzip, deflate, br',
	'Connection': 'keep-alive',
})

requests.packages.urllib3.disable_warnings()

# print(sheetNamesList)  # see all sheet names

# If productURL does not exist, just move the next item in the loop
				if (isNaN(productURL)):
			   		continue

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

				_session.headers = _headers
				response = _session.get(productURL, headers=_headers, verify=False).text
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

		update_excel(fileName, eachSheet, priceWatchDataFrame)	
except Exception as general_err:
    logging.error("Error occurred: ", general_err)