from django.db import models

from doctor.motion.managers import MotionDaysRangeQuerySet, MotionDailyAssessmentQuerySet
from doctor.models import (
    DailyAssessmentAbstractModel,
    DaysRangeAbstractModel,
    AssessmentAbstractModel
)


class MotionAssessment(AssessmentAbstractModel):
    """
        Model representing Initial Motion Assessment.
    """
    user = models.OneToOneField(
        'user.User',
        related_name='motion_assessment'
    )
    steps_each_day = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessment"
        indexes = AssessmentAbstractModel.Meta.indexes


class MotionDailyAssessment(DailyAssessmentAbstractModel):
    """
        Model representing Daily Motion Assessment.
    """
    objects = MotionDailyAssessmentQuerySet.as_manager()

    user = models.ForeignKey(
        'user.User',
        related_name='motion_daily_assessments'
    )
    days_range = models.ForeignKey(
        'motion.MotionDaysRange',
        related_name='assessments'
    )
    automated_step_count = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = "Daily Assessment"
        verbose_name_plural = "Daily Assessment"
        indexes = DailyAssessmentAbstractModel.Meta.indexes
        ordering = ['day']


class MotionDaysRange(DaysRangeAbstractModel):
    """
        Model representing Motion days range.
    """
    objects = MotionDaysRangeQuerySet.as_manager()

    class Meta:
        verbose_name = "Days Range"
        verbose_name_plural = "Days Range"
        indexes = DaysRangeAbstractModel.Meta.indexes
