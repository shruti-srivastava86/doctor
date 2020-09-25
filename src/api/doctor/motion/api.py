from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from api.generics.generics import (
    DualSerializerUpdateAPIView,
    DualSerializerCreateAPIView,
    SuccessResponseSerializer
)
from doctor.badges import enums
from doctor.motion.models import (
    MotionDailyAssessment,
    MotionDaysRange
)
from doctor.motion.serializers import (
    MotionAssessmentSerializer,
    MotionDashboardSerializer,
    MotionOverviewSerializer,
    MotionReopenAssessmentSerializer
)
from doctor.utils import get_assessment_overview_data


class MotionAssessmentRetrieveView(RetrieveAPIView):
    """
        View for retrieve and update users motion assessment
    """
    serializer_class = MotionAssessmentSerializer

    def get_object(self):
        return self.request.user.motion_assessment


class MotionDailyAssessmentLogView(RetrieveAPIView, DualSerializerUpdateAPIView):
    """
        View for updating daily motion assessment for a user
    """
    serializer_class = MotionDashboardSerializer
    request_serializer_class = serializer_class
    response_serializer_class = serializer_class

    def get_queryset(self):
        return MotionDailyAssessment.objects.for_user(
            self.request.user,
        )


class MotionOverviewView(RetrieveAPIView):
    """
        View for motion overview
    """
    serializer_class = MotionOverviewSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_assessment_overview_data(
            instance,
            enums.MOTION,
            instance.motion_daily_assessments.not_reset(),
            MotionDaysRange
        )
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class MotionAssessmentReopen(DualSerializerCreateAPIView):
    """
        View for motion assessment reopen
    """
    request_serializer_class = MotionReopenAssessmentSerializer
    response_serializer_class = SuccessResponseSerializer
