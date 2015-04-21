import iso8601
from django.db import models
from common.models import BaseModel
from .utils import YoutubeAPIQuery

class YoutubeModel(BaseModel):
    title = models.TextField()
    description = models.TextField()
    thumbnail = models.URLField()
    published_at = models.DateTimeField('publish time')

    @classmethod
    def convert_timestamp_strings(cls, info):
        if 'published_at' in info:
            info['published_at'] = iso8601.parse_date(info['published_at'])
        return info

    @classmethod
    def create_from_info(cls, info):
        info = cls.convert_timestamp_strings(info)
        return cls(**info)

    class Meta:
        abstract = True


class VideoModel(YoutubeModel):
    video_id = models.TextField(unique=True)

    class Meta:
        abstract = True


class Channel(YoutubeModel):
    channel_id = models.TextField(unique=True)
    uploads_playlist_id = models.TextField()

    @classmethod
    def create_from_web(cls, channel_id=None, username=None):
        if (channel_id is None and username is None) or (channel_id is not None and username is not None):
            raise AttributeError("Exactly one attribute is required.")
        if username is not None:
            channel_info = YoutubeAPIQuery.get_user(username)
        else:
            channel_info = YoutubeAPIQuery.get_channel(channel_id)
        return cls.create_from_info(**channel_info)


class Video(VideoModel):
    channel = models.ForeignKey(Channel, related_name='videos')

    @classmethod
    def create_from_web(cls, video_id):
        video_info = YoutubeAPIQuery.get_video(video_id)
        return cls.create_from_info(**video_info)