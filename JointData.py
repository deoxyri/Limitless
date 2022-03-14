def joint_data(data):

    import pandas as pd

    for skeleton in data.skeletons:

        data = pd.DataFrame(skeleton.head.projection)

    return data
