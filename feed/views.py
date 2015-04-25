from django.shortcuts import render

from .models import FeedVideo

def feed(request):
    feed_videos = FeedVideo.objects.order_by('-published_at').select_related('channel')
    return render(request, 'feed/feed.html', {'feed_videos': feed_videos})