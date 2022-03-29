from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import pandas as pd

from JointData import *

from FaceDetection import *
from SkeletonDetection import *
from data_write_program import *

data_zero = pd.DataFrame({"START": [0, 0, 0]})

data_head_df = pd.DataFrame({"START": [0, 0, 0]})
data_neck_df = pd.DataFrame({"START": [0, 0, 0]})
data_torso_df = pd.DataFrame({"START": [0, 0, 0]})
data_waist_df = pd.DataFrame({"START": [0, 0, 0]})
data_left_collar_df = pd.DataFrame({"START": [0, 0, 0]})
data_left_shoulder_df = pd.DataFrame({"START": [0, 0, 0]})
data_left_elbow_df = pd.DataFrame({"START": [0, 0, 0]})
data_left_wrist_df = pd.DataFrame({"START": [0, 0, 0]})
data_left_hand_df = pd.DataFrame({"START": [0, 0, 0]})
data_right_collar_df = pd.DataFrame({"START": [0, 0, 0]})
data_right_shoulder_df = pd.DataFrame({"START": [0, 0, 0]})
data_right_elbow_df = pd.DataFrame({"START": [0, 0, 0]})
data_right_wrist_df = pd.DataFrame({"START": [0, 0, 0]})
data_right_hand_df = pd.DataFrame({"START": [0, 0, 0]})
data_left_hip_df = pd.DataFrame({"START": [0, 0, 0]})
data_left_knee_df = pd.DataFrame({"START": [0, 0, 0]})
data_left_ankle_df = pd.DataFrame({"START": [0, 0, 0]})
data_right_hip_df = pd.DataFrame({"START": [0, 0, 0]})
data_right_knee_df = pd.DataFrame({"START": [0, 0, 0]})
data_right_ankle_df = pd.DataFrame({"START": [0, 0, 0]})



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

    for skeleton in data.skeletons:
        # Need to write a loop for the Object(skeleton) Attributes(.head, .neck, ....)
        data_head = pd.DataFrame(skeleton.head.projection)
        data_neck = pd.DataFrame(skeleton.neck.projection)
        data_torso = pd.DataFrame(skeleton.torso.projection)
        data_waist = pd.DataFrame(skeleton.waist.projection)
        data_left_collar = pd.DataFrame(skeleton.left_collar.projection)
        data_left_shoulder = pd.DataFrame(skeleton.left_shoulder.projection)
        data_left_elbow = pd.DataFrame(skeleton.left_elbow.projection)
        data_left_wrist = pd.DataFrame(skeleton.left_wrist.projection)
        data_left_hand = pd.DataFrame(skeleton.left_hand.projection)
        data_right_collar = pd.DataFrame(skeleton.right_collar.projection)
        data_right_shoulder = pd.DataFrame(skeleton.right_shoulder.projection)
        data_right_elbow = pd.DataFrame(skeleton.right_elbow.projection)
        data_right_wrist = pd.DataFrame(skeleton.right_wrist.projection)
        data_right_hand = pd.DataFrame(skeleton.right_hand.projection)
        data_left_hip = pd.DataFrame(skeleton.left_hip.projection)
        data_left_knee = pd.DataFrame(skeleton.left_knee.projection)
        data_left_ankle = pd.DataFrame(skeleton.left_ankle.projection)
        data_right_hip = pd.DataFrame(skeleton.right_hip.projection)
        data_right_knee = pd.DataFrame(skeleton.right_knee.projection)
        data_right_ankle = pd.DataFrame(skeleton.right_ankle.projection)

        # print(data_head)
        data_head_df = data_write_program(data_head_df, data_head)
        data_head_df = data_write_program(data_head_df, data_head)
        data_neck_df = data_write_program(data_neck_df, data_neck)
        data_torso_df = data_write_program(data_torso_df, data_torso)
        data_waist_df = data_write_program(data_waist_df, data_waist)
        data_left_collar_df = data_write_program(data_left_collar_df, data_left_collar)
        data_left_shoulder_df = data_write_program(data_left_shoulder_df, data_left_shoulder)
        data_left_elbow_df = data_write_program(data_left_elbow_df, data_left_elbow)
        data_left_wrist_df = data_write_program(data_left_wrist_df, data_left_wrist)
        data_left_hand_df = data_write_program(data_left_hand_df, data_left_hand)
        data_right_collar_df = data_write_program(data_right_collar_df, data_right_collar)
        data_right_shoulder_df = data_write_program(data_right_shoulder_df, data_right_shoulder)
        data_right_elbow_df = data_write_program(data_right_elbow_df, data_right_elbow)
        data_right_wrist_df = data_write_program(data_right_wrist_df, data_right_wrist)
        data_right_hand_df = data_write_program(data_right_hand_df, data_right_hand)
        data_left_hip_df = data_write_program(data_left_hip_df, data_left_hip)
        data_left_knee_df = data_write_program(data_left_knee_df, data_left_knee)
        data_left_ankle_df = data_write_program(data_left_ankle_df, data_left_ankle)
        data_right_hip_df = data_write_program(data_right_hip_df, data_right_hip)
        data_right_knee_df = data_write_program(data_right_knee_df, data_right_knee)
        data_right_ankle_df = data_write_program(data_right_ankle_df, data_right_ankle)

    # print(getattr(data.skeletons,joints_description[1]))

    # data_zero = data_write_program(data_zero, data_head)

    # Break loop on 'Esc'
    if key == 27:
        break

