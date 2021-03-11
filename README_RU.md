# AVStockParser

[![Build Status](https://travis-ci.com/Tim55667757/AVStockParser.svg?branch=master)](https://travis-ci.com/Tim55667757/AVStockParser)
[![pypi](https://img.shields.io/pypi/v/AVStockParser.svg)](https://pypi.python.org/pypi/AVStockParser)
[![license](https://img.shields.io/pypi/l/AVStockParser.svg)](https://github.com/Tim55667757/AVStockParser/blob/master/LICENSE)

Трейдерам необходимо получать исторические данные по акциям для дальнейшего анализа цен и построения графиков. Чаще всего эти данные платные или приходится тратить много времени и вручную загружать их со специальных сайтов.

Но есть множество онлайн-сервисов, которые предоставляют API для автоматического получения данных о ценах на акции бесплатно, но с некоторой задержкой. Например, Alpha Vantage. Основной источник данных для этого сервиса — биржа NASDAQ. Подробная документация по работе с Alpha Vantage API здесь: https://www.alphavantage.co/documentation/

**AVStockParser** это простая библиотека, которую можно использовать как python-модуль или запускать из командной строки и получать данные от Alpha Vantage. AVStockParser запрашивает историю цен на акции в формате .json с сайта www.alphavantage.co и конвертирует их в Pandas dataframe или в .csv-файл, которые содержат OHLCV-свечи в каждой строке. Вы получаете таблицу, которая содержит колонки данных в следующей последовательности: "date", "time", "open", "high", "low", "close", "volume". Одна строка — это набор данных для построения одной "японской свечи" (candlestick). Дополнительно можно отобразить данные на простом интерактивном свечном графике.

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
Запуск: python AVStockParser.py [параметры] [одна или несколько команд]

Получение данных о ценах акций через сервис Alpha Vantage. Можно получить
и сохранить исторические данные по ценам акций в .csv-файл или в виде
Pandas dataframe. Примеры: https://tim55667757.github.io/AVStockParser

Возможные параметры командной строки:
  -h, --help            Показать эту подсказку и выйти
  --api-key API_KEY     Параметр (обязательный): апи-кей для сервиса Alpha Vantage.
                        Запросить ключ для бесплатного доступа можно тут:
                        https://www.alphavantage.co/support/#api-key
  --ticker TICKER       Параметр (обязательный): тикер акции, например,
                        'GOOGL' или 'YNDX'.
  --output OUTPUT       Параметр: полный путь до .csv-файла. По умолчанию None
                        означает, что будет получен только Pandas dataframe.
  --period PERIOD       Параметр: можно использовать значения 'TIME_SERIES_INTRADAY',
                        'TIME_SERIES_DAILY', 'TIME_SERIES_WEEKLY' или
                        'TIME_SERIES_MONTHLY'. По умолчанию: 'TIME_SERIES_INTRADAY',
                        что означает, что api вернёт внутридневную историю цен для
                        предопределённого интервала. Больше примеров здесь:
                        https://www.alphavantage.co/documentation/
  --interval INTERVAL   Параметр: '1min', '5min', '15min', '30min' или '60min'.
                        Интервал используется только для внутридневной истории цен
                        для ключа --period='TIME_SERIES_INTRADAY'. По умолчанию: '60min',
                        что означает, что api вернёт внутридневную историю цен
                        и каждая свеча будет иметь интервал в 60 минут.
  --size SIZE           Параметр: сколько исторических свечей нужно скачать.
                        Значения могут быть 'full' или 'compact'. Этот параметр
                        использует сервис AV для параметра запроса 'outputsize'.
                        По умолчанию: 'compact' означает, что api вернёт 100 свечей.
  --retry RETRY         Параметр: количество попыток подключения к сервису AV.
                        По умолчанию: 3.
  --debug-level DEBUG_LEVEL
                        Параметр: уровень логирования для STDOUT,
                        например, 10 = DEBUG, 20 = INFO, 30 = WARNING,
                        40 = ERROR, 50 = CRITICAL.
  --parse               Команда: скачать историю цен как Pandas dataframe
                        или как .csv-файл (если ключ --output будет задан).
  --render              Команда: использовать библиотеку PriceGenerator для отрисовки
                        интерактивного графика цен после парсинга истории. Этот ключ
                        можно использовать только с ключом --parse.
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

Кроме того, вы можете построить интерактивный график цен (используя библиотеку [PriceGenerator](https://github.com/Tim55667757/PriceGenerator)). Для этого укажите ключ `--render` после ключа `--parse`:
```commandline
avstockparser --debug-level 10 --api-key "your token here" --ticker YNDX --period TIME_SERIES_DAILY --size compact --output YNDX1440.csv --parse --render
```

После выполнения команды выше вы получите три файла:
- `YNDX1440.csv` — файл в формате .csv, который содержит цены (пример: [./media/YNDX1440.csv](./media/YNDX1440.csv));
- `index.html` — график цен и статистику, отрисованные при помощи библиотеки Bokeh и сохранённые в .html-файл (пример: [./media/index.html](./media/index.html));
- `index.html.md` — статистика в текстовом виде, сохранённая в маркдаун-формате (пример: [./media/index.html.md](./media/index.html.md)).

![](./media/index.html.png)


### Через импорт модуля

Давайте рассмотрим только один простой пример запроса исторических данных по акциям IBM и как сохранить их в Pandas dataframe:
```
from avstockparser.AVStockParser import AVParseToPD as Parser

# Запрашиваем исторические данные по свечам и сохраняем их в переменную Pandas dataframe.
# Если переменная output не указана, то метод AVParseToPD не будет сохранять текстовый файл,
# а только вернёт данные в формате Pandas dataframe.
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
```


Успехов вам в автоматизации биржевой торговли! ;)
