from datetime import timedelta

from django.utils import timezone

from doctor import enums
from doctor.badges.utils import check_for_badges
from doctor.mind.models import (
    MindDaysRange,
    MindDailyAssessment
)
from doctor.surrounding.utils import create_surrounding_daily_assessment
from doctor.utils import (
    get_calculation_weight,
    get_initial_calculation_weight,
    set_best_day_streak,
    get_next_day_range,
    create_daily_assessment,
    check_previous_failed_assessment,
    reset_assessment,
    get_reset_first_day_range_date
)
from doctor.surrounding import enums as surrounding_enums


def get_initial_mind_assessment_score(average_stress_level, calculation_weight):
    if average_stress_level < 3:
        return 1 * calculation_weight
    elif average_stress_level < 5:
        return 9 * calculation_weight
    elif average_stress_level < 7:
        return 17 * calculation_weight
    elif average_stress_level < 9:
        return 25 * calculation_weight
    else:
        return 33 * calculation_weight


def get_mind_assessment_data(user, average_stress_level):
    initial_assessment_score = get_initial_mind_assessment_score(
        average_stress_level,
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
        "average_stress_level": average_stress_level
    }


def create_first_mind_daily_assessment(stage=1, **first_day_range_data):
    mind_first_day_range = MindDaysRange.objects.first_day_range(
        stage=stage
    ).first()
    if mind_first_day_range:
        create_daily_assessment(
            MindDailyAssessment,
            mind_first_day_range,
            **first_day_range_data
        )


def create_next_mind_daily_assessment(mind_daily_assessment):
    next_day_days_range = get_next_day_range(
        mind_daily_assessment,
        MindDaysRange
    )
    if next_day_days_range:
        create_daily_assessment(
            MindDailyAssessment,
            next_day_days_range,
            user=mind_daily_assessment.user,
            day=mind_daily_assessment.day + 1,
            assessment_date=mind_daily_assessment.assessment_date + timedelta(days=1)
        )
        create_surrounding_daily_assessment(
            mind_daily_assessment,
            next_day_days_range,
            surrounding_enums.MIND
        )


def complete_mind_daily_assessment_status(daily_assessment):
    daily_assessment.status = enums.COMPLETE
    daily_assessment.time_logs = [timezone.now().time()]
    daily_assessment.save()
    daily_assessment.user.mind_assessment.score += \
        daily_assessment.user.mind_assessment.calculation_weight
    if daily_assessment.user.mind_assessment.score > 100:
        daily_assessment.user.mind_assessment.score = 100
    daily_assessment.user.mind_assessment.save()
    check_for_badges(daily_assessment)
    set_best_day_streak(daily_assessment)


def check_mind_completion(mind_daily_assessment):
    if mind_daily_assessment.days_range.required_completions == \
            mind_daily_assessment.total_completed:
        complete_mind_daily_assessment_status(
            mind_daily_assessment
        )
        create_next_mind_daily_assessment(
            mind_daily_assessment
        )
    else:
        reset = check_previous_failed_assessment(
            mind_daily_assessment
        )
        if reset:
            mind_daily_assessment.status = enums.RESET
            reset_assessment(
                mind_daily_assessment.user.mind_assessment,
                MindDailyAssessment.objects.for_user(
                    mind_daily_assessment.user
                )
            )
            first_day_range_data = get_reset_first_day_range_date(
                mind_daily_assessment.user
            )
            create_first_mind_daily_assessment(
                stage=mind_daily_assessment.days_range.stage,
                **first_day_range_data
            )
        else:
            mind_daily_assessment.status = enums.INCOMPLETE
            create_next_mind_daily_assessment(
                mind_daily_assessment
            )
    mind_daily_assessment.save()
    return mind_daily_assessment
