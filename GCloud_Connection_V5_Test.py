#### Import Python libraries ####
import sqlite3
from google.cloud import storage
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys
import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import os
import sqlalchemy
# ----------------------------------------------------------------------------------------------------------------------
#from google.colab import auth
#auth.authenticate_user()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "X:\Limitless\A - Skeletal Tracking\Keys\service_key_gcloud.json"

INSTANCE_CONNECTION_NAME = f"applied-craft-372501:australia-southeast2:imikami-demo-v1"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "postgres"
DB_PASS = "Limitless@96"
DB_NAME = "postgres"
# ----------------------------------------------------------------------------------------------------------------------
# initialize Connector object
connector = Connector()
# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        enable_iam_auth = True
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
  # create ratings table in our movies database
  db_conn.execute(
      "CREATE TABLE IF NOT EXISTS Movies "
      "( id SERIAL NOT NULL, title VARCHAR(255) NOT NULL, "
      "genre VARCHAR(255) NOT NULL, rating FLOAT NOT NULL, "
      "PRIMARY KEY (id));"
  )
  # insert data into our ratings table
  insert_stmt = sqlalchemy.text(
      "INSERT INTO ratings (title, genre, rating) VALUES (:title, :genre, :rating)",
  )

  # insert entries into table
  db_conn.execute(insert_stmt, title="Batman Begins", genre="Action", rating=8.5)
  db_conn.execute(insert_stmt, title="Star Wars: Return of the Jedi", genre="Action", rating=9.1)
  db_conn.execute(insert_stmt, title="The Breakfast Club", genre="Drama", rating=8.3)

  # query and fetch ratings table
  results = db_conn.execute("SELECT * FROM ratings").fetchall()

  # show results
  for row in results:
    print(row)

connector.close()