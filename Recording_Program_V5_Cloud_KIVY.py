# IN DEVELOPMENT
# TO DO
# VERSION 6
# ----------------------------------------------------------------------------------------------------------------------
# DATABASE
from google.cloud.sql.connector import Connector, IPTypes
import os
import sqlalchemy
# ----------------------------------------------------------------------------------------------------------------------
import numpy as np
from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
# OTHER LIBRARIES
from data_write_program import *
from operator import attrgetter
# DRAWING POINTS
# from FaceDetection import *
from SkeletonDetection import *
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
from kivy.properties import StringProperty, ObjectProperty
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
        sm = ScreenManager()
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
        # --------------------------------------------------------------------------------------------------------------
        # User Input Text
        self.user = TextInput(multiline=False,
                              padding_y=(20, 20),
                              size_hint=(1, 1)
                              )
        self.window.add_widget(self.user)

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
        # --------------------------------------------------------------------------------------------------------------
        return self.window

    def callback(self, instance):
        if __name__ == '__main__':
            self.greeting.text = "You have selected:" + self.main_button.text
            ex_name = self.main_button.text
            print(ex_name)
            return self.main_button.text

    def close_application(self, instance):
        # closing application
        App.get_running_app().stop()
        # removing window
        Window.close()


# ----------------------------------------------------------------------------------------------------------------------
# RECORDING PROGRAM CLASS SETUP
class RecordingProgram(Widget):


 # JOINTS KEY HOLDER
 var_holder = {}
 var_joint_data_holder = {'data_head_df': {},
                         'data_neck_df': {},
                         'data_torso_df': {},
                         'data_waist_df': {},
                         'data_left_collar_df': {},
                         'data_left_shoulder_df': {},
                         'data_left_elbow_df': {},
                         'data_left_wrist_df': {},
                         'data_left_hand_df': {},
                         'data_right_collar_df': {},
                         'data_right_shoulder_df': {},
                         'data_right_elbow_df': {},
                         'data_right_wrist_df': {},
                         'data_right_hand_df': {},
                         'data_left_hip_df': {},
                         'data_left_knee_df': {},
                         'data_left_ankle_df': {},
                         'data_right_hip_df': {},
                         'data_right_knee_df': {},
                         'data_right_ankle_df': {},
                         }
 # ----------------------------------------------------------------------------------------------------------------------
 # JOINT DESCRIPTIONS
 joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow',
                      'left_wrist', 'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']
 # ----------------------------------------------------------------------------------------------------------------------
 # INITIALISE NUITRACK
 nuitrack = py_nuitrack.Nuitrack()
 nuitrack.init()
 # ----------------------------------------------------------------------------------------------------------------------
 # INITIALISE AND PRINT DEVICE
 devices = nuitrack.get_device_list()

 for i, dev in enumerate(devices):
    if i == 0:
        nuitrack.set_device(dev)

 nuitrack.create_modules()
 nuitrack.run()

 # SETTING DEPTH AND COLOR MODES
 modes = cycle(["depth", "color"])
 mode = next(modes)
 # ----------------------------------------------------------------------------------------------------------------------
 # VIDEO CAPTURE
 cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

 # VIDEO CONFIGURATION
 width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
 height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
 fps = cap.get(cv2.CAP_PROP_FPS)
 codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
 video_name = ex_name

 # VIDEO WRITER
 writer = cv2.VideoWriter(f"X:\Limitless\A - Skeletal Tracking\Tracking Programs\Exercise Videos\{video_name}.mp4",
                         codec, fps, (width, height))

 # LOOP
 while 1:
    key = cv2.waitKey(1)
    nuitrack.update()
    data = nuitrack.get_skeleton()
    img_color = nuitrack.get_color_data()

    # READING FRAME-BY-FRAME
    # ret, frame = cap.read()

    if img_color.size:
        draw_skeleton(img_color, data)

        writer.write(img_color)

        window_name = "Exercise Recording"
        cv2.namedWindow(window_name)
        cv2.moveWindow(window_name, 700, 250)
        cv2.imshow(window_name, img_color)

        # LOOP FOR WRITING DATA

    for skeleton in data.skeletons:
        i = 0
        while i < len(joints_description):
            var_holder['data_' + joints_description[i]] = attrgetter('{}.projection'.format(joints_description[i]))(
                skeleton)
            i += 1

        locals().update(var_holder)

        # CONVERT DICT TO LIST TO ACCESS KEYS
        keys_var_holder = list(var_holder)
        # CONCAT DATA OF JOINTS(KEYS) TO DICT
        j = 0
        while j < len(keys_var_holder):
            var_joint_data_holder['data_' + joints_description[j] + '_df'] = \
                data_write_program(var_joint_data_holder['data_' + joints_description[j] + '_df'],
                                   var_holder[keys_var_holder[j]])  # KEY CALLED FROM CONVERTED LIST
            j += 1

    # Break loop on 'Esc'
    if key == 27:
        break

 # Release everything if job is finished
 nuitrack.release()
 cap.release()
 writer.release()
 cv2.destroyAllWindows()
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
 # connect to connection pool
 with pool.connect() as db_conn:
    # LOOP ALL TABLES TO BE CREATED IN DATABASE - IF TABLES NOT FOUND
    i = 0
    while i < len(joints_description):
        db_conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {joints_description[i]}_data_{ex_name} (
            id SERIAL PRIMARY KEY,
            x_location REAL,
            y_location REAL,
            depth REAL
           )
           """
        )
        # --------------------------------------------------------------------------------------------------------------
        var_joint_data_holder['data_' + joints_description[i] + '_df'] = \
            var_joint_data_holder['data_' + joints_description[i] + '_df'].transpose()

        # CONVERTING TO TUPLE
        joint_data = [tuple(x) for x in var_joint_data_holder['data_' + joints_description[i] + '_df'].to_numpy()]
        print(joint_data)
        print(len(joint_data))
        print(len(joint_data[0]))
        # --------------------------------------------------------------------------------------------------------------
        # insert data into our ratings table
        insert_stmt = sqlalchemy.text(
            f"""INSERT INTO {joints_description[i]}_data_{ex_name}
            (x_location, y_location, depth)
             VALUES (:x_location, :y_location, :depth)""",
        )
        # DELETE QUERY
        delete_query = f"DELETE FROM {joints_description[i]}_data_{ex_name}"
        # --------------------------------------------------------------------------------------------------------------
        # DELETE OLD DATA
        db_conn.execute(delete_query)
        # DATA INSERT LOOP - OVERWRITING
        j = 0
        while j < len(joint_data):
            db_conn.execute(insert_stmt, x_location=joint_data[j][0],
                            y_location=joint_data[j][1],
                            depth=joint_data[j][2])
            j += 1
        # --------------------------------------------------------------------------------------------------------------
        i += 1
 connector.close()

# ----------------------------------------------------------------------------------------------------------------------
# method which will render our application
if __name__ == "__main__":
    ImiKami().run()
    I = ImiKami()
