from django.contrib import admin

from doctor.video.models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ["id", "type"]


admin.site.register(
    Video,
    VideoAdmin
)
