# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0015_cardlist_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardlist',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='cardlist',
            name='approved',
            field=models.BooleanField(default=False, help_text=b'Only approved items will be shown in the menu of the client'),
        ),
    ]
