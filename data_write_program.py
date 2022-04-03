def data_write_program(data_zero, data):
    # from ConcatDataFrame import *

    import pandas as pd
    data = pd.DataFrame(data)
    data_zero = pd.DataFrame(data_zero)

    if data.iat[0, 0] < 2000:
        # Concatenation Function Used for above-mentioned Purpose - Function in ConcatDataFrame.py
        data_zero = concat(data_zero, data)

    return data_zero


def concat(start_datapoint, end_datapoint):
    import pandas as pd

    start_datapoint = pd.DataFrame(start_datapoint)
    end_datapoint = pd.DataFrame(end_datapoint)

    data_points = pd.concat([start_datapoint, end_datapoint], axis=1)

    return data_points
