# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0004_auto_20151116_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='category',
            field=models.ForeignKey(related_name='category', blank=True, to='votes.Category', null=True),
        ),
    ]
