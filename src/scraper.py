# Import libraries
from bs4 import BeautifulSoup   # Install BeautifulSoup4
from urllib.request import Request, urlopen
from statistics import variance
from datetime import datetime

#dt = datetime.strptime('May 10, 2019', '%b %d, %Y')
#st = dt.strftime('%Y-%m-%d')

# Scrape the rows from a table with a given ID
def get_rows(url, table_id):
    # Read html from given url
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()

    # Parse the html using beautiful soup and store in variable soup
    soup = BeautifulSoup(page, 'html.parser')

    # Retrieve the table body containing the prices
    table = soup.find('table', attrs={'class': table_id})
    table_body = table.find('tbody')

    # Retrieve the rows from the table body
    return table_body.find_all('tr')

# Return the columns from a given bs4.element.Tag object containing a row of a table
def get_cols(row):
    # Create a list containing a bs4.element.Tag object for every element in the current row
    cols = row.find_all('td')
    # Return a list containing only the text for every cell in the current row
    return [cell.text.strip() for cell in cols]

# Scrape the prices for the given metal type and the respective url
def scrape_prices(urls):
    # Dictionary containing the scraped data as Python dictionary
    data = {}

    # Scrape the data
    for type, url in urls.items():
        # Retrieve the rows from the table containing the prices of the given metal type
        price_rows = get_rows(url, 'genTbl closedTbl historicalTbl')

        # Add the current type
        data.update({
            type:{
                'data': {},
                'mean': 0.0,
                'variance': 0.0,
            }
        })

        # Cycle through rows and store date and price
        for row in price_rows:
            # Get a list containing only the text for every cell in the current row
            cols = get_cols(row)

            # Transfor date from 'May 10, 2019' to '2019-05-10'
            dt = datetime.strptime(cols[0], '%b %d, %Y')
            cols[0] = dt.strftime('%Y-%m-%d')

            # Add first cell (containing the date) and second cell (containing the price)
            data[type]['data'].update({cols[0]:float(cols[1].replace(',',''))})

        # Retrieve the table body containing the statistics (low, high, mean, change)
        # This table contains only one row
        stats_row = get_rows(url, 'genTbl closedTbl historicalTblFooter')[0]

        # Transform each cell from format like 'Highest: 1,307.10' to ['Highest', '1307.10']
        stats = [[c.strip().replace(',','') for c in cell.split(':')] for cell in get_cols(stats_row)]

        # Transform the number values from string to float and store stats in dictionary
        stats = {e[0]:float(e[1]) for e in stats}

        # Add mean value
        data[type]['mean'] = stats['Average']

        # Add variance of prices (rounded on two decimals)
        data[type]['variance'] = round(variance([price for price in data[type]['data'].values()]),2)

    # Return data as Python dictionary
    return(data)
