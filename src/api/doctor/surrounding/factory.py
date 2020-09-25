import factory
from django.utils import timezone

from doctor.factory import DaysRangeAbstractModelFactory
from doctor.surrounding.models import (
    SurroundingDaysRange,
    SurroundingAssessment,
    SurroundingDailyAssessment
)
from doctor import enums


class SurroundingAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SurroundingAssessment

    initial_score = 0
    score = 0
    calculation_weight = '100.0000000000'


class SurroundingDaysRangeFactory(DaysRangeAbstractModelFactory):
    class Meta:
        model = SurroundingDaysRange


class SurroundingDailyAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SurroundingDailyAssessment

    days_range = factory.SubFactory(SurroundingDaysRangeFactory)
    day = 1
    status = enums.IN_PROGRESS
    assessment_date = timezone.now().date()
