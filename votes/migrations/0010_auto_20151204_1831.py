# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0009_card_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=255, blank=True)),
                ('shared', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='card',
            name='image_url',
            field=models.TextField(default=b'', help_text=b'Static Image url take from above image field', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='question_type',
            field=models.IntegerField(default=0, help_text=b'100 (A/B) or 101 (YES/NO)'),
        ),
    ]
