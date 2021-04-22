"""
Import the DecisionTreeClassifier model.
"""


from sklearn.tree import DecisionTreeClassifier


class CARTAlgorithm:

    """
    Class which represents the CART Algorithm(Classification and Regression Trees) for Decision Trees
    in order goal to to create a model that predicts the value of a target variable by learning simple decision rules
    inferred from the data features
    """

    def __init__(self, data_train, target_train, data_test, target_test, impurity_metric):
        """

        :param data_train: features data used to train
        :param target_train: target data used to train
        :param data_test: features data used to tes
        :param target_test: target data used to test
        :param impurity_metric: type of impurity metric used for the algorithm (entropy, gini)
        """
        self.model = DecisionTreeClassifier(criterion=impurity_metric)
        self.data_train = data_train
        self.target_train = target_train
        self.data_test = data_test
        self.target_test = target_test

    def build_model(self):
        """
        Build a decision tree classifier from the training set
        :return: None, model attribute is updated according to data
        """
        self.model.fit(self.data_train, self.target_train)

    def get_statistical_measures(self):
        score = self.model.score(self.target_test, self.get_predictions(self.data_test))
        return score

    def get_predictions(self, data_to_predict):
        """
        Get prediction
        :return:
        """
        results = self.model.predict(data_to_predict)
        return results

