from datetime import timedelta

from django.utils import timezone

from doctor import enums
from doctor.badges.utils import check_for_badges
from doctor.motion.models import (
    MotionDaysRange,
    MotionDailyAssessment
)
from doctor.surrounding.utils import create_surrounding_daily_assessment
from doctor.utils import (
    set_best_day_streak,
    get_reset_first_day_range_date
)
from doctor.utils import (
    get_calculation_weight,
    get_next_day_range,
    create_daily_assessment,
    get_initial_calculation_weight,
    check_previous_failed_assessment,
    reset_assessment
)
from doctor.surrounding import enums as surrounding_enums


def get_initial_motion_assessment_score(steps_each_day, calculation_weight):
    if steps_each_day < 2000:
        return 1 * calculation_weight
    elif steps_each_day < 4000:
        return 9 * calculation_weight
    elif steps_each_day < 8000:
        return 17 * calculation_weight
    elif steps_each_day < 10000:
        return 25 * calculation_weight
    else:
        return 33 * calculation_weight


def get_motion_assessment_data(user, steps_each_day):
    initial_assessment_score = get_initial_motion_assessment_score(
        steps_each_day,
        get_initial_calculation_weight()
    )
    calculation_weight = get_calculation_weight(
        initial_assessment_score
    )
    return {
        "user": user,
        "calculation_weight": calculation_weight,
        "initial_score": initial_assessment_score,
        "score": initial_assessment_score,
        "steps_each_day": steps_each_day
    }


def create_first_motion_daily_assessment(stage=1, **first_day_range_data):
    motion_first_day_range = MotionDaysRange.objects.first_day_range(
        stage=stage
    ).first()
    if motion_first_day_range:
        create_daily_assessment(
            MotionDailyAssessment,
            motion_first_day_range,
            **first_day_range_data
        )


def create_next_motion_daily_assessment(motion_daily_assessment):
    next_day_days_range = get_next_day_range(
        motion_daily_assessment,
        MotionDaysRange
    )
    if next_day_days_range:
        create_daily_assessment(
            MotionDailyAssessment,
            next_day_days_range,
            user=motion_daily_assessment.user,
            day=motion_daily_assessment.day + 1,
            assessment_date=motion_daily_assessment.assessment_date + timedelta(days=1)
        )
        create_surrounding_daily_assessment(
            motion_daily_assessment,
            next_day_days_range,
            surrounding_enums.MOTION
        )


def complete_motion_daily_assessment(daily_assessment):
    daily_assessment.status = enums.COMPLETE
    daily_assessment.time_logs = [timezone.now().time()]
    daily_assessment.save()
    daily_assessment.user.motion_assessment.score += \
        daily_assessment.user.motion_assessment.calculation_weight
    if daily_assessment.user.motion_assessment.score > 100:
        daily_assessment.user.motion_assessment.score = 100
    daily_assessment.user.motion_assessment.save()
    check_for_badges(daily_assessment)
    set_best_day_streak(daily_assessment)


def check_required_motion_completion(motion_daily_assessment):
    if motion_daily_assessment.days_range.required_completions <= \
            motion_daily_assessment.total_completed:
        complete_motion_daily_assessment(
            motion_daily_assessment
        )
        create_next_motion_daily_assessment(
            motion_daily_assessment
        )
    else:
        reset = check_previous_failed_assessment(
            motion_daily_assessment
        )
        if reset:
            motion_daily_assessment.status = enums.RESET
            reset_assessment(
                motion_daily_assessment.user.motion_assessment,
                MotionDailyAssessment.objects.for_user(
                    motion_daily_assessment.user
                )
            )
            first_day_range_data = get_reset_first_day_range_date(
                motion_daily_assessment.user
            )
            create_first_motion_daily_assessment(
                stage=motion_daily_assessment.days_range.stage,
                **first_day_range_data
            )
        else:
            motion_daily_assessment.status = enums.INCOMPLETE
            motion_daily_assessment.time_logs = None
            create_next_motion_daily_assessment(
                motion_daily_assessment
            )
        motion_daily_assessment.save()
