from datetime import timedelta
from django.utils import timezone
from django.core.management import BaseCommand, CommandError
from feed.models import FeedChannel, FeedVideo
from youtube.utils import YoutubeAPIQuery

MAX_VIDEOS_PER_CHANNEL = 100
MAX_LIFE_DAYS = 7

class Command(BaseCommand):
    help = "Grabs the most recent feed of videos from Youtube"

    def handle(self, *args, **options):
        current_time = timezone.now()
        feed_channels = FeedChannel.objects.all().select_related('channel')
        raw_videos_to_add = []
        for feed_channel in feed_channels:
            channel = feed_channel.channel
            raw_videos_to_add += channel.get_latest_videos(limit=MAX_VIDEOS_PER_CHANNEL)
        all_videos_ids_to_add = []
        for video in raw_videos_to_add:
            if current_time - video['published_at'] < timedelta(days=MAX_LIFE_DAYS+2):
                all_videos_ids_to_add.append(video['id'])
        all_videos_ids_to_add = [video['id'] for video in raw_videos_to_add]
        all_videos_to_add = YoutubeAPIQuery.get_videos(*all_videos_ids_to_add)
        FeedVideo.objects.all().delete()
        for video in all_videos_to_add:
            new_feed_video = FeedVideo()
            new_feed_video.set_info_from_youtube(video)
            new_feed_video.save()
        FeedVideo.remove_old_videos(days=MAX_LIFE_DAYS)