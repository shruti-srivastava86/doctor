from datetime import timedelta

from django.db import models
from django.db.models import Q, DateTimeField, F, DateField
from django.db.models.functions import Cast
from django.utils import timezone

from doctor.alerts import enums


class AlertQuerySet(models.QuerySet):

    def unread_count(self):
        return self.filter(
            read=False
        ).count()

    def type_completed(self):
        return self.filter(
            type=enums.COMPLETED
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

    def with_user_midnight_time(self):
        return self.filter(
            user_current_date_time__hour=0,
            user_current_date_time__minute=0
        )

    def previous_weeks_completed(self):
        return self.annotate(
            previous_one_week_date=Cast(
                F('user_current_date_time') - timedelta(
                    weeks=1
                ),
                DateField()
            )
        ).annotate(
            previous_two_week_date=Cast(
                F('user_current_date_time') - timedelta(
                    weeks=2
                ),
                DateField()
            )
        ).annotate(
            previous_three_week_date=Cast(
                F('user_current_date_time') - timedelta(
                    weeks=3
                ),
                DateField()
            )
        ).filter(
            Q(
                created_at__date=F('previous_one_week_date')
            ) | Q(
                created_at__date=F('previous_two_week_date')
            ) | Q(
                created_at__date=F('previous_three_week_date')
            )
        )

    def previous_month_completed(self):
        return self.annotate(
            previous_one_month_date=Cast(
                F('user_current_date_time') - timedelta(
                    weeks=4
                ),
                DateField()
            )
        ).annotate(
            previous_two_month_date=Cast(
                F('user_current_date_time') - timedelta(
                    weeks=8
                ),
                DateField()
            )
        ).filter(
            Q(
                created_at__date=F('previous_one_month_date')
            ) | Q(
                created_at__date=F('previous_two_month_date')
            )
        )
