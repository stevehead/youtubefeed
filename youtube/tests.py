import unittest
from django.conf import settings
from django.test import TestCase

from common.utils import convert_iso8601_duration_to_seconds, split_lists
from .models import Video, Channel
from .utils import YoutubeAPIQuery


test_channel_id = 'UCFKDEp9si4RmHFWJW1vYsMA'
test_username_id = 'ethoslab'
test_playlist_id = 'PLVPJ1jbg0CaEsRhyNmZy7PMSl9eb4PSg1'
test_video_id = 'rdwz7QiG0lk'

do_youtube_api_calls = settings.TEST_YOUTUBE_API_CALLS

@unittest.skipUnless(do_youtube_api_calls, "To speed up testing of non-api calls.")
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

    def test_multi_query_youtube_with_large_limit(self):
        limit = 75
        query = YoutubeAPIQuery.playlist_video_url_format % test_playlist_id
        results = YoutubeAPIQuery.multi_query_youtube(query=query, limit=limit)
        self.assertEqual(len(results), limit)

    def test_multi_query_youtube_without_limit(self):
        query = YoutubeAPIQuery.playlist_video_url_format % test_playlist_id
        results = YoutubeAPIQuery.multi_query_youtube(query=query)
        self.assertGreater(len(results), 50)

    def test_multi_video_query(self):
        limit = 75
        videos_raw = YoutubeAPIQuery.get_channel_videos(test_channel_id, limit=limit)
        self.assertEqual(len(videos_raw), limit)
        video_ids_list = [video['id'] for video in videos_raw]
        videos = YoutubeAPIQuery.get_videos(*video_ids_list)
        self.assertEqual(len(videos), limit)


class CommonUtilitiesTests(TestCase):
    def test_convert_iso8601_duration_to_seconds(self):
        tests = [
            {'string': 'PT5M6S', 'value': 5 * 60 + 6},                      # MS
            {'string': 'PT10M', 'value': 10 * 60},                          # M
            {'string': 'PT14S', 'value': 14},                               # S
            {'string': 'PT3H', 'value': 3 * 3600},                          # H
            {'string': 'PT5H38M', 'value': 5 * 3600 + 38 * 60},             # HM
            {'string': 'PT12H7S', 'value': 12 * 3600 + 7},                  # HS
            {'string': 'PT8H12M56S', 'value': 8 * 3600 + 12 * 60 + 56},     # HMS
        ]
        for test in tests:
            test_method_value = convert_iso8601_duration_to_seconds(test['string'])
            self.assertEqual(test_method_value, test['value'])

    def test_split_lists(self):
        test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        test_split = split_lists(test_list, 5)
        self.assertEqual(len(test_split), 3)
        self.assertEqual(len(test_split[0]), 5)
        self.assertEqual(len(test_split[1]), 5)
        self.assertEqual(len(test_split[2]), 3)
        for i in [1, 2, 3, 4, 5]:
            self.assertIn(i, test_split[0])
        for i in [6, 7, 8, 9, 10]:
            self.assertIn(i, test_split[1])
        for i in [11, 12, 13]:
            self.assertIn(i, test_split[2])



class VideoMethodTests(TestCase):
    @unittest.skipUnless(do_youtube_api_calls, "To speed up testing of non-api calls.")
    def test_create_video_from_web(self):
        test_video = Video.create_from_youtube(test_video_id)
        test_video.save()


class ChannelMethodTests(TestCase):
    @unittest.skipUnless(do_youtube_api_calls, "To speed up testing of non-api calls.")
    def test_create_channel_from_web(self):
        test_channel = Channel.create_from_youtube(test_channel_id)
        test_channel.save()