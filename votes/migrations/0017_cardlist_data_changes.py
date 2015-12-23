# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0016_auto_20151219_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardlist',
            name='data_changes',
            field=models.BooleanField(default=False),
        ),
    ]
