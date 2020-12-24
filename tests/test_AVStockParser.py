# -*- coding: utf-8 -*-

import pytest
import os
import pandas as pd
from avstockparser import AVStockParser

class TestBaseMethods():

    @pytest.fixture(scope='function', autouse=True)
    def init(self):
        AVStockParser.uLogger.level = 50  # Disable debug logging while test, logger CRITICAL = 50
        AVStockParser.uLogger.handlers[0].level = 50  # Disable debug logging for STDOUT
        AVStockParser.uLogger.handlers[1].level = 50  # Disable debug logging for log.txt
        # set up default parameters:
        self.reqURL = r"https://www.alphavantage.co/query?"
        self.apiKey = "demo"
        self.ticker = "IBM"  # used for demo test
        self.retry = 2

    def test_ParserReturnPandasDataframe(self):
        testData = [
            {
                "reqURL": self.reqURL,
                "apiKey": self.apiKey,
                "output": None,
                "ticker": self.ticker,
                "period": "TIME_SERIES_INTRADAY",
                "interval": "5min",
                "size": "full",
                "retry": self.retry,
            },
            {
                "reqURL": self.reqURL,
                "apiKey": self.apiKey,
                "output": None,
                "ticker": self.ticker,
                "period": "TIME_SERIES_DAILY",
                "size": "full",
                "retry": self.retry,
            },
        ]
        for test in testData:
            result = AVStockParser.AVParseToPD(**test)
            assert isinstance(result, pd.DataFrame) is True, "Expected Pandas DataFrame result output!"

    def test_ParserCreateOutputFile(self):
        testData = [
            {
                "reqURL": self.reqURL,
                "apiKey": self.apiKey,
                "output": os.path.abspath("tests/ibm_5min.csv"),
                "ticker": self.ticker,
                "period": "TIME_SERIES_INTRADAY",
                "interval": "5min",
                "size": "full",
                "retry": self.retry,
            },
            {
                "reqURL": self.reqURL,
                "apiKey": self.apiKey,
                "output": os.path.abspath("tests/ibm_daily.csv"),
                "ticker": self.ticker,
                "period": "TIME_SERIES_DAILY",
                "size": "full",
                "retry": self.retry,
            },
        ]
        for test in testData:
            AVStockParser.AVParseToPD(**test)
            assert os.path.exists(test["output"]), "Output file must be created after parser work finished!"
