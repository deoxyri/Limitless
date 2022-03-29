from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import pandas as pd
# import openpyxl
# from JointsAttributesClass import *
from JointData import *
# from ConcatDataFrame import *

from FaceDetection import *
from SkeletonDetection_Test import *
from SkeletonDetection import *

joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                      'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']

head_df = pd.read_excel(
    'X:\Limitless\A - Skeletal Tracking\Tracking Programs\{}_Data.xlsx'.format(joints_description[0]))
left_elbow_df = pd.read_excel(
    'X:\Limitless\A - Skeletal Tracking\Tracking Programs\{}_Data.xlsx'.format(joints_description[6]))

nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()

# ---enable if you want to use face tracking---
# nuitrack.set_config_value("Faces.ToUse", "true")
# nuitrack.set_config_value("DepthProvider.Depth2ColorRegistration", "true")

devices = nuitrack.get_device_list()
for i, dev in enumerate(devices):
    print(dev.get_name(), dev.get_serial_number())
    if i == 0:
        # dev.activate("ACTIVATION_KEY") # you can activate device using python api
        print(dev.get_activation())
        nuitrack.set_device(dev)

print(nuitrack.get_version())
print(nuitrack.get_license())

nuitrack.create_modules()
nuitrack.run()

modes = cycle(["depth", "color"])
mode = next(modes)

# Start Comparison
counter = 0  # COMPARISON TO BE CODED

while counter >= 0:
    # while mmm <= df_size: # Something Wrong

    key = cv2.waitKey(1)
    nuitrack.update()

    data = nuitrack.get_skeleton()

    for skeleton in data.skeletons:
        # Need to write a loop for the Object(skeleton) Attributes(.head, .neck, ....)
        head_joint_data = pd.DataFrame(skeleton.head.projection)
        left_elbow_joint_data = pd.DataFrame(skeleton.left_elbow.projection)

    data_head_live = pd.DataFrame(joint_data(data))

    data_instance = nuitrack.get_instance()
    img_depth = nuitrack.get_depth_data()

    if img_depth.size:
        cv2.normalize(img_depth, img_depth, 0, 255, cv2.NORM_MINMAX)
        img_depth = np.array(cv2.cvtColor(img_depth, cv2.COLOR_GRAY2RGB), dtype=np.uint8)
        img_color = nuitrack.get_color_data()

        # Actual Drawing
        draw_skeleton(img_depth, data)
        draw_skeleton(img_color, data)

        # Compare Recorded Data with Live for Dot Color
        draw_skeleton_test(img_depth, data, head_df, data_head_live, counter)
        draw_skeleton_test(img_color, data, head_df, data_head_live, counter)

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

    # counter += 1 # FIGURE OUT LOOP

    # Break loop on 'Esc'
    if key == 27:
        break

nuitrack.release()
