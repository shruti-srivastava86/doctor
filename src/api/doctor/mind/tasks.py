from celery.schedules import crontab
from celery.task import periodic_task
from django.db import transaction

from doctor import constants as general_constants
from doctor.mind import constants
from doctor.mind.models import MindDailyAssessment
from doctor.mind.utils import check_mind_completion


@periodic_task(run_every=(crontab(general_constants.CRON_30_MINUTES)), name=constants.DAILY_MIND_ASSESSMENTS)
def task_check_and_create_daily_sleep_assessment(**kwargs):
    """
        Task to check and create daily sleep assessment tasks
        Runs every 30 minutes
    """
    try:
        if not kwargs.get('test'):
            previous_mind_assessment_objects = MindDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day().with_user_midnight_time()
        else:
            previous_mind_assessment_objects = MindDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day()
        for previous_mind_assessment_object in previous_mind_assessment_objects:
            try:
                with transaction.atomic():
                    check_mind_completion(
                        previous_mind_assessment_object,
                    )
            except Exception as e:
                print(
                    general_constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.DAILY_MIND_ASSESSMENTS,
                        previous_mind_assessment_object.user.id,
                        str(e)
                    )
                )
        if not kwargs.get('test'):
            print(
                general_constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.DAILY_MIND_ASSESSMENTS
                )
            )
    except Exception as e:
        print(
            general_constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.DAILY_MIND_ASSESSMENTS,
                str(e)
            )
        )
