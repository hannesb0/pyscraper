# Import libraries
import mysql.connector  # Install mysql-connector-python
from statistics import mean, variance

db = {
    'host'     : 'localhost',
    'database' : 'pyscraper',
    'user'     : 'user',
    'password' : '$a8E21&3ie'
}

# Connect to given database
def connect_db(db):
    connection = mysql.connector.connect(host=db['host'],
                            database=db['database'],
                            user=db['user'],
                            password=db['password'])
    return connection

# Disconnect from given connection handler
def disconnect_db(connection):
    if(connection.is_connected()):
        cursor = connection.cursor()
        cursor.close()
        connection.close()

# Drop given table if it exists
def drop_if_exists(database, connection, table):
    cursor = connection.cursor()
    query = """
            DROP TABLE IF EXISTS {database}.{table};
        """.format(database=database, table=table)
    result = cursor.execute(query)
    connection.commit()
    return result

# Create given table (make sure, it does not already exist)
def create_table(database, connection, table):
    cursor = connection.cursor()
    query = """
            CREATE TABLE {database}.{table}(
            ID    INT NOT NULL AUTO_INCREMENT,
            DATE  DATETIME,
            PRICE DECIMAL(18,2),
            PRIMARY KEY (ID)
            );
        """.format(database=database, table=table)
    result = cursor.execute(query)
    connection.commit()
    return result

# Insert a row (date, price) into given table
def insert_row(database, connection, table, row):
    cursor = connection.cursor()
    query = """
            INSERT INTO {database}.{table} (`date`, `price`) VALUES ('{date}', {price});
        """.format(database=database, table=table, date=row[0], price=row[1])
    result = cursor.execute(query)
    connection.commit()
    return result

# Store scraped price data into database
def store_in_db(data):
    try:
        # Connect to database
        connection = connect_db(db)
        print("Sucessfully connected to database {}".format(db['database']))

        # Create table
        for type in data:
            drop_if_exists(db['database'], connection, type)
            create_table(db['database'], connection, type)
            print ("Sucessfully created table {}".format(type))

            for date, price in data[type]['data'].items():
                insert_row(db['database'], connection, type, [date, price])
            print ("Sucessfully stored data in table {}".format(type))

    except mysql.connector.Error as error :
        # Rollback if any exception occured
        connection.rollback()
        print("Failed storing data into database {}: {}".format(db['database'], error))
    finally:
            # Closing database connection.
            disconnect_db(connection)
            print("MySQL connection is closed")

# Retrieve rows within given date range
def read_between(database, connection, start, end, table):
    cursor = connection.cursor()
    query = """
            SELECT date, price
            FROM {database}.{table}
            WHERE date BETWEEN '{start}' AND '{end}';
    """.format(database=database, start=start, end=end, table=table)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# Retrieve given range for given commodity from database
def retrieve_range(start_date, end_date, commodity_type):

    data = {
        'data' : {},
        'mean' : 0.0,
        'variance' : 0.0,
    }

    try:
        # Connect to database
        connection = connect_db(db)
        print("Sucessfully connected to database {}".format(db['database']))

        # Retrieve rows for given range
        rows = read_between(db['database'], connection, start_date, end_date, commodity_type)

        if len(rows) == 0:
            print ("No data found in the given range ({} - {}) for commodity type {}".format(start_date, end_date, commodity_type))
            return {}

        # Order starting with oldest
        # -> not necessary if result data is stored in dictionary, since dict is unordered
        if rows[0][0] > rows[-1][0]:
            rows.reverse()

        # Populate data dictionary
        for row in rows:
            data['data'].update({row[0].strftime('%Y-%m-%d'):float(row[1])})
        print("Sucessfully read data from {}".format(commodity_type))

    except mysql.connector.Error as error :
        # Rollback if any exception occured
        connection.rollback()
        print("Failed reading data from database {}: {}".format(db['database'], error))
    finally:
            # Closing database connection.
            disconnect_db(connection)
            print("MySQL connection is closed")

    # Calculate mean and variance
    data['mean'] = round(mean([price for price in data['data'].values()]), 2)
    data['variance'] = round(variance([price for price in data['data'].values()]),2)

    return data

# Retrieve all rows for given table
def read_all(database, connection, table):
    cursor = connection.cursor()
    query = """
            SELECT date, price
            FROM {database}.{table};
    """.format(database=database, table=table)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# Retrieve given range for given commodity from database
def retrieve_all(commodity_type):

    data = {
        'data' : {},
        'mean' : 0.0,
        'variance' : 0.0,
    }

    try:
        # Connect to database
        connection = connect_db(db)
        print("Sucessfully connected to database {}".format(db['database']))

        # Retrieve rows for given range
        rows = read_all(db['database'], connection, commodity_type)

        if len(rows) == 0:
            print ("No data found for commodity type {}".format(commodity_type))
            return {}

        # Order starting with oldest
        # -> not necessary if result data is stored in dictionary, since dict is unordered
        if rows[0][0] > rows[-1][0]:
            rows.reverse()

        # Populate data dictionary
        for row in rows:
            data['data'].update({row[0].strftime('%Y-%m-%d'):float(row[1])})
        print("Sucessfully read data from {}".format(commodity_type))

    except mysql.connector.Error as error :
        # Rollback if any exception occured
        connection.rollback()
        print("Failed reading data from database {}: {}".format(db['database'], error))
    finally:
            # Closing database connection.
            disconnect_db(connection)
            print("MySQL connection is closed")

    # Calculate mean and variance
    data['mean'] = round(mean([price for price in data['data'].values()]), 2)
    data['variance'] = round(variance([price for price in data['data'].values()]),2)

    return data
