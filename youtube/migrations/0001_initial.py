# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('thumbnail', models.URLField()),
                ('published_at', models.DateTimeField(verbose_name=b'publish time')),
                ('channel_id', models.TextField(unique=True)),
                ('uploads_playlist_id', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('thumbnail', models.URLField()),
                ('published_at', models.DateTimeField(verbose_name=b'publish time')),
                ('video_id', models.TextField(unique=True)),
                ('channel', models.ForeignKey(to='youtube.Channel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
