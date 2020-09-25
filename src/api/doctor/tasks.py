from api.celery import app
from doctor import constants
from doctor.alerts import enums
from doctor.alerts.utils import create_alert
from doctor.utils import get_assessment_by_type


@app.task
def task_send_assessment_installed_alert(assessment_id, assessment_type, **kwargs):
    """
        Task to send a push notification for installing a assessment
    """
    try:
        assessment = get_assessment_by_type(
            assessment_type
        ).objects.with_id(
            assessment_id
        ).first()
        if assessment:
            data = {
                "type": enums.COMPLETED,
                "macro_type": assessment_type,
                "text": constants.HABIT_NOTIFICATION_TEXT[assessment_type]["text"],
                "message": constants.HABIT_NOTIFICATION_TEXT[assessment_type]["message"]
            }
            create_alert(
                assessment.user,
                assessment,
                **data
            )
        print(
            constants.SUCCESS_NOTIFICATION_MESSAGE.format(
                constants.HABIT_INSTALLING_TASK
            )
        )
    except Exception as e:
        print(
            constants.FAILED_NOTIFICATION_MESSAGE.format(
                constants.HABIT_INSTALLING_TASK,
                str(e)
            )
        )
