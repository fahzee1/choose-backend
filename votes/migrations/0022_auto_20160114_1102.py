# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0021_auto_20160112_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='created_by',
            field=models.IntegerField(default=1, choices=[(1, b'Staff'), (2, b'Community')]),
        ),
        migrations.AlterField(
            model_name='cardlist',
            name='cards',
            field=models.ManyToManyField(related_name='lists', to='votes.Card'),
        ),
    ]
