# Import packages
import os
import sys
import subprocess
import pprint
from scraper import scrape_prices
from sql import store_in_db, retrieve_all

# Use the respective input function depending which python version is used
py_version = sys.version_info[0]
def read_usr_input(txt):
    if py_version == 3:
        return input(txt)
    else:
        return raw_input(txt)

# Check if this script is run on Windows
def clear_sreen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

pp = pprint.PrettyPrinter(indent=2)

# Define urls and metal types to be scraped
urls = {
    'gold'   : 'https://www.investing.com/commodities/gold-historical-data',
    'silver' : 'https://www.investing.com/commodities/silver-historical-data',
}

data = None
db_data = None
api_status = False
LOG_FILE = 'log.log'

# Clear terminal
clear_sreen()

# Start menu
while True:
    print("=================================================")
    print("|  >>>          Python Web Scraper         <<<  |")
    print("=================================================")
    print("| Scrape data from web pages: . . . . . . . [1] |")
    print("| Show data:  . . . . . . . . . . . . . . . [2] |")
    print("| Store data in database: . . . . . . . . . [3] |")
    print("| Load gold prices from database: . . . . . [4] |")
    print("| Load silver prices from database: . . . . [5] |")
    print("| Start API web-servie: . . . . . . . . . . [6] |")
    print("| Stop API web-servie:  . . . . . . . . . . [7] |")
    print("| End application:  . . . . . . . . . . . . [x] |")
    print("=================================================")
    print("| Status:                                       |")
    print("| - Scraped data available:  [{}]                |"
        .format('X' if data != None else ' '))
    print("| - API web-service running: [{}]                |"
    .format('X' if api_status else ' '))
    #print("| Python {}.x".format(py_version))
    print("=================================================")

    # Wait for user input
    try:
        i = read_usr_input('> ')#input("> ")
    except:
        clear_sreen()
        i = '00'
        continue

    # Option 1: Scrape data from web pages
    if i == '1':
        print('Scraping data...')
        data = scrape_prices(urls)
        clear_sreen()
        continue

    # Option 2: Show scraped data
    elif i == '2':
        print('Scraped data:\n')
        pp.pprint(data)

    # Option 3: Store data in database
    elif i == '3':
        if data != None:
            print('Storing data into MYSQL database.')
            store_in_db(data)
        else:
            print('No data available to be stored, please scrape data first.')

    # Option 4: Load gold data from database
    elif i == '4':
        print('Loading gold prices from database.')
        db_data = retrieve_all('gold')
        print('Gold prices:')
        pp.pprint(db_data)

    # Option 5: Load silver data from database
    elif i == '5':
        print('Loading silver prices from database.')
        db_data = retrieve_all('silver')
        print('Silver prices:')
        pp.pprint(db_data)

    # Option 6: Starting API web-service
    elif i == '6':
        print('Starting API web-service.')

        my_env = os.environ.copy()
        my_env["FLASK_APP"] = 'web.py'
        my_env["FLASK_ENV"] = 'development'
        cmd = ["flask", "run", "--port=8080"]

        with open(LOG_FILE, "a") as outfile:
            subprocess.Popen(cmd, env=my_env, stdout=outfile, stderr=outfile)

        api_status = True

    # Option 7: Stopping API web-service
    elif i == '7':
        print('Stopping API web-service.')
        cmd = 'killall flask'
        os.system(cmd)
        api_status = False

    # End program
    elif i == 'x' or i == 'X':
        clear_sreen()

        # Kill any open flask sessions
        cmd = 'killall flask'
        os.system(cmd)

        # Break the loop and thus end the menu
        break

    # Wrong input
    else:
        print("\nWrong input!")

    try:
        read_usr_input("\nPlease press ENTER to continue.")
    except:
        print("")

    # Clear terminal
    clear_sreen()

# End of menu
