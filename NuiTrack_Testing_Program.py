from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import pandas as pd
import openpyxl
from JointsAttributesClass import *
from JointData import *
from ConcatDataFrame import *

from FaceDetection import *
from SkeletonDetection_Test import *

df = pd.read_excel (r'X:\Limitless\A - Skeletal Tracking\Tracking Programs\head_Data.xlsx')
print(df[0][0])
print(df[0][0] + 10)
df_size = df.size
# print(df_size)


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

# Start Comparison
mmm = 0

# while 1:
while mmm<=df_size:

    key = cv2.waitKey(1)
    nuitrack.update()

    data = nuitrack.get_skeleton()

    Data2 = pd.DataFrame(joint_data(data))
    # print(Data2[0][0])

    data_instance = nuitrack.get_instance()
    img_depth = nuitrack.get_depth_data()

    if img_depth.size:
        cv2.normalize(img_depth, img_depth, 0, 255, cv2.NORM_MINMAX)
        img_depth = np.array(cv2.cvtColor(img_depth, cv2.COLOR_GRAY2RGB), dtype=np.uint8)
        img_color = nuitrack.get_color_data()

        # Compare Recorded Data with Live for Dot Color
        draw_skeleton(img_depth, data, df, Data2, mmm)
        draw_skeleton(img_color, data, df, Data2, mmm)

        draw_face(img_depth, data_instance)
        draw_face(img_color, data_instance)

        if key == 32:
            mode = next(modes)
        if mode == "depth":
            cv2.imshow('Image', img_depth)
        if mode == "color":
            if img_color.size:
                cv2.imshow('Image', img_color)

    mmm +=1

    # Break loop on 'Esc'
    if key == 27:
        break

nuitrack.release()
