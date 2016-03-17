# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensorApp', '0003_auto_20160116_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorconstantoption',
            name='is_info',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sensoroption',
            name='is_info',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensorhistory',
            name='integer_value',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensoroption',
            name='integer_value',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
