# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('votes', '0003_remove_thevote_total_votes_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=b'images/%Y/%m/%d')),
                ('question', models.CharField(help_text=b'Title of card', max_length=255)),
                ('question_type', models.IntegerField(default=0)),
                ('left_votes_count', models.BigIntegerField(default=0)),
                ('right_votes_count', models.BigIntegerField(default=0)),
                ('facebook_shared', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('category', models.ForeignKey(related_name='category', to='votes.Category')),
                ('user', models.ForeignKey(related_name='twin_vote', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.RemoveField(
            model_name='thevote',
            name='category',
        ),
        migrations.RemoveField(
            model_name='thevote',
            name='user',
        ),
        migrations.DeleteModel(
            name='TheVote',
        ),
    ]
