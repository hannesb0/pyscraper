# pyscraper

This repository contains the source code for a very simple web scraping application. It scrapes the commodity prices from the following two urls:

* [https://www.investing.com/commodities/gold-historical-data](https://www.investing.com/commodities/gold-historical-data)
* [https://www.investing.com/commodities/silver-historical-data](https://www.investing.com/commodities/silver-historical-data)

## Deployment

It is recommended to create a virtual Python environment (I used Anaconda). Then install the packages in the environment:

* `mysql-connector-python`
* `flask`
* `BeautifulSoup4`

In the scope of this project, a MySQL database server has to be running on the local machine. These are the settings used to connect to the MySQL database:

    'host'     : 'localhost',
    'database' : 'pyscraper',
    'user'     : 'user',
    'password' : '$a8E21&3ie'

To run the application, just execute the script `menu.py`. And this menu will be presented to you: 

    =================================================
    |  >>>          Python Web Scraper         <<<  |
    =================================================
    | Scrape data from web pages: . . . . . . . [1] |
    | Show data:  . . . . . . . . . . . . . . . [2] |
    | Store data in database: . . . . . . . . . [3] |
    | Load gold prices from database: . . . . . [4] |
    | Load silver prices from database: . . . . [5] |
    | Start API web-servie: . . . . . . . . . . [6] |
    | Stop API web-servie:  . . . . . . . . . . [7] |
    | End application:  . . . . . . . . . . . . [x] |
    =================================================
    | Status:                                       |
    | - Scraped data available:  [ ]                |
    | - API web-service running: [ ]                |
    =================================================
    >

To test the web API, just paste one of the following URLs into your browser, change the start and end data respectively:

* [http://127.0.0.1:8080/commodity?start_date=2019-05-05&end_date=2019-05-10&commodity_type=gold](http://127.0.0.1:8080/commodity?start_date=2019-05-05&end_date=2019-05-10&commodity_type=gold)
* [http://127.0.0.1:8080/commodity?start_date=2019-05-05&end_date=2019-05-10&commodity_type=silver[(ttp://127.0.0.1:8080/commodity?start_date=2019-05-05&end_date=2019-05-10&commodity_type=silver)

The response will look something like this:

        {'data': {'2019-05-05': 1285.85, '2019-05-06': 1284.15, '2019-05-07': 1286.05, '2019-05-08': 1282.25, '2019-05-09': 1284.55, '2019-05-10': 1286.7}, 'mean': 1284.92, 'variance': 2.63}
