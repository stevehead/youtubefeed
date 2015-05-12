from operator import attrgetter

from datetime import timedelta
from django.conf import settings
from django.core.validators import ValidationError
from django.utils import timezone
from django.shortcuts import render, redirect

from youtube.models import Video
from .models import Show, ShowViewing, FeedVideo


def home(request):
    all_active_show_viewings = ShowViewing.objects.filter(is_active=True).exclude(status=ShowViewing.COMPLETED)\
        .select_related('show').prefetch_related('video_viewings', 'show__videos', 'show__show_type', 'show__videos__channel')
    primary_videos_to_watch = []
    secondary_videos_to_watch = []
    total_primary_duration = 0
    for show_viewing in all_active_show_viewings:
        watched_videos = [video_viewing.video_id for video_viewing in show_viewing.video_viewings.all()]
        all_videos = sorted(show_viewing.show.videos.all(), key=attrgetter('published_at'))
        unwatched_videos = []
        for video in all_videos:
            if video.pk not in watched_videos:
                unwatched_videos.append(video)
        if show_viewing.status == ShowViewing.SECONDARY:
            unwatched_videos = unwatched_videos[:1]
        for video in unwatched_videos:
            video.show_viewing = show_viewing
            if show_viewing.status == ShowViewing.PRIMARY:
                primary_videos_to_watch.append(video)
                total_primary_duration += video.duration
            else:
                secondary_videos_to_watch.append(video)

    primary_videos_to_watch = sorted(primary_videos_to_watch, key=attrgetter('published_at'))
    secondary_videos_to_watch = sorted(secondary_videos_to_watch, key=attrgetter('published_at'))
    videos_to_watch = primary_videos_to_watch + secondary_videos_to_watch

    context = {
        'videos_to_watch': videos_to_watch,
        'total_primary_videos': len(primary_videos_to_watch),
        'total_primary_duration': timedelta(seconds=total_primary_duration)
    }

    return render(request, 'feed/home.html', context)


def feed(request):
    errors = []

    # Feed form method.
    if request.method == 'POST':
        try:
            # Get IDs from form data.
            show_id = request.POST.get('show_id')
            video_id = request.POST.get('video_id')

            # The IDs are required.
            if not show_id:
                raise ValidationError("The show ID is required.", code='missing_field')
            if not video_id:
                raise ValidationError("The video ID is required.", code='missing_field')

            # Make sure the show exists in the database.
            try:
                show = Show.objects.get(pk=show_id)
            except Show.DoesNotExist:
                raise ValidationError("The show is not found in the database.", code='missing_db_object')

            # Make sure the show doesn't already have the video.
            if show.videos.filter(pk=video_id).count() > 0:
                raise ValidationError("The show already has the video.", code='duplicate_entry')

            # Grab the video from the DB or create it.
            try:
                video = Video.objects.get(pk=video_id)
            except Video.DoesNotExist:
                try:
                    video = Video.create_from_youtube(video_id)
                except Video.YoutubeQueryError:
                    raise ValidationError("The video could not be pulled from Youtube. Make sure it exists on Youtube.")

            # Add the video to the show.
            show.videos.add(video)

            # Delete the video from the feed.
            FeedVideo.objects.filter(pk=video_id).delete()

            # Redirect to self.
            redirect('feed:feed')
        except ValidationError as e:
            errors.append(e.message)
        except Exception as e:
            if settings.DEBUG:
                raise e
            else:
                errors.append("Unknown error.")

    # Display logic begins here.
    current_time = timezone.now()
    current_ongoing_shows = Show.objects.filter(is_active=True).filter(status=Show.ONGOING).prefetch_related('videos')
    current_ongoing_show_video_ids = []
    for show in current_ongoing_shows:
        current_ongoing_show_video_ids += [video.pk for video in show.videos.all()]
    feed_videos = FeedVideo.objects.order_by('-published_at').select_related('channel')

    video_sets_by_publish_time_raw = [
        {'display': 'moments ago', 'videos': [],},
        {'display': '15 minutes ago', 'videos': [],},
        {'display': '30 minutes ago', 'videos': [],},
        {'display': '1 hour ago', 'videos': [],},
        {'display': '3 hours ago', 'videos': [],},
        {'display': '6 hours ago', 'videos': [],},
        {'display': '12 hours ago', 'videos': [],},
        {'display': '1 day ago', 'videos': [],},
        {'display': '2 days ago', 'videos': [],},
        {'display': '3 days ago', 'videos': [],},
        {'display': '4 days ago', 'videos': [],},
        {'display': '5 days ago', 'videos': [],},
        {'display': '6 days ago', 'videos': [],},
        {'display': '7 days ago', 'videos': [],},
        {'display': 'more than 7 days ago', 'videos': []}
    ]

    for video in feed_videos:
        if video.pk in current_ongoing_show_video_ids:
            continue
        for show in current_ongoing_shows:
            if show.likely_has_video(video):
                video.likely_show = show
                break
        if current_time - video.published_at < timedelta(minutes=5):
            video_sets_by_publish_time_raw[0]['videos'].append(video)
        elif current_time - video.published_at < timedelta(minutes=15):
            video_sets_by_publish_time_raw[1]['videos'].append(video)
        elif current_time - video.published_at < timedelta(minutes=30):
            video_sets_by_publish_time_raw[2]['videos'].append(video)
        elif current_time - video.published_at < timedelta(hours=1):
            video_sets_by_publish_time_raw[3]['videos'].append(video)
        elif current_time - video.published_at < timedelta(hours=3):
            video_sets_by_publish_time_raw[4]['videos'].append(video)
        elif current_time - video.published_at < timedelta(hours=6):
            video_sets_by_publish_time_raw[5]['videos'].append(video)
        elif current_time - video.published_at < timedelta(hours=12):
            video_sets_by_publish_time_raw[6]['videos'].append(video)
        elif current_time - video.published_at < timedelta(days=1):
            video_sets_by_publish_time_raw[7]['videos'].append(video)
        elif current_time - video.published_at < timedelta(days=2):
            video_sets_by_publish_time_raw[8]['videos'].append(video)
        elif current_time - video.published_at < timedelta(days=3):
            video_sets_by_publish_time_raw[9]['videos'].append(video)
        elif current_time - video.published_at < timedelta(days=4):
            video_sets_by_publish_time_raw[10]['videos'].append(video)
        elif current_time - video.published_at < timedelta(days=5):
            video_sets_by_publish_time_raw[11]['videos'].append(video)
        elif current_time - video.published_at < timedelta(days=6):
            video_sets_by_publish_time_raw[12]['videos'].append(video)
        elif current_time - video.published_at < timedelta(days=7):
            video_sets_by_publish_time_raw[13]['videos'].append(video)
        else:
            video_sets_by_publish_time_raw[14]['videos'].append(video)

    video_sets_by_publish_time = []
    for video_set in video_sets_by_publish_time_raw:
        if len(video_set['videos']):
            video_sets_by_publish_time.append(video_set)

    context = {
        'errors': errors,
        'video_sets_by_publish_time': video_sets_by_publish_time,
        'shows': current_ongoing_shows
    }

    return render(request, 'feed/feed.html', context)