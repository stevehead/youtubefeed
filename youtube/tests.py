from django.test import TestCase

from .models import YoutubeModel, Video, Channel
from .utils import YoutubeAPIQuery


class YoutubeAPIQueryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(YoutubeAPIQueryTests, cls).setUpClass()

        # Youtube channel does not have a publishedAt time
        cls.youtube_channel = YoutubeAPIQuery.get_channel_from_username('Youtube')

        # NASAtelevision channel does have a publishedAt time
        cls.nasa_channel = YoutubeAPIQuery.get_channel_from_username('NASAtelevision')

    def test_query_youtube_channel(self):
        query = YoutubeAPIQuery.user_url_format % 'youtube'
        channel = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(channel['kind'], 'youtube#channel')

    def test_query_youtube_multiple_responses(self):
        pass

    def test_get_channel_from_username(self):
        for channel in [self.youtube_channel, self.nasa_channel]:
            for key in YoutubeAPIQuery.channel_properties:
                self.assertIn(key, channel)

    def test_get_channel_from_username_no_publish_date(self):
        self.assertEqual(self.youtube_channel['published_at'], YoutubeAPIQuery.default_datetime_string)

    def test_get_channel_from_username_with_publish_date(self):
        self.assertNotEqual(self.nasa_channel['published_at'], YoutubeAPIQuery.default_datetime_string)


class YoutubeModelTests(TestCase):
    pass


class VideoMethodTests(TestCase):
    pass


class ChannelMethodTests(TestCase):
    pass