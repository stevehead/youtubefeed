from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render

from .models import Show, FeedVideo


def feed(request):
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

    video_sets_by_publish_time = []
    for video_set in video_sets_by_publish_time_raw:
        if len(video_set['videos']):
            video_sets_by_publish_time.append(video_set)

    context = {
        'video_sets_by_publish_time': video_sets_by_publish_time,
        'shows': current_ongoing_shows
    }

    return render(request, 'feed/feed.html', context)