def draw_skeleton_test(img_color, var_joints_recorded_data, var_joints_live_data, counter):
    import cv2
    import numpy as np
    import pandas as pd

    img_color = img_color
    # img_color_2 = img_color

    # point_color = (59, 164, 0)  # GREEN
    # point_color_2 = (26, 26, 139)  # RED

    joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                          'left_hand', 'right_collar', 'right_shoulder',
                          'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                          'right_hip', 'right_knee', 'right_ankle']

    ## FINISH LOOP AND PHASE1 DONE ##
    ## -------------------------------------------- ##
    # RECORDED DATA
    data_recorded_head = pd.DataFrame(var_joints_recorded_data['head_df'])
    data_recorded_neck = pd.DataFrame(var_joints_recorded_data['neck_df'])
    data_recorded_torso = pd.DataFrame(var_joints_recorded_data['torso_df'])
    data_recorded_waist = pd.DataFrame(var_joints_recorded_data['waist_df'])
    data_recorded_left_collar = pd.DataFrame(var_joints_recorded_data['left_collar_df'])
    data_recorded_left_shoulder = pd.DataFrame(var_joints_recorded_data['left_shoulder_df'])
    data_recorded_left_elbow = pd.DataFrame(var_joints_recorded_data['left_elbow_df'])
    data_recorded_left_wrist = pd.DataFrame(var_joints_recorded_data['left_wrist_df'])
    data_recorded_left_hand = pd.DataFrame(var_joints_recorded_data['left_hand_df'])
    data_recorded_right_collar = pd.DataFrame(var_joints_recorded_data['right_collar_df'])
    data_recorded_right_shoulder = pd.DataFrame(var_joints_recorded_data['right_shoulder_df'])
    data_recorded_right_elbow = pd.DataFrame(var_joints_recorded_data['right_elbow_df'])
    data_recorded_right_wrist = pd.DataFrame(var_joints_recorded_data['right_wrist_df'])
    data_recorded_right_hand = pd.DataFrame(var_joints_recorded_data['right_hand_df'])
    data_recorded_left_hip = pd.DataFrame(var_joints_recorded_data['left_hip_df'])
    data_recorded_left_knee = pd.DataFrame(var_joints_recorded_data['left_knee_df'])
    data_recorded_left_ankle = pd.DataFrame(var_joints_recorded_data['left_ankle_df'])
    data_recorded_right_hip = pd.DataFrame(var_joints_recorded_data['right_hip_df'])
    data_recorded_right_knee = pd.DataFrame(var_joints_recorded_data['right_knee_df'])
    data_recorded_right_ankle = pd.DataFrame(var_joints_recorded_data['right_ankle_df'])

    # LIVE DATA
    data_live_head = np.array(var_joints_live_data.get('head'))
    data_live_neck = np.array(var_joints_live_data.get('neck'))
    data_live_torso = np.array(var_joints_live_data.get('torso'))
    data_live_waist = np.array(var_joints_live_data.get('waist'))
    data_live_left_collar = np.array(var_joints_live_data.get('left_collar'))
    data_live_left_shoulder = np.array(var_joints_live_data.get('left_shoulder'))
    data_live_left_elbow = np.array(var_joints_live_data.get('left_elbow'))
    data_live_left_wrist = np.array(var_joints_live_data.get('left_wrist'))
    data_live_left_hand = np.array(var_joints_live_data.get('left_hand'))
    data_live_right_collar = np.array(var_joints_live_data.get('right_collar'))
    data_live_right_shoulder = np.array(var_joints_live_data.get('right_shoulder'))
    data_live_right_elbow = np.array(var_joints_live_data.get('right_elbow'))
    data_live_right_wrist = np.array(var_joints_live_data.get('right_wrist'))
    data_live_right_hand = np.array(var_joints_live_data.get('right_hand'))
    data_live_left_hip = np.array(var_joints_live_data.get('left_hip'))
    data_live_left_knee = np.array(var_joints_live_data.get('left_knee'))
    data_live_left_ankle = np.array(var_joints_live_data.get('left_ankle'))
    data_live_right_hip = np.array(var_joints_live_data.get('right_hip'))
    data_live_right_knee = np.array(var_joints_live_data.get('right_knee'))
    data_live_right_ankle = np.array(var_joints_live_data.get('right_ankle'))

    # RED DOT FUNCTION CALL
    deviation_check_loop(img_color, counter, data_recorded_head, data_live_head)
    deviation_check_loop(img_color, counter, data_recorded_neck, data_live_neck)
    deviation_check_loop(img_color, counter, data_recorded_torso, data_live_torso)
    deviation_check_loop(img_color, counter, data_recorded_waist, data_live_waist)
    deviation_check_loop(img_color, counter, data_recorded_left_collar, data_live_left_collar)
    deviation_check_loop(img_color, counter, data_recorded_left_shoulder, data_live_left_shoulder)
    deviation_check_loop(img_color, counter, data_recorded_left_elbow, data_live_left_elbow)
    deviation_check_loop(img_color, counter, data_recorded_left_wrist, data_live_left_wrist)
    deviation_check_loop(img_color, counter, data_recorded_left_hand, data_live_left_hand)
    deviation_check_loop(img_color, counter, data_recorded_right_collar, data_live_right_collar)
    deviation_check_loop(img_color, counter, data_recorded_right_shoulder, data_live_right_shoulder)
    deviation_check_loop(img_color, counter, data_recorded_right_elbow, data_live_right_elbow)
    deviation_check_loop(img_color, counter, data_recorded_right_wrist, data_live_right_wrist)
    deviation_check_loop(img_color, counter, data_recorded_right_hand, data_live_right_hand)
    deviation_check_loop(img_color, counter, data_recorded_left_hip, data_live_left_hip)
    deviation_check_loop(img_color, counter, data_recorded_left_knee, data_live_left_knee)
    deviation_check_loop(img_color, counter, data_recorded_left_ankle, data_live_left_ankle)
    deviation_check_loop(img_color, counter, data_recorded_right_hip, data_live_right_hip)
    deviation_check_loop(img_color, counter, data_recorded_right_knee, data_live_right_knee)
    deviation_check_loop(img_color, counter, data_recorded_right_ankle, data_live_right_ankle)

    # cv2.imshow('Image', img_color)


