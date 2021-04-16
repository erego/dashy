
class Feature:

    def __init__(self, description):
        self.description = description
        self.type = None

    def get_statistics(self, values):
        raise NotImplementedError()

    @staticmethod
    def check_type(values):
        if values.size/values.nunique() < 0.2:
            return "Categorical"
        else:
            return "Continuous"


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
        self.statistics["count"] = values.size
        self.statistics["percent_miss"] = values.isna().sum()
        self.statistics["cadinality"] = values.nunique()
        self.statistics["min"] = values.min()
        self.statistics["first_quartile"] = values.quantile(0.25)
        self.statistics["mean"] = values.mean()
        self.statistics["median"] = values.median()
        self.statistics["third_quartile"] = values.quantile(0.75)
        self.statistics["max"] = values.max()
        self.statistics["std_deviation"] = values.std()
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

