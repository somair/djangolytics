from django.db import models
from django.contrib.auth.models import User

from oauth2client.django_orm import CredentialsField


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

class HourlySessions(models.Model):
    date = models.DateTimeField("The date that the session occurred")
    hour = models.IntegerField("The hour that the session occurred")
    num_sessions = models.IntegerField("The number of sessions")
