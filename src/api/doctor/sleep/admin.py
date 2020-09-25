from django.contrib import admin

from doctor.admin import (
    DailyAssessmentAbstractModelAdmin,
    DaysRangeAbstractModelAdmin,
    AssessmentAbstractModelAdmin
)
from doctor.sleep.models import (
    SleepAssessment,
    SleepDailyAssessment,
    SleepDaysRange
)


class SleepAssessmentAdmin(AssessmentAbstractModelAdmin):
    list_display = AssessmentAbstractModelAdmin.list_display


class SleepDailyAssessmentAdmin(DailyAssessmentAbstractModelAdmin):
    list_display = DailyAssessmentAbstractModelAdmin.list_display


class SleepDaysRangeAdmin(DaysRangeAbstractModelAdmin):
    list_display = DaysRangeAbstractModelAdmin.list_display


admin.site.register(
    SleepAssessment,
    SleepAssessmentAdmin
)
admin.site.register(
    SleepDailyAssessment,
    SleepDailyAssessmentAdmin
)
admin.site.register(
    SleepDaysRange,
    SleepDaysRangeAdmin
)
