from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from api.generics.generics import CustomSerializer
from api.generics.utils import Utils
from doctor.alerts import enums
from doctor.alerts.models import Alerts
from doctor.alerts.notification_utils import (
    register_device,
    unregister_device
)
from doctor.alerts.utils import create_push
from doctor.video.serializers import VideoSerializer


class DeviceRegistrationSerializer(CustomSerializer):
    token = serializers.CharField(required=True)
    uuid = serializers.CharField(required=True)
    type = serializers.CharField(required=True)

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            register_device(
                user,
                validated_data['token'],
                validated_data['uuid'],
                validated_data['type']
            )
            return Utils.success_response()
        except Exception as e:
            return Utils.error_response(str(e))


class DeviceUnRegistrationSerializer(CustomSerializer):
    token = serializers.CharField(required=True)
    uuid = serializers.CharField(required=False)

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            unregister_device(
                user,
                validated_data['token'],
                validated_data.get('uuid', None)
            )
            return Utils.success_response()
        except Exception as e:
            return Utils.error_response(str(e))


class AlertsViewSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        instance.read = True
        instance.save()
        return instance

    class Meta:
        model = Alerts
        exclude = [
            "user"
        ]


class TestNotificationSerializer(CustomSerializer):
    token = serializers.CharField(required=False)
    type = serializers.IntegerField(required=False)
    macro_type = serializers.IntegerField(required=False)

    def create(self, validated_data):
        if settings.DEBUG is False:
            return Utils.error_response("Test endpoint not allowed on live")
        try:
            user = self.context['request'].user
            data = {
                "type": validated_data.get('type', enums.TODAY),
                "macro_type": validated_data.get('macro_type', enums.WEIGHT),
                "text": "This is a test notification text",
                "message": "This is a test notification message",
                "object_id": validated_data.get('object_id', 0)
            }
            create_push(
                user,
                **data
            )
            return Utils.success_response()
        except Exception as e:
            return Utils.error_response(str(e))


class UnreadAlertsCountViewSerializer(CustomSerializer):
    unread = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.save()
        return {"unread": 0}
