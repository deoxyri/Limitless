def draw_face(image, data_instance):

    import cv2
    if not data_instance:
        return
    for instance in data_instance["Instances"]:
        line_color = (59, 164, 225)
        text_color = (59, 255, 255)
        if 'face' in instance.keys():
            bbox = instance["face"]["rectangle"]
        else:
            return
        x1 = (round(bbox["left"]), round(bbox["top"]))
        x2 = (round(bbox["left"]) + round(bbox["width"]), round(bbox["top"]))
        x3 = (round(bbox["left"]), round(bbox["top"]) + round(bbox["height"]))
        x4 = (round(bbox["left"]) + round(bbox["width"]), round(bbox["top"]) + round(bbox["height"]))
        cv2.line(image, x1, x2, line_color, 3)
        cv2.line(image, x1, x3, line_color, 3)
        cv2.line(image, x2, x4, line_color, 3)
        cv2.line(image, x3, x4, line_color, 3)
        cv2.putText(image, "User {}".format(instance["id"]),
                    x1, cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
        cv2.putText(image, "{} {}".format(instance["face"]["gender"], int(instance["face"]["age"]["years"])),
                    x3, cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)