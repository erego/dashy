from unittest import TestCase

import pandas as pd

from Predilectura.mlearning.multilayer_perceptron_based import PerceptronsAlgorithm


class TestPerceptronAlgorithm(TestCase):
    def setUp(self):
        self.data_train = pd.DataFrame([{'col1': -1, 'col2': -1, 'target': 1},
                                        {'col1': -2, 'col2': -1, 'target': 1},
                                        {'col1': -3, 'col2': -2, 'target': 1},
                                        {'col1': 1, 'col2': 1, 'target': 2},
                                        {'col1': 2, 'col2': 1, 'target': 2},
                                        {'col1': 3, 'col2': 2, 'target': 2}
                                        ])

        self.data_test = pd.DataFrame([{'col1': 2, 'col2': 2, 'target': 1},
                                       {'col1': 0, 'col2': 0, 'target': 1},
                                       {'col1': 3, 'col2': 3, 'target': 2},
                                       {'col1': 9, 'col2': 9, 'target': 2}
                                       ])

        self.x_train = self.data_train[['col1', 'col2']]
        self.y_train = self.data_train['target']
        self.x_test = self.data_test[['col1', 'col2']]
        self.y_test = self.data_test['target']

    def test_perceptron(self):
        perceptron_model = PerceptronsAlgorithm(self.x_train, self.y_train, self.x_test, self.y_test)
        perceptron_model.build_model()
        predict = perceptron_model.get_predictions([[-0.8, -1]])
        self.assertEqual(predict[0], 1)
        statistical_measures = perceptron_model.get_statistical_metrics()
        self.assertEqual(statistical_measures["accuracy"], 0.5)
