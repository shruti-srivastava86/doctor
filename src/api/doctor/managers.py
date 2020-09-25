from datetime import timedelta

from django.db import models
from django.db.models import F, DateField, DateTimeField, Q
from django.db.models.functions import Cast
from django.utils import timezone

from doctor import enums


class DailyAssessmentAbstractQuerySet(models.QuerySet):

    def with_id(self, id):
        return self.filter(
            id=id
        )

    def in_progress(self):
        return self.filter(
            status=enums.IN_PROGRESS
        )

    def incomplete(self):
        return self.filter(
            status=enums.INCOMPLETE
        )

    def complete(self):
        return self.filter(
            status=enums.COMPLETE
        )

    def not_reset(self):
        return self.filter(
            ~Q(status=enums.RESET)
        )

    def in_progress_or_complete(self):
        return self.filter(
            Q(status=enums.IN_PROGRESS) | Q(status=enums.COMPLETE),
        )

    def incomplete_or_reset(self):
        return self.filter(
            Q(status=enums.INCOMPLETE) | Q(status=enums.RESET),
        )

    def for_stage(self, stage=1):
        return self.filter(
            days_range__stage=stage
        )

    def for_day(self, day):
        return self.filter(
            day=day
        )

    def for_user(self, user):
        return self.filter(
            user=user
        )

    def today_assessment(self):
        return self.select_related('days_range').annotate(
            user_current_date=Cast(
                (
                    timezone.now() + (timedelta(seconds=1) * F('user__time_offset'))
                ),
                DateField()
            )
        ).filter(
            assessment_date=F('user_current_date')
        )

    def first_day_assessment(self):
        return self.filter(
            day=1
        )

    def with_no_meals(self):
        return self.filter(
            meals__isnull=True
        )

    def with_user_current_date_time(self):
        """
            To add user local date time in query
        """
        return self.annotate(
            user_current_date_time=Cast(
                timezone.now() + (timedelta(seconds=1) * F('user__time_offset')),
                DateTimeField()
            )
        )

    def for_previous_day(self, **kwargs):
        return self.annotate(
            previous_date=Cast(
                F('user_current_date_time') - timedelta(days=kwargs.get('days', 1)),
                DateField()
            )
        ).filter(
            assessment_date=F('previous_date')
        )

    def with_user_midnight_time(self):
        return self.filter(
            user_current_date_time__hour=0,
            user_current_date_time__minute=0
        )

    def previous_completed_assessments(self, days=6):
        from_date = timezone.now() - timedelta(days=days)
        return self.filter(
            assessment_date__gte=from_date.date(),
            assessment_date__lte=timezone.now().date(),
            status=enums.COMPLETE
        )

    def days_range(self, days_range):
        return self.filter(
            days_range=days_range
        )


class DaysRangeAbstractQuerySet(models.QuerySet):

    def for_day(self, day):
        return self.filter(
            start_range__lte=day,
            end_range__gte=day
        )

    def first_day_range(self, **kwargs):
        return self.filter(
            start_range=1,
            stage=kwargs.get('stage', 1)
        )

    def for_stage(self, stage):
        return self.filter(
            stage=stage
        )
