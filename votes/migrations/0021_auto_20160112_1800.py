# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0020_auto_20160112_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='fake_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='card',
            name='fake_notification_count',
            field=models.IntegerField(default=0, help_text=b'This is the amount of times we sent fake notifications'),
        ),
    ]
