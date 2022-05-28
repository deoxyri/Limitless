# DATABASE
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import register_adapter, AsIs
# ----------------------------------------------------------------------------------------------------------------------
import numpy as np
from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
# OTHER LIBRARIES
from data_write_program import *
from operator import attrgetter
# DRAWING POINTS
from FaceDetection import *
from SkeletonDetection import *
# ----------------------------------------------------------------------------------------------------------------------
# GUI - Tkinter
import tkinter as tk

root = tk.Tk()
canvas1 = tk.Canvas(root, width=400, height=300,  relief='raised')
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
    canvas1.create_window(200, 210, window=label3)
    return ex_num


button1 = tk.Button(text='Log Exercise Recording', command=exercise_name)
canvas1.create_window(200, 180, window=button1)
ex_num = exercise_name()

root.mainloop()  # TO RUN THE TKINTER LOOP

ex_name = ex_num.replace(' ', '_')
print(ex_name)
# ----------------------------------------------------------------------------------------------------------------------
# CREATE CONNECTION
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


# ADAPTING DIFFERENT DATA TYPES TO DATABASE
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


# FUNCTION TO EXECUTE QUERIES
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


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


# REGISTERING np datatypes for DATABASE
register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)
register_adapter(np.float32, addapt_numpy_float32)
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
nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()

# ---enable if you want to use face tracking---
# nuitrack.set_config_value("Faces.ToUse", "true")
# nuitrack.set_config_value("DepthProvider.Depth2ColorRegistration", "true")
# ----------------------------------------------------------------------------------------------------------------------
# INITIALISE AND PRINT DEVICE
devices = nuitrack.get_device_list()

for i, dev in enumerate(devices):
    # print(dev.get_name(), dev.get_serial_number())
    if i == 0:
        # dev.activate("ACTIVATION_KEY") #you can activate device using python api
        # print(dev.get_activation())
        nuitrack.set_device(dev)

# print(nuitrack.get_version())
# print(nuitrack.get_license())

nuitrack.create_modules()
nuitrack.run()

# SETTING DEPTH AND COLOR MODES
modes = cycle(["depth", "color"])
mode = next(modes)
# ----------------------------------------------------------------------------------------------------------------------
# LOOP
while 1:
    key = cv2.waitKey(1)
    nuitrack.update()
    data = nuitrack.get_skeleton()
    data_instance = nuitrack.get_instance()
    img_depth = nuitrack.get_depth_data()
    if img_depth.size:
        cv2.normalize(img_depth, img_depth, 0, 255, cv2.NORM_MINMAX)
        img_depth = np.array(cv2.cvtColor(img_depth, cv2.COLOR_GRAY2RGB), dtype=np.uint8)
        img_color = nuitrack.get_color_data()
        draw_skeleton(img_depth, data)
        draw_skeleton(img_color, data)
        draw_face(img_depth, data_instance)
        draw_face(img_color, data_instance)

        if img_color.size:
            cv2.imshow('Image', img_color)

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

# ----------------------------------------------------------------------------------------------------------------------
# WRITING DATA TO EXCEL FILES FOR RECORDED DATA
# j = 0
# while j < len(var_joint_data_holder):
#     var_joint_data_holder['data_' + joints_description[j] + '_df'].to_excel(
#         '{}_Data.xlsx'.format(joints_description[j]),
#         sheet_name='Sheet1', index=False)
#     j += 1
# ----------------------------------------------------------------------------------------------------------------------
# ENTERING VALUES INTO THE DATABASE
connection = create_connection("limitless_v1", "postgres", "Limitless@96", "127.0.0.1", "5432")

# LOOP ALL TABLES TO BE CREATED IN DATABASE - IF TABLES NOT FOUND
i = 0
while i < len(joints_description):
    create_table = f"""
     CREATE TABLE IF NOT EXISTS {joints_description[i]}_data_{ex_name} (
     id SERIAL PRIMARY KEY,
     x_location REAL,
     y_location REAL,
     depth REAL
    )
    """
    execute_query(connection, create_table)
    i += 1

# TRANSPOSING DATA FRAME FOR TUPLE TO BE 1X3 TO INSERT INTO COLUMNS
j = 0
while j < len(var_joint_data_holder):
    var_joint_data_holder['data_' + joints_description[j] + '_df'] = \
        var_joint_data_holder['data_' + joints_description[j] + '_df'].transpose()

    # CONVERTING TO TUPLE
    joint_data = [tuple(x) for x in var_joint_data_holder['data_' + joints_description[j] + '_df'].to_numpy()]
    joint_data_records = ", ".join(["%s"] * len(joint_data))

    # print(joint_data)

    # DELETE DATA QUERY - TRIAL ON SINGLE DATABASE FOR 1 EXERCISE - SO NEED TO REFRESH DATA EVERYTIME
    # FOR MULTIPLE EXERCISES WILL REQUIRE MULTIPLE DATABASES OR TABLES (WEIGH THE PROs AND CONs)
    delete_query = f"DELETE FROM {joints_description[j]}_data_{ex_name}"  # WHERE {joints_description[j]}_data.id IS NOT NULL "
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(delete_query)

    # INSERTING DATA INTO THE DATABASE

    insert_query = f"INSERT INTO {joints_description[j]}_data_{ex_name} " \
                   f"(x_location, y_location, depth) VALUES {joint_data_records}"

    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(insert_query, joint_data)

    j += 1
# ----------------------------------------------------------------------------------------------------------------------
# SELECTING DATA FROM DATABASE
# select_head_data = "SELECT * FROM head_data"
# user_head_data = execute_read_query(connection, select_head_data)
#
# for data in user_head_data:
#     print(data)

# ----------------------------------------------------------------------------------------------------------------------
# UPDATE DATA IN DATABASE - CHECK LATER
# update_post_description = """
# UPDATE
#   posts
# SET
#   description = "The weather has become pleasant now"
# WHERE
#   id = 2
# """
#
# execute_query(connection, update_post_description)
# ----------------------------------------------------------------------------------------------------------------------
# DELETE DATA IN DATABASE - CHECK LATER
# delete_comment = "DELETE FROM comments WHERE id = 2"
# execute_query(connection, delete_comment)
