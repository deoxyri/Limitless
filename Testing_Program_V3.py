from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import pandas as pd

# DRAWING POINTS
# from SkeletonDetection_Test import *
# from red_dot_test import *
# from red_dot_pause_test_function import *
# from red_dot_tracking_db_data import * # RED DOT FOR SINGLE JOINT WITH ARROW
# from red_dot_all_joints_test_db_data import *  # RED DOT FOR ALL JOINTS WITH ARROWS
from red_dot_no_arrows_db_data import *  # RED DOT FOR ALL JOINTS WITH NO ARROWS
# FUNCTION TEST
from var_holder_return_function import *
# ----------------------------------------------------------------------------------------------------------------------
# DATABASE
import psycopg2
from PIL._imagingmorph import apply
from psycopg2 import OperationalError
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import ttk
from psycopg2.extensions import register_adapter, AsIs


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


# ----------------------------------------------------------------------------------------------------------------------
# ADAPTING DIFFERENT DATA TYPES TO DATABASE
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


# REGISTERING np datatypes TO DATABASE
register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)
register_adapter(np.float32, addapt_numpy_float32)

# CONNECTING TO DATABASE
connection = create_connection("limitless_v1", "postgres", "Limitless@96", "127.0.0.1", "5432")
# ----------------------------------------------------------------------------------------------------------------------
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
root.geometry("+800+300")  # Position on Screen
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
clicked = tk.StringVar(root, "Select an Exercise from Below")

# DATA TO BE ENTERED - ENTRY ATTRIBUTE
# entry1 = tk.Entry(root, textvariable=clicked)
# canvas1.create_window(200, 150, window=entry1)

# Create Dropdown menu
# drop = OptionMenu(root, clicked, *options)
# drop.pack()  # PACK IS USED TO ORGANISE WIDGETS BEFORE PLACING THEM IN THE CANVAS
# canvas1.create_window(200, 200, window=drop)

# Create a Combobox
combobox = ttk.Combobox(root, textvariable=clicked, state="readonly")
combobox['values'] = options
canvas1.create_window(200, 200, window=combobox)
combobox.current(2)
# combobox.pack(pady=30, ipadx=20)


# Change the label text
def show():
    global ex_name
    # ex_name = entry1.get()
    ex_name = combobox.get()
    label4 = tk.Label(root, text='Exit Window to Continue', font=('helvetica', 10))
    canvas1.create_window(200, 350, window=label4)
    return ex_name


def destroy_window():
    canvas1.destroy()

    canvas2 = tk.Canvas(root, width=400, height=400, relief='raised')
    canvas2.pack()

    label5 = tk.Label(root, text='Starting Exercise ' + ex_name + ' in 3 Seconds', font=('helvetica', 10))
    canvas2.create_window(200, 200, window=label5)

    root.after(3000, lambda: root.destroy())


button2 = tk.Button(root, text="Vamos!", command=show)
canvas1.create_window(180, 250, window=button2)

# Button for closing
exit_button = tk.Button(root, text="Exit", command=destroy_window)
canvas1.create_window(230, 250, window=exit_button)

# EXTRACT EXERCISE NAME
ex_name = show()
# EXECUTE TKINTER LOOP
root.mainloop()
# PRINT VALUES
print(ex_name)

# ----------------------------------------------------------------------------------------------------------------------
joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                      'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']
# LIVE DATA HOLDER
data_tracking = {}
# ----------------------------------------------------------------------------------------------------------------------
# DATABASE DATA HOLDER
data_database = {}
ex_name = ex_name.replace(" ", "_")

select_data_database_query = f"""SELECT * FROM {joints_description[0]}_data_{ex_name}"""
# EXTRACTING TABLE NAMES
connection.autocommit = True
cursor = connection.cursor()
cursor.execute(select_data_database_query)
data_database_values_test = cursor.fetchall()
# print(data_database_values)
# ----------------------------------------------------------------------------------------------------------------------
# RECORDED DATA
var_joints_recorded_data = {}

i = 0
while i < len(joints_description):

    select_data_database_query = f"""SELECT x_location,y_location,depth FROM {joints_description[i]}_data_{ex_name}"""
    # EXTRACTING TABLE NAMES
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(select_data_database_query)
    data_database_values = cursor.fetchall()
    var_joints_recorded_data[joints_description[i] + '_df'] = data_database_values

    i += 1

# print(len(var_joints_recorded_data))
# print(var_joints_recorded_data)
# print(pd.DataFrame(var_joints_recorded_data['head_df']))

# RECORDED DATA
data_recorded = data_recorded_head = pd.DataFrame(var_joints_recorded_data['head_df'])

data_size = data_recorded.size / 3

counter = 0

# print(data_recorded.iat[0, counter])
# print(data_size)
# ----------------------------------------------------------------------------------------------------------------------
# DATA IN TABLES ON SYSTEM
# i = 0
# while i < len(joints_description):
#     var_joints_recorded_data[joints_description[i] + '_df'] = pd.read_excel(
#         'X:\Limitless\A - Skeletal Tracking\Tracking Programs\{}_Data.xlsx'.format(joints_description[i]))
#     i += 1
# ----------------------------------------------------------------------------------------------------------------------
# INITIALISE DEVICE
nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()
devices = nuitrack.get_device_list()

# DEVICE NAME, ID etc...
for i, dev in enumerate(devices):
    if i == 0:
        nuitrack.set_device(dev)

nuitrack.create_modules()
nuitrack.run()

modes = cycle(["depth", "color"])
mode = next(modes)

# START COMPARISON
counter = 0
while counter >= 0:
    key = cv2.waitKey(1)
    nuitrack.update()
    data = nuitrack.get_skeleton()
    data_instance = nuitrack.get_instance()
    img_depth = nuitrack.get_depth_data()

    var_joints_live_data = var_holder_return_function(data, joints_description)
    keys = list(var_joints_live_data)

    i = 0
    while i < len(keys):
        data_tracking['{}'.format(joints_description[i])] = var_joints_live_data['data_' + joints_description[i]]
        i += 1

    # DRAWING LOOP
    img_color = nuitrack.get_color_data()
    if img_color.size:
        # COMPARE LIVE DATA WITH RECORDED DATA (COLOUR) #
        draw_skeleton_test(img_color, var_joints_recorded_data, data_tracking, counter)

        cv2.imshow('Image', img_color)

    counter += 1

    # Break loop on 'Esc'
    if key == 27:
        break

nuitrack.release()
