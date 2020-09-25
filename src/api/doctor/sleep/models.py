from django.db import models

from doctor.models import (
    DailyAssessmentAbstractModel,
    DaysRangeAbstractModel,
    AssessmentAbstractModel
)
from doctor.sleep import enums
from doctor.sleep.managers import (
    SleepDaysRangeQuerySet,
    SleepDailyAssessmentQuerySet
)


class SleepAssessment(AssessmentAbstractModel):
    """
        Model representing Initial Sleep Assessment.
    """
    user = models.OneToOneField(
        'user.User',
        related_name='sleep_assessment'
    )
    sleep_hours_each_night = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessment"
        indexes = AssessmentAbstractModel.Meta.indexes


class SleepDailyAssessment(DailyAssessmentAbstractModel):
    """
        Model representing Daily Sleep Assessment.
    """
    objects = SleepDailyAssessmentQuerySet.as_manager()

    user = models.ForeignKey(
        'user.User',
        related_name='sleep_daily_assessments'
    )
    days_range = models.ForeignKey(
        'sleep.SleepDaysRange',
        related_name='assessments'
    )
    sleep_type = models.PositiveSmallIntegerField(
        choices=enums.SLEEP_TYPE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Daily Assessment"
        verbose_name_plural = "Daily Assessment"
        indexes = DailyAssessmentAbstractModel.Meta.indexes
        ordering = ['day']


class SleepDaysRange(DaysRangeAbstractModel):
    """
        Model representing Sleep days range.
    """
    objects = SleepDaysRangeQuerySet.as_manager()

    class Meta:
        verbose_name = "Days Range"
        verbose_name_plural = "Days Range"
        indexes = DaysRangeAbstractModel.Meta.indexes
