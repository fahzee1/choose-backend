# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0014_cardlist_last_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardlist',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
