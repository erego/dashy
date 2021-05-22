from unittest import TestCase
import datetime


class TestDateTime(TestCase):
    def setUp(self):
        self.created_at = '2019-11-22T11:26:09.643Z'
        self.updated_at = '2019-11-27T15:31:03.000Z'

    def test_utctime(self):
        date_time_created = datetime.datetime.strptime(self.created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        date_time_updated = datetime.datetime.strptime(self.updated_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        difference = date_time_updated - date_time_created
        days, seconds = difference.days, difference.seconds
        hours = days * 24 + seconds // 3600
        self.assertEqual(days, 5)
        self.assertEqual(hours, 124)




