from django.db import models


class YoutubeModel(models.Model):
    class Meta:
        abstract = True


class Video(YoutubeModel):
    pass


class Channel(YoutubeModel):
    pass