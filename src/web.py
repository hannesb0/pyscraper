from flask import Flask
from flask import request
import logging
from .sql import retrieve_range

# Set up logger
hdlr = logging.FileHandler('log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)

# Set up Flask app
app = Flask(__name__)
app.debug=True
app.logger.addHandler(hdlr)

# Handle API requests
@app.route("/commodity", methods=['GET'])
def commodity():
    query = {}
    query['start_date'] = request.args.get('start_date')
    query['end_date'] = request.args.get('end_date')
    query['commodity_type'] = request.args.get('commodity_type')

    result = retrieve_range(query['start_date'], query['end_date'], query['commodity_type'])

    return str(result)



# Start flask app through the terminal with this command:

"""
 $ FLASK_APP=web.py FLASK_ENV=development flask run
"""

# Use this URL:

"""
http://127.0.0.1:8080/commodity?start_date=2019-05-05&end_date=2019-05-10&commodity_type=gold
"""
