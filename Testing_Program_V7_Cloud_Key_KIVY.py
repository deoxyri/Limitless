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
# DATABASE
from google.cloud.sql.connector import Connector, IPTypes
import os
import sqlalchemy
# ----------------------------------------------------------------------------------------------------------------------
# KIVY - GUI
# ----------------------------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App, Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
# ----------------------------------------------------------------------------------------------------------------------
# DATABASE
from google.cloud.sql.connector import Connector, IPTypes
import os
import sqlalchemy
# ----------------------------------------------------------------------------------------------------------------------
# BUILDER FILE
Builder.load_file("kivy_custom_file.kv")
Builder.load_file("button_config.kv")
# ----------------------------------------------------------------------------------------------------------------------
# DATABASE CONNECTION FUNCTION
# ----------------------------------------------------------------------------------------------------------------------
# CREATE CONNECTION
# ----------------------------------------------------------------------------------------------------------------------
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "X:\Limitless\A - Skeletal Tracking\Keys\service_key_gcloud.json"

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
# WHITE BACKGROUND
Window.clearcolor = (1, 1, 1, 1)
# ----------------------------------------------------------------------------------------------------------------------
# APP - CLASS SETUP
class ImiKami(App):
    def build(self):
        self.window = GridLayout(orientation='tb-lr')
        self.window.cols = 1
        self.window.size_hint = (1, 1)
        self.window.pos_hint = {"centre_x": 0.5, "centre_y": 0.5}
        # --------------------------------------------------------------------------------------------------------------
        # LAYOUT
        # layout = FloatLayout()
        # add widgets to window
        # --------------------------------------------------------------------------------------------------------------
        # Image Widget
        self.window.add_widget(Image(source="Logo Sample 3.png"))
        # --------------------------------------------------------------------------------------------------------------
        # Label Widget
        self.greeting = Label(text="Welcome to the Training Session",
                              font_size=24,
                              font_name='Times.ttf',
                              color='#00000',
                              pos_hint={"center_x": 0.5, "center_y": 0.5}
                              )
        self.window.add_widget(self.greeting)
        # --------------------------------------------------------------------------------------------------------------
        # User Input Text
        # self.user = TextInput(multiline=False,
        #                       padding_y=(20, 20),
        #                       size_hint=(1, 1)
        #                       )
        # self.window.add_widget(self.user)
        # --------------------------------------------------------------------------------------------------------------
        # DROP DOWN MENU
        drop_down = DropDown()
        for index in exercises:
            # now, Add the button in the drop-down list
            drop_button = Button(text='%s' % index, size_hint_y=None, height=30)

            # now we will bind the button for showing the text when it is selected
            drop_button.bind(on_release=lambda btton: drop_down.select(btton.text))

            # then we will add the button inside the drop_down list
            drop_down.add_widget(drop_button)

            # now we will create the big main button
        main_button = Button(text='MENU', pos_hint={"center_x": 0.5, "center_y": 0.5})

        # now, we will first show the drop_down menu when the main button will releases
        # we should note that all of the bind() function calls will pass the instance of the caller
        # as the first argument of the callback (in this program, the main_button instance)
        # now, dropdown.open.
        main_button.bind(on_release=drop_down.open)

        # now we have to do last thing, listen for the selection in the
        # dropdown list and assign the data to the button text.
        drop_down.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))

        # runtouchApp:
        # If we pass only the widget in runtouchApp(), the Window will be
        # created and our widget will be added to that window as the root widget.
        self.window.add_widget(main_button)
        # runTouchApp(main_button)
        # --------------------------------------------------------------------------------------------------------------
        # Button Widget
        # CONFIRM / EXIT BUTTONS
        buttons = [["Confirm", "Exit"], ["Bye", "Hi"]]
        h_layout = BoxLayout()

        button_confirm = Button(
                    text="CONFIRM",
                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
        button_confirm.bind(on_press=self.callback)


        button_exit = Button(
                    text="EXIT",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
        button_exit.bind(on_press=self.close_application)

        h_layout.add_widget(button_confirm)
        h_layout.add_widget(button_exit)


        self.window.add_widget(h_layout)
        # return button_config()
        # --------------------------------------------------------------------------------------------------------------
        return self.window
        # --------------------------------------------------------------------------------------------------------------

    def callback(self, instance):
        self.greeting.text = "You have selected:"

    # method which will render our application
    def close_application(self, instance):
        # closing application
        App.get_running_app().stop()
        # removing window
        Window.close()
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    ImiKami().run()
# ----------------------------------------------------------------------------------------------------------------------
# JOINTS PROVIDED BY API/SDK
joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                      'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']
# LIVE DATA HOLDER - WEBCAM FEED DATA
data_tracking = {}
# ----------------------------------------------------------------------------------------------------------------------
# EXTRACT EXERCISE NAME
ex_name = ImiKami.show()
# PRINT VALUES
print(ex_name)
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

