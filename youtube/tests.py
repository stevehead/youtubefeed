from django.test import TestCase

from .models import YoutubeModel, Video, Channel
from .utils import YoutubeAPIQuery


class YoutubeAPIQueryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(YoutubeAPIQueryTests, cls).setUpClass()
        cls.test_channel = YoutubeAPIQuery.get_channel('UCFKDEp9si4RmHFWJW1vYsMA')
        cls.test_playlist = YoutubeAPIQuery.get_playlist('PLVPJ1jbg0CaGL_uKV3IP-V6OFk_rQDZCl')
        cls.test_video = YoutubeAPIQuery.get_video('rdwz7QiG0lk')

    def test_query_youtube_channel_from_username(self):
        query = YoutubeAPIQuery.user_url_format % 'youtube'
        channel = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(channel['kind'], 'youtube#channel')

    def test_query_youtube_channel_from_id(self):
        query = YoutubeAPIQuery.channel_url_format % 'UCJTWU5K7kl9EE109HBeoldA'
        channel = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(channel['kind'], 'youtube#channel')

    def test_query_youtube_playlist(self):
        query = YoutubeAPIQuery.playlist_url_format % 'PLFx-KViPXIkEfy1vrFoCepbtDemog0BjE'
        playlist = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(playlist['kind'], 'youtube#playlist')

    def test_query_youtube_video(self):
        query = YoutubeAPIQuery.video_url_format % 'cBxhbQ4TlDk'
        video = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(video['kind'], 'youtube#video')

    def test_get_channel_from_username(self):
        for key in YoutubeAPIQuery.channel_properties:
            self.assertIn(key, self.test_channel)

    def test_get_playlist(self):
        for key in YoutubeAPIQuery.playlist_properties:
            self.assertIn(key, self.test_playlist)

    def test_get_video(self):
        for key in YoutubeAPIQuery.video_properties:
            self.assertIn(key, self.test_video)


class YoutubeModelTests(TestCase):
    pass


class VideoMethodTests(TestCase):
    pass


class ChannelMethodTests(TestCase):
    pass