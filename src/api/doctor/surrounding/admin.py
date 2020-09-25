from django.contrib import admin

from doctor.admin import (
    DailyAssessmentAbstractModelAdmin,
    DaysRangeAbstractModelAdmin,
    AssessmentAbstractModelAdmin
)
from doctor.surrounding.models import (
    SurroundingAssessment,
    SurroundingDailyAssessment,
    SurroundingDaysRange
)


class SurroundingAssessmentAdmin(AssessmentAbstractModelAdmin):
    list_display = AssessmentAbstractModelAdmin.list_display


class SurroundingDailyAssessmentAdmin(DailyAssessmentAbstractModelAdmin):
    list_display = DailyAssessmentAbstractModelAdmin.list_display


class SurroundingDaysRangeAdmin(DaysRangeAbstractModelAdmin):
    list_display = DaysRangeAbstractModelAdmin.list_display + ["for_assessment"]
    list_filter = ["for_assessment"]


admin.site.register(
    SurroundingAssessment,
    SurroundingAssessmentAdmin
)
admin.site.register(
    SurroundingDailyAssessment,
    SurroundingDailyAssessmentAdmin
)
admin.site.register(
    SurroundingDaysRange,
    SurroundingDaysRangeAdmin
)
