from mock import Mock
from datetime import datetime
from datetime import date
# Django imports
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# App imports
from googleAnalytics.models import HourlyDataModel
from googleAnalytics.utils import create_str_from_date
from googleAnalytics.utils import create_date_from_str
from googleAnalytics.utils import generate_dot_chart_data
from googleAnalytics.forms import StartEndDateForm
from googleAnalytics.forms import date_order_validator

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

class UtilsTestCase(TestCase):
    def setUp(self):
        self.cannon_date = datetime.strptime("2014-01-01", "%Y-%m-%d").date()
        self.day_after = datetime.strptime("2014-01-02", "%Y-%m-%d").date()
        self.week_after = datetime.strptime("2014-01-08", "%Y-%m-%d").date()
        self.m1 = Mock(date=self.cannon_date, hour=1, num_sessions=1)
        self.m2 = Mock(date=self.day_after, hour=1, num_sessions=2)
        self.m3 = Mock(date=self.week_after, hour=1, num_sessions=2)
        self.m4 = Mock(date=self.cannon_date, hour=3, num_sessions=4)

        # TODO test incorrect inputs to these util functions

    def test_date_from_str(self):
        out_date = create_date_from_str("2014-01-01")
        self.assertEquals(self.cannon_date, out_date)
        out_date = create_date_from_str("20140101", "%Y%m%d")
        self.assertEquals(self.cannon_date, out_date)

    def test_str_from_date(self):
        out_str = create_str_from_date(self.cannon_date)
        self.assertEquals("2014-01-01", out_str)
        out_str = create_str_from_date(self.cannon_date, "%Y%m%d")
        self.assertEquals("20140101", out_str)

    def test_generate_dot_chart_data(self):
        cannon_result = [0 for i in range(7 * 24)]  # All zeros
        mock_query_set = []
        result = generate_dot_chart_data(mock_query_set)
        self.assertEquals(168, len(result))
        self.assertEquals(cannon_result, result)  # Should be all zeros

        mock_query_set.append(self.m1)  # Add a mocked model
        cannon_result[(24*3)+1] = 1  # Set 1am wednesday to 1 session
        result = generate_dot_chart_data(mock_query_set)
        self.assertEquals(168, len(result))
        self.assertEquals(cannon_result, result)

        mock_query_set.append(self.m2)  # Add another mocked model
        cannon_result[(24*4)+1] = 2  # Set 1am thursday to 2 sessions
        result = generate_dot_chart_data(mock_query_set)
        self.assertEquals(168, len(result))
        self.assertEquals(cannon_result, result)

        mock_query_set.append(self.m3)  # Add another mocked model
        cannon_result[(24*3)+1] = 3  # Set 1am wednesday to 3 sessions (2+1)
        result = generate_dot_chart_data(mock_query_set)
        self.assertEquals(168, len(result))
        self.assertEquals(cannon_result, result)

        mock_query_set.append(self.m4)  # Add another mocked model
        cannon_result[(24*3)+3] = 4  # Set 3am wednesday to 4 sessions
        result = generate_dot_chart_data(mock_query_set)
        self.assertEquals(168, len(result))
        self.assertEquals(cannon_result, result)

class FomsTestCase(TestCase):
    def test_date_order_validator(self):
        """Should raise a validation error if the second date is before the
        first date"""
        date1 = datetime.strptime("2014-01-01", "%Y-%m-%d").date()
        date2 = datetime.strptime("2014-01-02", "%Y-%m-%d").date()
        self.assertEquals(None, date_order_validator(date1, date2))
        self.assertEquals(None, date_order_validator(date1, date1))
        self.assertRaises(ValidationError, date_order_validator, date2, date1)

    def test_StartEndDateForm(self):
        form_data_good = [{"start_date":"2014-01-01", "end_date":"2014-01-01"},
                          {"start_date":"2014-01-01", "end_date":"2014-02-02"}]
        for form_data in form_data_good:
            form = StartEndDateForm(form_data)
            self.assertTrue(form.is_valid())

        form_data_bad = [{"start_date":"", "end_date":""},
                         {"start_date":"2014-01-01", "end_date":""},
                         {"start_date":"2014-01-01", "end_date":"badger"},
                         {"start_date":"", "end_date":"2014-02-02"},
                         {"start_date":"20140101", "end_date":"20140202"}]
        for form_data in form_data_bad:
            form = StartEndDateForm(form_data)
            self.assertFalse(form.is_valid())

