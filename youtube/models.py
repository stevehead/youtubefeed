import iso8601
import re
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from common.models import BaseModel
from .utils import YoutubeAPIQuery


class YoutubeModel(BaseModel):
    title = models.TextField()
    description = models.TextField()
    thumbnail = models.URLField()
    published_at = models.DateTimeField('publish time')

    default_duration = 0
    default_timestamp = iso8601.parse_date('2000-01-01T00:00:00.000Z')

    @classmethod
    def clean_info(cls, info):
        if 'published_at' in info and info['published_at'] is not None:
            info['published_at'] = iso8601.parse_date(info['published_at'])
        else:
            info['published_at'] = cls.default_timestamp
        return info

    def set_info_from_youtube(self, info):
        info = self.clean_info(info)
        for key, value in info.iteritems():
            setattr(self, key, value)

    @staticmethod
    def convert_duration_string_to_seconds(duration):
        regex_search = re.search('PT(\d)M(\d)S', duration)
        seconds = int(regex_search.group(1)) * 60
        seconds += int(regex_search.group(2))
        return seconds

    class Meta:
        abstract = True


class VideoModel(YoutubeModel):
    id = models.CharField(primary_key=True, max_length=11)

    class Meta:
        abstract = True


class Channel(YoutubeModel):
    id = models.CharField(primary_key=True, max_length=24)
    uploads_playlist_id = models.CharField(max_length=34)

    @classmethod
    def create_from_youtube(cls, channel_id=None, username=None):
        if (channel_id is None and username is None) or (channel_id is not None and username is not None):
            raise AttributeError("Exactly one attribute is required.")
        if username is not None:
            channel_info = YoutubeAPIQuery.get_user(username)
        else:
            channel_info = YoutubeAPIQuery.get_channel(channel_id)
        channel = cls()
        channel.set_info_from_youtube(channel_info)
        channel.save()
        return channel

    def update_from_youtube(self):
        channel_info = YoutubeAPIQuery.get_channel(self.pk)
        self.set_info_from_youtube(channel_info)
        self.save()


class Video(VideoModel):
    channel = models.ForeignKey(Channel, related_name='videos')

    def save(self, *args, **kwargs):
        try:
            Channel.objects.get(pk=self.channel_id)
        except ObjectDoesNotExist:
            Channel.create_from_youtube(channel_id=self.channel_id)
        super(VideoModel, self).save(*args, **kwargs)

    @classmethod
    def clean_info(cls, info):
        info = VideoModel.clean_info(info)
        info['duration'] = cls.convert_duration_string_to_seconds(info['duration'])
        return info

    @classmethod
    def create_from_youtube(cls, video_id):
        video_info = YoutubeAPIQuery.get_video(video_id)
        video = cls()
        video.set_info_from_youtube(video_info)
        video.save()
        return video

    def update_from_youtube(self):
        video_info = YoutubeAPIQuery.get_video(self.pk)
        self.set_info_from_youtube(video_info)
        self.save()