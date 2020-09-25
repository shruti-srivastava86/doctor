from django.db import models

from doctor.models import (
    DailyAssessmentAbstractModel,
    DaysRangeAbstractModel,
    AssessmentAbstractModel
)
from doctor.surrounding import enums
from doctor.surrounding.managers import (
    SurroundingDaysRangeQuerySet,
    SurroundingDailyAssessmentQuerySet
)


class SurroundingAssessment(AssessmentAbstractModel):
    """
        Model representing Initial Surrounding Assessment.
    """
    user = models.OneToOneField(
        'user.User',
        related_name='surrounding_assessment'
    )

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessment"
        indexes = AssessmentAbstractModel.Meta.indexes


class SurroundingDailyAssessment(DailyAssessmentAbstractModel):
    """
        Model representing Daily Surrounding Assessment.
    """
    objects = SurroundingDailyAssessmentQuerySet.as_manager()

    user = models.ForeignKey(
        'user.User',
        related_name='surrounding_daily_assessments'
    )
    days_range = models.ForeignKey(
        'surrounding.SurroundingDaysRange',
        related_name='assessments'
    )
    status = models.PositiveSmallIntegerField(
        choices=enums.ASSESSMENT_STATUS
    )

    class Meta:
        verbose_name = "Daily Assessment"
        verbose_name_plural = "Daily Assessment"
        indexes = DailyAssessmentAbstractModel.Meta.indexes
        ordering = ['day']


class SurroundingDaysRange(DaysRangeAbstractModel):
    """
        Model representing Surrounding days range.
    """
    objects = SurroundingDaysRangeQuerySet.as_manager()

    for_assessment = models.PositiveSmallIntegerField(
        choices=enums.FOR_ASSESSMENT,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Days Range"
        verbose_name_plural = "Days Range"
        indexes = DaysRangeAbstractModel.Meta.indexes
