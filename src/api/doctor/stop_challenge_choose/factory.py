import factory

from doctor.stop_challenge_choose.models import StopChallengeChoose


class StopChallengeChooseViewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StopChallengeChoose
