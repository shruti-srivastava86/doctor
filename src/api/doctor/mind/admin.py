from django.contrib import admin

from doctor.admin import (
    DailyAssessmentAbstractModelAdmin,
    DaysRangeAbstractModelAdmin,
    AssessmentAbstractModelAdmin
)
from doctor.mind.models import (
    MindAssessment,
    MindDailyAssessment,
    MindDaysRange
)


class MindAssessmentAdmin(AssessmentAbstractModelAdmin):
    list_display = AssessmentAbstractModelAdmin.list_display


class MindDailyAssessmentAdmin(DailyAssessmentAbstractModelAdmin):
    list_display = DailyAssessmentAbstractModelAdmin.list_display


class MindDaysRangeAdmin(DaysRangeAbstractModelAdmin):
    list_display = DaysRangeAbstractModelAdmin.list_display


admin.site.register(
    MindAssessment,
    MindAssessmentAdmin
)
admin.site.register(
    MindDailyAssessment,
    MindDailyAssessmentAdmin
)
admin.site.register(
    MindDaysRange,
    MindDaysRangeAdmin
)
