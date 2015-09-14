# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thevote',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='thevote',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
