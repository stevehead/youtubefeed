# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedChannel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('channel', models.ForeignKey(related_name='+', to='youtube.Channel', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeedVideo',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('thumbnail', models.URLField()),
                ('published_at', models.DateTimeField(verbose_name=b'publish time')),
                ('id', models.CharField(max_length=11, serialize=False, primary_key=True)),
                ('channel', models.ForeignKey(related_name='feed_videos', to='youtube.Channel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('name', models.TextField()),
                ('video_title_format', models.TextField(default=b'', blank=True)),
                ('status', models.CharField(default=b'O', max_length=1, choices=[(b'C', b'Completed'), (b'O', b'Ongoing')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShowType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('name', models.TextField(unique=True)),
                ('name_color', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShowViewing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('name', models.TextField(unique=True)),
                ('status', models.CharField(default=b'P', max_length=1, choices=[(b'C', b'Completed'), (b'P', b'Primary'), (b'S', b'Secondary')])),
                ('show', models.ForeignKey(related_name='viewings', to='feed.Show')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoViewing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('record_updated_at', models.DateTimeField(auto_now=True, verbose_name=b'record update time')),
                ('show_viewing', models.ForeignKey(related_name='video_viewings', to='feed.ShowViewing', null=True)),
                ('video', models.ForeignKey(related_name='viewings', to='youtube.Video')),
            ],
        ),
        migrations.AddField(
            model_name='show',
            name='show_type',
            field=models.ForeignKey(related_name='shows', to='feed.ShowType'),
        ),
        migrations.AddField(
            model_name='show',
            name='videos',
            field=models.ManyToManyField(to='youtube.Video'),
        ),
        migrations.AlterUniqueTogether(
            name='videoviewing',
            unique_together=set([('video', 'show_viewing')]),
        ),
    ]