def deviation_check_loop(img_color, counter, data_recorded, data_live):
    import cv2
    point_color = (59, 164, 0)  # GREEN
    point_color_2 = (26, 26, 139)  # RED

    data_size = data_recorded.size / 3
    # HEAD LOOP
    if counter < data_size and data_live.size > 1:
        # print("Counter Value = ", counter)

        if data_live[0] > data_recorded.iat[0, counter] + 20 or \
                data_live[0] < data_recorded.iat[0, counter] - 20:

            x = (round(data_live[0]), round(data_live[1]))
            cv2.circle(img_color, x, 6, point_color_2, thickness=3, lineType=8, shift=0)
            cv2.putText(img_color, "PLEASE CORRECT YOUR POSTURE", (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
            # DRAW ARROW
            start_point = x  # Live Data Point
            end_point = (round(data_recorded.iat[0, counter]), round(data_recorded.iat[1, counter]))
            color_arrow = (255, 0, 0)  # Blue Arrow
            thickness = 3  # In px

            cv2.arrowedLine(img_color, start_point, end_point, color_arrow, thickness)

        elif data_recorded.iat[0, counter] + 20 >= data_live[0] >= \
                data_recorded.iat[0, counter] - 20:

            x = (round(data_live[0]), round(data_live[1]))
            cv2.circle(img_color, x, 6, point_color, thickness=3, lineType=8, shift=0)
            cv2.putText(img_color, "GOOD POSTURE! :D", (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
