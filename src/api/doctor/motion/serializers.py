from django.db import transaction
from rest_framework import serializers

from api.generics.generics import (
    CustomModelSerializer,
    CustomSerializer
)
from api.generics.utils import Utils
from doctor.motion.models import (
    MotionDailyAssessment,
    MotionDaysRange,
    MotionAssessment
)
from doctor.utils import reopen_daily_assessment
from doctor.validators import Validations
from doctor.weight import enums
from doctor.badges import enums as badges_enum


class MotionAssessmentSerializer(CustomModelSerializer):
    """
        Serializer for retrieving motion assessment for a user.
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
        if badges_enum.MOTION in self.context.get('earned_assessment_badges', obj.user.earned_assessment_badges()):
            return enums.COMPLETE
        elif obj.user.motion_daily_assessments.today_assessment():
            return enums.IN_PROGRESS
        return enums.PENDING

    class Meta:
        model = MotionAssessment
        fields = [
            "id",
            "steps_each_day",
            "score",
            "status"
        ]


class MotionDaysRangeSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving motion days range for a assessment.
    """
    class Meta:
        model = MotionDaysRange
        exclude = [
            "created_at",
            "updated_at"
        ]


class MotionDashboardSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving and updating motion daily assessment.
    """
    days_range = MotionDaysRangeSerializer(read_only=True)

    def validate(self, attrs):
        return Validations.validate_status(
            self.instance,
            attrs
        )

    class Meta:
        model = MotionDailyAssessment
        exclude = [
            "user",
            "created_at",
            "updated_at"
        ]


class MotionDailyAssessmentOverviewSerializer(CustomModelSerializer):

    class Meta:
        model = MotionDailyAssessment
        fields = [
            "id",
            "day",
            "status"
        ]


class MotionOverviewSerializer(CustomSerializer):
    status = serializers.IntegerField()
    challenges = serializers.ListField()
    installation_progress = MotionDailyAssessmentOverviewSerializer(many=True)


class MotionReopenAssessmentSerializer(CustomSerializer):
    def create(self, validated_data):
        if not Validations.validate_reopen(self.context.get('request').user, badges_enum.MOTION):
            return Utils.error_response(
                "Your need to complete the assessment before you reopen."
            )
        try:
            with transaction.atomic():
                reopen_daily_assessment(
                    self.context.get('request').user,
                    self.context.get('request').user.motion_assessment,
                    MotionDailyAssessment,
                    MotionDaysRange
                )
                return Utils.success_response()
        except Exception as e:
            return Utils.error_response(str(e))
