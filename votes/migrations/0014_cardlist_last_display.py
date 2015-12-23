# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0013_auto_20151209_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardlist',
            name='last_display',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 15, 17, 33, 33, 878327, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
