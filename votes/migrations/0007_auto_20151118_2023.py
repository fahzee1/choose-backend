# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0006_auto_20151117_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='left_votes_count',
            field=models.BigIntegerField(default=23),
        ),
        migrations.AlterField(
            model_name='card',
            name='right_votes_count',
            field=models.BigIntegerField(default=100),
        ),
    ]
