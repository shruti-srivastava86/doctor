from celery.schedules import crontab
from celery.task import periodic_task

from doctor.motion import constants
from doctor import constants as general_constants
from doctor.motion.models import MotionDailyAssessment
from doctor.motion.utils import check_required_motion_completion


@periodic_task(run_every=(crontab(general_constants.CRON_30_MINUTES)), name=constants.DAILY_MOTION_ASSESSMENTS)
def task_check_and_create_daily_motion_assessment(**kwargs):
    """
        Task to check and create daily motion assessment tasks
        Runs every 30 minutes
    """
    try:
        if not kwargs.get('test'):
            previous_motion_assessment_objects = MotionDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day().with_user_midnight_time()
        else:
            previous_motion_assessment_objects = MotionDailyAssessment.objects.in_progress().\
                with_user_current_date_time().for_previous_day()
        for previous_motion_assessment_object in previous_motion_assessment_objects:
            try:
                check_required_motion_completion(
                    previous_motion_assessment_object
                )
            except Exception as e:
                print(
                    general_constants.FAILED_NOTIFICATION_USER_MESSAGE.format(
                        constants.DAILY_MOTION_ASSESSMENTS,
                        previous_motion_assessment_object.user.id,
                        str(e)
                    )
                )
        if not kwargs.get('test'):
            print(
                general_constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                    constants.DAILY_MOTION_ASSESSMENTS,
                )
            )
    except Exception as e:
        print(
            general_constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.DAILY_MOTION_ASSESSMENTS,
                str(e)
            )
        )
