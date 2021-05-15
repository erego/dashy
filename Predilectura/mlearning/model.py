from sklearn.model_selection import train_test_split
import pandas as pd


def get_train_test(path_to_data):

    data = pd.read_csv(path_to_data)

    data = data.dropna()
    x = data.drop(columns=["edition_id", "edition_language", "event_classes", "event_objs", "target"])
    y = data["target"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

    return x_train, x_test, y_train, y_test
