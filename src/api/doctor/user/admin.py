"""admin for user app"""
from django.contrib import admin

from doctor.user.models import (
    User,
    NotificationSettings,
    ForgotPassword
)


class UserAdmin(admin.ModelAdmin):
    """
        User model Admin
    """
    list_display = ['id', 'name', 'email', 'is_active', 'created_at']
    search_fields = ['name', 'email', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'badges']


class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "meal", "incomplete_day", "good_morning", "weekly_checkup"]
    list_filter = ["meal", "incomplete_day", "good_morning", "weekly_checkup"]
    search_fields = ["user__email"]


admin.site.register(
    User,
    UserAdmin
)
admin.site.register(
    NotificationSettings,
    NotificationSettingsAdmin
)
admin.site.register(
    ForgotPassword
)
