# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('googleAnalytics', '0003_auto_20141023_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourlyDataModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'The date that the session occurred')),
                ('hour', models.IntegerField(verbose_name=b'The hour that the session occurred')),
                ('num_sessions', models.IntegerField(verbose_name=b'The number of sessions')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='HourlySessions',
        ),
    ]
