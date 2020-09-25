from django.db import transaction
from rest_framework import serializers

from api.generics.generics import (
    CustomModelSerializer,
    CustomSerializer
)
from api.generics.utils import Utils
from doctor.food_hydration.models import (
    FoodAndHydrationDailyAssessment,
    FoodAndHydrationDaysRange,
    FoodAndHydrationAssessment
)
from doctor.utils import reopen_daily_assessment
from doctor.validators import Validations
from doctor.weight import enums
from doctor.badges import enums as badges_enum


class FoodAndHydrationAssessmentSerializer(CustomModelSerializer):
    """
        Serializer for retrieving food and hydration assessment for a user.
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
        if badges_enum.FOOD_AND_HYDRATION in self.context.get('earned_assessment_badges', obj.user.earned_assessment_badges()):
            return enums.COMPLETE
        return enums.IN_PROGRESS

    class Meta:
        model = FoodAndHydrationAssessment
        fields = [
            "id",
            "glasses_of_water_per_day",
            "score",
            "status"
        ]


class FoodAndHydrationDaysRangeSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving food and hydration days range for a assessment.
    """
    class Meta:
        model = FoodAndHydrationDaysRange
        exclude = [
            "created_at",
            "updated_at"
        ]


class FoodAndHydrationDashboardSerializer(CustomModelSerializer):
    """
        Serializer for retrieving and updating food and hydration daily assessment.
    """
    days_range = FoodAndHydrationDaysRangeSerializer(read_only=True)

    def validate(self, attrs):
        return Validations.validate_status(
            self.instance,
            attrs
        )

    class Meta:
        model = FoodAndHydrationDailyAssessment
        exclude = [
            "user",
            "created_at",
            "updated_at"
        ]


class FoodAndHydrationDailyAssessmentOverviewSerializer(CustomModelSerializer):

    class Meta:
        model = FoodAndHydrationDailyAssessment
        fields = [
            "id",
            "day",
            "status"
        ]


class FoodAndHydrationOverviewSerializer(CustomSerializer):
    status = serializers.IntegerField()
    challenges = serializers.ListField()
    installation_progress = FoodAndHydrationDailyAssessmentOverviewSerializer(many=True)


class FoodAndHydrationReopenAssessmentSerializer(CustomSerializer):
    def create(self, validated_data):
        if not Validations.validate_reopen(self.context.get('request').user, badges_enum.FOOD_AND_HYDRATION):
            return Utils.error_response(
                "Your need to complete the assessment before you reopen."
            )
        try:
            with transaction.atomic():
                reopen_daily_assessment(
                    self.context.get('request').user,
                    self.context.get('request').user.food_and_hydration_assessment,
                    FoodAndHydrationDailyAssessment,
                    FoodAndHydrationDaysRange
                )
                return Utils.success_response()
        except Exception as e:
            return Utils.error_response(str(e))
