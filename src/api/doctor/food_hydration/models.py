from django.db import models

from doctor.food_hydration.managers import (
    FoodAndHydrationDaysRangeQuerySet,
    FoodAndHydrationDailyAssessmentQuerySet
)
from doctor.models import (
    DailyAssessmentAbstractModel,
    DaysRangeAbstractModel,
    AssessmentAbstractModel
)


class FoodAndHydrationAssessment(AssessmentAbstractModel):
    """
        Model representing Initial Food and Hydration Assessment.
    """
    user = models.OneToOneField(
        'user.User',
        related_name='food_and_hydration_assessment'
    )
    glasses_of_water_per_day = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessment"
        indexes = AssessmentAbstractModel.Meta.indexes


class FoodAndHydrationDailyAssessment(DailyAssessmentAbstractModel):
    """
        Model representing Daily Food and Hydration Assessment.
    """
    objects = FoodAndHydrationDailyAssessmentQuerySet.as_manager()

    user = models.ForeignKey(
        'user.User',
        related_name='food_and_hydration_daily_assessments'
    )
    days_range = models.ForeignKey(
        'food_hydration.FoodAndHydrationDaysRange',
        related_name='assessments'
    )

    class Meta:
        verbose_name = "Daily Assessment"
        verbose_name_plural = "Daily Assessment"
        indexes = DailyAssessmentAbstractModel.Meta.indexes
        ordering = ['day']


class FoodAndHydrationDaysRange(DaysRangeAbstractModel):
    """
        Model representing Food and Hydration days range.
    """
    objects = FoodAndHydrationDaysRangeQuerySet.as_manager()

    class Meta:
        verbose_name = "Days Range"
        verbose_name_plural = "Days Range"
        indexes = DaysRangeAbstractModel.Meta.indexes
