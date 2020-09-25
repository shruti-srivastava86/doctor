import factory
from django.utils import timezone

from doctor.factory import DaysRangeAbstractModelFactory
from doctor.weight.models import (
    WeightDaysRange,
    WeightAssessment,
    WeightDailyAssessment,
    WeightDailyAssessmentMeal
)
from doctor import enums


class WeightAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeightAssessment

    initial_score = 24
    score = 24
    calculation_weight = '1.2352941176'
    bmi = '27.00'


class WeightDaysRangeFactory(DaysRangeAbstractModelFactory):
    class Meta:
        model = WeightDaysRange

    required_completions = 2


class WeightDailyAssessmentMealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeightDailyAssessmentMeal

    time = timezone.now().time()
    status = enums.IN_PROGRESS


class WeightDailyAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeightDailyAssessment

    days_range = factory.SubFactory(WeightDaysRangeFactory)
    day = 1
    status = enums.IN_PROGRESS
    assessment_date = timezone.now().date()
    meals = factory.RelatedFactory(
        WeightDailyAssessmentMealFactory,
        'daily_assessment'
    )
