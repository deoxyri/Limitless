def draw_skeleton_test(img_color, var_joints_recorded_data, var_joints_live_data, counter):
    import cv2
    import numpy as np

    point_color = (59, 164, 0)  # GREEN
    point_color_2 = (26, 26, 139)  # RED

    joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                          'left_hand', 'right_collar', 'right_shoulder',
                          'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                          'right_hip', 'right_knee', 'right_ankle']

    head_data_recorded = var_joints_recorded_data['head_df']

    # VARIABLES
    head_data_live = np.array(var_joints_live_data.get('0'))
    # neck_data_live = var_joints_live_data['data_neck']
    # torso_data_live = var_joints_live_data['data_torso']
    # waist_data_live = var_joints_live_data['data_waist']
    # left_collar_data_live = var_joints_live_data['data_left_collar']
    # left_shoulder_data_live = var_joints_live_data['data_left_shoulder']
    # left_elbow_data_live = var_joints_live_data['data_left_elbow']
    # left_wrist_data_live = var_joints_live_data['data_left_wrist']
    # left_hand_data_live = var_joints_live_data['data_left_hand']
    # right_collar_data_live = var_joints_live_data['data_right_collar']
    # right_shoulder_data_live = var_joints_live_data['data_right_shoulder']
    # right_elbow_data_live = var_joints_live_data['data_right_elbow']
    # right_wrist_data_live = var_joints_live_data['data_right_wrist']
    # right_hand_data_live = var_joints_live_data['data_right_hand']
    # left_hip_data_live = var_joints_live_data['data_left_hip']
    # left_knee_data_live = var_joints_live_data['data_left_knee']
    # left_ankle_data_live = var_joints_live_data['data_left_ankle']
    # right_hip_data_live = var_joints_live_data['data_right_hip']
    # right_knee_data_live = var_joints_live_data['data_right_knee']
    # right_ankle_data_live = var_joints_live_data['data_right_ankle']

    keys = list(var_joints_live_data)
    # i = 0
    # while i < len(keys):
    #    print(var_joints_live_data['data_' + joints_description[i]])
    #    i += 1

    data_size = head_data_recorded.size / 3

    # ACTUAL LOOP TO BE CONFIGURED

    # while counter < data_size:
    #
    #     if var_joints_live_data[0][counter] > var_joints_recorded_data[0][counter] + 20 or \
    #             var_joints_live_data[0][counter] < var_joints_recorded_data[0][counter] - 20:
    #
    #         x = [var_joints_live_data[0][counter], var_joints_live_data[1][counter]]
    #         cv2.circle(img_color, x, 8, point_color_2, -1)
    #         break
    #
    #     elif var_joints_recorded_data[0][counter] + 20 >= var_joints_live_data[0][counter] >= \
    #             var_joints_recorded_data[0][counter] - 20:
    #
    #         x = [var_joints_live_data[0][counter], var_joints_live_data[1][counter]]
    #         cv2.circle(img_color, x, 8, point_color, -1)
    #         break
    #     else:
    #         break

    # HEAD LOOP

    while counter < data_size:

        if head_data_live.size > 1:

            if head_data_live[0] > head_data_recorded[0][counter] + 20 or \
                    head_data_live[0] < head_data_recorded[0][counter] - 20:

                x = (round(head_data_live[0]), round(head_data_live[1]))
                cv2.circle(img_color, x, 8, point_color_2, -1)
                break

            elif head_data_recorded[0][counter] + 20 >= head_data_live[0] >= \
                    head_data_recorded[0][counter] - 20:

                x = (round(head_data_live[0]), round(head_data_live[1]))
                cv2.circle(img_color, x, 8, point_color, -1)
                break
            else:
                break
        else:
            break

    # counter += 1
