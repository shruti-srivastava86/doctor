from django.contrib import admin

from doctor.admin import (
    DailyAssessmentAbstractModelAdmin,
    DaysRangeAbstractModelAdmin,
    AssessmentAbstractModelAdmin
)
from doctor.food_hydration.models import (
    FoodAndHydrationAssessment,
    FoodAndHydrationDailyAssessment,
    FoodAndHydrationDaysRange
)


class FoodAndHydrationAssessmentAdmin(AssessmentAbstractModelAdmin):
    list_display = AssessmentAbstractModelAdmin.list_display


class FoodAndHydrationDailyAssessmentAdmin(DailyAssessmentAbstractModelAdmin):
    list_display = DailyAssessmentAbstractModelAdmin.list_display


class FoodAndHydrationDaysRangeAdmin(DaysRangeAbstractModelAdmin):
    list_display = DaysRangeAbstractModelAdmin.list_display


admin.site.register(
    FoodAndHydrationAssessment,
    FoodAndHydrationAssessmentAdmin
)
admin.site.register(
    FoodAndHydrationDailyAssessment,
    FoodAndHydrationDailyAssessmentAdmin
)
admin.site.register(
    FoodAndHydrationDaysRange,
    FoodAndHydrationDaysRangeAdmin
)
