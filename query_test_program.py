# DATABASE
from tkinter import ttk

import psycopg2
from PIL._imagingmorph import apply
from psycopg2 import OperationalError
import numpy as np
import tkinter as tk
from tkinter import *


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection("limitless_v1", "postgres", "Limitless@96", "127.0.0.1", "5432")


# CREATE DATABASE FUNCTION
def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# create_database_query = "CREATE DATABASE Limitless_V1"

# FUNCTION TO EXECUTE QUERIES
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


table_name_query = """SELECT table_name
FROM information_schema.tables
WHERE table_type='BASE TABLE'
AND table_schema='public'"""

# EXTRACTING TABLE NAMES
connection.autocommit = True
cursor = connection.cursor()
cursor.execute(table_name_query)
table_names = cursor.fetchall()

# EXTRACTING UNIQUE EXERCISE NAMES FROM DATA TABLES
table_names.sort()
drop_down_data = (table_names[0:len(table_names) // 20])
exercises = []

for strings in drop_down_data:
    strings = list(strings)
    strings = ' '.join([str(elem) for elem in strings])

    exercise_name = strings.replace("head_data_", "")
    exercise_name = exercise_name.replace("head_data", "SELECT FROM BELOW")
    exercise_name = exercise_name.replace("_", " ")
    exercises.append(exercise_name)

print(exercises)
# ----------------------------------------------------------------------------------------------------------------------
# DROP DOWN MENU - EXERCISE SELECTION
# Create object
root = Tk()
# Adjust size
# root.geometry("400x400")
canvas1 = tk.Canvas(root, width=400, height=400, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Hola!')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='What would you like to focus on today?')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

# CAPITALISING FIRST LETTER - FOR A BETTER UI/UX
exercises = [x.title() for x in exercises]

# DROPDOWN MENU OPTIONS
options = exercises
# DATATYPE FOR THE DROPDOWN MENU AND INITIAL VALUE
clicked = StringVar(root, "Select an Exercise")

# DATA TO BE ENTERED - ENTRY ATTRIBUTE
entry1 = tk.Entry(root, textvariable=clicked)
canvas1.create_window(200, 150, window=entry1)

# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.pack()  # PACK IS USED TO ORGANISE WIDGETS BEFORE PLACING THEM IN THE CANVAS
canvas1.create_window(200, 200, window=drop)


# Change the label text
def show():
    # label.config(text=clicked.get())
    global ex_name
    ex_name = entry1.get()
    label3 = tk.Label(root, text='Start Exercise: ' + ex_name, font=('helvetica', 10))
    canvas1.create_window(200, 300, window=label3)
    return ex_name


button2 = tk.Button(root, text="Vamos!", command=show)

label4 = tk.Label(root, text="Vamos!")
label4.config(font=('helvetica', 10))
canvas1.create_window(200, 250, window=button2)

# EXTRACT EXERCISE NAME
ex_name = show()
# EXECUTE TKINTER LOOP
root.mainloop()
# PRINT VALUES
print(ex_name)
