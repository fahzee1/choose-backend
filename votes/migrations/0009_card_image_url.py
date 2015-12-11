# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0008_card_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='image_url',
            field=models.CharField(default=b'', help_text=b'Static Image url take from above image field', max_length=255),
        ),
    ]
