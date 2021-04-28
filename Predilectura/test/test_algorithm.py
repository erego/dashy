from unittest import TestCase

import pandas as pd

from Predilectura.mlearning.information_based import CARTAlgorithm


class TestTreeAlgortihm(TestCase):
    def setUp(self):
        self.data_train = pd.DataFrame([{'col1': 1, 'col2': 1, 'target': 0},
                                        {'col1': 7, 'col2': 7, 'target': 1}])

        self.data_test = pd.DataFrame([{'col1': 2, 'col2': 2, 'target': 0},
                                       {'col1': 0, 'col2': 0, 'target': 0},
                                       {'col1': 3, 'col2': 3, 'target': 1},
                                       {'col1': 9, 'col2': 9, 'target': 1},
                                       {'col1': 15, 'col2': 15, 'target': 0},
                                       {'col1': 17, 'col2': 17, 'target': 0},
                                       {'col1': 18, 'col2': 18, 'target': 0},
                                       {'col1': 20, 'col2': 20, 'target': 1}
                                       ])

        self.x_train = self.data_train[['col1', 'col2']]
        self.y_train = self.data_train['target']
        self.x_test = self.data_test[['col1', 'col2']]
        self.y_test = self.data_test['target']

    def test_cart(self):
        cart_model = CARTAlgorithm(self.x_train, self.y_train, self.x_test, self.y_test,
                                   "entropy")
        cart_model.build_model()
        predict = cart_model.get_predictions([[3., 3.]])
        self.assertEqual(predict[0], 0)
        statistical_measures = cart_model.get_statistical_metrics()
        self.assertEqual(statistical_measures["accuracy"], 0.5)



