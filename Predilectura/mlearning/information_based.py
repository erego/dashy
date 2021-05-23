"""
Class to define machine learning models related to information based learning
"""

import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn import tree
from xgboost import XGBClassifier
from chefboost import Chefboost


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

    def export_tree(self, lst_features):
        """
        Export the decision tree in text format
        :param lst_features: List of features of dataset
        :return: Decision tree in text format
        """

        text_representation = tree.export_text(self.model, feature_names=lst_features)
        with open("./decision_tree_cart.log", "w") as file_out:
            file_out.write(text_representation)

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


class C4dot5Algorithm:
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
        target_train = target_train.rename('Decision', inplace=True)
        target_train.replace({0: "No", 1: "Yes"}, inplace=True)
        target_test = target_test.rename('Decision', inplace=True)
        target_test.replace({0: "No", 1: "Yes"}, inplace=True)

        self.model = None
        self.data_train = data_train
        self.target_train = target_train
        self.data_test = data_test
        self.target_test = target_test
        self.config = {'algorithm': 'C4.5'}

    def build_model(self):
        """
        Build a decision tree classifier from the training set
        :return: None, model attribute is updated according to data
        """

        df_to_build = pd.concat([self.data_train, self.target_train], axis=1)

        self.model = Chefboost.fit(df_to_build,
                                   config=self.config,
                                   validation_df=pd.concat([self.data_test, self.target_test], axis=1))

    def save_model(self, path_to_save):
        """
        Save a C4.5 model to an specific path
        :param path_to_save: path to save the mode
        :return: None, model saved in the specific path
        """

        model = self.model.copy()

        # modules cannot be saved. Save its reference instead.
        module_names = []
        for tree in model["trees"]:
            module_names.append(tree.__name__)

        model["trees"] = module_names

        f = open(path_to_save, "wb")
        pickle.dump(model, f)
        f.close()

    def get_predictions(self, data_to_predict):
        """
        Get prediction
        :return:
        """
        results = []
        for index, row in data_to_predict.iterrows():
            prediction = Chefboost.predict(self.model, param=row)
            actual = row["Decision"]
            results.append((prediction, actual))

        return results

    def get_statistical_metrics(self):
        df_statistics = pd.concat([self.data_test, self.target_test], axis=1)
        predictions = self.get_predictions(df_statistics)
        tp, tn, fp, fn = 0, 0, 0, 0

        for prediction in predictions:
            if (prediction[0] == prediction[1]) and prediction[0] == "Yes":
                tp += 1
            elif (prediction[0] == prediction[1]) and prediction[0] == "No":
                tn += 1
            elif (prediction[0] != prediction[1]) and prediction[0] == "Yes":
                fp += 1
            elif (prediction[0] != prediction[1]) and prediction[0] == "No":
                fn += 1

        accuracy = (tp + tn) / (tn + fn + tp + fp)
        recall = tp / (tp + fn)
        specificity = tn / (tn + fp)
        precision = tp / (tp + fp)
        f1_score = 2 * (recall * precision) / (recall + precision)
        dict_metrics = {"accuracy": accuracy, "recall": recall, "specificity": specificity,
                        "precision": precision, "f1_score": f1_score}
        return dict_metrics


class RandomForestAlgorithm:
    """
    Class which represents the Random Forest for Decision Trees
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
        self.model = RandomForestClassifier(criterion='entropy', max_depth=3, max_features=5,
                                               n_estimators=150)
        self.data_train = data_train
        self.target_train = target_train
        self.data_test = data_test
        self.target_test = target_test

    def build_model(self):
        """
        Build a decision tree classifier from the training set
        :return: None, model attribute is updated according to data
        """

        self.model.fit(X=self.data_train, y=self.target_train)

    def export_tree(self, lst_features):
        """
        Export the decision tree in text format
        :param lst_features: List of features of dataset
        :return: Decision tree in text format
        """

        text_representation = tree.export_text(self.model.estimators_[0], feature_names=lst_features)
        with open("./decision_tree_rf.log", "w") as file_out:
            file_out.write(text_representation)

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



class GradientBoostingAlgorithm:
    """
    Class which represents the Gradient Boostings for Decision Trees
    in order goal to to create a model that predicts the value of a target variable by learning simple decision rules
    inferred from the data features
    """

    def __init__(self, data_train, target_train, data_test, target_test, lst_features):
        """

        :param data_train: features data used to train
        :param target_train: target data used to train
        :param data_test: features data used to tes
        :param target_test: target data used to test
         """
        self.model = XGBClassifier(feature_names=lst_features)
        self.data_train = data_train
        self.target_train = target_train
        self.data_test = data_test
        self.target_test = target_test

    def build_model(self):
        """
        Build a decision tree classifier from the training set
        :return: None, model attribute is updated according to data
        """

        self.model.fit(X=self.data_train, y=self.target_train)

        print(self.model.feature_importances_)


    def export_tree(self):
        """
        Export the decision tree in text format
        :param lst_features: List of features of dataset
        :return: Decision tree in text format
        """
        import matplotlib.pyplot as plt
        from xgboost import plot_tree, plot_importance
        ##set up the parameters
        plot_importance(self.model)
        plt.savefig('importance.png')
        plot_tree(self.model)

        plt.savefig('tree.png')
        plt.show()

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
