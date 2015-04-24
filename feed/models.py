from django.db import models
from common.models import BaseModel
from youtube.models import Channel, Video, VideoModel


class ShowType(BaseModel):
    name = models.TextField(unique=True, blank=False)
    name_color = models.PositiveIntegerField(default=0)

    maximum_name_color_value = int('0xFFFFFF', 0)

    @property
    def name_hex_color(self):
        if self.name_color > self.maximum_name_color_value:
            raise AttributeError("The current name color value is outside the allowed hexadecimal range")
        hex = hex(self.name_color)
        hex = hex[2:]
        hex = '0' * (6 - len(hex)) + hex.capitalize()
        return hex

    @name_hex_color.setter
    def name_hex_color(self, value):
        if value[0] == '#':
            value = '0x' + value[1:]
        decimal_value = int(value)
        if decimal_value > self.maximum_name_color_value:
            raise AttributeError("The current name color value is outside the allowed hexadecimal range")
        return decimal_value


class Show(BaseModel):
    COMPLETED = 'C'
    ONGOING = 'O'
    STATUS_CHOICES = (
        (COMPLETED, 'Completed'),
        (ONGOING, 'Ongoing'),
    )
    show_type = models.ForeignKey(ShowType, related_name='shows')
    name = models.TextField(blank=False)
    video_title_format = models.TextField(default='', blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ONGOING)
    videos = models.ManyToManyField(Video)


class ShowViewing(BaseModel):
    COMPLETED = 'C'
    PRIMARY = 'P'
    SECONDARY = 'S'
    STATUS_CHOICES = (
        (COMPLETED, 'Completed'),
        (PRIMARY, 'Primary'),
        (SECONDARY, 'Secondary'),
    )
    show = models.ForeignKey(Show, related_name='viewings')
    name = models.TextField(unique=True, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PRIMARY)


class VideoViewing(BaseModel):
    video = models.ForeignKey(Video, related_name='viewings')
    show_viewing = models.ForeignKey(ShowViewing, null=True, related_name='video_viewings')

    class Meta:
        unique_together = ('video', 'show_viewing')


class FeedChannel(BaseModel):
    channel = models.ForeignKey(Channel, unique=True, related_name='+')


class FeedVideo(VideoModel):
    channel = models.ForeignKey(Channel, related_name='feed_videos')