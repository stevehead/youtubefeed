from django.db import models
from common.models import BaseModel
from youtube.models import Channel, Video, VideoModel


class ShowType(BaseModel):
    pass


class Show(BaseModel):
    show_type = models.ForeignKey(ShowType, related_name='shows')


class ShowViewing(BaseModel):
    show = models.ForeignKey(Show, related_name='viewings')


class VideoViewing(BaseModel):
    video = models.ForeignKey(Video, related_name='viewings')
    show_viewing = models.ForeignKey(ShowViewing, null=True, related_name='video_viewings')

    class Meta:
        unique_together = ('video', 'show_viewing')


class FeedVideo(VideoModel):
    channel = models.ForeignKey(Channel, related_name='feed_videos')