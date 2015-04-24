import unittest
from django.test import TestCase

from .models import YoutubeModel, Video, Channel
from .utils import YoutubeAPIQuery


test_channel_id = 'UCFKDEp9si4RmHFWJW1vYsMA'
test_username_id = 'ethoslab'
test_playlist_id = 'PLVPJ1jbg0CaEsRhyNmZy7PMSl9eb4PSg1'
test_video_id = 'rdwz7QiG0lk'

@unittest.skip("To speed up testing of the models.")
class YoutubeAPIQueryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(YoutubeAPIQueryTests, cls).setUpClass()
        cls.test_channel = YoutubeAPIQuery.get_channel(test_channel_id)
        cls.test_playlist = YoutubeAPIQuery.get_playlist(test_playlist_id)
        cls.test_video = YoutubeAPIQuery.get_video(test_video_id)
        cls.test_playlist_videos = YoutubeAPIQuery.get_playlist_videos(test_playlist_id)
        cls.test_channel_playlists = YoutubeAPIQuery.get_channel_playlists(test_channel_id)

    def test_query_youtube_channel_from_username(self):
        query = YoutubeAPIQuery.user_url_format % test_username_id
        channel = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(channel['kind'], 'youtube#channel')

    def test_query_youtube_channel_from_id(self):
        query = YoutubeAPIQuery.channel_url_format % test_channel_id
        channel = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(channel['kind'], 'youtube#channel')

    def test_query_youtube_playlist(self):
        query = YoutubeAPIQuery.playlist_url_format % test_playlist_id
        playlist = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(playlist['kind'], 'youtube#playlist')

    def test_query_youtube_playlist_video(self):
        query = YoutubeAPIQuery.playlist_video_url_format % test_playlist_id
        playlist_video = YoutubeAPIQuery.query_youtube(query, False)
        self.assertEqual(playlist_video['items'][0]['kind'], 'youtube#playlistItem')

    def test_query_youtube_video(self):
        query = YoutubeAPIQuery.video_url_format % test_video_id
        video = YoutubeAPIQuery.query_youtube(query, True)
        self.assertEqual(video['kind'], 'youtube#video')

    def test_get_channel(self):
        for key in YoutubeAPIQuery.channel_properties:
            self.assertIn(key, self.test_channel)

    def test_get_channel_playlists(self):
        for key in YoutubeAPIQuery.playlist_properties:
            self.assertIn(key, self.test_channel_playlists[0])

    def test_get_playlist(self):
        for key in YoutubeAPIQuery.playlist_properties:
            self.assertIn(key, self.test_playlist)

    def test_get_playlist_videos(self):
        self.assertEqual(len(self.test_playlist_videos), self.test_playlist['video_count'])
        for key in YoutubeAPIQuery.playlist_video_properties:
            self.assertIn(key, self.test_playlist_videos[0])

    def test_get_video(self):
        for key in YoutubeAPIQuery.video_properties:
            self.assertIn(key, self.test_video)

    def test_multi_query_youtube_with_limit(self):
        limit = 17
        query = YoutubeAPIQuery.playlist_video_url_format % test_playlist_id
        results = YoutubeAPIQuery.multi_query_youtube(query=query, limit=limit)
        self.assertEqual(len(results), limit)


class VideoMethodTests(TestCase):
    def test_create_video_from_web(self):
        test_video = Video.create_from_youtube(test_video_id)
        test_video.save()

class ChannelMethodTests(TestCase):
    def test_create_channel_from_web(self):
        test_channel = Channel.create_from_youtube(test_channel_id)
        test_channel.save()