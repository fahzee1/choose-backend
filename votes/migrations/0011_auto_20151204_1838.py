# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0010_auto_20151204_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharetext',
            name='display',
            field=models.CharField(default=b'popup', max_length=6, choices=[(b'alert', b'UIAlert'), (b'popup', b'UIPopup'), (b'banner', b'Banner')]),
        ),
        migrations.AlterField(
            model_name='sharetext',
            name='message',
            field=models.CharField(max_length=255),
        ),
    ]
