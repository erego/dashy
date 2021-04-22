from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


def get_train_test(path_to_data):

    data = pd.read_csv(path_to_data)

    # TODO add target column, done for training propose, it will be fill up in the future
    data["target"] = np.random.randint(0, 2, size=len(data))

    # TODO analize data in order to not drop nan
    data = data.dropna()
    x = data.drop(columns=["edition_language", "event_classes", "event_objs", "target"])
    y = data["target"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

    return x_train, x_test, y_train, y_test
