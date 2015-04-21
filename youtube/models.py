from django.db import models
from common.models import BaseModel


class YoutubeModel(BaseModel):
    title = models.TextField()
    description = models.TextField()
    thumbnail = models.UrlField()
    published_at = models.DateTimeField('publish time')

    class Meta:
        abstract = True


class Channel(YoutubeModel):
    channel_id = models.TextField(unique=True)
    uploads_playlist_id = models.TextField


class Video(YoutubeModel):
    channel = models.ForeignKey(Channel)
    video_id = models.TextField(unique=True)