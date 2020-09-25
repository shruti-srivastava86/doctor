from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from api.generics.generics import (
    DualSerializerUpdateAPIView,
    DualSerializerCreateAPIView,
    SuccessResponseSerializer
)
from doctor.badges import enums
from doctor.mind.models import MindDailyAssessment, MindDaysRange
from doctor.mind.serializers import (
    MindAssessmentSerializer,
    MindDashboardSerializer,
    MindOverviewSerializer,
    MindReopenAssessmentSerializer
)
from doctor.utils import get_assessment_overview_data


class MindAssessmentRetrieveView(RetrieveAPIView):
    """
        View for retrieve users Mind assessment
    """
    serializer_class = MindAssessmentSerializer

    def get_object(self):
        return self.request.user.mind_assessment


class MindDailyAssessmentLogView(RetrieveAPIView, DualSerializerUpdateAPIView):
    """
        View for updating daily mind assessment for a user
    """
    serializer_class = MindDashboardSerializer
    request_serializer_class = serializer_class
    response_serializer_class = serializer_class

    def get_queryset(self):
        return MindDailyAssessment.objects.for_user(
            self.request.user,
        )


class MindOverviewView(RetrieveAPIView):
    """
        View for mind overview
    """
    serializer_class = MindOverviewSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_assessment_overview_data(
            instance,
            enums.MIND,
            instance.mind_daily_assessments.not_reset(),
            MindDaysRange
        )
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class MindAssessmentReopen(DualSerializerCreateAPIView):
    """
        View for mind assessment reopen
    """
    request_serializer_class = MindReopenAssessmentSerializer
    response_serializer_class = SuccessResponseSerializer
