from datetime import timedelta
from django.utils import timezone
from django.core.management import BaseCommand, CommandError
from feed.models import FeedChannel, FeedVideo
from youtube.utils import YoutubeAPIQuery

MAX_VIDEOS_PER_CHANNEL = 50
MAX_LIFE_DAYS = 7

class Command(BaseCommand):
    help = "Grabs the most recent feed of videos from Youtube"

    def handle(self, *args, **options):
        self.stdout.write("Youtubefeed has begun.")
        current_time = timezone.now()
        feed_channels = FeedChannel.objects.all().select_related('channel')
        raw_videos_to_add = []
        for feed_channel in feed_channels:
            channel = feed_channel.channel
            raw_videos_to_add += channel.get_latest_videos(limit=MAX_VIDEOS_PER_CHANNEL)
            self.stdout.write("Channel \"%s\" videos pre-loaded." % channel.title)
        all_videos_ids_to_add = []
        for video in raw_videos_to_add:
            if current_time - video['published_at'] < timedelta(days=MAX_LIFE_DAYS+2):
                all_videos_ids_to_add.append(video['id'])
        all_videos_ids_to_add = [video['id'] for video in raw_videos_to_add]
        all_videos_to_add = YoutubeAPIQuery.get_videos(*all_videos_ids_to_add)
        for video in all_videos_to_add:
            try:
                feed_video = FeedVideo.objects.get(pk=video['id'])
            except FeedVideo.DoesNotExist:
                feed_video = FeedVideo()
            feed_video.set_info_from_youtube(video)
            feed_video.save()
            self.stdout.write("Video \"%s\" video processed." % feed_video.title)
        FeedVideo.remove_old_videos(days=MAX_LIFE_DAYS)
        self.stdout.write("Old videos removed.")
        self.stdout.write("Youtubefeed is complete.")