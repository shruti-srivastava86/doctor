from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import F, Q
from django.utils import timezone

from doctor import constants, enums
from doctor.alerts.models import Alerts
from doctor.alerts.utils import create_alert, create_push
from doctor.user.models import User
from doctor.alerts import enums as alert_enums
from doctor.utils import get_category_by_assessment


@periodic_task(run_every=crontab(minute=constants.CRON_30_MINUTES), name=constants.TASKS_CHECK)
def task_send_check_tasks_for_the_day_notification(**kwargs):
    """
        Task to set a reminder to users to check their tasks for the day
        Runs every 30 minutes
    """
    try:
        users = User.filter.with_user_local_date_time().filter(
            local_time__time__hour=constants.TASK_CHECK_REMINDER_TIME_HOUR,
            local_time__time__minute=constants.TASK_CHECK_REMINDER_TIME_MINUTE,
            notification_settings__good_morning=True
        )
        data = {
            "type": alert_enums.TODAY,
            "text": constants.CHECK_TASK_NOTIFICATION_TEXT,
            "message": constants.CHECK_TASK_NOTIFICATION_MESSAGE
        }
        for user in users:
            try:
                data[
                    "object_id"
                ] = user.id
                create_push(
                    user,
                    **data
                )
            except Exception as e:
                print(
                    constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.TASKS_CHECK,
                        user.id,
                        str(e)
                    )
                )
        if not kwargs.get('test'):
            print(
                constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.TASKS_CHECK
                )
            )
    except Exception as e:
        print(
            constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.TASKS_CHECK,
                str(e)
            )
        )


@periodic_task(run_every=crontab(minute=constants.CRON_30_MINUTES), name=constants.INCOMPLETE_TASKS_CHECK)
def task_send_incomplete_check_tasks_for_the_day_notification(**kwargs):
    """
        Task to set a reminder to users to update their tasks for the day
        Runs every 30 minutes
    """
    try:
        users = User.filter.with_user_local_date_time().filter(
            local_time__time__hour=constants.INCOMPLETE_TASK_CHECK_REMINDER_TIME_HOUR,
            local_time__time__minute=constants.INCOMPLETE_TASK_CHECK_REMINDER_TIME_MINUTE,
        ).filter(
            Q(
                food_and_hydration_daily_assessments__assessment_date=F('local_date'),
                food_and_hydration_daily_assessments__status=enums.IN_PROGRESS,
                food_and_hydration_daily_assessments__total_completed__lt=F(
                    'food_and_hydration_daily_assessments__days_range__required_completions'
                )
            ) |
            Q(
                mind_daily_assessments__assessment_date=F('local_date'),
                mind_daily_assessments__status=enums.IN_PROGRESS,
                mind_daily_assessments__total_completed__lt=F(
                    'mind_daily_assessments__days_range__required_completions'
                )
            ) |
            Q(
                motion_daily_assessments__assessment_date=F('local_date'),
                motion_daily_assessments__status=enums.IN_PROGRESS,
                motion_daily_assessments__total_completed__lt=F(
                    'motion_daily_assessments__days_range__required_completions'
                )
            ) |
            Q(
                sleep_daily_assessments__assessment_date=F('local_date'),
                sleep_daily_assessments__status=enums.IN_PROGRESS,
                sleep_daily_assessments__total_completed__lt=F(
                    'sleep_daily_assessments__days_range__required_completions'
                )
            ) |
            Q(
                surrounding_daily_assessments__assessment_date=F('local_date'),
                surrounding_daily_assessments__status=enums.IN_PROGRESS,
                surrounding_daily_assessments__total_completed__lt=F(
                    'surrounding_daily_assessments__days_range__required_completions'
                )
            )
        ).distinct()
        data = {
            "type": alert_enums.TODAY,
            "text": constants.INCOMPLETE_CHECK_TASK_NOTIFICATION_TEXT,
            "message": constants.INCOMPLETE_CHECK_TASK_NOTIFICATION_MESSAGE
        }
        for user in users:
            try:
                create_alert(
                    user,
                    user,
                    **data
                )
                if user.notification_settings.incomplete_day:
                    data[
                        "object_id"
                    ] = user.id
                    create_push(
                        user,
                        **data
                    )
            except Exception as e:
                print(
                    constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.INCOMPLETE_TASKS_CHECK,
                        user.id,
                        str(e)
                    )
                )
        if not kwargs.get('test'):
            print(
                constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.INCOMPLETE_TASKS_CHECK
                )
            )
    except Exception as e:
        print(
            constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.INCOMPLETE_TASKS_CHECK,
                str(e)
            )
        )


