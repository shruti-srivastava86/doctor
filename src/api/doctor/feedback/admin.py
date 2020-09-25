from django.contrib import admin

from doctor.feedback.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "user"]


admin.site.register(
    Feedback, FeedbackAdmin
)
