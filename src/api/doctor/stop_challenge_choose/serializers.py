from api.generics.generics import CustomModelSerializer
from doctor.stop_challenge_choose.models import (
    StopChallengeChooseAssessment,
    StopChallengeChoose
)


class StopChallengeChooseViewSerializer(CustomModelSerializer):

    class Meta:
        model = StopChallengeChoose
        exclude = ['user', 'created_at', 'updated_at']


class StopChallengeChooseAssessmentListCreateSerializer(CustomModelSerializer):

    def create(self, validated_data):
        return StopChallengeChooseAssessment.objects.create(
            user=self.context['request'].user,
            **validated_data
        )

    class Meta:
        model = StopChallengeChooseAssessment
        exclude = ['user']
