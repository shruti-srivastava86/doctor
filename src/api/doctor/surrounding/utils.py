from django.utils import timezone
from datetime import timedelta

from doctor import enums
from doctor.badges.utils import check_for_badges
from doctor.surrounding.models import (
    SurroundingDaysRange,
    SurroundingDailyAssessment
)
from doctor.utils import get_calculation_surrounding_weight, create_daily_assessment


def get_surroundings_assessment_data(user):
    calculation_weight = get_calculation_surrounding_weight()
    return {
        "user": user,
        "calculation_weight": calculation_weight,
        "initial_score": 0,
        "score": 0
    }


def check_surrounding_days_range(assessment_type, day, stage):
    return SurroundingDaysRange.objects.for_assessment(
        assessment_type
    ).for_day(
        day
    ).for_stage(
        stage
    )


def complete_surrounding_daily_assessment(daily_assessment):
    daily_assessment.time_logs = [timezone.now().time()]
    daily_assessment.user.surrounding_assessment.score += \
        daily_assessment.user.surrounding_assessment.calculation_weight
    if daily_assessment.user.surrounding_assessment.score > 100:
        daily_assessment.user.surrounding_assessment.score = 100
    daily_assessment.user.surrounding_assessment.save()
    if daily_assessment.user.surrounding_assessment.score == 100:
        check_for_badges(daily_assessment)


def create_first_surrounding_daily_assessment(stage=1, **first_day_range_data):
    surrounding_first_day_range = SurroundingDaysRange.objects.first_day_range(
        stage=stage
    ).first()
    if surrounding_first_day_range:
        SurroundingDailyAssessment.objects.create(
            days_range=surrounding_first_day_range,
            **first_day_range_data
        )


def get_assessment_overview_data(user, assessment_type, daily_assessments, days_range):
    challenges = list()
    if assessment_type in user.earned_assessment_badges():
        data = {
            "status": enums.COMPLETE
        }
    else:
        data = {
            "status": enums.IN_PROGRESS
        }
        current_assessments = daily_assessments.today_assessment().order_by('assessment_date')
        if current_assessments:
            for current_assessment in current_assessments:
                challenges.append(
                    current_assessment.days_range.challenge
                )
    data[
        "challenges"
    ] = challenges
    data[
        "completed_tasks"
    ] = daily_assessments.complete().values_list('days_range__challenge', flat=True)
    return data


def create_surrounding_daily_assessment(assessment, next_days_range, type):
    if not assessment.user.surrounding_daily_assessments.for_stage(
        next_days_range.stage,
    ).for_day(
        assessment.day + 1
    ).for_assessment(
        type
    ):
        surrounding_days_range_objects = check_surrounding_days_range(
            type,
            assessment.day + 1,
            next_days_range.stage
        )
        for surrounding_days_range_obj in surrounding_days_range_objects:
            create_daily_assessment(
                SurroundingDailyAssessment,
                surrounding_days_range_obj,
                user=assessment.user,
                day=assessment.day + 1,
                assessment_date=assessment.assessment_date + timedelta(days=1)
            )
