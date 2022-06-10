import pandas as _pandas

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

FILENAME = 'pricewatch.xlsx'


def update_excel(filename, sheetname, dataframe):
    with _pandas.ExcelWriter(filename, engine='openpyxl',
                             mode='a', if_sheet_exists='replace') as writer:
        writer.book
        dataframe.to_excel(writer, sheet_name=sheetname, index=False)
        writer.save()
    # writer.close()


def retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(429, 500, 502, 503, 504),
):
    retry_strategy = Retry(total=retries,
                           read=retries,
                           connect=retries,
                           backoff_factor=backoff_factor,
                           status_forcelist=status_forcelist,
                           method_whitelist=frozenset(['GET', 'POST', 'PUT', 'DELETE']))

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session
