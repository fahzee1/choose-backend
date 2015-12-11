# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0012_auto_20151209_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='left_votes_count',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='card',
            name='right_votes_count',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
