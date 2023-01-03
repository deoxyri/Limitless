# DATABASE
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import register_adapter, AsIs
from google.cloud.sql.connector import Connector
import sqlalchemy
import os
import numpy
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------
def create_connection(db_name, db_user, db_password, db_host, db_port,ssl_cert, ssl_key, root_cert):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            sslmode = 'require',
            sslcert = ssl_cert,
            sslkey = ssl_key,
            sslrootcert = root_cert
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection
# ----------------------------------------------------------------------------------------------------------------------
# FUNCTION TO EXECUTE QUERIES
def execute_query(connection, query):
    # connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
# ----------------------------------------------------------------------------------------------------------------------
# READING DATABASE DATA
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")
# ----------------------------------------------------------------------------------------------------------------------
# ENTERING VALUES INTO THE DATABASE
# ssl_cert = 'X:\Limitless\A - Skeletal Tracking\Tracking \client-cert.pem'
# ssl_key = 'X:\Limitless\A - Skeletal Tracking\Tracking \client-key.pem'
# root_cert = 'X:\Limitless\A - Skeletal Tracking\Tracking \server-ca.pem'

ssl_cert = 'client-cert.pem'
ssl_key = 'client-key.pem'
root_cert = 'server-ca.pem'

connection = create_connection("postgres", "postgres", "Limitless@96", "34.129.78.3", "5432",ssl_cert,ssl_key,root_cert)
# ----------------------------------------------------------------------------------------------------------------------
# LOOP ALL TABLES TO BE CREATED IN DATABASE - IF TABLES NOT FOUND
# create_table = f"""
#      CREATE TABLE IF NOT EXISTS test_data (
#      id SERIAL PRIMARY KEY,
#      x_location REAL,
#      y_location REAL,
#      depth REAL
#     )
#     """

create_table = f"""CREATE TABLE Persons (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255))"""
execute_query(connection, create_table)
# ----------------------------------------------------------------------------------------------------------------------
# READING EXISTING DATA
select_data_database_query = f"""SELECT title,genre,rating FROM ratings"""
# EXTRACTING TABLE NAMES
# connection.autocommit = True
cursor = connection.cursor()
cursor.execute(select_data_database_query)
data_database_values = cursor.fetchall()

tables_list = f"""
SELECT table_schema,table_name
FROM information_schema.tables
ORDER BY table_schema,table_name;
"""
cursor.execute(tables_list)
table_names = cursor.fetchall()
print(table_names)

create_table = f"""
CREATE TABLE head_data_test (
id SERIAL PRIMARY KEY,
x_location REAL,
y_location REAL,
depth REAL)
"""

cursor.execute(create_table)

tables_list_new = f"""
SELECT table_schema,table_name
FROM information_schema.tables
ORDER BY table_schema,table_name;
"""
cursor.execute(tables_list)
table_names_new = cursor.fetchall()
print(table_names_new)

# ----------------------------------------------------------------------------------------------------------------------
test_values = {}
test_values['sample'] = data_database_values
print(test_values)
# ----------------------------------------------------------------------------------------------------------------------
# CLOSE CONNECTION
connection.close()