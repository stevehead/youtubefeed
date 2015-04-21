import json
import urllib2
from abc import ABCMeta, abstractmethod
from datetime import datetime

from django.conf import settings


class YoutubeAPIQuery:
    __metaclass__ = ABCMeta

    api_key = settings.YOUTUBE_API_KEY
    api_base_url = 'https://www.googleapis.com/youtube/v3/'
    default_datetime_string = '1970-01-01T00:00:00.000Z'

    channel_properties = ['id', 'title', 'description', 'thumbnail', 'published_at', 'uploads_playlist_id',
        'video_count']
    channel_url_parts = ['contentDetails', 'snippet', 'statistics']
    user_url_format = api_base_url + 'channels?part=' + ','.join(channel_url_parts) + '&forUsername=%s&key=' + api_key

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
        channel = dict()

        try:
            channel['id'] = channel_item['id']
            channel['title'] = channel_item['snippet']['title']
            channel['description'] = channel_item['snippet']['description']
            channel['thumbnail'] = channel_item['snippet']['thumbnails']['default']['url']
            channel['published_at'] = channel_item['snippet'].get('publishedAt', cls.default_datetime_string)
            channel['uploads_playlist_id'] = channel_item['contentDetails']['relatedPlaylists']['uploads']
            channel['video_count'] = channel_item['statistics']['videoCount']
            return channel
        except Exception as e:
            raise YoutubeAPIQueryError("JSON parsing failed: %s" % e)

    @classmethod
    def get_channel_from_username(cls, username):
        query = cls.user_url_format % username
        channel_item = cls.query_youtube(query, True)
        return cls.parse_channel_results(channel_item)


class YoutubeAPIQueryError(Exception):
    pass