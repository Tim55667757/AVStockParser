# -*- coding: utf-8 -*-
# Author: Timur Gilmullin

# Build with Travis CI


from setuptools import setup
import os

__version__ = "1.1"

devStatus = "4 - Beta"

if "TRAVIS_BUILD_NUMBER" in os.environ and "TRAVIS_BRANCH" in os.environ:
    print("This is TRAVIS-CI build")
    print("TRAVIS_BUILD_NUMBER = {}".format(os.environ["TRAVIS_BUILD_NUMBER"]))
    print("TRAVIS_BRANCH = {}".format(os.environ["TRAVIS_BRANCH"]))

    __version__ += ".{}{}".format(
        "" if "release" in os.environ["TRAVIS_BRANCH"] or os.environ["TRAVIS_BRANCH"] == "master" else "dev",
        os.environ["TRAVIS_BUILD_NUMBER"],
    )

    devStatus = "5 - Production/Stable" if "release" in os.environ["TRAVIS_BRANCH"] or os.environ["TRAVIS_BRANCH"] == "master" else devStatus

else:
    print("This is local build")
    __version__ += ".dev0"  # set version as major.minor.localbuild if local build: python setup.py install

print("AVStockParser build version = {}".format(__version__))

setup(
    name="avstockparser",

    version=__version__,

    description="Get time series with stock history data in .json-format from www.alphavantage.co and convert into pandas dataframe or .csv file with OHLCV-candlestick in every strings. Also you can draw an interactive chart.",

    long_description="GitHub Pages: https://tim55667757.github.io/AVStockParser",

    license="MIT",

    author="Timur Gilmullin",

    author_email="tim55667757@gmail.com",

    url="https://github.com/Tim55667757/AVStockParser/",

    download_url="https://github.com/Tim55667757/AVStockParser.git",

    entry_points={"console_scripts": ["avstockparser = avstockparser.AVStockParser:Main"]},

    classifiers=[
        "Development Status :: {}".format(devStatus),
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],

    keywords=[
        "broker",
        "history",
        "csv",
        "stock",
        "trade",
        "candlestick",
        "chart",
        "parser",
        "alphavantage",
    ],

    tests_require=[
        "pytest>=6.2.2",
        "requests>=2.25.1",
        "pandas>=1.2.2",
        "pricegenerator>=1.2.46",
    ],

    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.2",
        "pricegenerator>=1.2.46",
    ],

    packages=[
        "avstockparser",
    ],

    zip_safe=True,
)
