# pyscraper

This repository contains the source code for a very simple web scraping application. It scrapes the commodity prices from the following two urls:

* [https://www.investing.com/commodities/gold-historical-data](https://www.investing.com/commodities/gold-historical-data)
* [https://www.investing.com/commodities/silver-historical-data](https://www.investing.com/commodities/silver-historical-data)

## Deployment

It is recommended to create a virtual Python environment (I used Anaconda). Then install the packages in the environment:

* `mysql-connector-python`
* `flask`
* `BeautifulSoup4`

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
