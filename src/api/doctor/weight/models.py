from django.db import models

from doctor.models import (
    DailyAssessmentAbstractModel,
    DaysRangeAbstractModel,
    AssessmentAbstractModel,
    TimestampedModel
)

from doctor.weight import enums
from doctor.weight.managers import (
    WeightDaysRangeQuerySet,
    WeightDailyAssessmentQuerySet,
    WeightDailyAssessmentMealQuerySet,
    WeightWeeklyAssessmentLogsQuerySet
)


class WeightAssessment(AssessmentAbstractModel):
    """
        Model representing Weight Assessment.
    """
    user = models.OneToOneField(
        'user.User',
        related_name='weight_assessment'
    )
    bmi = models.DecimalField(
        max_digits=4,
        decimal_places=2,
    )
    first_meal_of_day = models.TimeField(
        null=True,
        blank=True
    )
    meal_plan = models.PositiveSmallIntegerField(
        choices=enums.MEAL_PLAN,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessment"
        indexes = AssessmentAbstractModel.Meta.indexes + [
            models.Index(fields=['first_meal_of_day']),
            models.Index(fields=['meal_plan'])
        ]


class WeightWeeklyAssessmentLogs(TimestampedModel):
    """
        Model representing user's Weekly assessment
    """
    objects = WeightWeeklyAssessmentLogsQuerySet.as_manager()

    user = models.ForeignKey(
        'user.User',
        related_name='weight_weekly_assessment'
    )
    bmi = models.IntegerField(
        null=True,
        blank=True
    )
    waist = models.IntegerField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Weekly Assessment"
        verbose_name_plural = "Weekly Assessment"
        ordering = ['-created_at']


class WeightDailyAssessmentMeal(TimestampedModel):
    """
        Model representing Daily Weight Assessment Meal.
    """
    objects = WeightDailyAssessmentMealQuerySet.as_manager()

    meal_type = models.PositiveSmallIntegerField(
        choices=enums.MEAL_TYPE,
        blank=True,
        null=True
    )
    time = models.TimeField()
    status = models.PositiveSmallIntegerField(
        choices=enums.MEAL_ASSESSMENT_STATUS,
        default=enums.PENDING
    )
    daily_assessment = models.ForeignKey(
        'weight.WeightDailyAssessment',
        related_name='meals'
    )

    def __str__(self):
        return "Daily assessment: {} - User: {}".format(
            self.daily_assessment.id,
            self.daily_assessment.user.email
        )

    class Meta:
        verbose_name = "Daily Assessment Meal"
        verbose_name_plural = "Daily Assessment Meal"
        ordering = ['id']


class WeightDailyAssessment(DailyAssessmentAbstractModel):
    """
        Model representing Daily Weight Assessment.
    """
    objects = WeightDailyAssessmentQuerySet.as_manager()

    user = models.ForeignKey(
        'user.User',
        related_name='weight_daily_assessments'
    )
    days_range = models.ForeignKey(
        'weight.WeightDaysRange',
        related_name='assessments'
    )
    meal_plan = models.PositiveSmallIntegerField(
        choices=enums.MEAL_PLAN,
        blank=True,
        null=True
    )

    def __str__(self):
        return "Id: {} - User: {}".format(
            self.id,
            self.user.email
        )

    class Meta:
        verbose_name = "Daily Assessment"
        verbose_name_plural = "Daily Assessment"
        indexes = DailyAssessmentAbstractModel.Meta.indexes
        ordering = ['day']


class WeightDaysRange(DaysRangeAbstractModel):
    """
        Model representing Weight days range.
    """
    objects = WeightDaysRangeQuerySet.as_manager()

    class Meta:
        verbose_name = "Days Range"
        verbose_name_plural = "Days Range"
        indexes = DaysRangeAbstractModel.Meta.indexes
