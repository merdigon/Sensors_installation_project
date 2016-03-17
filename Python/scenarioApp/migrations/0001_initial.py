# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensorApp', '0006_sensorregistration_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField()),
                ('scenario_name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScenarioElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_warning', models.BooleanField(default=False)),
                ('integer_below', models.IntegerField()),
                ('integer_above', models.IntegerField()),
                ('trigger_when', models.BooleanField()),
                ('option', models.ForeignKey(to='sensorApp.SensorOption')),
                ('scenario', models.ForeignKey(to='scenarioApp.Scenario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
