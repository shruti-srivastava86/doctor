from doctor import constants
from doctor.alerts import enums
from doctor.alerts.models import Alerts
from doctor.alerts.notification_utils import send_message_to_devices


def create_alert(user, content_object, **data):
    Alerts.objects.create(
        user=user,
        content_object=content_object,
        **data
    )


def create_failed_assessment_alert(user, content_object, assessment_category, assessment_type, video):
    data = {
        "type": enums.FAILED,
        "text": constants.INCOMPLETE_ASSESSMENT_NOTIFICATION_TEXT,
        "message": constants.INCOMPLETE_ASSESSMENT_NOTIFICATION_MESSAGE.format(
            assessment_category
        ),
        "macro_type": assessment_type,
        "video": video
    }
    create_alert(user, content_object, **data)


def create_failed_assessment_day_alert(user, content_object, assessment_category, assessment_type, day, video):
    data = {
        "type": enums.FAILED,
        "text": constants.INCOMPLETE_ASSESSMENT_DAY_NOTIFICATION_TEXT.format(day),
        "message": constants.INCOMPLETE_ASSESSMENT_DAY_NOTIFICATION_MESSAGE.format(
            assessment_category,
            day
        ),
        "macro_type": assessment_type,
        "video": video
    }
    create_alert(user, content_object, **data)


def create_push(user, **data):
    send_message_to_devices(
        user.devices.all(),
        data,
        user.alerts.unread_count()
    )
