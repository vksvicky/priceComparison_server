from tqdm import tqdm
from pandas import DataFrame, read_csv
from requests.exceptions import HTTPError

import pandas as _pandas
import requests
import json

fileName = 'pricewatch.xlsx'
priceWatchXLS = _pandas.ExcelFile(fileName)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Co-op']

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

		# Printing top 10 rows
		#print(priceWatchDataFrame.head(10))
		numberOfRows = priceWatchDataFrame.shape[0]

		# Reading the URL for each row in the sheet
		try:
			for eachItem in tqdm(range(0, numberOfRows, 1)):
			   productURL = priceWatchDataFrame.loc[eachItem, 'URL']
			   # print(isNaN(productURL))

			   # If productURL does not exist, just move the next item in the loop
			   if (isNaN(productURL)):
			   		continue

			   response = requests.get(productURL)
			   productDetails = response.json()
			   # print(productDetails)

			   productPrice = productDetails['price']
			   # print(productPrice)

			   priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
		except HTTPError as http_err:
		    print(f'HTTP error occurred: {http_err}')
		except Exception as err:
		    print(f'Other error occurred: {err}')
		# priceWatchDataFrame.to_excel("./pricewatch.xlsx",index=False);

		update_excel(fileName, eachSheet, priceWatchDataFrame)	
except Exception as general_err:
    print(f'Error occurred: {general_err}')