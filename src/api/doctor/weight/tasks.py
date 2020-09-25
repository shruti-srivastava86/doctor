from datetime import timedelta

from celery.schedules import crontab
from celery.task import periodic_task
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from doctor.alerts.utils import (
    create_alert,
    create_push
)
from doctor.user.models import User
from doctor.utils import (
    check_previous_failed_assessment,
    reset_assessment,
    get_reset_first_day_range_date
)
from doctor.weight import enums, constants
from doctor import constants as general_constants
from doctor.alerts import enums as alert_enums
from doctor.weight.models import (
    WeightDailyAssessment,
    WeightDailyAssessmentMeal,
    WeightWeeklyAssessmentLogs
)
from doctor.weight.utils import (
    create_next_weight_daily_assessment,
    check_required_weight_completion,
    create_first_weight_daily_assessment,
    create_weight_daily_assessment_meal
)


@periodic_task(run_every=(crontab(minute=general_constants.CRON_30_MINUTES)), name=constants.DAILY_WEIGHT_ASSESSMENTS)
def task_check_and_create_daily_weight_assessment(**kwargs):
    """
        Task to check and create daily weight assessment tasks
        Runs every 30 minutes
    """
    try:
        if not kwargs.get('test'):
            previous_weight_assessment_objects = WeightDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day().with_user_midnight_time()
        else:
            previous_weight_assessment_objects = WeightDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day()
        for previous_weight_assessment_object in previous_weight_assessment_objects:
            try:
                with transaction.atomic():
                    reset = check_previous_failed_assessment(
                        previous_weight_assessment_object
                    )
                    if reset:
                        reset_assessment(
                            previous_weight_assessment_object.user.weight_assessment,
                            WeightDailyAssessment.objects.for_user(
                                previous_weight_assessment_object.user
                            )
                        )
                        first_day_range_data = get_reset_first_day_range_date(
                            previous_weight_assessment_object.user
                        )
                        first_day_weight_daily_assessment = create_first_weight_daily_assessment(
                            stage=previous_weight_assessment_object.days_range.stage,
                            **first_day_range_data
                        )
                        if first_day_weight_daily_assessment:
                            first_day_weight_daily_assessment.meal_plan = \
                                previous_weight_assessment_object.user.weight_assessment.meal_plan
                            first_day_weight_daily_assessment.save()
                            create_weight_daily_assessment_meal(
                                previous_weight_assessment_object.user.weight_assessment.first_meal_of_day,
                                first_day_weight_daily_assessment,
                                status=enums.PENDING
                            )
                    else:
                        previous_weight_assessment_object.status = enums.INCOMPLETE
                        previous_weight_assessment_object.save()
                        create_next_weight_daily_assessment(
                            previous_weight_assessment_object
                        )
            except Exception as e:
                print(
                    general_constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.DAILY_WEIGHT_ASSESSMENTS,
                        previous_weight_assessment_object.user.id,
                        str(e)
                    )
                )
        if not kwargs.get('test'):
            print(
                general_constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.DAILY_WEIGHT_ASSESSMENTS
                )
            )
    except Exception as e:
        print(
            general_constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.DAILY_WEIGHT_ASSESSMENTS,
                str(e)
            )
        )


@periodic_task(run_every=(crontab()), name=constants.PENDING_MEAL_PROGRESS)
def task_change_pending_to_progress_weight_assessment_meal(**kwargs):
    """
        Task to change daily weight assessment meals from pending to progress
        Runs every minute
    """
    try:
        if not kwargs.get('test'):
            weight_daily_assessment_meals = WeightDailyAssessmentMeal.objects.in_pending().\
                with_user_current_date_time().for_today().before_time()
        else:
            weight_daily_assessment_meals = WeightDailyAssessmentMeal.objects.in_pending(). \
                with_user_current_date_time().before_time()
        for weight_daily_assessment_meal in weight_daily_assessment_meals:
            try:
                with transaction.atomic():
                    check_required_weight_completion(
                        weight_daily_assessment_meal,
                        weight_daily_assessment_meal.daily_assessment
                    )
                    weight_daily_assessment_meal.status = enums.IN_PROGRESS
                    weight_daily_assessment_meal.save()
            except Exception as e:
                print(
                    general_constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.PENDING_MEAL_PROGRESS,
                        weight_daily_assessment_meal.daily_assessment.user.id,
                        str(e)
                    )
                )
        if not kwargs.get('test'):
            print(
                general_constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.PENDING_MEAL_PROGRESS
                )
            )
    except Exception as e:
        print(
            general_constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.PENDING_MEAL_PROGRESS,
                str(e)
            )
        )


