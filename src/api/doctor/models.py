from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from doctor import enums


class TimestampedModel(models.Model):
    """
        Abstract model for Created at and Updated at fields
    """
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class AssessmentAbstractModel(TimestampedModel):
    """
        Abstract model for Initial Assessment
    """
    initial_score = models.PositiveIntegerField()
    score = models.DecimalField(
        max_digits=14,
        decimal_places=10
    )
    calculation_weight = models.DecimalField(
        max_digits=14,
        decimal_places=10,
        editable=False
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['calculation_weight'])
        ]


class DailyAssessmentAbstractModel(TimestampedModel):
    """
        Abstract model for Assessment
    """
    day = models.IntegerField()
    time_logs = ArrayField(
        models.TimeField(),
        null=True,
        blank=True
    )
    total_completed = models.PositiveIntegerField(
        default=0,
    )
    status = models.PositiveSmallIntegerField(
        choices=enums.ASSESSMENT_STATUS
    )
    assessment_date = models.DateField(
        editable=settings.DEBUG
    )
    from_apple_health = models.BooleanField(
        default=False
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['assessment_date'])
        ]


class DaysRangeAbstractModel(TimestampedModel):
    """
        Abstract model for Days Range
    """
    start_range = models.PositiveSmallIntegerField()
    end_range = models.PositiveSmallIntegerField()
    required_completions = models.PositiveSmallIntegerField()
    challenge = models.TextField()
    stage = models.PositiveSmallIntegerField()

    def __str__(self):
        return "Stage: {} - Start: {} - End: {}".format(
            self.stage,
            self.start_range,
            self.end_range
        )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['start_range', 'stage'])
        ]
