from django.db import models
from django.contrib.auth.models import User

from oauth2client.django_orm import CredentialsField


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

#TODO add constraints to hour and num_sessions
class HourlyDataModel(models.Model):
    date = models.DateField("The date that the session occurred")
    hour = models.IntegerField("The hour that the session occurred")
    #TODO consider subclassing to add min value and max value
    num_sessions = models.IntegerField("The number of sessions")
    #TODO consider subclassing to add min value

    def __unicode__():
        formattable_str = "date:{}  hour:{}  number of sessions:{}"
        return formattable_str.format(self.date, self.hour, self.num_sessions)

