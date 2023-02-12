# DATABASE
# ----------------------------------------------------------------------------------------------------------------------
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
import nuitrack
import pathlib
# ----------------------------------------------------------------------------------------------------------------------
# GUI - Tkinter
import tkinter as tk
# ----------------------------------------------------------------------------------------------------------------------
# KEYRING
import keyring

# ----------------------------------------------------------------------------------------------------------------------
root = tk.Tk()
# ROOT GEOMETRY
root.geometry("+800+300")  # Position on Screen
canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Exercise Recording Data')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Assign Name to the Exercise Recording:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def exercise_name():
    global ex_num
    ex_num = entry1.get()
    label3 = tk.Label(root, text='Exercise Recording is: ' + ex_num, font=('helvetica', 10))
    canvas1.create_window(200, 250, window=label3)
    return ex_num


# DESTROY GUI WINDOW AFTER EXIT CLICK
def destroy_window():
    canvas1.destroy()

    canvas2 = tk.Canvas(root, width=400, height=400, relief='raised')
    canvas2.pack()

    label5 = tk.Label(root, text='Exercise Name: ' + ex_num + '\nRecording Starts in 3 Seconds', font=('helvetica', 10))
    canvas2.create_window(200, 200, window=label5)

    root.after(3000, lambda: root.destroy())


# LOG EXERCISE BUTTON
button1 = tk.Button(text='Log Exercise', command=exercise_name)
canvas1.create_window(180, 200, window=button1)
ex_num = exercise_name()
# EXIT BUTTON
exit_button = tk.Button(root, text="Exit", command=destroy_window)
canvas1.create_window(240, 200, window=exit_button)

root.mainloop()  # TO RUN THE TKINTER LOOP

ex_name = ex_num.replace(' ', '_')
print(ex_name)

# ----------------------------------------------------------------------------------------------------------------------
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
cwd = os.getcwd()
print(cwd)
# ----------------------------------------------------------------------------------------------------------------------
# SETTING NUITRACK PATHS
current_path = pathlib.Path(__file__).parent.resolve()
print(current_path)

nuitrack_path = rf"{current_path}\nuitrack"
bin_path = nuitrack_path + r"\bin"
data_path = nuitrack_path + r"\data"
middleware_path = nuitrack_path + r"\middleware"

os.environ["PATH"] += os.pathsep + bin_path + os.pathsep + data_path + os.pathsep + middleware_path
# ----------------------------------------------------------------------------------------------------------------------
nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()
# ----------------------------------------------------------------------------------------------------------------------
# INITIALISE AND PRINT DEVICE
devices = nuitrack.get_device_list()
print(devices)
# devices.GetActivationStatus()
# print(devices.GetActivationStatus())

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
# writer = cv2.VideoWriter(f"X:\Limitless\A - Skeletal Tracking\Tracking Programs\Exercise Videos\{video_name}.mp4",
#                          codec, fps, (width, height))
# VIDEO WRITER
# writer = cv2.VideoWriter(f"G:\Limitless\Videos\{video_name}.mp4",
#                          codec, fps, (width, height))
writer = cv2.VideoWriter(f"C:\{video_name}.mp4",
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
user = os.getlogin()
print(user)
# ----------------------------------------------------------------------------------------------------------------------
# CHECKING GCLOUD INSTALLATION
import subprocess
import shutil

gcloud_path = rf"C:\Users\{user}\AppData\Roaming\gcloud"
os.environ["PATH"] = gcloud_path + ";" + os.environ["PATH"]


def check_gcloud_installed():
    return shutil.which("gcloud") is not None


def install_gcloud():
    subprocess.run(["cmd", "/c", "install_gcloud.bat"])


def authenticate_gcloud():
    # subprocess.run(["gcloud", "auth", "application-default", "login"], check=True)
    os.system("gcloud auth application-default login --no browser")


if check_gcloud_installed():
    authenticate_gcloud()
    print("Successfully authenticated with Google Cloud Platform.")
else:
    print("Installing gcloud CLI...")
    install_gcloud()
    print("gcloud CLI installed.")
# ----------------------------------------------------------------------------------------------------------------------
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
