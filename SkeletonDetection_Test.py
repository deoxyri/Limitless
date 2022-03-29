def draw_skeleton_test(image, data, record_data, live_data, df_size):
    import cv2
    point_color = (59, 164, 0)  # GREEN

    point_color_2 = (26, 26, 139)  # RED

    for skel in data.skeletons:
        for el in skel[1:]:
            x = (round(el.projection[0]), round(el.projection[1]))

            if live_data[0][df_size] > record_data[0][df_size]+20 or live_data[0][df_size] < record_data[0][df_size]-20:
                cv2.circle(image, x, 8, point_color_2, -1)
                break

            elif record_data[0][df_size] + 20 >= live_data[0][df_size] >= record_data[0][df_size] - 20:
                cv2.circle(image, x, 8, point_color, -1)
                break
            else:
                break
