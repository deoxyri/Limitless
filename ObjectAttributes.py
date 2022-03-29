from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import pandas as pd

from FaceDetection import *
from SkeletonDetection import *

import csv

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

while 1:
    key = cv2.waitKey(1)
    nuitrack.update()
    data = nuitrack.get_skeleton()
    data_instance = nuitrack.get_instance()
    img_depth = nuitrack.get_depth_data()

    for skel in data.skeletons:
        print(skel)
        for el in skel[1:]:
            print(el)
            # x = (round(el.projection[0]), round(el.projection[1]))
            # cv2.circle(image, x, 8, point_color, -1)

    if img_depth.size:
        cv2.normalize(img_depth, img_depth, 0, 255, cv2.NORM_MINMAX)
        img_depth = np.array(cv2.cvtColor(img_depth, cv2.COLOR_GRAY2RGB), dtype=np.uint8)
        img_color = nuitrack.get_color_data()
        draw_skeleton(img_depth, data)
        draw_skeleton(img_color, data)
        draw_face(img_depth, data_instance)
        draw_face(img_color, data_instance)

        joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow',
                              'left_wrist',
                              'left_hand', 'right_collar', 'right_shoulder',
                              'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                              'right_hip', 'right_knee', 'right_ankle']
        i = 0
        for skeleton in data.skeletons:

            while i < len(joints_description):
                print(getattr(skeleton, joints_description[i]))
                i += 1

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

nuitrack.release()
