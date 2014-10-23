from django.db import models
from django.contrib.auth.models import User

from oauth2client.django_orm import CredentialsField


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

class Sessions(models.Model):
    start_datetime = models.DateTimeField("Session start time")
