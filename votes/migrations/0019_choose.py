# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0018_auto_20151219_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choose',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(default=b'Your cards are ready for the day!', max_length=255)),
                ('ready', models.BooleanField(default=True)),
                ('last_update', models.DateTimeField(auto_now_add=True)),
                ('lists', models.ManyToManyField(related_name='choose', to='votes.CardList')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
