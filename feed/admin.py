from django.contrib import admin

from .models import Show, ShowType, ShowViewing, FeedChannel, FeedVideo


class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel_titles', 'status', )
    ordering = ('record_created_at', 'name')


admin.site.register(Show, ShowAdmin)
admin.site.register(ShowType)
admin.site.register(ShowViewing)
admin.site.register(FeedChannel)
admin.site.register(FeedVideo)