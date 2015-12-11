# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(default=b'', max_length=255, blank=True)),
                ('first_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('last_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'T', b'Transgender')])),
                ('location', models.CharField(default=b'', max_length=255, blank=True)),
                ('score', models.CharField(default=b'0', max_length=10, null=True, blank=True)),
                ('facebook_user', models.BooleanField(default=True)),
                ('facebook_id', models.CharField(default=b'', max_length=255, blank=True)),
                ('device_token', models.CharField(default=b'', max_length=255, blank=True)),
                ('send_notifications', models.BooleanField(default=True)),
                ('fake_user', models.BooleanField(default=False)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address')),
                ('date_of_birth', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(related_name='auth_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UpperUserProfile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('users.userprofile',),
        ),
        migrations.AlterUniqueTogether(
            name='userprofile',
            unique_together=set([('username', 'facebook_id')]),
        ),
    ]