@periodic_task(run_every=crontab(minute=constants.CRON_30_MINUTES), name=constants.WEEKLY_ASSESSMENT_TASK)
def task_send_weekly_reassessment_alert(**kwargs):
    try:
        alerts = Alerts.objects.with_user_current_date_time().previous_weeks_completed().\
            with_user_midnight_time().type_completed()
        for alert in alerts:
            try:
                data = {
                    "macro_type": alert.macro_type
                }
                data[
                    "type"
                ] = int(
                    (
                        (timezone.now() - alert.created_at).days / 7
                    ) + alert_enums.ONE_WEEK_CHECKUP
                )
                data[
                    "text"
                ] = constants.WEEKLY_REASSESSMENT_ALERT_TEXT.format(
                    int(
                        (
                            timezone.now() - alert.created_at
                        ).days / 7
                    ) + 1
                )
                data[
                    "message"
                ] = constants.WEEKLY_REASSESSMENT_ALERT_MESSAGE.format(
                    get_category_by_assessment(
                        alert.macro_type
                    )
                ) if not alert.macro_type == alert_enums.MIND else constants.WEEKLY_REASSESSMENT_ALERT_MIND_MESSAGE
                create_alert(
                    alert.user,
                    None,
                    **data
                )
            except Exception as e:
                print(
                    constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.WEEKLY_ASSESSMENT_TASK,
                        alert.user.id,
                        str(e)
                    )
                )
        print(
            constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                constants.WEEKLY_ASSESSMENT_TASK
            )
        )
    except Exception as e:
        print(
            constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.WEEKLY_ASSESSMENT_TASK,
                str(e)
            )
        )


@periodic_task(run_every=crontab(minute=constants.CRON_30_MINUTES), name=constants.MONTHLY_ASSESSMENT_TASK)
def task_send_monthly_reassessment_alert(**kwargs):
    try:
        alerts = Alerts.objects.with_user_current_date_time().previous_month_completed().\
            with_user_midnight_time().type_completed()
        for alert in alerts:
            try:
                data = {
                    "macro_type": alert.macro_type
                }
                data[
                    "type"
                ] = int(
                    (
                        (timezone.now() - alert.created_at).days / 7 / 4
                    ) + alert_enums.ONE_MONTH_CHECKUP
                )
                data[
                    "text"
                ] = constants.MONTHLY_REASSESSMENT_ALERT_TEXT.format(
                    int(
                        (
                            timezone.now() - alert.created_at
                        ).days / 7 / 4
                    ) + 1
                )
                data[
                    "message"
                ] = constants.MONTHLY_REASSESSMENT_ALERT_MESSAGE.format(
                    get_category_by_assessment(
                        alert.macro_type
                    )
                ) if not alert.macro_type == alert_enums.MIND else constants.MONTHLY_REASSESSMENT_ALERT_MIND_MESSAGE
                create_alert(
                    alert.user,
                    None,
                    **data
                )
            except Exception as e:
                print(
                    constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.MONTHLY_ASSESSMENT_TASK,
                        alert.user.id,
                        str(e)
                    )
                )
        print(
            constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                constants.MONTHLY_ASSESSMENT_TASK
            )
        )
    except Exception as e:
        print(
            constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.MONTHLY_ASSESSMENT_TASK,
                str(e)
            )
        )
