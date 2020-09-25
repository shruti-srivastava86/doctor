from doctor.alerts.utils import create_alert
from doctor.badges import enums, constants
from doctor.alerts import enums as alert_enums
from doctor.badges.models import Badges
from doctor.food_hydration.models import FoodAndHydrationDailyAssessment
from doctor.motion.models import MotionDailyAssessment
from doctor.utils import get_assessment
from doctor import constants as generic_constants
from doctor.video.models import Video


def create_badge_alert(user, badge_object):
    """
        Create badge alert
    """
    data = {
        "type": alert_enums.BADGE,
        "macro_type": None,
        "text": constants.BADGE_NOTIFICATION_TEXT,
        "message": constants.BADGE_NOTIFICATION_MESSAGE
    }
    create_alert(
        user,
        badge_object,
        **data
    )


def get_installation_video(assessment_type):
    return {
        enums.WEIGHT: Video.objects.weight_installation(),
        enums.FOOD_AND_HYDRATION: Video.objects.food_and_hydration_installation(),
        enums.MOTION: Video.objects.motion_installation(),
        enums.SLEEP: Video.objects.sleep_installation(),
        enums.MIND: Video.objects.mind_installation(),
        enums.SURROUNDINGS: None
    }[assessment_type]


def create_assessment_installed_alert(assessment, assessment_type):
    """
        Create assessment installed alert
    """
    data = {
        "type": alert_enums.COMPLETED,
        "macro_type": assessment_type,
        "text": generic_constants.HABIT_NOTIFICATION_TEXT[assessment_type]["text"],
        "message": generic_constants.HABIT_NOTIFICATION_TEXT[assessment_type]["message"],
        "video": get_installation_video(assessment_type)
    }
    create_alert(
        assessment.user,
        assessment,
        **data
    )


def check_perfect_run_badge(instance, assessment, badge_object, badges_awarded):
    perfect_run_badge_object = badge_object.filter(type=enums.PERFECT_RUN).first()
    if enums.PERFECT_RUN not in badges_awarded and \
            not assessment.for_stage(stage=instance.days_range.stage).incomplete_or_reset() and \
            perfect_run_badge_object:
        instance.user.badges.add(
            perfect_run_badge_object
        )
        create_badge_alert(
            instance.user,
            perfect_run_badge_object
        )


def check_assessment_badge(instance, assessment_type, badge_object, badges_awarded):
    """
        Check for assessment badge
    """
    assessment_badge_object = badge_object.filter(type=assessment_type).first()
    if assessment_type not in badges_awarded and assessment_badge_object:
        instance.user.badges.add(
            assessment_badge_object
        )
        create_badge_alert(
            instance.user,
            assessment_badge_object
        )
        create_assessment_installed_alert(
            instance,
            assessment_type
        )


def week_streak_badge(instance, assessment, badge_object, badges_awarded):
    """
        Check for week streak badge
    """
    week_streak_types = [
        enums.ONE_WEEK_STREAK,
        enums.TWO_WEEK_STREAK,
        enums.THREE_WEEK_STREAK,
        enums.FOUR_WEEK_STREAK,
        enums.FIVE_WEEK_STREAK,
        enums.SIX_WEEK_STREAK,
        enums.SEVEN_WEEK_STREAK,
        enums.EIGHT_WEEK_STREAK,
    ]
    i = 1
    for week_streak_type in week_streak_types:
        if week_streak_type not in badges_awarded:
            days = 7 * i
            if isinstance(instance, FoodAndHydrationDailyAssessment) or isinstance(instance, MotionDailyAssessment):
                previous_week_completed_assessments_count = assessment.previous_completed_assessments(
                    days=days
                ).count()
            else:
                previous_week_completed_assessments_count = assessment.previous_completed_assessments(
                    days=days - 1
                ).count()
            if previous_week_completed_assessments_count == days:
                badge_object = badge_object.filter(type=week_streak_type).first()
                instance.user.badges.add(
                    badge_object
                )
                create_badge_alert(
                    instance.user,
                    badge_object
                )
        i += 1


def check_for_badges(instance):
    """
        Check for badges
    """
    badge_object = Badges.objects.all()
    badges_awarded = instance.user.badges.values_list('type', flat=True)
    assessment_type, assessment = get_assessment(instance)
    if instance.days_range.end_range == 66 or assessment_type == enums.SURROUNDINGS:
        check_assessment_badge(
            instance,
            assessment_type,
            badge_object,
            badges_awarded
        )
    if not assessment_type == enums.SURROUNDINGS:
        check_perfect_run_badge(
            instance,
            assessment,
            badge_object,
            badges_awarded
        )
        week_streak_badge(
            instance,
            assessment,
            badge_object,
            badges_awarded
        )
