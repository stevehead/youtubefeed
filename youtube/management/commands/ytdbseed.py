import json, os
from django.core.management import BaseCommand, CommandError
from django.conf import settings
from youtube.models import Channel, Video
from youtube.utils import YoutubeAPINoResultsFound

SEED_FILE = os.path.join(os.path.join(settings.BASE_DIR, 'datadump'), 'youtube.json')


class Command(BaseCommand):
    help = "Seeds the database with Youtube data from a previous application"

    def handle(self, *args, **options):
        if not os.path.isfile(SEED_FILE):
            raise CommandError("The seed file \"%s\" does not exist." % SEED_FILE)

        with open(SEED_FILE, 'r') as f:
            json_info = json.load(f)

        yt_channel_ids = [channel.id for channel in Channel.objects.all()]
        yt_video_ids = [video.id for video in Video.objects.all()]

        for channel_id in json_info['CHANNELS']:
            if channel_id in yt_channel_ids:
                continue
            try:
                channel = Channel.create_from_youtube(channel_id=channel_id)
                self.stdout.write("Channel \"%s\" seeded." % channel.title)
            except YoutubeAPINoResultsFound:
                self.stdout.write("Channel \"%s\" could not be found." % channel_id)

        for video_id in json_info['VIDEOS']:
            if video_id in yt_video_ids:
                continue
            try:
                video = Video.create_from_youtube(video_id)
                self.stdout.write("Video \"%s\" seeded." % video.title)
            except YoutubeAPINoResultsFound:
                self.stdout.write("Video \"%s\" could not be found." % video_id)
