from django.utils import timezone
from datetime import timedelta

from doctor import enums
from doctor.badges.utils import check_for_badges
from doctor.sleep import enums as sleep_enums

from doctor.sleep.models import (
    SleepDaysRange,
    SleepDailyAssessment
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


def get_initial_sleep_assessment_score(sleep_hours_each_night, calculation_weight):
    if sleep_hours_each_night < 4:
        return 1 * calculation_weight
    elif sleep_hours_each_night < 6:
        return 9 * calculation_weight
    elif sleep_hours_each_night < 7:
        return 17 * calculation_weight
    elif sleep_hours_each_night < 8:
        return 25 * calculation_weight
    else:
        return 33 * calculation_weight


def get_sleep_assessment_data(user, sleep_hours_each_night):
    initial_assessment_score = get_initial_sleep_assessment_score(
        sleep_hours_each_night,
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
        "sleep_hours_each_night": sleep_hours_each_night
    }


def is_sleep_completed_criteria_satisfied(days_range, sleep_type):
    if days_range.end_range <= 21:
        return True
    elif days_range.end_range <= 43 and not sleep_type == sleep_enums.UNHEALTHY:
        return True
    elif days_range.end_range <= 66 and sleep_type == sleep_enums.HEALTHY:
        return True
    return False


def create_first_sleep_daily_assessment(stage=1, **first_day_range_data):
    sleep_first_day_range = SleepDaysRange.objects.first_day_range(
        stage=stage
    ).first()
    if sleep_first_day_range:
        create_daily_assessment(
            SleepDailyAssessment,
            sleep_first_day_range,
            **first_day_range_data
        )


def create_next_sleep_daily_assessment(sleep_daily_assessment):
    next_day_days_range = get_next_day_range(
        sleep_daily_assessment,
        SleepDaysRange
    )
    if next_day_days_range:
        create_daily_assessment(
            SleepDailyAssessment,
            next_day_days_range,
            user=sleep_daily_assessment.user,
            day=sleep_daily_assessment.day + 1,
            assessment_date=sleep_daily_assessment.assessment_date + timedelta(days=1)
        )
        create_surrounding_daily_assessment(
            sleep_daily_assessment,
            next_day_days_range,
            surrounding_enums.SLEEP
        )


def complete_sleep_daily_assessment_status(daily_assessment):
    daily_assessment.status = enums.COMPLETE
    daily_assessment.time_logs = [timezone.now().time()]
    daily_assessment.save()
    daily_assessment.user.sleep_assessment.score += \
        daily_assessment.user.sleep_assessment.calculation_weight
    if daily_assessment.user.sleep_assessment.score > 100:
        daily_assessment.user.sleep_assessment.score = 100
    daily_assessment.user.sleep_assessment.save()
    check_for_badges(daily_assessment)
    set_best_day_streak(daily_assessment)


def check_required_sleep_completion(sleep_daily_assessment, sleep_type):
    if sleep_daily_assessment.days_range.required_completions <= sleep_daily_assessment.total_completed \
            and is_sleep_completed_criteria_satisfied(
                sleep_daily_assessment.days_range,
                sleep_type
            ):
        complete_sleep_daily_assessment_status(
            sleep_daily_assessment
        )
        create_next_sleep_daily_assessment(
            sleep_daily_assessment
        )
    else:
        reset = check_previous_failed_assessment(
            sleep_daily_assessment
        )
        if reset:
            sleep_daily_assessment.status = enums.RESET
            reset_assessment(
                sleep_daily_assessment.user.sleep_assessment,
                SleepDailyAssessment.objects.for_user(
                    sleep_daily_assessment.user
                )
            )
            first_day_range_data = get_reset_first_day_range_date(
                sleep_daily_assessment.user
            )
            create_first_sleep_daily_assessment(
                stage=sleep_daily_assessment.days_range.stage,
                **first_day_range_data
            )
        else:
            sleep_daily_assessment.status = enums.INCOMPLETE
            sleep_daily_assessment.time_logs = None
            create_next_sleep_daily_assessment(
                sleep_daily_assessment
            )
    sleep_daily_assessment.save()
    return sleep_daily_assessment
