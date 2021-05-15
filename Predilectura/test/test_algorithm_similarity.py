from unittest import TestCase

import pandas as pd

from Predilectura.mlearning.similarity_based import KMeansAlgorithm, KNearestNeighboursAlgorithm


class TestKMeansAlgorithm(TestCase):
    def setUp(self):

        self.data_train = pd.DataFrame([{'col1': 1, 'col2': 2, 'target': 0},
                                        {'col1': 1, 'col2': 4, 'target': 0},
                                        {'col1': 1, 'col2': 0, 'target': 0},
                                        {'col1': 10, 'col2': 2, 'target': 1},
                                        {'col1': 10, 'col2': 4, 'target': 1},
                                        {'col1': 10, 'col2': 0, 'target': 1},
                                        {'col1': 12, 'col2': 0, 'target': 1}
                                        ])

        self.data_test = pd.DataFrame([{'col1': 3, 'col2': 3, 'target': 0},
                                       {'col1': 12, 'col2': 12, 'target': 1}])

        self.x_train = self.data_train[['col1', 'col2']]
        self.y_train = self.data_train['target']
        self.x_test = self.data_test[['col1', 'col2']]
        self.y_test = self.data_test['target']

    def test_kmeans(self):
        kmeans_model = KMeansAlgorithm(self.x_train, self.y_train, self.x_test, self.y_test, "elkan")
        kmeans_model.build_model()

        a = kmeans_model.model.cluster_centers_
        predict = kmeans_model.get_predictions([[3., 3.]])
        self.assertEqual(predict[0], 1)
        predict = kmeans_model.get_predictions([[12., 12.]])
        self.assertEqual(predict[0], 0)
        statistical_measures = kmeans_model.get_statistical_metrics()
        self.assertEqual(statistical_measures["accuracy"], 1.0)


class TestKNNAlgorithm(TestCase):
    def setUp(self):

        self.data_train = pd.DataFrame([{'col1': 1, 'col2': 2, 'target': 0},
                                        {'col1': 1, 'col2': 4, 'target': 0},
                                        {'col1': 1, 'col2': 0, 'target': 0},
                                        {'col1': 10, 'col2': 2, 'target': 1},
                                        {'col1': 10, 'col2': 4, 'target': 1},
                                        {'col1': 10, 'col2': 0, 'target': 1},
                                        {'col1': 12, 'col2': 0, 'target': 1}
                                        ])

        self.data_test = pd.DataFrame([{'col1': 3, 'col2': 3, 'target': 0},
                                       {'col1': 1, 'col2': 1, 'target': 0},
                                       {'col1': 12, 'col2': 12, 'target': 1},
                                       {'col1': 9, 'col2': 9, 'target': 0}])

        self.x_train = self.data_train[['col1', 'col2']]
        self.y_train = self.data_train['target']
        self.x_test = self.data_test[['col1', 'col2']]
        self.y_test = self.data_test['target']

    def test_knn(self):
        knn_model = KNearestNeighboursAlgorithm(self.x_train, self.y_train, self.x_test, self.y_test)
        knn_model.build_model()
        predict = knn_model.get_predictions([[3., 3.]])
        self.assertEqual(predict[0], 0)
        predict = knn_model.get_predictions([[12., 12.]])
        self.assertEqual(predict[0], 1)
        statistical_measures = knn_model.get_statistical_metrics()
        self.assertEqual(statistical_measures["accuracy"], 0.75)
