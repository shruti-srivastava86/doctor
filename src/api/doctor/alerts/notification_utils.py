import json

from django.conf import settings
from django.db.models import Q
from scarface.models import (
    Application,
    Platform,
    Device,
    PushMessage
)


"""
    Manage Applications/Platforms
"""


def get_or_setup_apns_application():
    application, created = Application.objects.get_or_create(
        name=settings.SCARFACE_APNS_APPLICATION_NAME
    )
    return application


def get_or_setup_gcm_application():
    application, created = Application.objects.get_or_create(
        name=settings.SCARFACE_GCM_APPLICATION_NAME
    )
    return application


def get_or_setup_apns_platform():
    application = get_or_setup_apns_application()
    apns_platform, created = Platform.objects.get_or_create(
        platform=settings.SCARFACE_APNS_PLATFORM,
        application=application,
        arn=settings.SCARFACE_APNS_ARN
    )
    apns_platform.is_registered_or_register()
    return apns_platform, application


def get_or_setup_gcm_platform():
    application = get_or_setup_gcm_application()
    gcm_platform, created = Platform.objects.get_or_create(
        platform=settings.SCARFACE_GCM_PLATFORM,
        application=application,
        arn=settings.SCARFACE_GCM_ARN
    )
    gcm_platform.is_registered_or_register()
    return gcm_platform, application


"""
    Managing devices
"""


def register_device(user, token, uuid, device_type):
    platform = ''
    unregister_device(user, token, uuid)

    if device_type == "apns":
        platform, application = get_or_setup_apns_platform()
    elif device_type == "gcm":
        platform, application = get_or_setup_gcm_platform()

    if platform:
        device, created = Device.objects.get_or_create(
            device_id=uuid,
            push_token=token,
            platform=platform
        )
        device.is_registered_or_register()
        user.devices.add(device)


def unregister_device(user, token, uuid):
    devices = Device.objects.filter(
        Q(push_token=token) | Q(device_id=uuid)
    )
    for device in devices:
        user.devices.remove(device)
    devices.delete()


def unregister_all_devices_for_user(user):
    devices = user.devices.all()
    for device in devices:
        device.delete()


"""
    Sending Push Messages
"""


def send_message_to_devices(devices, data, badge_count):
    get_or_setup_apns_platform()
    push_message = {
        "title": data.get("text"),
        "body": data.get("message", None)
    }
    message = PushMessage(
        context=json.dumps(data),
        context_id='none',
        has_new_content=True,
        message=push_message,
        sound="default",
        badge_count=badge_count,
    )

    for device in devices:
        device.update()
        device.send(message)
