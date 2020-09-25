from api.generics.generics import (
    DualSerializerCreateAPIView,
    CustomRetrieveUpdateAPIView,
    CustomListAPIView
)
from doctor.stop_challenge_choose.serializers import (
    StopChallengeChooseViewSerializer,
    StopChallengeChooseAssessmentListCreateSerializer
)


class StopChallengeChooseView(CustomRetrieveUpdateAPIView):
    """
        View for updating stop challenge choose for a user
    """
    serializer_class = StopChallengeChooseViewSerializer

    def get_object(self):
        return self.request.user.stop_challenge_choose


class StopChallengeChooseAssessmentListCreateView(CustomListAPIView, DualSerializerCreateAPIView):
    """
        View for listing and creating a stop challenge choose for a user
    """
    serializer_class = StopChallengeChooseAssessmentListCreateSerializer
    request_serializer_class = serializer_class
    response_serializer_class = serializer_class

    def get_queryset(self):
        return self.request.user.assessments.all()
