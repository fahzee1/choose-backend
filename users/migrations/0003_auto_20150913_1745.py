# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={},
        ),
        migrations.AlterField(
            model_name='token',
            name='key',
            field=models.CharField(max_length=40, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.CharField(default=b'', max_length=3, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'T', b'Transgender')]),
        ),
        migrations.AlterUniqueTogether(
            name='userprofile',
            unique_together=set([('username', 'facebook_id')]),
        ),
    ]
