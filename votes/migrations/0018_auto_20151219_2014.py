# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0017_cardlist_data_changes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardlist',
            old_name='data_changes',
            new_name='data_changed',
        ),
    ]
