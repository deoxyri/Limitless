from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import pandas as pd

from operator import attrgetter

# DRAWING POINTS
from FaceDetection import *
from SkeletonDetection_Test import *
from SkeletonDetection import *

# FUNCTION TEST
from var_holder_return_function import *

joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                      'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']
# LIVE DATA HOLDER
# var_holder = {}
data_tracking = {}

# RECORDED DATA
var_joints_recorded_data = {}

i = 0
while i < len(joints_description):
    var_joints_recorded_data[joints_description[i] + '_df'] = pd.read_excel(
        'X:\Limitless\A - Skeletal Tracking\Tracking Programs\{}_Data_Variable.xlsx'.format(joints_description[i]))
    i += 1

# print(var_joints_recorded_data['head_df'])
# INITIALISE DEVICE
nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()

# ---enable if you want to use face tracking---
# nuitrack.set_config_value("Faces.ToUse", "true")
# nuitrack.set_config_value("DepthProvider.Depth2ColorRegistration", "true")

devices = nuitrack.get_device_list()

# DEVICE NAME, ID etc...
for i, dev in enumerate(devices):
    # print(dev.get_name(), dev.get_serial_number())
    if i == 0:
        # dev.activate("ACTIVATION_KEY") # you can activate device using python api
        # print(dev.get_activation())
        nuitrack.set_device(dev)

# print(nuitrack.get_version())
# print(nuitrack.get_license())

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

    # print(var_joints_live_data)

    i = 0
    while i < len(keys):
        data_tracking['{}'.format(i)] = var_joints_live_data['data_'+joints_description[i]]
        # print(var_joints_live_data['data_'+joints_description[i]])
        i += 1

    # print(data_tracking)

    # DRAWING LOOP
    if img_depth.size:
        cv2.normalize(img_depth, img_depth, 0, 255, cv2.NORM_MINMAX)
        img_depth = np.array(cv2.cvtColor(img_depth, cv2.COLOR_GRAY2RGB), dtype=np.uint8)
        img_color = nuitrack.get_color_data()

        # Actual Drawing
        draw_skeleton(img_depth, data)
        draw_skeleton(img_color, data)

        # print(data_tracking)

        # COMPARE LIVE DATA WITH RECORDED DATA (COLOUR) ########
        # draw_skeleton_test(img_color, var_joints_recorded_data, var_joints_live_data)
        draw_skeleton_test(img_color, var_joints_recorded_data, data_tracking)

        # Draw Face
        draw_face(img_depth, data_instance)
        draw_face(img_color, data_instance)

        if key == 32:
            mode = next(modes)
        if mode == "depth":
            cv2.imshow('Image', img_depth)
        if mode == "color":
            if img_color.size:
                cv2.imshow('Image', img_color)

    # Break loop on 'Esc'
    if key == 27:
        break

# print(var_holder['data_head'])

nuitrack.release()
