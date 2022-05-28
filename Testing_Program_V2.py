from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import pandas as pd

# DRAWING POINTS
# from SkeletonDetection_Test import *
# from red_dot_test import *
from red_dot_pause_test_function import *

# FUNCTION TEST
from var_holder_return_function import *
# ----------------------------------------------------------------------------------------------------------------------
# DATABASE
from create_tables_db_limitlessv1 import *
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import register_adapter, AsIs


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


# DATABASE CONNECTION
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


# REGISTERING np datatypes TO DATABASE
register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)
register_adapter(np.float32, addapt_numpy_float32)

connection = create_connection("limitless_v1", "postgres", "Limitless@96", "127.0.0.1", "5432")
# ----------------------------------------------------------------------------------------------------------------------
joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                      'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']
# LIVE DATA HOLDER
data_tracking = {}

# RECORDED DATA
var_joints_recorded_data = {}

i = 0
while i < len(joints_description):
    var_joints_recorded_data[joints_description[i] + '_df'] = pd.read_excel(
        'X:\Limitless\A - Skeletal Tracking\Tracking Programs\{}_Data.xlsx'.format(joints_description[i]))
    i += 1

# while i < len(joints_description):
#     var_joints_recorded_data[joints_description[i] + '_df'] = pd.read_excel(
#         'F:\Limitless\Programs\Limitless\{}_Data.xlsx'.format(joints_description[i]))
#     i += 1


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
