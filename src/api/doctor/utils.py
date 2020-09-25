from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
import uuid
import os

from api.generics.utils import send_mail
from doctor import enums, constants
from doctor.alerts.utils import (
    create_failed_assessment_alert,
    create_failed_assessment_day_alert
)
from doctor.badges import enums as badges_enum
from doctor.constants import ASSESSMENT_DAYS_RANGE_CATEGORY_BY_TYPE
from doctor.food_hydration.models import FoodAndHydrationDailyAssessment
from doctor.mind.models import MindDailyAssessment
from doctor.motion.models import MotionDailyAssessment
from doctor.sleep.models import SleepDailyAssessment
from doctor.surrounding.models import (
    SurroundingDaysRange,
    SurroundingDailyAssessment
)
from doctor.video.models import Video
from doctor.weight.models import WeightDailyAssessment


def get_initial_calculation_weight():
    return constants.TOTAL_INITIAL_ASSESSMENT_SCORE / constants.MAXIMUM_INITIAL_ASSESSMENT_SCORE


def get_calculation_weight(initial_assessment_score):
    remaining_score = (
        constants.TOTAL_INITIAL_ASSESSMENT_SCORE + constants.TOTAL_INSTALLATION_SCORE
    ) - initial_assessment_score
    return remaining_score / constants.TOTAL_INSTALLATION_DAYS


def get_calculation_surrounding_weight():
    total_stage_1 = SurroundingDaysRange.objects.total_stage_1()
    if total_stage_1:
        return constants.TOTAL_SCORE / total_stage_1
    return total_stage_1


class ErrorResponse:
    @staticmethod
    def build_serializer_error(serializer, status):
        return Response({"status": "error", "errors": serializer.errors},
                        status=status)

    @staticmethod
    def build_text_error(text, status):
        return Response({"status": "error", "errors": text}, status=status)


def random_profile_image_name(instance, old_filename):
    extension = os.path.splitext(old_filename)[1]
    filename = str(uuid.uuid4()) + extension
    return 'profile_images/' + filename


def random_media_name(instance, old_filename):
    extension = os.path.splitext(old_filename)[1]
    filename = str(uuid.uuid4()) + extension
    return 'media/' + filename


def random_thumbnail_name(instance, old_filename):
    extension = os.path.splitext(old_filename)[1]
    filename = str(uuid.uuid4()) + extension
    return 'thumbnails/' + filename


def send_email(subject, message, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL]
    )


def get_next_day_range(assessment, days_range):
    """
        Get the next day range for an assessment
    """
    if assessment.day + 1 <= assessment.days_range.end_range:
        return assessment.days_range
    else:
        next_day_days_range = days_range.objects.for_day(
            assessment.day + 1
        ).for_stage(
            assessment.days_range.stage
        ).first()
        if not next_day_days_range:
            return days_range.objects.for_day(1).for_stage(
                assessment.days_range.stage + 1
            ).first()
        return next_day_days_range


def create_daily_assessment(assessment, days_range, *args, **kwargs):
    """
        Create daily assessment for any macro
    """
    return assessment.objects.create(
        user=kwargs.get('user'),
        days_range=days_range,
        day=kwargs.get('day'),
        status=kwargs.get('status', enums.IN_PROGRESS),
        assessment_date=kwargs.get('assessment_date', timezone.now().date())
    )


def get_assessment(instance):
    """
        Get the badge type and assessment type based on instance
    """
    assessment_type = None
    assessment = None
    if isinstance(instance, WeightDailyAssessment):
        assessment_type = badges_enum.WEIGHT
        assessment = instance.user.weight_daily_assessments
    elif isinstance(instance, FoodAndHydrationDailyAssessment):
        assessment_type = badges_enum.FOOD_AND_HYDRATION
        assessment = instance.user.food_and_hydration_daily_assessments
    elif isinstance(instance, MotionDailyAssessment):
        assessment_type = badges_enum.MOTION
        assessment = instance.user.motion_daily_assessments
    elif isinstance(instance, SleepDailyAssessment):
        assessment_type = badges_enum.SLEEP
        assessment = instance.user.sleep_daily_assessments
    elif isinstance(instance, MindDailyAssessment):
        assessment_type = badges_enum.MIND
        assessment = instance.user.mind_daily_assessments
    elif isinstance(instance, SurroundingDailyAssessment):
        assessment_type = badges_enum.SURROUNDINGS
        assessment = instance.user.surrounding_daily_assessments
    return assessment_type, assessment


def get_assessment_by_type(type):
    """
        Get assessment object based on type
    """
    return constants.ASSESSMENT_DAYS_RANGE_CATEGORY_BY_TYPE[type]["assessment"]


