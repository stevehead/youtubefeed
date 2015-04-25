from django.core.management import BaseCommand, CommandError
from feed.models import FeedChannel, FeedVideo

class Command(BaseCommand):
    help = "Grabs the most recent feed of videos from Youtube"

    def handle(self, *args, **options):
        current_video_ids = [video.pk for video in FeedVideo.objects.all()]
        feed_channels = FeedChannel.objects.all().select_related('channel')
        for feed_channel in feed_channels:
            channel = feed_channel.channel
            this_videos = channel.get_latest_videos(limit=100)

            for video in this_videos:
                if video['id'] not in current_video_ids:
                    new_feed_video = FeedVideo.create_from_youtube(video['id'])
        FeedVideo.remove_old_videos(days=14)