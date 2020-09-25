import factory
from django.utils import timezone

from doctor.factory import DaysRangeAbstractModelFactory
from doctor.motion.models import (
    MotionDaysRange,
    MotionAssessment,
    MotionDailyAssessment
)
from doctor import enums


class MotionAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MotionAssessment

    initial_score = 9
    score = 9
    calculation_weight = '1.6764705882'
    steps_each_day = 3500


class MotionDaysRangeFactory(DaysRangeAbstractModelFactory):
    class Meta:
        model = MotionDaysRange


class MotionDailyAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MotionDailyAssessment

    days_range = factory.SubFactory(MotionDaysRangeFactory)
    day = 1
    status = enums.IN_PROGRESS
    assessment_date = timezone.now().date()
