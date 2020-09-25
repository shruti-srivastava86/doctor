from rest_framework.response import Response

from api.generics.generics import (
    RetrieveAPIView,
    DualSerializerUpdateAPIView,
    DualSerializerCreateAPIView,
    SuccessResponseSerializer
)
from doctor.badges import enums
from doctor.sleep.models import (
    SleepDailyAssessment,
    SleepDaysRange
)
from doctor.sleep.serializers import (
    SleepAssessmentSerializer,
    SleepDashboardSerializer,
    SleepOverviewSerializer,
    SleepReopenAssessmentSerializer
)
from doctor.utils import get_assessment_overview_data


class SleepAssessmentRetrieveUpdateView(RetrieveAPIView):
    """
        View for retrieve and update users Weight assessment
    """
    serializer_class = SleepAssessmentSerializer

    def get_object(self):
        return self.request.user.sleep_assessment


class SleepDailyAssessmentLogView(RetrieveAPIView, DualSerializerUpdateAPIView):
    """
        View for updating daily assessment for a user
    """
    serializer_class = SleepDashboardSerializer
    request_serializer_class = serializer_class
    response_serializer_class = serializer_class

    def get_queryset(self):
        return SleepDailyAssessment.objects.for_user(
            self.request.user
        )


class SleepOverviewView(RetrieveAPIView):
    """
        View for sleep overview
    """
    serializer_class = SleepOverviewSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_assessment_overview_data(
            instance,
            enums.SLEEP,
            instance.sleep_daily_assessments.not_reset(),
            SleepDaysRange
        )
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class SleepAssessmentReopen(DualSerializerCreateAPIView):
    """
        View for sleep assessment reopen
    """
    request_serializer_class = SleepReopenAssessmentSerializer
    response_serializer_class = SuccessResponseSerializer
