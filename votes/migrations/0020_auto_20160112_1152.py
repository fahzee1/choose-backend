# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0019_choose'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='left_votes_fake',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='right_votes_fake',
            field=models.BigIntegerField(default=0),
        ),
    ]
