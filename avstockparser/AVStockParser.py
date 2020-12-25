# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


# Module: Alpha Vantage Stock History Parser.
# Request time series with stock history data in .json-format from www.alphavantage.co and convert into pandas dataframe or .csv file with OHLCV-candlestick in every strings.
# Alpha Vantage API Documentation: https://www.alphavantage.co/documentation/
# Alpha Vantage use NASDAQ list of stocks: https://www.nasdaq.com/market-activity/stocks/screener
# In additional you can see more analytics by tickers here: https://www.infrontanalytics.com/fe-en/NL0009805522/Yandex-NV/stock-performance


import os
import sys
sys.path.append("..")
import time
from datetime import datetime
import json
import requests
import pandas as pd
from argparse import ArgumentParser

import avstockparser.UniLogger as uLog
import traceback as tb


# --- Common technical parameters:

uLogger = uLog.UniLogger
uLogger.level = 10  # debug level by default
uLogger.handlers[0].level = 20  # info level by default for STDOUT
uLogger.handlers[1].level = 10  # debug level by default for log.txt


def AVParseToPD(reqURL=r"https://www.alphavantage.co/query?", apiKey=None, output=None, ticker=None,
                period="TIME_SERIES_INTRADAY", interval="60min", size="compact", retry=5):
    """
    Get and parse stock data from Alpha Vantage service. Save to .csv if needed. Return pandas dataframe.
    :param reqURL: string - base api requests url, default is r"https://www.alphavantage.co/query?".
    :param apiKey: string - Alpha Vantage service's api key (alphanumeric string token), default is None.
    :param output: string - full path to .csv-file, default is None mean that function return only pandas dataframe object.
    :param ticker: string - stock ticker, e.g. "GOOGL" or "YNDX".
    :param period: string - value for "function" AV api parameter - "TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY" etc, default is "TIME_SERIES_INTRADAY".
    :param interval: string - value in minutes, used only if period="TIME_SERIES_INTRADAY". Values can be "1min", "5min", "15min", "30min", "60min", default is "60min".
    :param size: string - how many last candles returns for history, e.g. "full" or "compact". Default is "compact" means that api returns only 100 values of stock history data (more faster).
    :param retry: int - number of connection retry for data request before raise exception.
    """
    if apiKey is None or not apiKey:
        raise Exception("apiKey variable must be required!")

    if ticker is None or not ticker:
        raise Exception("ticker variable must be required!")

    respJSON = {}
    intervalParam = "&interval={}".format(interval) if period == "TIME_SERIES_INTRADAY" else ""
    req = "{}function={}&symbol={}{}&outputsize={}&apikey={}".format(reqURL, period, ticker, intervalParam, size, apiKey)
    reqHid = "{}function={}&symbol={}{}&outputsize={}&apikey=***".format(reqURL, period, ticker, intervalParam, size)  # do not print api key in log
    uLogger.debug("Request to Alpha Vantage: [{}]".format(reqHid))

    for i in range(retry):
        try:
            uLogger.debug("Trying ({}) to send request...".format(i + 1))
            response = requests.get(req, stream=True)
            responseRaw = response.text
            respJSON = json.loads(responseRaw, encoding="UTF-8")

            if "Error Message" in respJSON.keys():
                uLogger.error(respJSON["Error Message"])
                raise Exception("Alpha Vantage returns an error! Maybe current ticker not in NASDAQ list?")

            if "Note" in respJSON.keys() and i < retry:
                uLogger.warning("Alpha Vantage returns warning: '{}'".format(respJSON["Note"]))
                uLogger.debug("Waiting until 60 sec and will try again...")
                time.sleep(60)

            else:
                break

        except Exception as e:
            uLogger.error(e)
            exc = tb.format_exc().split("\n")
            for line in exc:
                if line:
                    uLogger.error(line)

            uLogger.debug("Waiting until 30 sec and will try again...")
            time.sleep(30)

    avTSHeaders = {
        "TIME_SERIES_MONTHLY": "Monthly Time Series",
        "TIME_SERIES_WEEKLY": "Weekly Time Series",
        "TIME_SERIES_DAILY": "Time Series (Daily)",
        "TIME_SERIES_INTRADAY": "Time Series ({})".format(interval),
    }
    rawDataDict = respJSON[avTSHeaders[period]]
    dateKeys = list(rawDataDict.keys())  # list from json response with all given dates
    dates = pd.to_datetime(dateKeys)

    df = pd.DataFrame(
        data={
            "date": dates,
            "time": dates,
            "open": [rawDataDict[item]["1. open"] for item in dateKeys],
            "high": [rawDataDict[item]["2. high"] for item in dateKeys],
            "low": [rawDataDict[item]["3. low"] for item in dateKeys],
            "close": [rawDataDict[item]["4. close"] for item in dateKeys],
            "volume": [rawDataDict[item]["5. volume"] for item in dateKeys],
        },
        index=range(len(rawDataDict)),
        columns=["date", "time", "open", "high", "low", "close", "volume"],
    )
    df["date"] = df["date"].dt.strftime("%Y.%m.%d")  # only dates in "date" field
    df["time"] = df["time"].dt.strftime("%H:%M")  # only times in "time" field
    df = df.iloc[::-1]
    df.reset_index(drop=True, inplace=True)  # change index from oldest to latest candles

    if "6. Time Zone" in respJSON["Meta Data"].keys():
        timeZone = respJSON["Meta Data"]["6. Time Zone"]

    elif "5. Time Zone" in respJSON["Meta Data"].keys():
        timeZone = respJSON["Meta Data"]["5. Time Zone"]

    else:
        timeZone = respJSON["Meta Data"]["4. Time Zone"]

    uLogger.info("It was received {} candlesticks data from Alpha Vantage service".format(len(df)))
    uLogger.info("Showing last 3 rows with Time Zone: '{}':".format(timeZone))
    lines = pd.DataFrame.to_string(df[["date", "time", "open", "high", "low", "close", "volume"]][-3:], max_cols=20).split("\n")
    for line in lines:
        uLogger.info(line)

    if output is not None:
        df.to_csv(output, sep=",", index=False, header=False)
        uLogger.info("Stock history saved to .csv-formatted file [{}]".format(os.path.abspath(output)))

    else:
        uLogger.debug("--output key is not defined. Parsed history file not saved to .csv-file, only pandas dataframe returns.")

    return df


