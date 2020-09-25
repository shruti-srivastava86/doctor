from datetime import timedelta

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from api.generics.generics import CustomModelSerializer, CustomSerializer
from doctor.surrounding.models import (
    SurroundingDailyAssessment,
    SurroundingDaysRange,
    SurroundingAssessment
)
from doctor.surrounding.utils import complete_surrounding_daily_assessment
from doctor.surrounding.validators import Validations
from doctor.weight import enums
from doctor.badges import enums as badges_enums
from doctor.surrounding import enums as surrounding_enums


class SurroundingAssessmentSerializer(CustomModelSerializer):
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
        if badges_enums.SURROUNDINGS in self.context.get('earned_assessment_badges', obj.user.earned_assessment_badges()):
            return enums.COMPLETE
        elif obj.user.surrounding_daily_assessments.today_assessment():
            return enums.IN_PROGRESS
        return enums.PENDING

    class Meta:
        model = SurroundingAssessment
        fields = [
            "id",
            "score",
            "status"
        ]


class SurroundingDaysRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SurroundingDaysRange
        exclude = [
            "created_at",
            "updated_at"
        ]


class SurroundingDashboardSerializer(serializers.ModelSerializer):
    days_range = SurroundingDaysRangeSerializer(read_only=True)
    status = serializers.ChoiceField(choices=surrounding_enums.ASSESSMENT_STATUS, required=False)

    def validate(self, attrs):
        return Validations.validate_status(
            self.instance,
            attrs
        )

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if validated_data.get('status') == surrounding_enums.REMIND_ME_LATER:
            instance.assessment_date += timedelta(days=7)
        else:
            complete_surrounding_daily_assessment(instance)
        instance.save()
        return instance

    class Meta:
        model = SurroundingDailyAssessment
        exclude = [
            "user",
            "created_at",
            "updated_at"
        ]


class SurroundingDaysRangeOverviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = SurroundingDaysRange
        fields = [
            "id",
            "challenge"
        ]


class SurroundingOverviewSerializer(CustomSerializer):
    status = serializers.IntegerField()
    challenges = serializers.ListField()
    completed_tasks = serializers.ListField()
