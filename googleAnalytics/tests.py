from datetime import date
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from googleAnalytics.models import HourlyDataModel
from googleAnalytics.utils import create_date_from_str

class HourlyDataModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test user")
        self.dt1 = create_date_from_str("2014-10-05")
        self.dt2 = create_date_from_str("2014-10-07")
        HourlyDataModel.objects.create(user=self.user, date=self.dt1,
                hour = 0, num_sessions = 4)
        HourlyDataModel.objects.create(user=self.user, date=self.dt2,
                hour = 20, num_sessions = 2)

    def test_HourlyDataModel_construtor(self):
        time1 = HourlyDataModel.objects.get(hour=0)
        time2 = HourlyDataModel.objects.get(hour=20)

        self.assertEquals(time1.hour, 0) # Can get existing data
        self.assertEquals(time1.num_sessions, 4)
        self.assertEquals(time1.date, self.dt1)
        self.assertEquals(time1.user, self.user)

        self.assertEquals(time2.hour, 20)
        self.assertEquals(time2.num_sessions, 2)
        self.assertEquals(time2.date, self.dt2)
        self.assertEquals(time1.user, self.user)

    def test_HourlyDataModel_bad_construtor(self):
        bad_params = [
            {"date":self.dt1, "hour":-1, "num_sessions": 2},
            {"date":self.dt1, "hour":24, "num_sessions": 2},
            {"date":self.dt1, "hour":2, "num_sessions": -1}
        ]
        for params in bad_params:
            m = HourlyDataModel(**params)
            self.assertRaises(ValidationError, m.clean_fields)

