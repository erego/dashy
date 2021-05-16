"""
Class to define machine learning models related to information based learning
"""

import pickle
import multiprocessing
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import confusion_matrix

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
        # from sklearn import tree
        # text_representation = tree.export_text(self.model, feature_names=self.columns)
        # with open("./decision_tree.log", "w") as file_out:
        #     file_out.write(text_representation)

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
        self.model = None
        self.data_train = data_train
        self.target_train = target_train
        self.data_test = data_test
        self.target_test = target_test

    def build_model(self):
        """
        Build a decision tree classifier from the training set
        :return: None, model attribute is updated according to data
        """
        param_grid = {'n_estimators': [150],
                      'max_features': [5, 7, 9],
                      'max_depth': [None, 3, 10, 20],
                      'criterion': ['gini', 'entropy']
                      }

        grid = GridSearchCV(
            estimator=RandomForestClassifier(random_state=123),
            param_grid=param_grid,
            scoring='accuracy',
            n_jobs=multiprocessing.cpu_count() - 1,
            cv=RepeatedKFold(n_splits=5, n_repeats=3, random_state=123),
            refit=True,
            verbose=0,
            return_train_score=True
        )

        grid.fit(X=self.data_train, y=self.target_train)
        self.model = grid.best_estimator_

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
