"""User model managers"""
from datetime import timedelta

from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import F, DateTimeField, DateField
from django.db.models.functions import Cast, ExtractWeekDay
from django.utils import timezone

from doctor.user import enums


class DoctorUserManager(UserManager):
    """
        Custom manager for the User model.
    """
    def _create_user(self, **kwargs):
        user = self.model(**kwargs)
        user.save(using=self._db)
        user.is_active = True
        user.set_password(kwargs.get('password'))
        user.save(using=self._db)
        return user

    def create_user(self, **kwargs):
        return self._create_user(**kwargs)

    def create_superuser(self, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('gender', enums.OTHER)
        kwargs.setdefault('dob', timezone.now())
        kwargs.setdefault('height', 182)
        kwargs.setdefault('weight', 80)
        kwargs.setdefault('waist', 75)
        return self._create_user(**kwargs)


class DoctorUserQueryset(models.QuerySet):
    """
        Queryset manager for the User model.
    """
    def with_id(self, user_id):
        """
            To filter users with id.
        """
        return self.filter(id=user_id)

    def with_email(self, email):
        """
            To filter users with email.
        """
        return self.filter(email=email)

    def with_user_local_date_time(self):
        """
            To add user local date time in query
        """
        return self.annotate(
            local_time=Cast(
                timezone.now() + (timedelta(seconds=1) * F('time_offset')),
                DateTimeField()
            ),
            local_date=Cast(
                timezone.now() + (timedelta(seconds=1) * F('time_offset')),
                DateField()
            )
        )

    def with_weekday(self):
        """
            To add weekday from the user local time
        """
        return self.annotate(
            weekday=ExtractWeekDay('local_time')
        )

    def with_incomplete_macro_for_today(self):
        return self.filter(
            food_and_hydration_daily_assessments__assessment_date=F('local_date')
        )

    def with_complete_macro(self, macro_type):
        return self.filter(
            badges__type__in=[macro_type]
        )
