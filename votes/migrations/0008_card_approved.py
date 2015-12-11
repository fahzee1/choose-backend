# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0007_auto_20151118_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
