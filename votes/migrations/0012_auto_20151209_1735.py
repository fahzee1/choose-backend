# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0011_auto_20151204_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of Card list', max_length=255)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='Tag',
        ),
        migrations.RemoveField(
            model_name='card',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='card',
            name='category',
        ),
        migrations.AddField(
            model_name='card',
            name='tags',
            field=models.ManyToManyField(related_name='tag', null=True, to='votes.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='cardlist',
            name='cards',
            field=models.ManyToManyField(to='votes.Card'),
        ),
    ]
