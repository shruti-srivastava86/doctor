from datetime import timedelta
from decimal import Decimal

from doctor.badges.utils import check_for_badges
from doctor.surrounding.utils import create_surrounding_daily_assessment
from doctor.utils import (
    get_calculation_weight,
    get_next_day_range,
    create_daily_assessment,
    get_initial_calculation_weight,
    set_best_day_streak
)
from doctor.weight import enums
from doctor.weight.constants import NEXT_MEAL_TIME_DIFFERENCE
from doctor.weight.models import (
    WeightDailyAssessmentMeal,
    WeightDailyAssessment,
    WeightDaysRange,
    WeightWeeklyAssessmentLogs
)
from doctor.surrounding import enums as surrounding_enums


def get_initial_weight_assessment_score(bmi, calculation_weight):
    if bmi < 24:
        return 33 * calculation_weight
    elif bmi < 30:
        return 24 * calculation_weight
    elif bmi < 40:
        return 12 * calculation_weight
    else:
        return 2 * calculation_weight


def calculate_bmi(weight, height):
    return round((weight * 100 * 100) / (height * height))


def get_weight_assessment_data(user, bmi):
    initial_assessment_score = get_initial_weight_assessment_score(
        bmi,
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
        "bmi": Decimal(bmi)
    }


def create_weight_daily_assessment_meal(time, daily_assessment, **kwargs):
    return WeightDailyAssessmentMeal.objects.create(
        time=time,
        daily_assessment=daily_assessment,
        status=kwargs.get('status', enums.PENDING)
    )


def complete_weight_daily_assessment(daily_assessment):
    daily_assessment.status = enums.COMPLETE
    daily_assessment.save()
    daily_assessment.user.weight_assessment.score += \
        daily_assessment.user.weight_assessment.calculation_weight
    if daily_assessment.user.weight_assessment.score > 100:
        daily_assessment.user.weight_assessment.score = 100
    daily_assessment.user.weight_assessment.save()
    check_for_badges(daily_assessment)
    set_best_day_streak(daily_assessment)


def create_first_weight_daily_assessment(stage=1, **first_day_range_data):
    weight_first_day_range = WeightDaysRange.objects.first_day_range(
        stage=stage
    ).first()
    if weight_first_day_range:
        return create_daily_assessment(
            WeightDailyAssessment,
            weight_first_day_range,
            **first_day_range_data
        )
    return


def create_next_weight_daily_assessment(weight_assessment_object):
    next_day_days_range = get_next_day_range(
        weight_assessment_object,
        WeightDaysRange
    )
    if next_day_days_range:
        new_weight_assessment_object = create_daily_assessment(
            WeightDailyAssessment,
            next_day_days_range,
            user=weight_assessment_object.user,
            day=weight_assessment_object.day + 1,
            assessment_date=weight_assessment_object.assessment_date + timedelta(days=1)
        )
        new_weight_assessment_object.meal_plan = weight_assessment_object.user.weight_assessment.meal_plan
        new_weight_assessment_object.save()
        create_weight_daily_assessment_meal(
            weight_assessment_object.user.weight_assessment.first_meal_of_day,
            new_weight_assessment_object
        )
        create_surrounding_daily_assessment(
            weight_assessment_object,
            next_day_days_range,
            surrounding_enums.WEIGHT
        )


def check_required_weight_completion(meal_object, weight_daily_assessment):
    next_meal_hour = (meal_object.time.hour + NEXT_MEAL_TIME_DIFFERENCE) % 24
    if weight_daily_assessment.meals.all().count() < \
            weight_daily_assessment.days_range.required_completions and \
            not weight_daily_assessment.meals.filter(
                time__hour=next_meal_hour
            ):
        create_weight_daily_assessment_meal(
            meal_object.time.replace(
                hour=next_meal_hour
            ),
            weight_daily_assessment
        )
    elif weight_daily_assessment.days_range.required_completions == \
            weight_daily_assessment.total_completed:
        complete_weight_daily_assessment(
            weight_daily_assessment
        )
        create_next_weight_daily_assessment(
            weight_daily_assessment
        )


def is_meal_completed_criteria_satisfied(days_range, meal_type):
    if days_range.end_range <= 33 and not meal_type == enums.UNHEALTHY:
        return True
    elif days_range.end_range <= 66 and meal_type in [enums.FIVE_AND_ONE, enums.THREE_AND_THREE, enums.HEALTHY]:
        return True
    return False


def create_weight_weekly_assessment_log(**data):
    return WeightWeeklyAssessmentLogs.objects.create(**data)
