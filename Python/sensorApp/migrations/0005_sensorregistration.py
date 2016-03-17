# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensorApp', '0004_auto_20160117_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sensor_id', models.IntegerField()),
                ('registered', models.BooleanField(default=False)),
                ('sensor_type', models.ForeignKey(to='sensorApp.SensorType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
