from django.contrib import admin

from doctor.admin import (
    DailyAssessmentAbstractModelAdmin,
    DaysRangeAbstractModelAdmin,
    AssessmentAbstractModelAdmin
)
from doctor.motion.models import (
    MotionAssessment,
    MotionDailyAssessment,
    MotionDaysRange
)


class MotionAssessmentAdmin(AssessmentAbstractModelAdmin):
    list_display = AssessmentAbstractModelAdmin.list_display


class MotionDailyAssessmentAdmin(DailyAssessmentAbstractModelAdmin):
    list_display = DailyAssessmentAbstractModelAdmin.list_display


class MotionDaysRangeAdmin(DaysRangeAbstractModelAdmin):
    list_display = DaysRangeAbstractModelAdmin.list_display


admin.site.register(
    MotionAssessment,
    MotionAssessmentAdmin
)
admin.site.register(
    MotionDailyAssessment,
    MotionDailyAssessmentAdmin
)
admin.site.register(
    MotionDaysRange,
    MotionDaysRangeAdmin
)