def ParseArgs():
    """
    Function get and parse command line keys.
    """
    parser = ArgumentParser()  # command-line string parser

    parser.description = "Alpha Vantage data parser. Get, parse, and save stock history as .csv-file or pandas dataframe. See examples: https://tim55667757.github.io/AVStockParser"
    parser.usage = "python AVStockParser.py [some options] [one command]"

    # options:
    parser.add_argument("--api-key", type=str, required=True, help="Option (required): Alpha Vantage service's api key. Request free api key at this page: https://www.alphavantage.co/support/#api-key")
    parser.add_argument("--ticker", type=str, required=True, help="Option (required): stock ticker, e.g., 'GOOGL' or 'YNDX'.")
    parser.add_argument("--output", type=str, default=None, help="Option: full path to .csv output file. Default is None mean that function return only pandas dataframe.")
    parser.add_argument("--period", type=str, default="TIME_SERIES_INTRADAY", help="Option: values can be 'TIME_SERIES_INTRADAY', 'TIME_SERIES_DAILY', 'TIME_SERIES_WEEKLY', 'TIME_SERIES_MONTHLY'. Default: 'TIME_SERIES_INTRADAY' means that api returns intraday stock history data with pre-define interval. More examples: https://www.alphavantage.co/documentation/")
    parser.add_argument("--interval", type=str, default="60min", help="Option: '1min', '5min', '15min', '30min' or '60min'. This is intraday period used only with --period='TIME_SERIES_INTRADAY' key. Default: '60min' means that api returns stock history with 60 min interval.")
    parser.add_argument("--size", type=str, default="compact", help="Option: how many last candles returns for history. Values can be 'full' or 'compact'. This parameter used for 'outputsize' AV api parameter. Default: 'compact' means that api returns only 100 values of stock history data.")
    parser.add_argument("--retry", type=int, default=3, help="Option: number of connections retry for data request before raise exception. Default is 3.")
    parser.add_argument("--debug-level", type=int, default=20, help="Option: showing STDOUT messages of minimal debug level, e.g., 10 = DEBUG, 20 = INFO, 30 = WARNING, 40 = ERROR, 50 = CRITICAL.")

    # commands:
    parser.add_argument("--parse", action="store_true", help="Command: get, parse, and save stock history as pandas dataframe or .csv-file if --output key is defined.")

    cmdArgs = parser.parse_args()
    return cmdArgs


def Main():
    """
    Main function for reading, parsing and saving stock history from Alpha Vantage service as .csv or pandas dataframe.
    """
    # set up default parameters:
    reqURL = r"https://www.alphavantage.co/query?"
    apiKey = None
    output = None
    ticker = "YNDX"
    period = "TIME_SERIES_INTRADAY"
    interval = "60min"
    size = "compact"
    retry = 5

    args = ParseArgs()  # get and parse command-line parameters
    exitCode = 0

    if args.debug_level:
        uLogger.level = 10  # always debug level by default
        uLogger.handlers[0].level = args.debug_level  # level for STDOUT
        uLogger.handlers[1].level = 10  # always debug level for log.txt

    start = datetime.now()
    uLogger.debug("Alpha Vantage data parser started: {}".format(start.strftime("%Y-%m-%d %H:%M:%S")))

    try:
        # --- set options:

        if args.api_key:
            apiKey = args.api_key

        if args.output:
            output = args.output

        if args.ticker:
            ticker = args.ticker

        if args.period:
            period = args.period

        if args.interval:
            interval = args.interval

        if args.size:
            size = args.size

        if args.retry:
            retry = args.retry

        # --- do one command:

        if not args.parse:
            raise Exception("One of the possible commands must be selected! See: python AVStockParser.py --help")

        if args.parse:
            AVParseToPD(reqURL, apiKey, output, ticker, period, interval, size, retry)

    except Exception:
        exc = tb.format_exc().split("\n")
        for line in exc:
            if line:
                uLogger.debug(line)
        exitCode = 255

    finally:
        finish = datetime.now()

        if exitCode == 0:
            uLogger.debug("All Alpha Vantage data parser operations are finished success (summary code is 0).")

        else:
            uLogger.error("An errors occurred during the work! See full debug log with --debug-level 10. Summary code: {}".format(exitCode))

        uLogger.debug("Alpha Vantage data parser work duration: {}".format(finish - start))
        uLogger.debug("Alpha Vantage data parser finished: {}".format(finish.strftime("%Y-%m-%d %H:%M:%S")))

        sys.exit(exitCode)


if __name__ == "__main__":
    Main()
