def joint_data(data):
    import pandas as pd

    for skeleton in data.skeletons:
        # Need to write a loop for the Object(skeleton) Attributes(.head, .neck, ....)
        data = pd.DataFrame(skeleton.head.projection)

    return data
