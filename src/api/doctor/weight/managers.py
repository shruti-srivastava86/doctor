from datetime import timedelta

from django.db import models
from django.db.models import (
    DateTimeField,
    F,
    DateField,
    ExpressionWrapper,
    TimeField
)
from django.db.models.functions import Cast
from django.utils import timezone

from doctor.weight import enums
from doctor.managers import (
    DailyAssessmentAbstractQuerySet,
    DaysRangeAbstractQuerySet
)


class WeightDailyAssessmentMealQuerySet(DailyAssessmentAbstractQuerySet):

    def with_id(self, id):
        return self.filter(
            id=id
        )

    def in_pending(self):
        return self.filter(
            status=enums.PENDING
        )

    def in_progress(self):
        return self.filter(
            status=enums.IN_PROGRESS
        )

    def for_user(self, user):
        return self.filter(
            daily_assessment__user=user
        )

    def with_user_current_date_time(self):
        return self.annotate(
            user_current_date_time=Cast(
                timezone.now() + (timedelta(seconds=1) * F('daily_assessment__user__time_offset')),
                DateTimeField()
            )
        )

    def for_today(self):
        return self.annotate(
            current_date=Cast(
                F('user_current_date_time'),
                DateField()
            )
        ).filter(
            daily_assessment__assessment_date=F('current_date')
        )

    def before_time(self):
        return self.annotate(
            utc_time_as_local_time=Cast(
                timezone.now() + (
                    timedelta(seconds=1) * F('daily_assessment__user__time_offset')
                ),
                DateTimeField()
            )
        ).annotate(
            dummy_local_date=Cast(
                F('utc_time_as_local_time'),
                DateField()
            )
        ).annotate(
            dummy_local_date_time=Cast(
                F('dummy_local_date'),
                DateTimeField()
            )
        ).annotate(
            meal_time_as_date_time=ExpressionWrapper(
                F('time') + F('dummy_local_date_time'),
                output_field=DateTimeField()
            )
        ).filter(
            meal_time_as_date_time__lte=F('utc_time_as_local_time')
        )

    def upcoming_meal(self):
        return self.annotate(
            utc_time_as_local_time=Cast(
                timezone.now().replace(second=0, microsecond=0) + (
                    timedelta(seconds=1) * F('daily_assessment__user__time_offset')
                ),
                DateTimeField()
            )
        ).annotate(
            reminder_time=Cast(
                F('utc_time_as_local_time') + timedelta(minutes=10),
                TimeField()
            )
        ).filter(
            time=F('reminder_time')
        )


class WeightDailyAssessmentQuerySet(DailyAssessmentAbstractQuerySet):

    pass


class WeightDaysRangeQuerySet(DaysRangeAbstractQuerySet):

    pass


class WeightWeeklyAssessmentLogsQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(
            user=user
        )
