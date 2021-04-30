"""
Class to define machine learning models related to similarity based learning
"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix


class KMeansAlgorithm:
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
        self.model = KMeans(n_clusters=2, random_state=0)
        self.data_train = data_train
        self.target_train = target_train
        self.data_test = data_test
        self.target_test = target_test
        self.cluster = dict()

    def build_model(self):
        """
        Build a 2-means from the training set
        :return: None, model attribute is updated according to data
        """
        self.model.fit(self.data_train)
        self.cluster = self.get_clusters()

    def get_clusters(self):
        """
        This method associate each cluster to read or not read according to data train

        :return: A dictionary with tho values read associate to the number or cluster related and notread
        associated to the number of cluster related
        """
        dict_clusters = dict()
        predictions = self.get_predictions(self.data_train)
        df_cluster = pd.DataFrame({'target': self.target_train, 'cluster': predictions})
        total_read = df_cluster[df_cluster["target"] == 1].shape[0]
        total_read_cluster0 = df_cluster[(df_cluster["target"] == 1) & (df_cluster["cluster"] == 0)].shape[0]
        if total_read_cluster0 > total_read/2:
            dict_clusters["read"] = 0
            dict_clusters["notread"] = 1
        else:
            dict_clusters["notread"] = 0
            dict_clusters["read"] = 1

        return dict_clusters

    def get_statistical_metrics(self):
        predictions = self.get_predictions(self.data_test)

        if self.cluster["read"] == 0:
            test_values = self.target_test.copy().replace({0: 1, 1: 0})
        else:
            test_values = self.target_test.copy()
        tn, fp, fn, tp = confusion_matrix(test_values, predictions).ravel()
        accuracy = (tp + tn)/(tn + fn + tp + fp)
        recall = tp/(tp+fn)
        specificity = tn/(tn+fp)
        precision = tp/(tp+fp)
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


class KNearstNeighboursAlgorithm:
    """
       Class which represents the C4.5 Algorithm(Classification and Regression Trees) for Decision Trees
       in order goal to to create a model that predicts the value of a target variable by learning simple decision rules
       inferred from the data features
       """

    def __init__(self, data_train, target_train, data_test, target_test):
        """

        :param data_train: features data used to train
        :param target_train: target data used to train
        :param data_test: features data used to tes
        :param target_test: target data used to test

        """
        self.model = KNeighborsClassifier(n_neighbors=2)
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
