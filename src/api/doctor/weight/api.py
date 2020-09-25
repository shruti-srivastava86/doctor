from rest_framework.response import Response

from api.generics.generics import (
    RetrieveAPIView,
    DualSerializerUpdateAPIView,
    CustomListAPIView,
    DualSerializerCreateAPIView,
    SuccessResponseSerializer
)
from doctor.badges import enums
from doctor.utils import get_assessment_overview_data
from doctor.weight.models import (
    WeightDailyAssessment,
    WeightWeeklyAssessmentLogs,
    WeightDaysRange
)
from doctor.weight.serializers import (
    WeightAssessmentSerializer,
    WeightAssessmentUpdateSerializer,
    WeightDashboardSerializer,
    WeightDashboardUpdateSerializer,
    WeightWeeklyAssessmentLogsSerializer,
    WeightOverviewSerializer,
    WeightReopenAssessmentSerializer
)


class WeightAssessmentRetrieveUpdateView(RetrieveAPIView, DualSerializerUpdateAPIView):
    """
        View for retrieve and update users Weight assessment
    """
    serializer_class = WeightAssessmentSerializer
    request_serializer_class = WeightAssessmentUpdateSerializer
    response_serializer_class = serializer_class

    def get_object(self):
        return self.request.user.weight_assessment


class WeightDailyAssessmentLogView(RetrieveAPIView, DualSerializerUpdateAPIView):
    """
        View for updating daily assessment for a user
    """
    serializer_class = WeightDashboardSerializer
    request_serializer_class = WeightDashboardUpdateSerializer
    response_serializer_class = serializer_class

    def get_queryset(self):
        return WeightDailyAssessment.objects.for_user(
            self.request.user
        )


class WeightWeeklyAssessmentListView(CustomListAPIView):
    """
        View for updating users weekly bmi assessment
    """
    serializer_class = WeightWeeklyAssessmentLogsSerializer

    def get_queryset(self):
        return WeightWeeklyAssessmentLogs.objects.for_user(
            self.request.user
        )


class WeightWeeklyAssessmentUpdateView(DualSerializerUpdateAPIView):
    """
        View for updating users weekly bmi assessment
    """
    serializer_class = WeightWeeklyAssessmentLogsSerializer
    request_serializer_class = serializer_class
    response_serializer_class = serializer_class

    def get_queryset(self):
        return WeightWeeklyAssessmentLogs.objects.for_user(
            self.request.user
        )


class WeightOverviewView(RetrieveAPIView):
    """
        View for weight overview
    """
    serializer_class = WeightOverviewSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_assessment_overview_data(
            instance,
            enums.WEIGHT,
            instance.weight_daily_assessments.not_reset(),
            WeightDaysRange
        )
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class WeightAssessmentReopen(DualSerializerCreateAPIView):
    """
        View for weight overview
    """
    request_serializer_class = WeightReopenAssessmentSerializer
    response_serializer_class = SuccessResponseSerializer
