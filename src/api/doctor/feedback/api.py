from rest_framework.generics import ListCreateAPIView

from doctor.feedback.serializers import FeedbackListSerializer


class FeedbackListCreateView(ListCreateAPIView):
    serializer_class = FeedbackListSerializer

    def get_queryset(self):
        return self.request.user.feedback.all()
