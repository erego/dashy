from unittest import TestCase

import pandas as pd

from Predilectura.mlearning.information_based import CARTAlgorithm, C4dot5Algorithm, RandomForestAlgorithm


class TestTreeAlgorithm(TestCase):
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

        self.data_train_c45 = pd.DataFrame([{'Outlook': 'Sunny', 'Temperature': 85, 'Humidity': 85, 'Wind': 'Weak',
                                            'Decision': 'No'},
                                           {'Outlook': 'Sunny', 'Temperature': 80, 'Humidity': 90, 'Wind': 'Strong',
                                            'Decision': 'No'},
                                           {'Outlook': 'Overcast', 'Temperature': 83, 'Humidity': 78, 'Wind': 'Weak',
                                            'Decision': 'Yes'},
                                           {'Outlook': 'Rain', 'Temperature': 70, 'Humidity': 96, 'Wind': 'Weak',
                                            'Decision': 'Yes'},
                                           {'Outlook': 'Rain', 'Temperature': 68, 'Humidity': 80, 'Wind': 'Weak',
                                            'Decision': 'Yes'},
                                           {'Outlook': 'Rain', 'Temperature': 65, 'Humidity': 70, 'Wind': 'Strong',
                                            'Decision': 'No'},
                                           {'Outlook': 'Rain', 'Temperature': 64, 'Humidity': 65, 'Wind': 'Strong',
                                            'Decision': 'Yes'}])

        self.data_test_c45 = pd.DataFrame([{'Outlook': 'Sunny', 'Temperature': 72, 'Humidity': 95, 'Wind': 'Weak',
                                            'Decision': 'No'},
                                           {'Outlook': 'Sunny', 'Temperature': 69, 'Humidity': 70, 'Wind': 'Weak',
                                            'Decision': 'Yes'},
                                           {'Outlook': 'Rain', 'Temperature': 75, 'Humidity': 80, 'Wind': 'Weak',
                                            'Decision': 'Yes'}])

        self.x_train_c45 = self.data_train_c45[['Outlook', 'Temperature', 'Humidity', 'Wind']]
        self.y_train_c45 = self.data_train_c45['Decision']
        self.x_test_c45 = self.data_test_c45[['Outlook', 'Temperature', 'Humidity', 'Wind']]
        self.y_test_c45 = self.data_test_c45['Decision']

    def test_cart(self):
        cart_model = CARTAlgorithm(self.x_train, self.y_train, self.x_test, self.y_test,
                                   "entropy")
        cart_model.build_model()
        predict = cart_model.get_predictions([[3., 3.]])
        self.assertEqual(predict[0], 0)
        statistical_measures = cart_model.get_statistical_metrics()
        self.assertEqual(statistical_measures["accuracy"], 0.5)

    def test_c4dot5(self):

        c4dot5_model = C4dot5Algorithm(self.x_train_c45, self.y_train_c45, self.x_test_c45, self.y_test_c45)
        c4dot5_model.build_model()

        df_to_predict = pd.concat([self.x_test_c45, self.y_test_c45], axis=1)
        predict = c4dot5_model.get_predictions(df_to_predict)
        self.assertEqual(predict[0][0], "No")
        statistical_measures = c4dot5_model.get_statistical_metrics()
        self.assertEqual(statistical_measures["recall"], 0.5)

