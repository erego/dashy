from unittest import TestCase
import datetime
import pandas as pd

class TestDateTime(TestCase):
    def setUp(self):
        self.created_at = '2019-11-22T11:26:09.643Z'
        self.updated_at = '2019-11-27T15:31:03.000Z'
        self.datetime_test = pd.DataFrame([{'edition_id': 2895389, 'user_id': 2142047,
                                            'created_at': '2019-11-22T11:31:18.642Z',
                                            'updated_at': '2019-11-22T11:31:18.642Z'},
                                           {'edition_id': 2895389, 'user_id': 2142047,
                                            'created_at': '2019-12-02T10:00:22.000Z',
                                            'updated_at': '2019-12-02T10:00:26.478Z'},
                                           {'edition_id': 2895389, 'user_id': 2142047,
                                            'created_at': '2019-11-27T15:31:03.000Z',
                                            'updated_at': '2019-11-27T15:31:05.730Z'},
                                           {'edition_id': 2895389, 'user_id': 2142047,
                                            'created_at': '2019-12-02T10:00:27.000Z',
                                            'updated_at': '2019-12-02T10:00:31.533Z'},
                                           {'edition_id': 2895396, 'user_id': 2142047,
                                            'created_at': '2019-12-02T10:02:22.000Z',
                                            'updated_at': '2019-12-02T10:02:23.631Z'},
                                           {'edition_id': 2895396, 'user_id': 2142047,
                                            'created_at': '2019-12-02T10:02:24.000Z',
                                            'updated_at': '2019-12-02T10:02:28.043Z'},
                                           {'edition_id': 2895396, 'user_id': 2142047,
                                            'created_at': '2019-12-02T10:02:25.000Z',
                                            'updated_at': '2019-12-02T10:02:28.174Z'},
                                           {'edition_id': 2895401, 'user_id': 2142704,
                                            'created_at': '2019-12-14T18:43:23.000Z',
                                            'updated_at': '2019-12-14T18:43:23.928Z'},
                                           {'edition_id': 2895401, 'user_id': 2142704,
                                            'created_at': '2019-12-14T18:43:33.000Z',
                                            'updated_at': '2019-12-14T18:43:34.130Z'}])

    def test_utctime(self):
        date_time_created = datetime.datetime.strptime(self.created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        date_time_updated = datetime.datetime.strptime(self.updated_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        difference = date_time_updated - date_time_created
        days, seconds = difference.days, difference.seconds
        hours = days * 24 + seconds // 3600
        self.assertEqual(days, 5)
        self.assertEqual(hours, 124)

    def test_features_time(self):
        self.datetime_test['created_at'] = pd.to_datetime(self.datetime_test['created_at'],
                                                          format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')
        self.datetime_test['updated_at'] = pd.to_datetime(self.datetime_test['updated_at'],
                                                          format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')

        self.datetime_test.sort_values('created_at', inplace=True)

        self.datetime_test['time_diff'] = self.datetime_test.groupby(["user_id", "edition_id"])['created_at'].diff()

        self.datetime_test['time_diff'] = (self.datetime_test['time_diff'].dt.seconds) / 60

        self.datetime_test['time_diff'] = (self.datetime_test['time_diff'])

        self.assertEqual(self.datetime_test.iloc[3]['time_diff'], 0.08333333333333333)




