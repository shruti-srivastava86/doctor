"""user factory"""
import factory

from doctor.food_hydration.factory import (
    FoodAndHydrationAssessmentFactory,
    FoodAndHydrationDailyAssessmentFactory
)
from doctor.mind.factory import MindAssessmentFactory
from doctor.motion.factory import (
    MotionAssessmentFactory,
    MotionDailyAssessmentFactory
)
from doctor.sleep.factory import (
    SleepAssessmentFactory,
    SleepDailyAssessmentFactory
)
from doctor.stop_challenge_choose.factory import StopChallengeChooseViewFactory
from doctor.surrounding.factory import (
    SurroundingAssessmentFactory,
    SurroundingDailyAssessmentFactory
)
from doctor.user.models import User, NotificationSettings
from doctor.user import enums
from doctor.weight.factory import (
    WeightAssessmentFactory,
    WeightDailyAssessmentFactory
)


class NotificationSettingsFactory(factory.django.DjangoModelFactory):
    """
        User notification setting factory boy setup.
    """

    class Meta:
        model = NotificationSettings


class UserFactory(factory.django.DjangoModelFactory):
    """
        User factory boy setup.
    """
    class Meta:
        model = User

    name = "Shruti Factory"
    email = "shruti_srivastav86@yahoo.com"
    password = factory.PostGenerationMethodCall(
        'set_password',
        'Password123'
    )
    gender = enums.MALE
    height = 168
    waist = 75
    weight = 75
    dob = "1986-11-26"
    weight_assessment = factory.RelatedFactory(
        WeightAssessmentFactory,
        'user'
    )
    food_and_hydration_assessment = factory.RelatedFactory(
        FoodAndHydrationAssessmentFactory,
        'user'
    )
    motion_assessment = factory.RelatedFactory(
        MotionAssessmentFactory,
        'user'
    )
    sleep_assessment = factory.RelatedFactory(
        SleepAssessmentFactory,
        'user'
    )
    mind_assessment = factory.RelatedFactory(
        MindAssessmentFactory,
        'user'
    )
    surrounding_assessment = factory.RelatedFactory(
        SurroundingAssessmentFactory,
        'user'
    )
    stop_choose_challenge = factory.RelatedFactory(
        StopChallengeChooseViewFactory,
        'user'
    )
    weight_daily_assessments = factory.RelatedFactory(
        WeightDailyAssessmentFactory,
        'user'
    )
    food_and_hydration_daily_assessment = factory.RelatedFactory(
        FoodAndHydrationDailyAssessmentFactory,
        'user'
    )
    motion_daily_assessment = factory.RelatedFactory(
        MotionDailyAssessmentFactory,
        'user'
    )
    sleep_daily_assessment = factory.RelatedFactory(
        SleepDailyAssessmentFactory,
        'user'
    )
    surrounding_daily_assessment = factory.RelatedFactory(
        SurroundingDailyAssessmentFactory,
        'user'
    )
    notification_settings = factory.RelatedFactory(
        NotificationSettingsFactory,
        'user'
    )
