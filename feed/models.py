import re

from datetime import timedelta
from django.utils import timezone
from django.db import models

from common.models import BaseModel
from youtube.models import Channel, Video, VideoModel


class ShowType(BaseModel):
    name = models.TextField(unique=True, blank=False)
    name_color = models.PositiveIntegerField(default=0)

    maximum_name_color_value = int('0xFFFFFF', 0)

    def save(self, *args, **kwargs):
        if self.name_color > self.maximum_name_color_value:
            raise AttributeError("The current name color value is outside the allowed hexadecimal range")
        super(ShowType, self).save(*args, **kwargs)

    @property
    def name_hex_color(self):
        if self.name_color > self.maximum_name_color_value:
            raise AttributeError("The current name color value is outside the allowed hexadecimal range")
        hex_string = hex(self.name_color)
        hex_string = hex_string[2:]
        hex_string = '#' + '0' * (6 - len(hex_string)) + hex_string.capitalize()
        return hex_string

    @name_hex_color.setter
    def name_hex_color(self, value):
        if value[0] == '#':
            value = '0x' + value[1:]
        decimal_value = int(value, 16)
        if decimal_value > self.maximum_name_color_value:
            raise AttributeError("The current name color value is outside the allowed hexadecimal range")
        self.name_color = decimal_value

    def __unicode__(self):
        return self.name


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

    @property
    def channel_titles(self):
        try:
            return self._cache_info['channel_titles']
        except KeyError:
            all_channels = []
            for video in self.videos.all().select_related('channel'):
                channel_title = video.channel.title
                if channel_title not in all_channels:
                    all_channels.append(channel_title)
            self._cache_info['channel_titles'] = ' | '.join(all_channels)
            return self._cache_info['channel_titles']

    @property
    def video_title_format_regex(self):
        try:
            return self._cache_info['video_title_format_regex']
        except KeyError:
            if self.video_title_format:
                regex_string = re.escape(self.video_title_format)
                regex_string = regex_string.replace(r'\%\%', '__doublepercent__')
                regex_string = regex_string.replace(r'\%n', '[0-9]+[a-zA-Z]*')
                regex_string = regex_string.replace(r'\%t', '.+')
                regex_string = regex_string.replace('__doublepercent__', r'\%')
                self._cache_info['video_title_format_regex'] = re.compile(regex_string)
            else:
                self._cache_info['video_title_format_regex'] = None
            return self._cache_info['video_title_format_regex']

    def likely_has_video(self, video):
        if self.video_title_format_regex and self.video_title_format_regex.match(video.title):
            return True
        else:
            return False

    def __unicode__(self):
        return "%s: %s" % (self.channel_titles, self.name)


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
    name = models.TextField(blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PRIMARY)

    def __unicode__(self):
        return "%s : %s" % (self.show.name, self.name)

    class Meta:
        unique_together = ('show', 'name')


class VideoViewing(BaseModel):
    video = models.ForeignKey(Video, related_name='viewings')
    show_viewing = models.ForeignKey(ShowViewing, null=True, related_name='video_viewings')

    class Meta:
        unique_together = ('video', 'show_viewing')

    def __unicode__(self):
        if self.show_viewing:
            return "%s : %s" % (self.show_viewing.name, self.video.name)
        else:
            return "Random Viewing : %s" % self.video.name


class FeedChannel(BaseModel):
    channel = models.OneToOneField(Channel, primary_key=True)

    def __unicode__(self):
        return self.channel.title


class FeedVideo(VideoModel):
    channel = models.ForeignKey(Channel, related_name='feed_videos')

    @classmethod
    def remove_old_videos(cls, days=7):
        cls.objects.filter(published_at__lte=timezone.now()-timedelta(days=days)).delete()

    def __unicode__(self):
        return self.title