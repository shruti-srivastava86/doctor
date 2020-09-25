from rest_framework.permissions import AllowAny

from api.generics.generics import CustomRetrieveAPIView
from doctor.video.models import Video
from doctor.video.serializers import VideoSerializer


class WelcomeView(CustomRetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer

    def get_object(self):
        return Video.objects.welcome()


class StopChallengeChooseView(CustomRetrieveAPIView):
    serializer_class = VideoSerializer

    def get_object(self):
        return Video.objects.stop_challenge_choose_welcome()
