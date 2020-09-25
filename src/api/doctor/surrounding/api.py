from rest_framework.response import Response

from api.generics.generics import (
    RetrieveAPIView,
    DualSerializerUpdateAPIView
)
from doctor.badges import enums
from doctor.surrounding.models import SurroundingDailyAssessment, SurroundingDaysRange
from doctor.surrounding.serializers import (
    SurroundingAssessmentSerializer,
    SurroundingDashboardSerializer,
    SurroundingOverviewSerializer
)
from doctor.surrounding.utils import get_assessment_overview_data


class SurroundingRetrieveUpdateView(RetrieveAPIView):
    """
        View for retrieve and update users Weight assessment
    """
    serializer_class = SurroundingAssessmentSerializer

    def get_object(self):
        return self.request.user.surrounding_assessment


class SurroundingDailyAssessmentLogView(DualSerializerUpdateAPIView, RetrieveAPIView):
    """
        View for updating daily assessment for a user
    """
    serializer_class = SurroundingDashboardSerializer
    request_serializer_class = serializer_class
    response_serializer_class = serializer_class

    def get_queryset(self):
        return SurroundingDailyAssessment.objects.for_user(
            self.request.user
        )


class SurroundingOverviewView(RetrieveAPIView):
    """
            View for weight overview
        """
    serializer_class = SurroundingOverviewSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_assessment_overview_data(
            instance,
            enums.SURROUNDINGS,
            instance.surrounding_daily_assessments.not_reset(),
            SurroundingDaysRange
        )
        serializer = self.get_serializer(data)
        return Response(serializer.data)
