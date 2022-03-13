def concat(start_datapoint, end_datapoint):
    import pandas as pd

    start_datapoint = pd.DataFrame(start_datapoint)
    end_datapoint = pd.DataFrame(end_datapoint)

    data_points = pd.concat([start_datapoint, end_datapoint], axis=1)

    return data_points

