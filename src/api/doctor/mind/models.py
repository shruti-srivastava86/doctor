from django.db import models

from doctor.mind.managers import (
    MindDaysRangeQuerySet,
    MindDailyAssessmentQuerySet
)
from doctor.models import (
    DailyAssessmentAbstractModel,
    DaysRangeAbstractModel,
    AssessmentAbstractModel
)


class MindAssessment(AssessmentAbstractModel):
    """
        Model representing Initial Mind Assessment.
    """
    user = models.OneToOneField(
        'user.User',
        related_name='mind_assessment'
    )
    average_stress_level = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessment"
        indexes = AssessmentAbstractModel.Meta.indexes


class MindDailyAssessment(DailyAssessmentAbstractModel):
    """
        Model representing Daily Mind Assessment.
    """
    objects = MindDailyAssessmentQuerySet.as_manager()

    user = models.ForeignKey(
        'user.User',
        related_name='mind_daily_assessments'
    )
    days_range = models.ForeignKey(
        'mind.MindDaysRange',
        related_name='assessments'
    )
    identify = models.TextField(
        blank=True
    )
    choose = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "Daily Assessment"
        verbose_name_plural = "Daily Assessment"
        indexes = DailyAssessmentAbstractModel.Meta.indexes
        ordering = ['day']


class MindDaysRange(DaysRangeAbstractModel):
    """
        Model representing Mind days range.
    """
    objects = MindDaysRangeQuerySet.as_manager()
    help_text = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "Days Range"
        verbose_name_plural = "Days Range"
        indexes = DaysRangeAbstractModel.Meta.indexes