@periodic_task(run_every=(crontab()), name=constants.UPCOMING_MEAL)
def task_send_upcoming_meal_notification(**kwargs):
    """
        Task to send a reminder notification to user for an upcoming meal
        Runs every minute
    """
    try:
        weight_daily_assessment_upcoming_meals = WeightDailyAssessmentMeal.objects.in_pending().\
            with_user_current_date_time().for_today().upcoming_meal()
        data = {
            "type": alert_enums.REMINDER,
            "macro_type": alert_enums.WEIGHT,
            "text": constants.UPCOMING_MEAL_NOTIFICATION_TEXT
        }
        for weight_daily_assessment_upcoming_meal in weight_daily_assessment_upcoming_meals:
            try:
                data["message"] = constants.UPCOMING_MEAL_NOTIFICATION_MESSAGE.format(
                    weight_daily_assessment_upcoming_meal.time.strftime("%H:%M")
                )
                create_alert(
                    weight_daily_assessment_upcoming_meal.daily_assessment.user,
                    weight_daily_assessment_upcoming_meal.daily_assessment,
                    **data
                )
                if weight_daily_assessment_upcoming_meal.daily_assessment.user.notification_settings.meal:
                    data[
                        "object_id"
                    ] = weight_daily_assessment_upcoming_meal.daily_assessment.id
                    create_push(
                        weight_daily_assessment_upcoming_meal.daily_assessment.user,
                        **data
                    )
            except Exception as e:
                print(
                    general_constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.UPCOMING_MEAL,
                        weight_daily_assessment_upcoming_meal.daily_assessment.user.id,
                        str(e)
                    )
                )
        if not kwargs.get('test'):
            print(
                general_constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.UPCOMING_MEAL
                )
            )
    except Exception as e:
        print(
            general_constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.UPCOMING_MEAL,
                str(e)
            )
        )


@periodic_task(run_every=(crontab(minute=general_constants.CRON_30_MINUTES)), name=constants.WEEKLY_WEIGHT_ASSESSMENT)
def task_send_weekly_weight_assessment_notification(**kwargs):
    """
        Task to set a reminder for weekly assessment
        Runs every 30 minutes
    """
    try:
        users = User.filter.with_user_local_date_time().with_weekday().filter(
            local_time__time__hour=general_constants.WEEKLY_REMINDER_TIME_HOUR,
            local_time__time__minute=general_constants.WEEKLY_REMINDER_TIME_MINUTE,
        ).filter(
            created_at__week_day=F('weekday'),
            created_at__lt=timezone.now() - timedelta(days=1)
        )
        data = {
            "type": alert_enums.WEEKLY_WEIGHT_CHECKUP,
            "macro_type": alert_enums.WEIGHT,
            "text": constants.WEEKLY_CHECK_UP_NOTIFICATION_TEXT,
            "message": constants.WEEKLY_CHECK_UP_NOTIFICATION_MESSAGE
        }
        for user in users:
            try:
                weight_assessment_log = WeightWeeklyAssessmentLogs.objects.create(
                    user=user
                )
                create_alert(
                    user,
                    weight_assessment_log,
                    **data
                )
                if user.notification_settings.weekly_checkup:
                    data[
                        "object_id"
                    ] = weight_assessment_log.id
                    create_push(
                        user,
                        **data
                    )
            except Exception as e:
                print(
                    general_constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.WEEKLY_WEIGHT_ASSESSMENT,
                        user.id,
                        str(e)
                    )
                )
        if not kwargs.get('test'):
            print(
                general_constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.WEEKLY_WEIGHT_ASSESSMENT
                )
            )
    except Exception as e:
        print(
            general_constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.WEEKLY_WEIGHT_ASSESSMENT,
                str(e)
            )
        )
