"""
Class to define machine learning models related to probability based learning
"""
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix


class NaiveBayesAlgorithm:
    """
       Class which represents the K-Means Algorithm(Clustering Algortihms). In this case will be a 2-Means algorithm
       for binary
       classification(read or not read)
       """

    def __init__(self, data_train, target_train, data_test, target_test):
        """

        :param data_train: features data used to train
        :param data_test: features data used to tes
        :param target_test: target data used to test
        """
        self.model = GaussianNB()
        self.data_train = data_train
        self.target_train = target_train
        self.data_test = data_test
        self.target_test = target_test

    def build_model(self):
        """
        Build a 2-means from the training set
        :return: None, model attribute is updated according to data
        """
        self.model.fit(self.data_train, self.target_train)


    def get_statistical_metrics(self):
        predictions = self.get_predictions(self.data_test)
        tn, fp, fn, tp = confusion_matrix(self.target_test, predictions).ravel()
        accuracy = (tp + tn) / (tn + fn + tp + fp)
        recall = tp / (tp + fn)
        specificity = tn / (tn + fp)
        precision = tp / (tp + fp)
        f1_score = 2 * (recall * precision) / (recall + precision)
        dict_metrics = {"accuracy": accuracy, "recall": recall, "specificity": specificity,
                        "precision": precision, "f1_score": f1_score}
        return dict_metrics

    def get_predictions(self, data_to_predict):
        """
        Get prediction
        :return:
        """
        results = self.model.predict(data_to_predict)
        return results

