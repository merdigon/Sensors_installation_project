# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenarioApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='message',
            field=models.CharField(default='none', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scenarioelement',
            name='integer_above',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scenarioelement',
            name='integer_below',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scenarioelement',
            name='trigger_when',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
