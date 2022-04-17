# from pandas import DataFrame, read_csv
# from requests.exceptions import HTTPError
# from collections import OrderedDict
# from bs4 import BeautifulSoup
# from tqdm import tqdm

# import pandas as _pandas
# import requests
# import logging
# import json

# logging.basicConfig(level=logging.DEBUG, filename='aldi.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')


# BASE_URL = "https://groceries.aldi.co.uk"
# fileName = 'pricewatch.xlsx'
# priceWatchXLS = _pandas.ExcelFile(fileName)
# # sheetNamesList = priceWatchXLS.sheet_names
# sheetNamesList = ['Aldi']

# requests.packages.urllib3.disable_warnings()

# # print(sheetNamesList)  # see all sheet names

# def isNaN(string):
#     return string != string

# def update_excel(filename, sheetname, dataframe):
#     with _pandas.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer: 
#         workBook = writer.book
#         dataframe.to_excel(writer, sheet_name=sheetname, index=False)
#         writer.save()
#         # writer.close()

# try:
# 	for eachSheet in sheetNamesList:
# 		priceWatchDataFrame = _pandas.read_excel(fileName, sheet_name=eachSheet, engine="openpyxl")
# 		# print(priceWatchDataFrame.head(5))
		
# 		numberOfRows = priceWatchDataFrame.shape[0]
# 		# numberOfRows = 1
# 		# print("numberOfRows = ", numberOfRows);

# 		# # Reading the URL for each row in the sheet
# 		try:
# 			for eachItem in tqdm(range(0, numberOfRows, 1), "Reteriving data..."):
# 				productURL = priceWatchDataFrame.loc[eachItem, 'URL']
# 				# print("productURL = ", productURL)

# 				# If productURL does not exist, just move the next item in the loop
# 				if (isNaN(productURL)):
# 			   		continue

# 				# # Get product Id from URL
# 				# productId = str(productURL).split("/")
# 				# print("productId = ", productId[5])

# 				_headers ={
# 	                "Content-Type": "application/json",
# 					"Accept": "application/json, text/javascript, */*; q=0.01",
# 					"Accept-Encoding": "gzip, deflate, br",
# 					"Accept-Language": "en-GB",
# 					"Origin": BASE_URL,
# 					"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
# 					"Referer": productURL
# 	            }

# 				# _session.headers = _headers
# 				productDetails = requests.get(productURL, headers=_headers, verify=False)
# 				# print(productDetails.text)

# 				soup = BeautifulSoup(productDetails.text, 'html.parser')
# 				print(soup)

# 				# # Finding the price using the class name
# 				# productPrice = (soup.find(class_='product-price h4 m-0 font-weight-bold').text).lstrip('£')
# 				# print(productPrice)

# 				# productDetails = response.json()
# 				# productPrice = productDetails['data']['tempo_cms_content']['zones'][0]['configs']['products']['items'][0]['price']['price_info']['price'].lstrip('£')
# 				# print(productPrice)

			   
# 				# print(response.status_code)
# 				# print(response.text)

# 				# 
# 			   	# htmldoc = html.fromstring(response)
# 				# soup = BeautifulSoup(response, 'html.parser')

# 				# print("price = ", soup.find_all("span", class_="value"))
# 				# print("price = ", soup.findAll("span", {"class": "value"}))

# 				# # Identifiying the Div which contains the price
# 				# productPriceDiv = soup.find("div", {"class": "price-control-wrapper"})

# 				# # Using the idenfified div that contains the price, find the span with the price
# 				# productPrice = productPriceDiv.find("span", {"class": "value"})
				
# 				# # Update the cell in the sheet with the price
# 				# # print("price = ", productPrice.text)
# 				# priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice

# 				# for span in soup.find_all('form'):
# 				# 	print(span.get('span'))

# 			   	# productDetails = response.json()
# 			   	# print("productDetails = ", productDetails);

# 			   	# productPrice = productDetails['products'][0]['retail_price']['price']
# 			   	# # print(productPrice)
# 			   	# priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
# 		except HTTPError as http_err:
# 		    logging.error("HTTTP Error: ", http_err)
# 		except Exception as err:
# 		    logging.error("Other Error: ", err)
# 		# # priceWatchDataFrame.to_excel("./pricewatch.xlsx",index=False);

# 		# update_excel(fileName, eachSheet, priceWatchDataFrame)	
# except Exception as general_err:
#     logging.error("Error occurred: ", general_err)


from pandas import DataFrame, read_csv
from requests.exceptions import HTTPError
from collections import OrderedDict
from bs4 import BeautifulSoup
# from requests import Session
from tqdm import tqdm

import pandas as _pandas
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG, filename='aldi.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

BASE_URL = "https://groceries.aldi.co.uk/api/product/calculatePrices"
fileName = 'pricewatch.xlsx'
priceWatchXLS = _pandas.ExcelFile(fileName)
# sheetNamesList = priceWatchXLS.sheet_names
sheetNamesList = ['Aldi']

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

				_headers ={
	                "Content-Type": "application/json",
	                "Accept": "application/json, text/javascript, */*; q=0.01",
	                "Accept-Encoding": "gzip, deflate, br",
	                "Accept-Language": "en-GB",
	                "Host": "groceries.aldi.co.uk",
	                "Origin": "https://groceries.aldi.co.uk",
	                "X-Requested-With": "XMLHttpRequest",
				}

				data_binary = json.dumps({
					"products": [
						productId[5]
					]
				})

				# _session.headers = _headers
				productDetails = requests.post(BASE_URL, headers=_headers, data=data_binary, verify=False)
				# print(productDetails.content)

				productDetailsContent = json.loads(productDetails.content)
				# print(productDetailsContent)

				productPrice = productDetailsContent['ProductPrices'][0]['ListPrice'].lstrip('£')
				# print(productPrice)

				priceWatchDataFrame.loc[eachItem, 'Price'] = productPrice
		except HTTPError as http_err:
		    logging.error("HTTTP Error: ", http_err)
		except Exception as err:
		    logging.error("Other Error: ", err)

		update_excel(fileName, eachSheet, priceWatchDataFrame)	
except Exception as general_err:
	logging.error("Error occurred: ", general_err)