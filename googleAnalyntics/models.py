from django.db import models

class Sessions(models.Model):
    start_datetime = models.DateTimeField("Session start time")
