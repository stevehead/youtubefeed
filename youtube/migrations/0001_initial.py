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
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('thumbnail', models.URLField()),
                ('published_at', models.DateTimeField(verbose_name=b'publish time')),
                ('id', models.CharField(max_length=22, serialize=False, primary_key=True)),
                ('uploads_playlist_id', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('thumbnail', models.URLField()),
                ('published_at', models.DateTimeField(verbose_name=b'publish time')),
                ('id', models.CharField(max_length=11, serialize=False, primary_key=True)),
                ('video_id', models.TextField(unique=True)),
                ('channel', models.ForeignKey(related_name='videos', to='youtube.Channel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
