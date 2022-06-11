"""Utility functions required for PriceComparison"""

import sys
import logging
import os.path
import http.client
from enum import Enum
from logging.handlers import TimedRotatingFileHandler
import pandas as _pandas

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

FILENAME = 'pricewatch.xlsx'


class SuperMarkets(str, Enum):
    Aldi = 'Aldi'
    Asda = 'Asda'
    Coop = 'Coop'
    Morrisons = 'Morrisons'
    Ocado = 'Ocado'
    Sainsburys = 'Sainsburys'
    Tesco = 'Tesco'


def update_excel(filename, sheetname, dataframe):
    "Function to update the specific sheet in the excel_file"
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
    "Function to perform REST API retries"
    retry_strategy = Retry(total=retries,
                           read=retries,
                           connect=retries,
                           backoff_factor=backoff_factor,
                           status_forcelist=status_forcelist,
                           allowed_methods=frozenset(['GET', 'POST', 'PUT']))

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = Session()
    session.mount("https://", adapter)
    # Not sure if this is required? session.mount("http://", adapter)

    return session


def setup_logging(log_level, log_filename, log_path='.'):
    "Function to enable logging"
    # the file handler receives all messages from level DEBUG on up, regardless
    file_handler = TimedRotatingFileHandler(
        os.path.join(log_path, log_filename + ".log"),
        when="midnight"
    )
    file_handler.setLevel(logging.DEBUG)
    handlers = [file_handler]

    if log_level is not None:
        # if a log level is configured, use that for logging to the console
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(log_level)
        handlers.append(stream_handler)

    if log_level == logging.DEBUG:
        # when logging at debug level, make http.client extra chatty too
        # http.client *uses `print()` calls*, not logging.
        http.client.HTTPConnection.debuglevel = 1

    # finally, configure the root logger with our choice of handlers
    # the logging level of the root set to DEBUG (defaults to WARNING otherwise).
    log_format = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"

    #NOSONAR
    logging.basicConfig( #NOSONAR
        format=log_format, datefmt="%d-%m-%Y %H:%M:%S", #NOSONAR
        handlers=handlers, level=logging.DEBUG #NOSONAR
    )
