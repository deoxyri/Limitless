# SKELETON TRACKING LIBRARY
from PyNuitrack import py_nuitrack
# ----------------------------------------------------------------------------------------------------------------------
# GENERAL LIBRARIES
import cv2
from itertools import cycle
import numpy as np
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------
# APP PROGRAM
# ----------------------------------------------------------------------------------------------------------------------
# DRAWING POINTS PROGRAMS IMPORT
# from SkeletonDetection_Test import *
# from red_dot_test import *
# from red_dot_pause_test_function import *
# from red_dot_tracking_db_data import * # RED DOT FOR SINGLE JOINT WITH ARROW
# from red_dot_all_joints_test_db_data import *  # RED DOT FOR ALL JOINTS WITH ARROWS
from red_dot_no_arrows_db_data import *  # RED DOT FOR ALL JOINTS WITH NO ARROWS
# ----------------------------------------------------------------------------------------------------------------------
# FUNCTION TEST
from var_holder_return_function import *
# ----------------------------------------------------------------------------------------------------------------------
# GUI LIBRARIES
import tkinter as tk
from tkinter import *
from tkinter import ttk
# ----------------------------------------------------------------------------------------------------------------------
# DATABASE
from google.cloud.sql.connector import Connector, IPTypes
import os
import sqlalchemy

# ----------------------------------------------------------------------------------------------------------------------
# DATABASE CONNECTION FUNCTION
# ----------------------------------------------------------------------------------------------------------------------
# CREATE CONNECTION
# ----------------------------------------------------------------------------------------------------------------------
user = os.getlogin()
print(user)

os.system("gcloud auth application-default login")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    rf"C:\Users\{user}\AppData\Roaming\gcloud\application_default_credentials.json"

INSTANCE_CONNECTION_NAME = f"applied-craft-372501:australia-southeast2:imikami-demo-v1"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "postgres"
DB_PASS = "Limitless@96"
DB_NAME = "postgres"

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
        enable_iam_auth=True
    )
    return conn


# ----------------------------------------------------------------------------------------------------------------------
# WRITING DATA INTO DATABASE
# ----------------------------------------------------------------------------------------------------------------------
# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)
# ----------------------------------------------------------------------------------------------------------------------
table_name_query = """SELECT table_name
FROM information_schema.tables
WHERE table_type='BASE TABLE'
AND table_schema='public'"""

# connect to connection pool
with pool.connect() as db_conn:
    table_names = db_conn.execute(table_name_query).fetchall()

# EXTRACTING UNIQUE EXERCISE NAMES FROM DATA TABLES
table_names.sort()
drop_down_data = (table_names[0:len(table_names) // 20])
exercises = []
print(exercises)

for strings in drop_down_data:
    strings = list(strings)
    strings = ' '.join([str(elem) for elem in strings])

    exercise_name = strings.replace("head_data_", "")
    exercise_name = exercise_name.replace("head_data", "SELECT FROM BELOW")
    exercise_name = exercise_name.replace("_", " ")
    exercises.append(exercise_name)

# CAPITALISING FIRST LETTER - FOR A BETTER UI/UX
exercises = [x.title() for x in exercises]
print(exercises)
# ----------------------------------------------------------------------------------------------------------------------
# DROP DOWN MENU - EXERCISE SELECTION
# CREATE TKINTER OBJECT
root = Tk()

# ROOT GEOMETRY
root.geometry("+800+300")  # Position on Screen
canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

# SAY 'HI!'
label1 = tk.Label(root, text='HOLA!')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

# INTRODUCTION
label2 = tk.Label(root, text='Welcome to Your Training Session!\n\n What would you like to focus on today?')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

# DROPDOWN MENU OPTIONS
options = exercises
# DATATYPE FOR THE DROPDOWN MENU AND INITIAL VALUE
clicked = tk.StringVar(root, "Select an Exercise from Below")

# COMBOBOX CREATION
combobox = ttk.Combobox(root, textvariable=clicked, state="readonly")
combobox['values'] = options
canvas1.create_window(200, 150, window=combobox)
combobox.current(0)


# TAKE COMBOX INPUT
def show():
    global ex_name
    # ex_name = entry1.get()
    ex_name = combobox.get()
    label4 = tk.Label(root, text='Confirm Exercise and Exit Window to Continue', font=('helvetica', 10))
    canvas1.create_window(200, 250, window=label4)

    return ex_name


# DESTROY GUI WINDOW AFTER EXIT CLICK
def destroy_window():
    canvas1.destroy()

    canvas2 = tk.Canvas(root, width=400, height=400, relief='raised')
    canvas2.pack()

    label5 = tk.Label(root, text='Starting Exercise ' + ex_name + ' in 3 Seconds', font=('helvetica', 10))
    canvas2.create_window(200, 200, window=label5)

    root.after(3000, lambda: root.destroy())


# MISC BUTTONS
# CONFIRM BUTTON
button2 = tk.Button(root, text="Confirm", command=show)
canvas1.create_window(170, 200, window=button2)

# EXIT BUTTON
exit_button = tk.Button(root, text="Exit", command=destroy_window)
canvas1.create_window(230, 200, window=exit_button)

# EXTRACT EXERCISE NAME
ex_name = show()
# EXECUTE TKINTER LOOP
root.mainloop()
# PRINT VALUES
print(ex_name)

# ----------------------------------------------------------------------------------------------------------------------
# JOINTS PROVIDED BY API/SDK
joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                      'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']
# LIVE DATA HOLDER - WEBCAM FEED DATA
data_tracking = {}
# ----------------------------------------------------------------------------------------------------------------------
# REVERTING NAMES BACK TO REFLECT DATABASE NAME STRUCTURE
ex_name = ex_name.replace(" ", "_")
# ----------------------------------------------------------------------------------------------------------------------
# RECORDED DATA HOLDER
var_joints_recorded_data = {}
# EXTRACTING VALUES FROM DATABASE BASED ON EXERCISE NAME
i = 0
while i < len(joints_description):
    with pool.connect() as db_conn:
        select_data_database_query = f"""SELECT x_location,y_location,depth FROM {joints_description[i]}_data_{ex_name}"""
        # EXTRACTING TABLE NAMES
        data_database_values = db_conn.execute(select_data_database_query).fetchall()
        var_joints_recorded_data[joints_description[i] + '_df'] = data_database_values

    i += 1
# ----------------------------------------------------------------------------------------------------------------------
# INITIALISE DEVICE
nuitrack = py_nuitrack.Nuitrack()

# nuitrack.init(r"./nuitrack/data/nuitrack.config")
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

        window_name = "Exercise"
        cv2.namedWindow(window_name)
        cv2.moveWindow(window_name, 700, 250)
        cv2.imshow(window_name, img_color)

    counter += 1

    # Break loop on 'Esc'
    if key == 27:
        break

nuitrack.release()
connector.close()
