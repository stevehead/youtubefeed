from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from common.models import BaseModel
from common.utils import convert_iso8601_duration_to_seconds, convert_iso8601_to_datetime
from .utils import YoutubeAPIQuery


class YoutubeModel(BaseModel):
    title = models.TextField()
    description = models.TextField()
    thumbnail = models.URLField()
    published_at = models.DateTimeField('publish time')

    def set_info_from_youtube(self, info):
        for key, value in info.iteritems():
            setattr(self, key, value)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class VideoModel(YoutubeModel):
    id = models.CharField(primary_key=True, max_length=11)

    @property
    def url(self):
        return "https://www.youtube.com/watch?v=%s" % self.pk

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

    def get_latest_videos(self, *args, **kwargs):
        return YoutubeAPIQuery.get_playlist_videos(self.uploads_playlist_id, *args, **kwargs)


class Video(VideoModel):
    channel = models.ForeignKey(Channel, related_name='videos')
    duration = models.IntegerField()

    def save(self, *args, **kwargs):
        try:
            Channel.objects.get(pk=self.channel_id)
        except ObjectDoesNotExist:
            Channel.create_from_youtube(channel_id=self.channel_id)
        super(Video, self).save(*args, **kwargs)