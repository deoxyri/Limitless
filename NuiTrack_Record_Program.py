from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import pandas as pd
from pandas.io.formats import console

from data_write_program import *
from operator import attrgetter

# DRAWING POINTS
from FaceDetection import *
from SkeletonDetection import *

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

# JOINT DESCRIPTIONS
joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow',
                      'left_wrist', 'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']

# INITIALISE NUITRACK
nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()

# ---enable if you want to use face tracking---
# nuitrack.set_config_value("Faces.ToUse", "true")
# nuitrack.set_config_value("DepthProvider.Depth2ColorRegistration", "true")

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

        if key == 32:
            mode = next(modes)
        if mode == "depth":
            cv2.imshow('Image', img_depth)

        if mode == "color":
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

# print(var_holder)
# print(var_joint_data_holder)

# WRITING DATA TO EXCEL FILES FOR RECORDED DATA
j = 0
while j < len(var_joint_data_holder):
    var_joint_data_holder['data_' + joints_description[j] + '_df'].to_excel(
        '{}_Data.xlsx'.format(joints_description[j]),
        sheet_name='Sheet1', index=False)
    j += 1
# -----------------------------------------------------------------------------------
