from celery.schedules import crontab
from celery.task import periodic_task

from doctor.food_hydration import constants
from doctor import constants as general_constants
from doctor.food_hydration.models import FoodAndHydrationDailyAssessment
from doctor.food_hydration.utils import (
    check_required_food_and_hydration_completion
)


@periodic_task(run_every=(crontab(minute=general_constants.CRON_30_MINUTES)), name=constants.DAILY_FOOD_AND_HYDRATION_ASSESSMENTS)
def task_check_and_create_daily_food_and_hydration_assessment(**kwargs):
    """
        Task to check and create daily food and hydration assessment tasks
        Runs every 30 minutes
    """
    try:
        if not kwargs.get('test'):
            previous_food_and_hydration_assessment_objects = FoodAndHydrationDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day().with_user_midnight_time()
        else:
            previous_food_and_hydration_assessment_objects = FoodAndHydrationDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day()
        for previous_food_and_hydration_assessment_object in previous_food_and_hydration_assessment_objects:
            try:
                check_required_food_and_hydration_completion(
                    previous_food_and_hydration_assessment_object
                )
            except Exception as e:
                print(
                    general_constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.DAILY_FOOD_AND_HYDRATION_ASSESSMENTS,
                        previous_food_and_hydration_assessment_object.user.id,
                        str(e)
                    )
                )
        if not kwargs.get('test'):
            print(
                general_constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.DAILY_FOOD_AND_HYDRATION_ASSESSMENTS
                )
            )
    except Exception as e:
        print(
            general_constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.DAILY_FOOD_AND_HYDRATION_ASSESSMENTS,
                str(e)
            )
        )
