from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import pyrealsense2 as rs
import pandas as pd
import openpyxl
from JointData import *
from ConcatDataFrame import *

from FaceDetection import *
from SkeletonDetection import *

import xlsxwriter

# for skeleton in data.skeletons

nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()

# ---enable if you want to use face tracking---
# nuitrack.set_config_value("Faces.ToUse", "true")
# nuitrack.set_config_value("DepthProvider.Depth2ColorRegistration", "true")

devices = nuitrack.get_device_list()
for i, dev in enumerate(devices):
    print(dev.get_name(), dev.get_serial_number())
    if i == 0:
        # dev.activate("ACTIVATION_KEY") #you can activate device using python api
        print(dev.get_activation())
        nuitrack.set_device(dev)

print(nuitrack.get_version())
print(nuitrack.get_license())

nuitrack.create_modules()
nuitrack.run()

modes = cycle(["depth", "color"])
mode = next(modes)

# Zero DataFrame for initialisation purpose - Find a workaround
Data1 = {"START": [0, 0, 0]}
Data1 = pd.DataFrame(Data1)

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
        if key == 32:
            mode = next(modes)
        if mode == "depth":
            cv2.imshow('Image', img_depth)
        if mode == "color":
            if img_color.size:
                cv2.imshow('Image', img_color)

    # Different Joints Available
    joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                          'left_hand', 'right_collar', 'right_shoulder',
                          'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                          'right_hip', 'right_knee', 'right_ankle']

    # Extracting Specific Joint Data from the SDK - Here Head - Function in JointData.py
    Data2 = JOINTS(data, joints_description)
    Data2 = pd.DataFrame(Data2.joint_data())

    # Initial Data1 is null
    # Data1 DataFrame Updates with the First Data Point Recognised (Data2)
    # Then Iteration takes cares of the concatenation (i.e., Data1 keeps getting appended; Data2 is the latest data)

    # Concatenation Function Used for above-mentioned Purpose - Function in ConcatDataFrame.py

    # Threshold to allow for tracking to start
    if Data2.iat[0, 0] < 2000:
        Data1 = concat(Data1, Data2)
    else:
        continue

    # Break loop on 'Esc'
    if key == 27:
        break

Data1.to_excel('{}_Data.xlsx'.format(joints_description[0]), sheet_name='Sheet1', index=False)

nuitrack.release()