def get_days_range_by_assessment(type):
    """
        Get days range object based on assessment type
    """
    return constants.ASSESSMENT_DAYS_RANGE_CATEGORY_BY_TYPE[type]["days_range"]


def get_category_by_assessment(type):
    """
        Get category based on assessment type
    """
    return constants.ASSESSMENT_DAYS_RANGE_CATEGORY_BY_TYPE[type]["category"]


def check_best_day_streak(instance):
    """
        Check for best day streak for user
    """
    assessment_type, assessment = get_assessment(instance)
    latest_incomplete_assessment = assessment.incomplete_or_reset().latest('assessment_date')
    if latest_incomplete_assessment:
        best_streak = assessment.complete().filter(
            assessment_date__lte=timezone.now().date(),
            assessment_date__gt=latest_incomplete_assessment.assessment_date
        ).count()
    else:
        best_streak = assessment.complete().count()
    if best_streak > instance.user.best_day_streak:
        instance.user.best_day_streak = best_streak
        instance.user.save()


def check_previous_failed_assessment(instance):
    assessment_type, assessment = get_assessment(instance)
    total_incomplete = 1
    previous_one_day_daily_assessment = assessment.with_user_current_date_time().for_previous_day(
        days=2
    ).incomplete().first()
    if previous_one_day_daily_assessment:
        total_incomplete += 1
        previous_two_day_daily_assessment = assessment.with_user_current_date_time().for_previous_day(
            days=3
        ).incomplete().first()
        if previous_two_day_daily_assessment:
            total_incomplete += 1
    video_object = Video.objects.missing_a_day() if total_incomplete < 3 else Video.objects.failing_a_macro()
    if total_incomplete > 1:
        create_failed_assessment_day_alert(
            instance.user,
            instance,
            ASSESSMENT_DAYS_RANGE_CATEGORY_BY_TYPE[assessment_type]["category"],
            assessment_type,
            total_incomplete,
            video_object
        )
    else:
        create_failed_assessment_alert(
            instance.user,
            instance,
            ASSESSMENT_DAYS_RANGE_CATEGORY_BY_TYPE[assessment_type]["category"],
            assessment_type,
            video_object
        )
    if total_incomplete == 3:
        return True
    return False


def reset_assessment(assessment, daily_assessments):
    assessment.score = assessment.initial_score
    assessment.save()
    daily_assessments.update(status=enums.RESET)


def get_first_day_range_data(user):
    return {
        "user": user,
        "day": 1,
        "status": enums.IN_PROGRESS,
        "assessment_date": (
            timezone.now() + timedelta(days=1, seconds=user.time_offset)
        ).date()
    }


def get_reset_first_day_range_date(user):
    return {
        "user": user,
        "day": 1,
        "status": enums.IN_PROGRESS,
        "assessment_date": (
            timezone.now() + timedelta(seconds=user.time_offset)
        ).date()
    }


def set_best_day_streak(instance):
    assessment_type, assessment = get_assessment(instance)
    previous_complete_assessment_count = assessment.with_user_current_date_time().previous_completed_assessments(
        days=instance.user.best_day_streak + 1
    ).count()
    if previous_complete_assessment_count > instance.user.best_day_streak:
        instance.user.best_day_streak = previous_complete_assessment_count
        instance.user.save()


def get_assessment_overview_data(user, assessment_type, daily_assessments, days_range):
    challenges = list()
    if assessment_type in user.earned_assessment_badges():
        data = {
            "status": enums.COMPLETE
        }
    else:
        current_assessment = daily_assessments.today_assessment().first()
        if current_assessment:
            data = {
                "status": enums.IN_PROGRESS
            }
            assessment_day_ranges = days_range.objects.all().order_by(
                'start_range'
            )
            for assessment_day_range in assessment_day_ranges:
                if (assessment_day_range.start_range <= current_assessment.day <= assessment_day_range.end_range) or (
                        assessment_day_range.end_range < current_assessment.day
                ):
                    challenges.append(
                        assessment_day_range.challenge
                    )
        else:
            data = {
                "status": enums.LOCKED
            }
    installation_progress = daily_assessments.all()
    data[
        "challenges"
    ] = challenges
    data[
        "installation_progress"
    ] = installation_progress
    return data


def reopen_daily_assessment(user, assessment, daily_Assessment, days_range):
    last_days_range = days_range.objects.order_by(
        '-start_range'
    ).first()
    last_assessment_range = daily_Assessment.objects.days_range(
        last_days_range
    )
    assessment.score -= (last_assessment_range.count() * assessment.calculation_weight)
    assessment.save()
    last_assessment_range.update(
        status=enums.RESET
    )
    return create_daily_assessment(
        daily_Assessment,
        last_days_range,
        user=user,
        day=last_days_range.start_range,
        assessment_date=timezone.now() + timedelta(days=1)
    )
