# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0005_auto_20151116_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='branch_link',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='user',
            field=models.ForeignKey(related_name='card', to=settings.AUTH_USER_MODEL),
        ),
    ]
