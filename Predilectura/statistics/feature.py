
class Feature:

    def __init__(self, description):
        self.description = description
        self.type = None

    def get_statistics(self, values):
        raise NotImplementedError()

    @staticmethod
    def check_type(values):
        if values.nunique()/values.size < 0.05:
            return "Categorical"
        else:
            return "Continuous"

    @staticmethod
    def check_cardinality_one(values):
        if len(values.value_counts()) == 1:
            return True
        else:
            return False


class FeatureContinuous(Feature):
    def __init__(self, description):
        super().__init__(description)
        self.type = "Continuous"
        self.statistics = None

    def get_statistics(self, values):
        self.statistics = dict()
        self.statistics["count"] = values.size
        self.statistics["missing"] = values.isna().sum()
        self.statistics["cardinality"] = values.nunique()
        self.statistics["percent_missing"] = round((values.isna().sum() / self.statistics["count"]) * 100, 4)
        self.statistics["min"] = round(values.min(), 4)
        self.statistics["first_quartile"] = values.quantile(0.25)
        self.statistics["mean"] = round(values.mean(), 4)
        self.statistics["median"] = round(values.median(), 4)
        self.statistics["third_quartile"] = round(values.quantile(0.75), 4)
        self.statistics["max"] = round(values.max(), 4)
        self.statistics["std_deviation"] = round(values.std(), 4)
        return self.statistics


class FeatureCategorical(Feature):
    def __init__(self, description):
        super().__init__(description)
        self.type = "Categorical"
        self.statistics = None
        return self.statistics

    def get_statistics(self, values):
        self.statistics = dict()
        self.statistics["count"] = values.size
        self.statistics["missing"] = values.isna().sum()
        self.statistics["cardinality"] = values.nunique()
        self.statistics["percent_missing"] = round((values.isna().sum() / self.statistics["count"]) * 100, 4)
        self.statistics["mode"] = values.value_counts().index[0]
        self.statistics["mode_frequency"] = values.value_counts().iat[0]
        self.statistics["mode_percent"] = round((self.statistics["mode_frequency"] / self.statistics["count"]) * 100, 4)
        self.statistics["mode_second"] = values.value_counts().index[1]
        self.statistics["mode_second_frequency"] = values.value_counts().iat[1]
        self.statistics["mode_second_percent"] = round((self.statistics["mode_second_frequency"] / self.statistics["count"]) * 100, 4)
        return self.statistics
