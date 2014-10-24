# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('googleAnalytics', '0004_auto_20141024_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hourlydatamodel',
            name='hour',
            field=models.IntegerField(verbose_name=b'The hour that the session occurred', validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='hourlydatamodel',
            name='num_sessions',
            field=models.IntegerField(verbose_name=b'The number of sessions', validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
