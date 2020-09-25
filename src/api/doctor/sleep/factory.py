import factory
from django.utils import timezone

from doctor.factory import DaysRangeAbstractModelFactory
from doctor.sleep.models import (
    SleepDaysRange,
    SleepAssessment,
    SleepDailyAssessment
)
from doctor import enums


class SleepAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SleepAssessment

    initial_score = 17
    score = 17
    calculation_weight = '1.4411764706'
    sleep_hours_each_night = 6


class SleepDaysRangeFactory(DaysRangeAbstractModelFactory):
    class Meta:
        model = SleepDaysRange


class SleepDailyAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SleepDailyAssessment

    days_range = factory.SubFactory(SleepDaysRangeFactory)
    day = 1
    status = enums.IN_PROGRESS
    assessment_date = timezone.now().date()
