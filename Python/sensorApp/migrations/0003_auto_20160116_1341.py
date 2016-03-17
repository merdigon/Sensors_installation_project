# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensorApp', '0002_auto_20160115_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('integer_value', models.IntegerField(null=True)),
                ('triggered', models.BooleanField(default=False)),
                ('sensor_option', models.ForeignKey(to='sensorApp.SensorOption')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sensorconstantoption',
            name='is_integer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sensorconstantoption',
            name='is_warning',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sensoroption',
            name='integer_value',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sensoroption',
            name='is_integer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
