from django.test import TestCase

from .models import YoutubeModel, Video, Channel
from .utils import YoutubeAPIQuery


class YoutubeAPIQueryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(YoutubeAPIQueryTests, cls).setUpClass()
        cls.youtube_channel = YoutubeAPIQuery.get_channel_from_username('Youtube')
        cls.nasa_channel = YoutubeAPIQuery.get_channel_from_username('NASAtelevision')
        cls.test_channel = YoutubeAPIQuery.get_channel('UCJTWU5K7kl9EE109HBeoldA')
        cls.test_video = YoutubeAPIQuery.get_video('rdwz7QiG0lk')

    def test_query_youtube_channel_from_username(self):
        query = YoutubeAPIQuery.user_url_format % 'youtube'
        channel = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(channel['kind'], 'youtube#channel')

    def test_query_youtube_channel_from_id(self):
        query = YoutubeAPIQuery.channel_url_format % 'UCJTWU5K7kl9EE109HBeoldA'
        channel = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(channel['kind'], 'youtube#channel')

    def test_query_youtube_video(self):
        query = YoutubeAPIQuery.video_url_format % 'cBxhbQ4TlDk'
        channel = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(channel['kind'], 'youtube#video')

    def test_get_channel_from_username(self):
        for key in YoutubeAPIQuery.channel_properties:
            self.assertIn(key, self.test_channel)

    def test_get_channel_from_username_no_publish_date(self):
        self.assertEqual(self.youtube_channel['published_at'], YoutubeAPIQuery.default_datetime_string)

    def test_get_channel_from_username_with_publish_date(self):
        self.assertNotEqual(self.nasa_channel['published_at'], YoutubeAPIQuery.default_datetime_string)

    def test_get_video(self):
        for key in YoutubeAPIQuery.video_properties:
            self.assertIn(key, self.test_video)


class YoutubeModelTests(TestCase):
    pass


class VideoMethodTests(TestCase):
    pass


class ChannelMethodTests(TestCase):
    pass