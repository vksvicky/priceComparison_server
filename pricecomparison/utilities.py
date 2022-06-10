"""Utility functions required for PriceComparison"""

import sys
import logging
import os.path
import http.client
from logging.handlers import TimedRotatingFileHandler
import pandas as _pandas

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

FILENAME = 'pricewatch.xlsx'

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
                           method_whitelist=frozenset(['GET', 'POST', 'PUT', 'DELETE']))

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session

def setup_logging(loglevel, logFileName, logPath='.'):
    "Function to enable logging"
    # the file handler receives all messages from level DEBUG on up, regardless
    fileHandler = TimedRotatingFileHandler(
        os.path.join(logPath, logFileName + ".log"),
        when="midnight"
    )
    fileHandler.setLevel(logging.DEBUG)
    handlers = [fileHandler]

    if loglevel is not None:
        # if a log level is configured, use that for logging to the console
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(loglevel)
        handlers.append(stream_handler)

    if loglevel == logging.DEBUG:
        # when logging at debug level, make http.client extra chatty too
        # http.client *uses `print()` calls*, not logging.
        http.client.HTTPConnection.debuglevel = 1

    # finally, configure the root logger with our choice of handlers
    # the logging level of the root set to DEBUG (defaults to WARNING otherwise).
    logFormat = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    logging.basicConfig(
        format=logFormat, datefmt="%d-%m-%Y %H:%M:%S",
        handlers=handlers, level=logging.DEBUG
    )
