from pricecomparison.pricecomparison import fileName, eachSheet, eachItem


def update_excel(filename, sheetname, dataframe):
    with _pandas.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        workBook = writer.book
        dataframe.to_excel(writer, sheet_name=sheetname, index=False)
        writer.save()
        # writer.close()


priceWatchDataFrame = _pandas.read_excel(fileName, sheet_name=eachSheet, engine="openpyxl")
numberOfRows = priceWatchDataFrame.shape[0]
productURL = priceWatchDataFrame.loc[eachItem, 'URL']
response = requests.get(productURL)
productDetails = response.json()
productPrice = productDetails['products'][0]['retail_price']['price']