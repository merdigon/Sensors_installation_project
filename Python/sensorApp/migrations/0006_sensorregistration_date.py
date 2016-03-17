# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sensorApp', '0005_sensorregistration'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorregistration',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 17, 20, 4, 14, 314000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
