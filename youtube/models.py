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

    def update_info_from_youtube(self, info):
        info = self.convert_timestamp_strings(info)
        for key, value in info.iteritems():
            setattr(self, key, value)

    class Meta:
        abstract = True


class VideoModel(YoutubeModel):
    id = models.CharField(primary_key=True, max_length=11)
    video_id = models.TextField(unique=True)

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
        channel.update_info_from_youtube(channel_info)
        return channel


class Video(VideoModel):
    channel = models.ForeignKey(Channel, related_name='videos')

    @classmethod
    def create_from_youtube(cls, video_id):
        video_info = YoutubeAPIQuery.get_video(video_id)
        video = cls()
        video.update_info_from_youtube(video_info)
        return video