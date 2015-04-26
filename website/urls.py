from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from feed.urls import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^feed/', include('feed.urls', namespace='feed')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, dcoument_root=settings.STATIC_ROOT)