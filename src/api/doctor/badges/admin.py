from django.contrib import admin

from doctor.badges.models import Badges


class BadgesAdmin(admin.ModelAdmin):
    list_filter = ["id", "name", "type"]


admin.site.register(Badges)
