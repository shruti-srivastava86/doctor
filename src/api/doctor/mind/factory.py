import factory

from doctor.factory import DaysRangeAbstractModelFactory
from doctor.mind.models import (
    MindDaysRange,
    MindAssessment,
    MindDailyAssessment
)


class MindAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MindAssessment

    initial_score = 17
    score = 17
    calculation_weight = '1.4411764706'
    average_stress_level = 5


class MindDaysRangeFactory(DaysRangeAbstractModelFactory):
    class Meta:
        model = MindDaysRange


class MindDailyAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MindDailyAssessment

    days_range = factory.SubFactory(MindDaysRangeFactory)
