from django.contrib import admin

from doctor.admin import (
    DailyAssessmentAbstractModelAdmin,
    DaysRangeAbstractModelAdmin,
    AssessmentAbstractModelAdmin
)
from doctor.weight.models import (
    WeightAssessment,
    WeightDailyAssessment,
    WeightDaysRange,
    WeightDailyAssessmentMeal,
    WeightWeeklyAssessmentLogs
)


class WeightAssessmentAdmin(AssessmentAbstractModelAdmin):
    list_display = AssessmentAbstractModelAdmin.list_display


class WeightDailyAssessmentMealInline(admin.TabularInline):
    model = WeightDailyAssessmentMeal
    extra = 0


class WeightDailyAssessmentMealAdmin(admin.ModelAdmin):
    list_display = ['id', 'daily_assessment', 'meal_type', 'time', 'status']
    list_filter = ['meal_type', 'status']
    search_fields = [
        'daily_assessment__user__name',
        'daily_assessment__user__email'
    ]


class WeightDailyAssessmentAdmin(DailyAssessmentAbstractModelAdmin):
    list_display = DailyAssessmentAbstractModelAdmin.list_display
    inlines = [
        WeightDailyAssessmentMealInline,
    ]


class WeightDaysRangeAdmin(DaysRangeAbstractModelAdmin):
    list_display = DaysRangeAbstractModelAdmin.list_display


class WeightWeeklyAssessmentLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bmi', 'waist']


admin.site.register(
    WeightAssessment,
    WeightAssessmentAdmin
)
admin.site.register(
    WeightDailyAssessmentMeal,
    WeightDailyAssessmentMealAdmin
)
admin.site.register(
    WeightDailyAssessment,
    WeightDailyAssessmentAdmin
)
admin.site.register(
    WeightDaysRange,
    WeightDaysRangeAdmin
)
admin.site.register(
    WeightWeeklyAssessmentLogs,
    WeightWeeklyAssessmentLogsAdmin
)
