import pandas as pd


class DataSetABT:

    def __init__(self, path):
        self.path = path

    def drop_features(self, lst_features):
        data = pd.read_csv(self.path)
        data.drop(lst_features, axis='columns', inplace=True)
        data.to_csv(self.path)

    def complete_case_analysis(self):
        data = pd.read_csv(self.path)
        data.dropna(axis=0, how='any', inplace=True)
        data.to_csv(self.path)

    def imputation(self, lst_features, type_imputation):
        pass

    def clamp(self, lst_features):
        pass