data_head_df.to_excel('{}_Data.xlsx'.format(joints_description[0]), sheet_name='Sheet1', index=False)
data_neck_df.to_excel('{}_Data.xlsx'.format(joints_description[1]), sheet_name='Sheet1', index=False)
data_torso_df.to_excel('{}_Data.xlsx'.format(joints_description[2]), sheet_name='Sheet1', index=False)
data_waist_df.to_excel('{}_Data.xlsx'.format(joints_description[3]), sheet_name='Sheet1', index=False)
data_left_collar_df.to_excel('{}_Data.xlsx'.format(joints_description[4]), sheet_name='Sheet1', index=False)
data_left_shoulder_df.to_excel('{}_Data.xlsx'.format(joints_description[5]), sheet_name='Sheet1', index=False)
data_left_elbow_df.to_excel('{}_Data.xlsx'.format(joints_description[6]), sheet_name='Sheet1', index=False)
data_left_wrist_df.to_excel('{}_Data.xlsx'.format(joints_description[7]), sheet_name='Sheet1', index=False)
data_left_hand_df.to_excel('{}_Data.xlsx'.format(joints_description[8]), sheet_name='Sheet1', index=False)
data_right_collar_df.to_excel('{}_Data.xlsx'.format(joints_description[9]), sheet_name='Sheet1', index=False)
data_right_shoulder_df.to_excel('{}_Data.xlsx'.format(joints_description[10]), sheet_name='Sheet1', index=False)
data_right_elbow_df.to_excel('{}_Data.xlsx'.format(joints_description[11]), sheet_name='Sheet1', index=False)
data_right_wrist_df.to_excel('{}_Data.xlsx'.format(joints_description[12]), sheet_name='Sheet1', index=False)
data_right_hand_df.to_excel('{}_Data.xlsx'.format(joints_description[13]), sheet_name='Sheet1', index=False)
data_left_hip_df.to_excel('{}_Data.xlsx'.format(joints_description[14]), sheet_name='Sheet1', index=False)
data_left_knee_df.to_excel('{}_Data.xlsx'.format(joints_description[15]), sheet_name='Sheet1', index=False)
data_left_ankle_df.to_excel('{}_Data.xlsx'.format(joints_description[16]), sheet_name='Sheet1', index=False)
data_right_hip_df.to_excel('{}_Data.xlsx'.format(joints_description[17]), sheet_name='Sheet1', index=False)
data_right_knee_df.to_excel('{}_Data.xlsx'.format(joints_description[18]), sheet_name='Sheet1', index=False)
data_right_ankle_df.to_excel('{}_Data.xlsx'.format(joints_description[19]), sheet_name='Sheet1', index=False)

nuitrack.release()
