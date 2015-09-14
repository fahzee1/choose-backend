# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TheVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=b'images')),
                ('left_label', models.CharField(help_text=b'Most likely name of user', max_length=255)),
                ('right_label', models.CharField(help_text=b'Most likey name of celebrity', max_length=255)),
                ('total_votes_count', models.BigIntegerField(default=0)),
                ('total_votes_yes', models.BigIntegerField(default=0)),
                ('total_votes_no', models.BigIntegerField(default=0)),
                ('facebook_shared', models.BooleanField(default=False)),
                ('category', models.ForeignKey(related_name='category', to='votes.Category')),
                ('user', models.ForeignKey(related_name='twin_vote', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
