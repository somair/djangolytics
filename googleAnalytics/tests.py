from datetime import date
from django.test import TestCase
from googleAnalytics.models import HourlyDataModel
from googleAnalytics.utils import create_date_from_str

# Create your tests here.
class HourlyDataModelTestCase(TestCase):
    def setUp(self):
        self.dt1 = create_date_from_str("2014-10-05")
        self.dt2 = create_date_from_str("2014-10-07")
        HourlyDataModel.objects.create(date=self.dt1, hour = 0, num_sessions = 4)
        HourlyDataModel.objects.create(date=self.dt2, hour = 20, num_sessions = 2)

    def test_HourlyDataModel_construtor(self):
        time1 = HourlyDataModel.objects.get(hour=0)
        time2 = HourlyDataModel.objects.get(hour=20)

        self.assertEquals(time1.hour, 0)
        self.assertEquals(time1.num_sessions, 4)
        self.assertEquals(time1.date, self.dt1)

        self.assertEquals(time2.hour, 20)
        self.assertEquals(time2.num_sessions, 2)
        self.assertEquals(time2.date, self.dt2)


