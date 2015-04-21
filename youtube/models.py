from django.db import models


class YoutubeModel:
    class Meta:
        abstract = True


class Video(YoutubeModel):
    pass


class Channel(YoutubeModel):
    pass