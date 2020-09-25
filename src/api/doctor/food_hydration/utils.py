from datetime import timedelta

from django.utils import timezone

from doctor import enums
from doctor.badges.utils import check_for_badges
from doctor.food_hydration.models import (
    FoodAndHydrationDailyAssessment,
    FoodAndHydrationDaysRange
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


def get_initial_food_and_hydration_assessment_score(glasses_of_water_per_day, calculation_weight):
    if glasses_of_water_per_day == 0:
        return 1 * calculation_weight
    elif glasses_of_water_per_day < 4:
        return 9 * calculation_weight
    elif glasses_of_water_per_day < 6:
        return 17 * calculation_weight
    elif glasses_of_water_per_day < 8:
        return 25 * calculation_weight
    else:
        return 33 * calculation_weight


def get_food_and_hydration_assessment_data(user, glasses_of_water_per_day):
    initial_assessment_score = get_initial_food_and_hydration_assessment_score(
        glasses_of_water_per_day,
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
        "glasses_of_water_per_day": glasses_of_water_per_day
    }


def complete_food_and_hydration_daily_assessment(daily_assessment):
    daily_assessment.status = enums.COMPLETE
    daily_assessment.time_logs = [timezone.now().time()]
    daily_assessment.save()
    daily_assessment.user.food_and_hydration_assessment.score += \
        daily_assessment.user.food_and_hydration_assessment.calculation_weight
    if daily_assessment.user.food_and_hydration_assessment.score > 100:
        daily_assessment.user.food_and_hydration_assessment.score = 100
    daily_assessment.user.food_and_hydration_assessment.save()
    check_for_badges(daily_assessment)
    set_best_day_streak(daily_assessment)


def create_first_food_and_hydration_daily_assessment(stage=1, **first_day_range_data):
    food_and_hydration_first_day_range = FoodAndHydrationDaysRange.objects.first_day_range(
        stage=stage
    ).first()
    if food_and_hydration_first_day_range:
        create_daily_assessment(
            FoodAndHydrationDailyAssessment,
            food_and_hydration_first_day_range,
            **first_day_range_data
        )


def create_next_food_and_hydration_daily_assessment(food_and_hydration_daily_assessment):
    next_day_days_range = get_next_day_range(
        food_and_hydration_daily_assessment,
        FoodAndHydrationDaysRange
    )
    if next_day_days_range:
        create_daily_assessment(
            FoodAndHydrationDailyAssessment,
            next_day_days_range,
            user=food_and_hydration_daily_assessment.user,
            day=food_and_hydration_daily_assessment.day + 1,
            assessment_date=food_and_hydration_daily_assessment.assessment_date + timedelta(days=1)
        )
        create_surrounding_daily_assessment(
            food_and_hydration_daily_assessment,
            next_day_days_range,
            surrounding_enums.FOOD_AND_HYDRATION
        )


def check_required_food_and_hydration_completion(food_and_hydration_daily_assessment):
    if food_and_hydration_daily_assessment.days_range.required_completions <= \
            food_and_hydration_daily_assessment.total_completed:
        complete_food_and_hydration_daily_assessment(
            food_and_hydration_daily_assessment
        )
        create_next_food_and_hydration_daily_assessment(
            food_and_hydration_daily_assessment
        )
    else:
        reset = check_previous_failed_assessment(
            food_and_hydration_daily_assessment
        )
        if reset:
            food_and_hydration_daily_assessment.status = enums.RESET
            reset_assessment(
                food_and_hydration_daily_assessment.user.food_and_hydration_assessment,
                FoodAndHydrationDailyAssessment.objects.for_user(
                    food_and_hydration_daily_assessment.user
                )
            )
            first_day_range_data = get_reset_first_day_range_date(
                food_and_hydration_daily_assessment.user
            )
            create_first_food_and_hydration_daily_assessment(
                stage=food_and_hydration_daily_assessment.days_range.stage,
                ** first_day_range_data
            )
        else:
            food_and_hydration_daily_assessment.status = enums.INCOMPLETE
            create_next_food_and_hydration_daily_assessment(
                food_and_hydration_daily_assessment
            )
        food_and_hydration_daily_assessment.save()
