import factory
from django.utils import timezone

from doctor.factory import DaysRangeAbstractModelFactory
from doctor.food_hydration.models import (
    FoodAndHydrationDaysRange,
    FoodAndHydrationDailyAssessment,
    FoodAndHydrationAssessment
)
from doctor import enums


class FoodAndHydrationAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodAndHydrationAssessment

    initial_score = 9
    score = 9
    calculation_weight = '1.6764705882'
    glasses_of_water_per_day = 3


class FoodAndHydrationDaysRangeFactory(DaysRangeAbstractModelFactory):
    class Meta:
        model = FoodAndHydrationDaysRange


class FoodAndHydrationDailyAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodAndHydrationDailyAssessment

    days_range = factory.SubFactory(FoodAndHydrationDaysRangeFactory)
    day = 1
    status = enums.IN_PROGRESS
    assessment_date = timezone.now().date()
