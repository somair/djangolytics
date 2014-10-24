from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

from oauth2client.django_orm import CredentialsField


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

class HourlyDataModel(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField("The date that the session occurred")
    hour = models.IntegerField("The hour that the session occurred",
            validators=[MaxValueValidator(23), MinValueValidator(0)])
    num_sessions = models.IntegerField("The number of sessions",
            validators=[MinValueValidator(0)])

    def __unicode__(self):
        formattable_str = "date:{}  hour:{}  number of sessions:{}"
        return formattable_str.format(self.date, self.hour, self.num_sessions)

