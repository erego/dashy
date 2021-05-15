import pandas as pd

from Predilectura.statistics.feature import Feature

class DataSetABT:

    def __init__(self, path):
        self.path = path

    def drop_features(self, lst_features, output_path):
        data = pd.read_csv(self.path)
        data.drop(lst_features, axis='columns', inplace=True)
        data.to_csv(output_path, index=False)

    def complete_case_analysis(self, output_path):
        data = pd.read_csv(self.path)
        data.dropna(axis=0, how='any', inplace=True)
        data.to_csv(output_path, index=False)

    def imputation(self, lst_features, type_imputation, output_path):
        data = pd.read_csv(self.path)
        for feature in lst_features:
            if type_imputation == "mean":
                data[feature].fillna(data[feature].mean(), inplace=True)
            elif type_imputation == "median":
                data[feature].fillna(data[feature].median(), inplace=True)

        data.to_csv(output_path, index=False)

    def missing_reading_indicator(self, output_path):
        data = pd.read_csv(self.path)
        data['event_reading'] = data['chapters_readings'].notnull().astype(int)
        data.update(data[['min_words', 'max_words', 'avg_words', 'min_percent', 'max_percent', 'avg_percent',
                          'premium', 'devices_readings', 'versions_readings', 'chapters_readings']].fillna(-1))
        data.to_csv(output_path, index=False)

    def clamp(self, lst_features):
        data = pd.read_csv(self.path)
        for feature in lst_features:
            # Only for continuous features
            if Feature.check_type(data[feature]) == "Continuous":
                first_quartile = data[feature].quantile(0.25)
                third_quartile = data[feature].quantile(0.75)
                data[feature].values[data[feature].values < first_quartile] = first_quartile
                data[feature].values[data[feature].values > third_quartile] = third_quartile
        data.to_csv(self.path, index=False)



