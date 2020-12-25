# AVStockParser

[![build](https://travis-ci.org/Tim55667757/AVStockParser.svg)](https://travis-ci.org/Tim55667757/AVStockParser)
[![pypi](https://img.shields.io/pypi/v/AVStockParser.svg)](https://pypi.python.org/pypi/AVStockParser)
[![license](https://img.shields.io/pypi/l/AVStockParser.svg)](https://github.com/Tim55667757/AVStockParser/blob/master/LICENSE)

Трейдерам необходимо получать исторические данные по акциям для дальнейшего анализа цен и построения графиков. Чаще всего эти данные платные или приходится тратить много времени и вручную загружать их со специальных сайтов.

Но есть множество онлайн-сервисов, которые предоставляют API для автоматического получения данных о ценах на акции. Например, Alpha Vantage. Основной источник данных для этого сервиса — биржа NASDAQ. Подробная документация по работе с Alpha Vantage API здесь: https://www.alphavantage.co/documentation/

**AVStockParser** это простая библиотека, которую можно использовать как python-модуль или запускать из командной строки и получать данные от Alpha Vantage. AVStockParser запрашивает историю цен на акции в формате .json с сайта www.alphavantage.co и конвертирует их в pandas dataframe или в .csv-файл, которые содержат OHLCV-свечи в каждой строке. Вы получаете таблицу, которая содержит колонки данных в следующей последовательности: "date", "time", "open", "high", "low", "close", "volume". Одна строка — это набор данных для построения одной "японской свечи" (candlestick).

Инструкция на английском здесь (see english readme here): https://github.com/Tim55667757/AVStockParser/blob/master/README.md

## Как установить

Проще всего использовать установку через PyPI:
```commandline
pip install avstockparser
```

После этого можно проверить установку командой:
```commandline
pip show avstockparser
```


## Аутентификация

Сервис Alpha Vantage использует для аутентификации апи-кей. Запросить бесплатный ключ можно тут: https://www.alphavantage.co/support/#api-key

Апи-кей — это алфавитно-цифровой токен. Этот токен необходимо отправлять на сервер с каждым запросом. Для этого, при работе с библиотекой AVStockParser, просто используйте ключ `--api-key "your token here"` или указывайте апи-кей при вызове метода: ```AVParseToPD(apiKey="your token here"```.


## Примеры использования

### Из командной строки

Внутренняя справка по ключам:
```commandline
avstockparser --help
```

Вывод:
```
usage: python AVStockParser.py [some options] [one command]

Alpha Vantage data parser. Get, parse, and save stock history as .csv-file or
pandas dataframe. See examples: https://tim55667757.github.io/AVStockParser

optional arguments:
  -h, --help            show this help message and exit
  --api-key API_KEY     Option (required): Alpha Vantage service's api key.
                        Request free api key at this page:
                        https://www.alphavantage.co/support/#api-key
  --ticker TICKER       Option (required): stock ticker, e.g., 'GOOGL' or
                        'YNDX'.
  --output OUTPUT       Option: full path to .csv output file. Default is None
                        mean that function return only pandas dataframe.
  --period PERIOD       Option: values can be 'TIME_SERIES_INTRADAY',
                        'TIME_SERIES_DAILY', 'TIME_SERIES_WEEKLY',
                        'TIME_SERIES_MONTHLY'. Default: 'TIME_SERIES_INTRADAY'
                        means that api returns intraday stock history data
                        with pre-define interval. More examples:
                        https://www.alphavantage.co/documentation/
  --interval INTERVAL   Option: '1min', '5min', '15min', '30min' or '60min'.
                        This is intraday period used only with
                        --period='TIME_SERIES_INTRADAY' key. Default: '60min'
                        means that api returns stock history with 60 min
                        interval.
  --size SIZE           Option: how many last candles returns for history.
                        Values can be 'full' or 'compact'. This parameter used
                        for 'outputsize' AV api parameter. Default: 'compact'
                        means that api returns only 100 values of stock
                        history data.
  --retry RETRY         Option: number of connections retry for data request
                        before raise exception. Default is 3.
  --debug-level DEBUG_LEVEL
                        Option: showing STDOUT messages of minimal debug
                        level, e.g., 10 = DEBUG, 20 = INFO, 30 = WARNING, 40 =
                        ERROR, 50 = CRITICAL.
  --parse               Command: get, parse, and save stock history as pandas
                        dataframe or .csv-file if --output key is defined.
```

Давайте попробуем получить дневные свечи по акциям Яндекса (тикер YNDX) и сохранить их в файл YNDX1440.csv. Команда может выглядеть как-то так:
```commandline
avstockparser --debug-level 10 --api-key "your token here" --ticker YNDX --period TIME_SERIES_DAILY --size full --output YNDX1440.csv --parse
```

В случае успеха вы должны получить вывод логов примерно следующего содержания:
```
AVStockParser.py    L:184  DEBUG   [2020-12-25 01:03:13,459] Alpha Vantage data parser started: 2020-12-25 01:03:13
AVStockParser.py    L:51   DEBUG   [2020-12-25 01:03:13,459] Request to Alpha Vantage: [https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=YNDX&outputsize=full&apikey=***]
AVStockParser.py    L:55   DEBUG   [2020-12-25 01:03:13,459] Trying (1) to send request...
AVStockParser.py    L:119  INFO    [2020-12-25 01:03:15,013] It was received 2415 candlesticks data from Alpha Vantage service
AVStockParser.py    L:120  INFO    [2020-12-25 01:03:15,013] Showing last 3 rows with Time Zone: 'US/Eastern':
AVStockParser.py    L:123  INFO    [2020-12-25 01:03:15,018]             date   time     open     high      low    close   volume
AVStockParser.py    L:123  INFO    [2020-12-25 01:03:15,018] 2412  2020.12.22  00:00  67.2800  67.4400  66.3000  67.1100  1002761
AVStockParser.py    L:123  INFO    [2020-12-25 01:03:15,018] 2413  2020.12.23  00:00  67.7300  68.7700  67.6400  67.6900   822039
AVStockParser.py    L:123  INFO    [2020-12-25 01:03:15,018] 2414  2020.12.24  00:00  68.1800  68.2900  67.1700  67.6500   359133
AVStockParser.py    L:127  INFO    [2020-12-25 01:03:15,027] Stock history saved to .csv-formatted file [./YNDX1440.csv]
AVStockParser.py    L:229  DEBUG   [2020-12-25 01:03:15,027] All Alpha Vantage data parser operations are finished success (summary code is 0).
AVStockParser.py    L:234  DEBUG   [2020-12-25 01:03:15,028] Alpha Vantage data parser work duration: 0:00:01.568581
AVStockParser.py    L:235  DEBUG   [2020-12-25 01:03:15,028] Alpha Vantage data parser finished: 2020-12-25 01:03:15

Process finished with exit code 0
```

Для консольного ключа `--period` вы можете указывать значения: `TIME_SERIES_DAILY`, `TIME_SERIES_WEEKLY` и `TIME_SERIES_MONTHLY` для получения дневных, недельных и месячных свечей соответственно. По умолчанию используется значение `TIME_SERIES_INTRADAY`.

В следующем примере давайте попробуем получить внутридневные часовые свечи по акциям 3M (тикер MMM) и сохранить их в файл MMM60.csv. Команда может быть примерно такой:
```commandline
avstockparser --debug-level 10 --api-key "your token here" --ticker MMM --period TIME_SERIES_INTRADAY --interval 60min --size compact --output MMM60.csv --parse
```

В случае успеха вы получите вывод, похожий на этот:
```
AVStockParser.py    L:184  DEBUG   [2020-12-25 01:09:44,601] Alpha Vantage data parser started: 2020-12-25 01:09:44
AVStockParser.py    L:51   DEBUG   [2020-12-25 01:09:44,601] Request to Alpha Vantage: [https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MMM&interval=60min&outputsize=compact&apikey=***]
AVStockParser.py    L:55   DEBUG   [2020-12-25 01:09:44,601] Trying (1) to send request...
AVStockParser.py    L:119  INFO    [2020-12-25 01:09:45,542] It was received 100 candlesticks data from Alpha Vantage service
AVStockParser.py    L:120  INFO    [2020-12-25 01:09:45,542] Showing last 3 rows with Time Zone: 'US/Eastern':
AVStockParser.py    L:123  INFO    [2020-12-25 01:09:45,551]           date   time      open      high       low     close  volume
AVStockParser.py    L:123  INFO    [2020-12-25 01:09:45,551] 97  2020.12.23  16:00  174.5700  175.0200  173.9550  174.0200  332340
AVStockParser.py    L:123  INFO    [2020-12-25 01:09:45,551] 98  2020.12.23  17:00  173.9900  173.9900  173.9600  173.9600  316682
AVStockParser.py    L:123  INFO    [2020-12-25 01:09:45,551] 99  2020.12.23  18:00  173.9900  173.9900  173.9900  173.9900    1410
AVStockParser.py    L:127  INFO    [2020-12-25 01:09:45,555] Stock history saved to .csv-formatted file [./MMM60.csv]
AVStockParser.py    L:229  DEBUG   [2020-12-25 01:09:45,555] All Alpha Vantage data parser operations are finished success (summary code is 0).
AVStockParser.py    L:234  DEBUG   [2020-12-25 01:09:45,555] Alpha Vantage data parser work duration: 0:00:00.953904
AVStockParser.py    L:235  DEBUG   [2020-12-25 01:09:45,555] Alpha Vantage data parser finished: 2020-12-25 01:09:45

Process finished with exit code 0
```

Файл ./MMM60.csv из этого примера будет содержать похожие данные по часовым свечам и столбцы: "date", "time", "open", "high", "low", "close", "volume":
```
2020.12.11,09:00,171.9100,171.9100,171.5500,171.8300,1663
2020.12.11,10:00,172.0100,173.6800,172.0100,173.5900,214065
2020.12.11,11:00,173.5800,173.9770,172.6700,173.0800,268294
...
2020.12.23,16:00,174.5700,175.0200,173.9550,174.0200,332340
2020.12.23,17:00,173.9900,173.9900,173.9600,173.9600,316682
2020.12.23,18:00,173.9900,173.9900,173.9900,173.9900,1410
```

Ключ `--size` может принимать значение `full` (Alpha Vantage сервис отправит всю доступную историческую информацию по свечам) или `compact` (будут отправлены только последние 100 свечей).

Ключ `--interval` используется только с ключом и значением `--period TIME_SERIES_INTRADAY`. Интервалы для внутридневных свечей могут принимать значения: `1min`, `5min`, `15min`, `30min` или `60min`.


### Через импорт модуля

Давайте рассмотрим только один простой пример запроса исторических данных по акциям IBM и как сохранить их в pandas dataframe:
```
from avstockparser.AVStockParser import AVParseToPD as Parser

# Запрашиваем исторические данные по свечам и сохраняем их в переменную pandas dataframe.
# Если переменная output не указана, то метод AVParseToPD не будет сохранять текстовый файл,
# а только вернёт данные в формате pandas dataframe.
df = Parser(
    reqURL=r"https://www.alphavantage.co/query?",
    apiKey="demo",
    output=None,
    ticker="IBM",
    period="TIME_SERIES_INTRADAY",
    interval="5min",
    size="full",
    retry=2,
)
print(df)
```

При запуске получим аналогичный вывод:
```
AVStockParser.py    L:119  INFO    [2020-12-25 01:49:51,612] It was received 2001 candlesticks data from Alpha Vantage service
AVStockParser.py    L:120  INFO    [2020-12-25 01:49:51,612] Showing last 3 rows with Time Zone: 'US/Eastern':
AVStockParser.py    L:123  INFO    [2020-12-25 01:49:51,616]             date   time      open      high       low     close volume
AVStockParser.py    L:123  INFO    [2020-12-25 01:49:51,616] 1998  2020.12.23  17:35  124.1000  124.1000  124.1000  124.1000   1571
AVStockParser.py    L:123  INFO    [2020-12-25 01:49:51,617] 1999  2020.12.23  18:45  124.0500  124.0500  124.0000  124.0000    278
AVStockParser.py    L:123  INFO    [2020-12-25 01:49:51,617] 2000  2020.12.23  20:00  123.9100  123.9100  123.9100  123.9100    225
            date   time      open      high       low     close volume
0     2020.11.25  06:50  124.3500  124.3500  124.2000  124.2000   1218
1     2020.11.25  07:05  124.2000  124.2000  124.2000  124.2000    150
2     2020.11.25  07:10  124.1000  124.1000  124.1000  124.1000    100
3     2020.11.25  07:35  124.0000  124.0000  124.0000  124.0000    510
4     2020.11.25  08:05  123.8201  124.2000  123.8200  123.8200   1414
...          ...    ...       ...       ...       ...       ...    ...
1996  2020.12.23  17:05  123.9100  123.9100  123.9100  123.9100    100
1997  2020.12.23  17:20  123.9000  123.9000  123.9000  123.9000   1146
1998  2020.12.23  17:35  124.1000  124.1000  124.1000  124.1000   1571
1999  2020.12.23  18:45  124.0500  124.0500  124.0000  124.0000    278
2000  2020.12.23  20:00  123.9100  123.9100  123.9100  123.9100    225

[2001 rows x 7 columns]

Process finished with exit code 0
```


Успехов вам в автоматизации биржевой торговли! ;)
