import json
import urllib2
from abc import ABCMeta, abstractmethod
from datetime import datetime

from django.conf import settings


class YoutubeAPIQuery:
    __metaclass__ = ABCMeta

    api_key = settings.YOUTUBE_API_KEY
    api_base_url = 'https://www.googleapis.com/youtube/v3/'

    channel_properties = ['channel_id', 'title', 'description', 'thumbnail', 'published_at', 'uploads_playlist_id']
    channel_url_parts = ['contentDetails', 'snippet']
    channel_url_format = api_base_url + 'channels?part=' + ','.join(channel_url_parts) + '&id=%s&key=' + api_key
    user_url_format = api_base_url + 'channels?part=' + ','.join(channel_url_parts) + '&forUsername=%s&key=' + api_key

    playlist_properties = ['playlist_id', 'title', 'description', 'thumbnail', 'published_at', 'channel_id', 'video_count']
    playlist_url_parts = ['contentDetails', 'snippet']
    playlist_url_format = api_base_url + 'playlists?part=' + ','.join(channel_url_parts) + '&id=%s&key=' + api_key
    playlist_from_channel_url_format = api_base_url + 'playlists?part=' + ','.join(channel_url_parts) + '&channelId=%s&key=' + api_key

    playlist_video_properties = ['video_id', 'title', 'description', 'thumbnail', 'published_at', 'channel_id', 'duration']
    playlist_video_url_parts = ['snippet']
    playlist_video_url_format = api_base_url + 'playlistItems?part=' + ','.join(playlist_video_url_parts) + '&playlistId=%s&key=' + api_key

    video_properties = ['video_id', 'title', 'description', 'thumbnail', 'published_at', 'channel_id', 'duration']
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
        # Else return everything
        else:
            return json_response

    @classmethod
    def multi_query_youtube(cls, query, parse_method=None):
        main_query = query + '&maxResults=50'
        all_items = []
        pageToken = None
        while True:
            if pageToken:
                this_query = main_query + '&pageToken=' + pageToken
            else:
                this_query = main_query
            query_results = cls.query_youtube(query=this_query, requires_one_response=False)
            for result in query_results['items']:
                if parse_method:
                    all_items.append(parse_method(result))
                else:
                    all_items.append(result)
            if 'nextPageToken' in query_results:
                pageToken = query_results['nextPageToken']
            else:
                break
        return all_items

    @staticmethod
    def parse_channel_results(channel_item):
        try:
            channel = dict()
            channel['channel_id'] = channel_item['id']
            channel['title'] = channel_item['snippet']['title']
            channel['description'] = channel_item['snippet']['description']
            channel['thumbnail'] = channel_item['snippet']['thumbnails']['default']['url']
            try:
                channel['published_at'] = channel_item['snippet']['publishedAt']
            except KeyError:
                channel['published_at'] = None
            channel['uploads_playlist_id'] = channel_item['contentDetails']['relatedPlaylists']['uploads']
            return channel
        except Exception as e:
            raise YoutubeAPIQueryError("JSON parsing failed: %s" % e)

    @staticmethod
    def parse_playlist_results(playlist_item):
        try:
            playlist = dict()
            playlist['playlist_id'] = playlist_item['id']
            playlist['channel_id'] = playlist_item['snippet']['channelId']
            playlist['title'] = playlist_item['snippet']['title']
            playlist['description'] = playlist_item['snippet']['description']
            playlist['thumbnail'] = playlist_item['snippet']['thumbnails']['default']['url']
            try:
                playlist['published_at'] = playlist_item['snippet']['publishedAt']
            except KeyError:
                playlist['published_at'] = None
            playlist['video_count'] = playlist_item['contentDetails']['itemCount']
            return playlist
        except Exception as e:
            raise YoutubeAPIQueryError("JSON parsing failed: %s" % e)

    @staticmethod
    def parse_playlist_video_results(video_item):
        try:
            video = dict()
            video['video_id'] = video_item['snippet']['resourceId']['videoId']
            video['channel_id'] = video_item['snippet']['channelId']
            video['title'] = video_item['snippet']['title']
            video['description'] = video_item['snippet']['description']
            video['thumbnail'] = video_item['snippet']['thumbnails']['default']['url']
            try:
                video['published_at'] = video_item['snippet']['publishedAt']
            except KeyError:
                video['published_at'] = None
            video['duration'] = None
            return video
        except Exception as e:
            raise YoutubeAPIQueryError("JSON parsing failed: %s" % e)

    @staticmethod
    def parse_video_results(video_item):
        try:
            video = dict()
            video['video_id'] = video_item['id']
            video['channel_id'] = video_item['snippet']['channelId']
            video['title'] = video_item['snippet']['title']
            video['description'] = video_item['snippet']['description']
            video['thumbnail'] = video_item['snippet']['thumbnails']['default']['url']
            try:
                video['published_at'] = video_item['snippet']['publishedAt']
            except KeyError:
                video['published_at'] = None
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
    def get_channel_playlists(cls, channel_id):
        query = cls.playlist_from_channel_url_format % channel_id
        return cls.multi_query_youtube(query, cls.parse_playlist_results)

    @classmethod
    def get_channel_videos(cls, channel_id):
        channel = cls.get_channel(channel_id)
        return cls.get_playlist_videos(channel['uploads_playlist_id'])

    @classmethod
    def get_user(cls, username):
        query = cls.user_url_format % username
        channel_item = cls.query_youtube(query, True)
        return cls.parse_channel_results(channel_item)

    @classmethod
    def get_user_playlists(cls, username):
        channel = cls.get_user(username)
        return cls.get_channel_playlists(channel['id'])

    @classmethod
    def get_user_videos(cls, username):
        user = cls.get_user(username)
        return cls.get_playlist_videos(user['uploads_playlist_id'])

    @classmethod
    def get_playlist(cls, playlist_id):
        query = cls.playlist_url_format % playlist_id
        playlist_item = cls.query_youtube(query, True)
        return cls.parse_playlist_results(playlist_item)

    @classmethod
    def get_playlist_channel(cls, playlist_id):
        playlist = cls.get_playlist(playlist_id)
        return cls.get_channel(playlist['channel_id'])

    @classmethod
    def get_playlist_videos(cls, playlist_id):
        query = cls.playlist_video_url_format % playlist_id
        return cls.multi_query_youtube(query, cls.parse_playlist_video_results)

    @classmethod
    def get_video(cls, video_id):
        query = cls.video_url_format % video_id
        video_item = cls.query_youtube(query, True)
        return cls.parse_video_results(video_item)

    @classmethod
    def get_video_channel(cls, video_id):
        video = cls.get_video(video_id)
        return cls.get_channel(video['channel_id'])


class YoutubeAPIQueryError(Exception):
    pass