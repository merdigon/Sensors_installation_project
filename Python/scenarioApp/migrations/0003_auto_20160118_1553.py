# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenarioApp', '0002_auto_20160118_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenarioelement',
            name='is_warning',
        ),
        migrations.AddField(
            model_name='scenario',
            name='is_warning',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
