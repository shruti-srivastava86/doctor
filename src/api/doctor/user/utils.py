import os
import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from doctor.food_hydration.models import FoodAndHydrationAssessment
from doctor.food_hydration.utils import (
    get_food_and_hydration_assessment_data,
    create_first_food_and_hydration_daily_assessment
)
from doctor.mind.models import MindAssessment
from doctor.mind.utils import get_mind_assessment_data
from doctor.motion.models import MotionAssessment
from doctor.motion.utils import get_motion_assessment_data
from doctor.sleep.models import SleepAssessment
from doctor.sleep.utils import get_sleep_assessment_data
from doctor.stop_challenge_choose.models import StopChallengeChoose
from doctor.surrounding.models import SurroundingAssessment
from doctor.surrounding.utils import (
    get_surroundings_assessment_data,
    create_first_surrounding_daily_assessment
)
from doctor.utils import get_first_day_range_data
from doctor.weight.models import WeightAssessment
from doctor.weight.utils import get_weight_assessment_data


def profile_photo(instance, filename):
    extension = os.path.splitext(str(filename))[1]
    filename = str(uuid.uuid4()) + extension
    return 'profile_photo/' + filename


def send_forgot_password_email(user, token):
    url = settings.BASE_URL + reverse(
        'doctor.user:forgot_password',
        kwargs={'token': token}
    )
    subject = "Doctor Account Password Reset"
    message = "Hello {}, \n\nClick this link to reset your password \n\n{}".format(
        user.name,
        url
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )


def create_assessments(user, assessment_data):
    """
        Create user initial assessments.
    """
    WeightAssessment.objects.create(
        **get_weight_assessment_data(
            user,
            assessment_data['bmi']
        )
    )
    FoodAndHydrationAssessment.objects.create(
        **get_food_and_hydration_assessment_data(
            user,
            assessment_data['glasses_of_water_per_day']
        )
    )
    MotionAssessment.objects.create(
        **get_motion_assessment_data(
            user,
            assessment_data['steps_each_day']
        )
    )
    SleepAssessment.objects.create(
        **get_sleep_assessment_data(
            user,
            assessment_data['sleep_hours_each_night']
        )
    )
    MindAssessment.objects.create(
        **get_mind_assessment_data(
            user,
            assessment_data['average_stress_level']
        )
    )
    SurroundingAssessment.objects.create(
        **get_surroundings_assessment_data(
            user,
        )
    )
    StopChallengeChoose.objects.create(
        user=user
    )


def create_user_daily_assessment(user):
    """
        Create user first day assessments.
    """
    first_day_range_data = get_first_day_range_data(
        user
    )
    create_first_food_and_hydration_daily_assessment(
        **first_day_range_data
    )
    create_first_surrounding_daily_assessment(
        **first_day_range_data
    )
