import json, os, iso8601
from django.core.management import BaseCommand, CommandError
from django.conf import settings
from feed.models import ShowType, Show, ShowViewing, VideoViewing
from youtube.models import Video

SEED_FILE = os.path.join(os.path.join(settings.BASE_DIR, 'datadump'), 'feed.json')


class Command(BaseCommand):
    help = "Seeds the database with feed data from a previous application"

    def handle(self, *args, **options):
        if not os.path.isfile(SEED_FILE):
            raise CommandError("The seed file \"%s\" does not exist." % SEED_FILE)

        with open(SEED_FILE, 'r') as f:
            json_info = json.load(f)

        db_show_types = dict()
        db_shows = dict()
        db_show_viewings = dict()
        db_videos = dict()

        for info in json_info['SHOW_TYPES']:
            show_type = ShowType()
            show_type.name = info['NAME']
            show_type.name_hex_color = info['NAME_HEX_COLOR']
            show_type.is_active = info['IS_ACTIVE']
            show_type.save()
            ShowType.objects.filter(pk=show_type.pk).update(record_created_at=iso8601.parse_date(info['RECORD_CREATED_AT']))

            db_show_types[info['ID']] = show_type

        for info in json_info['SHOWS']:
            show = Show()
            show.name = info['NAME']
            show.video_title_format = info['VIDEO_TITLE_FORMAT']
            show.show_type = db_show_types[info['SHOW_TYPE_ID']]
            show.is_active = info['IS_ACTIVE']
            show.save()
            Show.objects.filter(pk=show.pk).update(record_created_at=iso8601.parse_date(info['RECORD_CREATED_AT']))

            for video_id in info['VIDEOS']:
                video = Video.objects.get(pk=video_id)
                show.videos.add(video)
                db_videos[video.pk] = video

            db_shows[info['ID']] = show

        for info in json_info['SHOW_VIEWINGS']:
            show_viewing = ShowViewing()
            show_viewing.show = db_shows[info['SHOW_ID']]
            show_viewing.name = info['NAME']
            show_viewing.is_active = info['IS_ACTIVE']
            show_viewing.status = info['STATUS']
            show_viewing.save()
            ShowViewing.objects.filter(pk=show_viewing.pk).update(record_created_at=iso8601.parse_date(info['RECORD_CREATED_AT']))

            db_show_viewings[info['ID']] = show_viewing

        for info in json_info['VIDEO_VIEWINGS']:
            video_viewing = VideoViewing()
            if info['SHOW_VIEWING_ID'] != '':
                video_viewing.show_viewing = db_show_viewings[info['SHOW_VIEWING_ID']]
            video_viewing.video = db_videos[info['VIDEO_ID']]
            video_viewing.is_active = info['IS_ACTIVE']
            video_viewing.save()
            VideoViewing.objects.filter(pk=video_viewing.pk).update(record_created_at=iso8601.parse_date(info['RECORD_CREATED_AT']))