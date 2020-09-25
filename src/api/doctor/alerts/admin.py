from django.contrib import admin

from doctor.alerts.models import Alerts


class AlertsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "text", "type", "macro_type", "read"]
    list_filter = ["type", "macro_type"]
    search_fields = ["user__email"]


admin.site.register(
    Alerts,
    AlertsAdmin
)
