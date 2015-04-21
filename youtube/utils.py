import json
import urllib2
from abc import ABCMeta, abstractmethod
from datetime import datetime

from django.conf import settings


class YoutubeAPIQuery:
    __metaclass__ = ABCMeta

    api_key = settings.YOUTUBE_API_KEY
    api_base_url = 'https://www.googleapis.com/youtube/v3/'

    channel_properties = ['id', 'title', 'description', 'thumbnail', 'published_at', 'uploads_playlist_id']
    channel_url_parts = ['contentDetails', 'snippet']
    channel_url_format = api_base_url + 'channels?part=' + ','.join(channel_url_parts) + '&id=%s&key=' + api_key
    user_url_format = api_base_url + 'channels?part=' + ','.join(channel_url_parts) + '&forUsername=%s&key=' + api_key

    playlist_properties = ['id', 'title', 'description', 'thumbnail', 'published_at', 'channel_id', 'video_count']
    playlist_url_parts = ['contentDetails', 'snippet']
    playlist_url_format = api_base_url + 'playlists?part=' + ','.join(channel_url_parts) + '&id=%s&key=' + api_key

    video_properties = ['id', 'title', 'description', 'thumbnail', 'published_at', 'channel_id', 'duration']
    video_url_parts = ['contentDetails', 'snippet']
    video_url_format = api_base_url + 'videos?part=' + ','.join(video_url_parts) + '&id=%s&key=' + api_key

    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def query_youtube(query, requires_one_response=False):
        # Get response object from Youtube.
        try:
            http_request = urllib2.urlopen(query)
        except Exception as e:
            raise YoutubeAPIQueryError("Web request failed: %s" % e)

        # Convert response into JSON.
        try:
            json_response = json.load(http_request)
        except Exception as e:
            raise YoutubeAPIQueryError("JSON loading failed: %s" % e)

        # Return exactly one item for single-response queries
        if requires_one_response:
            if len(json_response['items']) > 1:
                raise YoutubeAPIQueryError("This request must contain exactly one item")
            elif len(json_response['items']) == 0:
                raise YoutubeAPIQueryError("The request could not find any results.")
            return json_response['items'][0]
        # Else return all the items
        else:
            return json_response['items']

    @classmethod
    def parse_channel_results(cls, channel_item):
        try:
            channel = dict()
            channel['id'] = channel_item['id']
            channel['title'] = channel_item['snippet']['title']
            channel['description'] = channel_item['snippet']['description']
            channel['thumbnail'] = channel_item['snippet']['thumbnails']['default']['url']
            channel['published_at'] = channel_item['snippet']['publishedAt']
            channel['uploads_playlist_id'] = channel_item['contentDetails']['relatedPlaylists']['uploads']
            return channel
        except Exception as e:
            raise YoutubeAPIQueryError("JSON parsing failed: %s" % e)

    @classmethod
    def parse_playlist_results(cls, playlist_item):
        try:
            playlist = dict()
            playlist['id'] = playlist_item['id']
            playlist['channel_id'] = playlist_item['snippet']['channelId']
            playlist['title'] = playlist_item['snippet']['title']
            playlist['description'] = playlist_item['snippet']['description']
            playlist['thumbnail'] = playlist_item['snippet']['thumbnails']['default']['url']
            playlist['published_at'] = playlist_item['snippet']['publishedAt']
            playlist['video_count'] = playlist_item['contentDetails']['itemCount']
            return playlist
        except Exception as e:
            raise YoutubeAPIQueryError("JSON parsing failed: %s" % e)

    @classmethod
    def parse_video_results(cls, video_item):
        try:
            video = dict()
            video['id'] = video_item['id']
            video['channel_id'] = video_item['snippet']['channelId']
            video['title'] = video_item['snippet']['title']
            video['description'] = video_item['snippet']['description']
            video['thumbnail'] = video_item['snippet']['thumbnails']['default']['url']
            video['published_at'] = video_item['snippet']['publishedAt']
            video['duration'] = video_item['contentDetails']['duration']
            return video
        except Exception as e:
            raise YoutubeAPIQueryError("JSON parsing failed: %s" % e)

    @classmethod
    def get_channel(cls, channel_id):
        query = cls.channel_url_format % channel_id
        channel_item = cls.query_youtube(query, True)
        return cls.parse_channel_results(channel_item)

    @classmethod
    def get_channel_from_username(cls, username):
        query = cls.user_url_format % username
        channel_item = cls.query_youtube(query, True)
        return cls.parse_channel_results(channel_item)

    @classmethod
    def get_playlist(cls, playlist_id):
        query = cls.playlist_url_format % playlist_id
        playlist_item = cls.query_youtube(query, True)
        return cls.parse_playlist_results(playlist_item)

    @classmethod
    def get_video(cls, video_id):
        query = cls.video_url_format % video_id
        video_item = cls.query_youtube(query, True)
        return cls.parse_video_results(video_item)


class YoutubeAPIQueryError(Exception):
    pass