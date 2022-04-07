def draw_skeleton_test(img_color, var_joints_recorded_data, var_joints_live_data, counter):
    import cv2
    import numpy as np
    import pandas as pd

    img_color = img_color

    point_color = (59, 164, 0)  # GREEN
    point_color_2 = (26, 26, 139)  # RED

    joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                          'left_hand', 'right_collar', 'right_shoulder',
                          'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                          'right_hip', 'right_knee', 'right_ankle']

    ## FINISH LOOP AND PHASE1 DONE ##

    joints = 0
    # while joints < len(joints_description):
    # RECORDED DATA
    data_recorded = pd.DataFrame(var_joints_recorded_data[joints_description[joints] + '_df'])
    # LIVE DATA
    data_live = np.array(var_joints_live_data.get(joints_description[joints]))
    # RED DOT LOOP
    deviation_check_loop(img_color, counter, data_recorded, data_live)
    # joints += 1


def deviation_check_loop(img_color, counter, data_recorded, data_live):
    import cv2
    point_color = (59, 164, 0)  # GREEN
    point_color_2 = (26, 26, 139)  # RED

    data_size = data_recorded.size / 3
    # HEAD LOOP
    if counter < data_size and data_live.size > 1:
        print("Counter Value = ", counter)
        # print(head_data_recorded[0][counter])

        if data_live[0] > data_recorded.iat[0, counter] + 20 or \
                data_live[0] < data_recorded.iat[0, counter] - 20:

            x = (round(data_live[0]), round(data_live[1]))
            cv2.circle(img_color, x, 8, point_color_2, -1)
            # break

        elif data_recorded.iat[0, counter] + 20 >= data_live[0] >= \
                data_recorded.iat[0, counter] - 20:

            x = (round(data_live[0]), round(data_live[1]))
            cv2.circle(img_color, x, 8, point_color, -1)
