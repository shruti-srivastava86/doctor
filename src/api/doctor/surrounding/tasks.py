from datetime import timedelta

from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import F

from doctor import constants as general_constants, enums
from doctor.surrounding import constants
from doctor.surrounding.models import SurroundingDailyAssessment


@periodic_task(run_every=(crontab(minute=general_constants.CRON_30_MINUTES)), name=constants.REMIND_ME_SURROUNDING_ASSESSMENTS)
def check_and_change_remind_me_daily_surrounding_assessment(**kwargs):
    """
        Task to check and create daily weight assessment tasks
        Runs every 30 minutes
    """
    try:
        if not kwargs.get('test'):
            SurroundingDailyAssessment.objects.remind_me_later().\
                with_user_current_date_time().for_previous_day().with_user_midnight_time().update(
                status=enums.IN_PROGRESS
            )
        else:
            SurroundingDailyAssessment.objects.remind_me_later().\
                with_user_current_date_time().for_previous_day().update(
                status=enums.IN_PROGRESS
            )
        if not kwargs.get('test'):
            print(
                general_constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.REMIND_ME_SURROUNDING_ASSESSMENTS
                )
            )
    except Exception as e:
        print(
            general_constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.REMIND_ME_SURROUNDING_ASSESSMENTS,
                str(e)
            )
        )


@periodic_task(run_every=(crontab(minute=general_constants.CRON_30_MINUTES)), name=constants.IN_PROGRESS_SURROUNDING_ASSESSMENT)
def check_and_change_in_progress_daily_surrounding_assessment(**kwargs):
    """
        Task to check and create daily weight assessment tasks
        Runs every 30 minutes
    """
    try:
        if not kwargs.get('test'):
            SurroundingDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day().with_user_midnight_time().update(
                assessment_date=F('assessment_date') + timedelta(days=7)
            )
        else:
            SurroundingDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day().update(
                assessment_date=F('assessment_date') + timedelta(days=7)
            )
        if not kwargs.get('test'):
            print(
                general_constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.IN_PROGRESS_SURROUNDING_ASSESSMENT
                )
            )
    except Exception as e:
        print(
            general_constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.IN_PROGRESS_SURROUNDING_ASSESSMENT,
                str(e)
            )
        )
