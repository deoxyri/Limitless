def draw_skeleton_test(img_color, var_joints_recorded_data, var_joints_live_data, counter):
    import cv2
    import numpy as np
    import pandas as pd

    img_color = img_color
    # img_color_2 = img_color

    point_color = (59, 164, 0)  # GREEN
    point_color_2 = (26, 26, 139)  # RED

    joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                          'left_hand', 'right_collar', 'right_shoulder',
                          'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                          'right_hip', 'right_knee', 'right_ankle']

    ## FINISH LOOP AND PHASE1 DONE ##
    ## PAUSE TEST ##
    ## -------------------------------------------- ##
    # RECORDED DATA
    data_recorded_head = pd.DataFrame(var_joints_recorded_data['head_df'])

    data_recorded = data_recorded_head

    # LIVE DATA
    data_live_head = np.array(var_joints_live_data.get('head'))

    data_live = data_live_head

    # RED DOT FUNCTION CALL

    data_size = data_recorded.size / 3
    # HEAD LOOP
    if counter < data_size and data_live.size > 1:
        print("Counter Value First Loop = ", counter)

        if data_live[0] > data_recorded.iat[0, counter] + 20 or \
                data_live[0] < data_recorded.iat[0, counter] - 20:

            x = (round(data_live[0]), round(data_live[1]))
            cv2.circle(img_color, x, 6, point_color_2, thickness=3, lineType=8, shift=0)

            cv2.putText(img_color, "PLEASE CORRECT YOUR POSITION", (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)

            start_point = x
            # End coordinate
            end_point = (round(data_recorded.iat[0, counter]), round(data_recorded.iat[1, counter]))
            # Green color in BGR
            color_arrow = (255, 0, 0)
            # Line thickness of 9 px
            thickness = 3
            # Using cv2.arrowedLine() method
            # Draw a diagonal green arrow line
            # with thickness of 9 px
            cv2.arrowedLine(img_color, start_point, end_point, color_arrow, thickness)

            cv2.waitKey()

            print("Counter Value Dot Loop = ", counter)
            # continue

        elif data_recorded.iat[0, counter] + 20 >= data_live[0] >= \
                data_recorded.iat[0, counter] - 20:

            x = (round(data_live[0]), round(data_live[1]))
            cv2.circle(img_color, x, 6, point_color, thickness=3, lineType=8, shift=0)
            cv2.putText(img_color, "GOOD POSTURE! :D", (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)

    # deviation_check_loop(img_color, counter, data_recorded_head, data_live_head)


# def deviation_check_loop(img_color, counter, data_recorded, data_live):
#     import cv2
#     point_color = (59, 164, 0)  # GREEN
#     point_color_2 = (26, 26, 139)  # RED
#
#     data_size = data_recorded.size / 3
#     # HEAD LOOP
#     if counter < data_size and data_live.size > 1:
#         # print("Counter Value = ", counter)
#
#         if data_live[0] > data_recorded.iat[0, counter] + 20 or \
#                 data_live[0] < data_recorded.iat[0, counter] - 20:
#
#             x = (round(data_live[0]), round(data_live[1]))
#             cv2.circle(img_color, x, 6, point_color_2, thickness=3, lineType=8, shift=0)
#
#         elif data_recorded.iat[0, counter] + 20 >= data_live[0] >= \
#                 data_recorded.iat[0, counter] - 20:
#
#             x = (round(data_live[0]), round(data_live[1]))
#             cv2.circle(img_color, x, 6, point_color, thickness=3, lineType=8, shift=0)
