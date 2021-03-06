def draw_skeleton(image, data):

    import cv2
    point_color = (59, 164, 0)
    for skel in data.skeletons:
        for el in skel[1:]:
            x = (round(el.projection[0]), round(el.projection[1]))
            cv2.circle(image, x, 6, point_color, thickness=3, lineType=8, shift=0)