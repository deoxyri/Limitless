def draw_skeleton_test(img_color, var_joints_recorded_data, var_joints_live_data, counter):
    import cv2
    import numpy as np
    import pandas as pd

    point_color = (59, 164, 0)  # GREEN
    point_color_2 = (26, 26, 139)  # RED

    joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                          'left_hand', 'right_collar', 'right_shoulder',
                          'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                          'right_hip', 'right_knee', 'right_ankle']

    # RECORDED DATA
    head_data_recorded = pd.DataFrame(var_joints_recorded_data['head_df'])
    # LIVE DATA
    head_data_live = np.array(var_joints_live_data.get('0'))
    # SIZE OF RECORDED DATA
    data_size = head_data_recorded.size / 3

    # print("Size of Recorded Data = ", data_size)
    # print("Live Data Array = ", head_data_live)
    print(head_data_recorded)
    print("First Value = ", head_data_recorded.iat[0, counter])

    # HEAD LOOP
    if counter < data_size and head_data_live.size > 1:
        print("Counter Value = ", counter)
        # print(head_data_recorded[0][counter])

        if head_data_live[0] > head_data_recorded.iat[0, counter] + 20 or \
                head_data_live[0] < head_data_recorded.iat[0, counter] - 20:

            x = (round(head_data_live[0]), round(head_data_live[1]))
            cv2.circle(img_color, x, 8, point_color_2, -1)
            # break

        elif head_data_recorded.iat[0, counter] + 20 >= head_data_live[0] >= \
                head_data_recorded.iat[0, counter] - 20:

            x = (round(head_data_live[0]), round(head_data_live[1]))
            cv2.circle(img_color, x, 8, point_color, -1)
    # else:
    #  break
