from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from api.generics.generics import CustomModelSerializer, CustomSerializer
from api.generics.utils import Utils
from doctor.mind.models import (
    MindDailyAssessment,
    MindDaysRange,
    MindAssessment
)
from doctor.mind.utils import check_mind_completion
from doctor.mind.validators import Validations
from doctor.utils import reopen_daily_assessment
from doctor.weight import enums
from doctor.badges import enums as badges_enum
from doctor.validators import Validations as generic_validations


class MindAssessmentSerializer(CustomModelSerializer):
    """
        Serializer for retrieving weight assessment for a user.
    """
    status = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    def get_score(self, obj):
        """
            Rounding off the score
        """
        return 100 if int(round(obj.score)) > 100 else int(round(obj.score))

    def get_status(self, obj):
        """
            Get status of the assessment
        """
        if badges_enum.MIND in self.context.get('earned_assessment_badges', obj.user.earned_assessment_badges()):
            return enums.COMPLETE
        elif obj.user.mind_daily_assessments.today_assessment():
            return enums.IN_PROGRESS
        return enums.PENDING

    class Meta:
        model = MindAssessment
        fields = [
            "id",
            "average_stress_level",
            "score",
            "status"
        ]


class MindDaysRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MindDaysRange
        exclude = [
            "created_at",
            "updated_at"
        ]


class MindDashboardSerializer(serializers.ModelSerializer):
    days_range = MindDaysRangeSerializer(read_only=True)

    def validate(self, attrs):
        Validations.validate_identify(
            attrs.get('identify'),
            self.instance.day
        )
        Validations.validate_choose(
            attrs.get('choose'),
            self.instance.day
        )
        return attrs

    def update(self, instance, validated_data):
        if instance.status == enums.IN_PROGRESS:
            with transaction.atomic():
                raise_errors_on_nested_writes('update', self, validated_data)
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.total_completed = 1
                instance.save()
                check_mind_completion(
                    instance
                )
        return instance

    class Meta:
        model = MindDailyAssessment
        exclude = [
            "user",
            "created_at",
            "updated_at"
        ]


class MindDailyAssessmentOverviewSerializer(CustomModelSerializer):
    class Meta:
        model = MindDailyAssessment
        fields = [
            "id",
            "day",
            "status"
        ]


class MindOverviewSerializer(CustomSerializer):
    status = serializers.IntegerField()
    challenges = serializers.ListField()
    installation_progress = MindDailyAssessmentOverviewSerializer(many=True)


class MindReopenAssessmentSerializer(CustomSerializer):
    def create(self, validated_data):
        if not generic_validations.validate_reopen(self.context.get('request').user, badges_enum.MIND):
            return Utils.error_response(
                "Your need to complete the assessment before you reopen."
            )
        try:
            with transaction.atomic():
                reopen_daily_assessment(
                    self.context.get('request').user,
                    self.context.get('request').user.mind_assessment,
                    MindDailyAssessment,
                    MindDaysRange
                )
                return Utils.success_response()
        except Exception as e:
            return Utils.error_response(str(e))
