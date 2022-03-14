def draw_skeleton_test(image, data, df, data2, df_size):
    import cv2
    point_color = (59, 164, 0)

    point_color_2 = (26, 26, 139)

    for skel in data.skeletons:
        for el in skel[1:]:
            x = (round(el.projection[0]), round(el.projection[1]))

            if data2[0][df_size] <= df[0][df_size] + 10:
                cv2.circle(image, x, 8, point_color, -1)
                break

            elif data2[0][df_size] >= df[0][df_size] + 10:
                cv2.circle(image, x, 8, point_color_2, -1)
                break
            else:
                break
