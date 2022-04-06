def draw_skeleton_test(img_color, var_joints_recorded_data, var_joints_live_data):
    import cv2
    point_color = (59, 164, 0)  # GREEN
    point_color_2 = (26, 26, 139)  # RED

    joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow', 'left_wrist',
                          'left_hand', 'right_collar', 'right_shoulder',
                          'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                          'right_hip', 'right_knee', 'right_ankle']

    keys = list(var_joints_live_data)
    i = 0
    while i < len(keys):
        print(var_joints_live_data['data_' + joints_description[i]])
        i += 1

    data_size = var_joints_recorded_data.size / 3
    counter = 0

    while counter < data_size:

        if var_joints_live_data[0][counter] > var_joints_recorded_data[0][counter] + 20 or \
                var_joints_live_data[0][counter] < var_joints_recorded_data[0][counter] - 20:

            x = [var_joints_live_data[0][counter], var_joints_live_data[1][counter]]
            cv2.circle(img_color, x, 8, point_color_2, -1)
            break

        elif var_joints_recorded_data[0][counter] + 20 >= var_joints_live_data[0][counter] >= \
                var_joints_recorded_data[0][counter] - 20:

            x = [var_joints_live_data[0][counter], var_joints_live_data[1][counter]]
            cv2.circle(img_color, x, 8, point_color, -1)
            break
        else:
            break

    counter += 1
