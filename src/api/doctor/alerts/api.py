from rest_framework.response import Response

from api.generics.generics import (
    DualSerializerCreateAPIView,
    SuccessResponseSerializer,
    CustomListAPIView,
    CustomRetrieveUpdateAPIView
)
from doctor.alerts.serializers import (
    DeviceRegistrationSerializer,
    DeviceUnRegistrationSerializer,
    AlertsViewSerializer,
    TestNotificationSerializer,
    UnreadAlertsCountViewSerializer
)
from doctor.user.models import GeneralSettings


class DeviceRegister(DualSerializerCreateAPIView):
    """
        View for registering device token
    """
    request_serializer_class = DeviceRegistrationSerializer
    response_serializer_class = SuccessResponseSerializer


class DeviceUnregister(DeviceRegister):
    """
        View for un registering device token
    """
    request_serializer_class = DeviceUnRegistrationSerializer


class TestNotification(DualSerializerCreateAPIView):
    """
        View to send a test notification to user devices
    """
    request_serializer_class = TestNotificationSerializer
    response_serializer_class = SuccessResponseSerializer


class AlertsView(CustomListAPIView):
    """
        View for listing all user alerts
    """
    serializer_class = AlertsViewSerializer

    def get_queryset(self):
        return self.request.user.alerts.all()


class AlertUpdateView(CustomRetrieveUpdateAPIView):
    """
        View for making an alert as read
    """
    serializer_class = AlertsViewSerializer

    def get_queryset(self):
        return self.request.user.alerts.all()


class NewAlertsCountView(CustomRetrieveUpdateAPIView):
    """
        View for fetching and updating unread alerts count
    """
    serializer_class = UnreadAlertsCountViewSerializer

    def get_object(self):
        return self.request.user.general_settings

    def retrieve(self, request, *args, **kwargs):
        if hasattr(self.request.user, 'general_settings'):
            new_alerts_count = self.request.user.alerts.filter(
                created_at__gt=self.request.user.general_settings.alert_last_checked
            ).count()
        else:
            GeneralSettings.objects.create(
                user=self.request.user
            )
            new_alerts_count = 0
        serializer = self.get_serializer(
            {
                "unread": new_alerts_count
            }
        )
        return Response(serializer.data)
