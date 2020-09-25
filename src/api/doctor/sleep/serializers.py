from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from api.generics.generics import (
    CustomModelSerializer,
    CustomSerializer
)
from api.generics.utils import Utils
from doctor import enums
from doctor.sleep.models import (
    SleepDailyAssessment,
    SleepDaysRange,
    SleepAssessment
)
from doctor.sleep.utils import check_required_sleep_completion
from doctor.sleep.validators import Validations
from doctor.utils import reopen_daily_assessment
from doctor.weight import enums as weight_enum
from doctor.badges import enums as badges_enum
from doctor.validators import Validations as generic_validations


class SleepAssessmentSerializer(CustomModelSerializer):
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
        if badges_enum.SLEEP in self.context.get('earned_assessment_badges', obj.user.earned_assessment_badges()):
            return weight_enum.COMPLETE
        elif obj.user.sleep_daily_assessments.today_assessment():
            return weight_enum.IN_PROGRESS
        return weight_enum.PENDING

    class Meta:
        model = SleepAssessment
        fields = [
            "id",
            "sleep_hours_each_night",
            "score",
            "status"
        ]


class SleepDaysRangeSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving sleep days range for a assessment.
    """
    class Meta:
        model = SleepDaysRange
        exclude = [
            "created_at",
            "updated_at"
        ]


class SleepDashboardSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving and updating sleep daily assessment.
    """
    days_range = SleepDaysRangeSerializer(read_only=True)

    def validate(self, attrs):
        return generic_validations.validate_status(
            self.instance,
            attrs
        )

    def update(self, instance, validated_data):
        if instance.status == enums.IN_PROGRESS:
            with transaction.atomic():
                Validations.validate_sleep(
                    validated_data.get('sleep_type', None)
                )
                raise_errors_on_nested_writes('update', self, validated_data)
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                instance = check_required_sleep_completion(
                    instance,
                    instance.sleep_type
                )
        return instance

    class Meta:
        model = SleepDailyAssessment
        exclude = [
            "user",
            "created_at",
            "updated_at"
        ]


class SleepDailyAssessmentOverviewSerializer(CustomModelSerializer):

    class Meta:
        model = SleepDailyAssessment
        fields = [
            "id",
            "day",
            "status"
        ]


class SleepOverviewSerializer(CustomSerializer):
    status = serializers.IntegerField()
    challenges = serializers.ListField()
    installation_progress = SleepDailyAssessmentOverviewSerializer(many=True)


class SleepReopenAssessmentSerializer(CustomSerializer):
    def create(self, validated_data):
        if not generic_validations.validate_reopen(self.context.get('request').user, badges_enum.SLEEP):
            return Utils.error_response(
                "Your need to complete the assessment before you reopen."
            )
        try:
            with transaction.atomic():
                reopen_daily_assessment(
                    self.context.get('request').user,
                    self.context.get('request').user.sleep_assessment,
                    SleepDailyAssessment,
                    SleepDaysRange
                )
                return Utils.success_response()
        except Exception as e:
            return Utils.error_response(str(e))
