from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from api.generics.generics import (
    DualSerializerUpdateAPIView,
    DualSerializerCreateAPIView,
    SuccessResponseSerializer
)
from doctor.badges import enums
from doctor.food_hydration.models import (
    FoodAndHydrationDailyAssessment,
    FoodAndHydrationDaysRange
)
from doctor.food_hydration.serializers import (
    FoodAndHydrationAssessmentSerializer,
    FoodAndHydrationDashboardSerializer,
    FoodAndHydrationOverviewSerializer,
    FoodAndHydrationReopenAssessmentSerializer
)
from doctor.utils import get_assessment_overview_data


class FoodAndHydrationAssessmentRetrieveView(RetrieveAPIView):
    """
        View for retrieve and update users food and hydration assessment
    """
    serializer_class = FoodAndHydrationAssessmentSerializer

    def get_object(self):
        return self.request.user.food_and_hydration_assessment


class FoodAndHydrationDailyAssessmentLogView(RetrieveAPIView, DualSerializerUpdateAPIView):
    """
        View for updating daily food and hydration assessment for a user
    """
    serializer_class = FoodAndHydrationDashboardSerializer
    request_serializer_class = serializer_class
    response_serializer_class = serializer_class

    def get_queryset(self):
        return FoodAndHydrationDailyAssessment.objects.for_user(
            self.request.user,
        )


class FoodAndHydrationOverviewView(RetrieveAPIView):
    """
        View for food and hydration overview
    """
    serializer_class = FoodAndHydrationOverviewSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_assessment_overview_data(
            instance,
            enums.FOOD_AND_HYDRATION,
            instance.food_and_hydration_daily_assessments.not_reset(),
            FoodAndHydrationDaysRange
        )
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class FoodAndHydrationAssessmentReopen(DualSerializerCreateAPIView):
    """
        View for food and hydration assessment reopen
    """
    request_serializer_class = FoodAndHydrationReopenAssessmentSerializer
    response_serializer_class = SuccessResponseSerializer
