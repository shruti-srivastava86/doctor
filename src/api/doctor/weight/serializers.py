from django.db import transaction
from django.utils import timezone


from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from api.generics.generics import (
    CustomModelSerializer,
    CustomSerializer
)
from api.generics.utils import Utils
from doctor.utils import (
    reopen_daily_assessment,
    get_first_day_range_data
)
from doctor.weight import enums
from doctor.weight.models import (
    WeightDailyAssessment,
    WeightDaysRange,
    WeightDailyAssessmentMeal,
    WeightAssessment,
    WeightWeeklyAssessmentLogs
)
from doctor.weight.utils import (
    create_weight_daily_assessment_meal,
    check_required_weight_completion,
    is_meal_completed_criteria_satisfied,
    create_first_weight_daily_assessment
)
from doctor.badges import enums as badges_enum
from doctor.weight.validators import Validations
from doctor.validators import Validations as generic_validations


class WeightAssessmentSerializer(CustomModelSerializer):
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
        if badges_enum.WEIGHT in self.context.get('earned_assessment_badges', obj.user.earned_assessment_badges()):
            return enums.COMPLETE
        return enums.IN_PROGRESS

    class Meta:
        model = WeightAssessment
        fields = [
            "id",
            "bmi",
            "first_meal_of_day",
            "meal_plan",
            "score",
            "status"
        ]


class WeightAssessmentUpdateSerializer(WeightAssessmentSerializer):
    """
        Serializer for updating weight assessment for a user.
    """
    def check_or_create_weight_daily_assessment_meal(self, instance):
        first_day_range_data = get_first_day_range_data(
            instance.user
        )
        first_day_weight_daily_assessment = create_first_weight_daily_assessment(
            **first_day_range_data
        )
        first_day_weight_daily_assessment.meal_plan = instance.meal_plan
        first_day_weight_daily_assessment.save()
        create_weight_daily_assessment_meal(
            instance.first_meal_of_day,
            first_day_weight_daily_assessment,
            status=enums.PENDING
        )

    def update(self, instance, validated_data):
        with transaction.atomic():
            raise_errors_on_nested_writes('update', self, validated_data)
            create_new_meal = False
            if not instance.first_meal_of_day:
                create_new_meal = True
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            if create_new_meal:
                self.check_or_create_weight_daily_assessment_meal(
                    instance,
                )
        return instance

    class Meta(WeightAssessmentSerializer.Meta):
        fields = [
            "first_meal_of_day",
            "meal_plan"
        ]


class WeightDaysRangeSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving weight days range.
    """
    class Meta:
        model = WeightDaysRange
        exclude = [
            "created_at",
            "updated_at"
        ]


class WeightDailyAssessmentMealSerializer(CustomModelSerializer):
    """
        Serializer for retrieving daily weight assessment for a user.
    """
    class Meta:
        model = WeightDailyAssessmentMeal
        fields = [
            "id",
            "meal_type",
            "time",
            "status"
        ]


class WeightDashboardSerializer(CustomModelSerializer):
    """
        Serializer for weight dashboard for a user.
    """
    days_range = WeightDaysRangeSerializer(read_only=True)
    meals = WeightDailyAssessmentMealSerializer(many=True, read_only=True)
    previous_incomplete = serializers.SerializerMethodField()

    def get_previous_incomplete(self, obj):
        previous_incomplete = 0
        previous_one_day_weight_daily_assessment = obj.user.weight_daily_assessments.with_user_current_date_time().\
            for_previous_day().first()
        if previous_one_day_weight_daily_assessment and (
                    previous_one_day_weight_daily_assessment.status == enums.INCOMPLETE):
            previous_incomplete += 1
            previous_two_day_weight_daily_assessment = obj.user.weight_daily_assessments.with_user_current_date_time().\
                for_previous_day(
                days=2
            ).first()
            if previous_two_day_weight_daily_assessment and (
                        previous_two_day_weight_daily_assessment.status == enums.INCOMPLETE):
                previous_incomplete += 1
        return previous_incomplete

    class Meta:
        model = WeightDailyAssessment
        exclude = [
            "user",
            "created_at",
            "updated_at"
        ]


class WeightDailyAssessmentMealUpdateSerializer(WeightDailyAssessmentMealSerializer):
    """
        Serializer for updating daily weight assessment meal for a user.
    """
    id = serializers.IntegerField(required=True)


class WeightDashboardUpdateSerializer(WeightDashboardSerializer):
    """
        Serializer for updating daily weight assessment for a user.
    """
    meal = WeightDailyAssessmentMealUpdateSerializer()

    def validate(self, attrs):
        return generic_validations.validate_status(
            self.instance,
            attrs
        )

    def update(self, instance, validated_data):
        with transaction.atomic():
            meal_data = validated_data.pop('meal', None)
            meal = Validations.validate_meal(
                instance, meal_data
            )
            raise_errors_on_nested_writes('update', self, validated_data)

            for attr, value in dict(meal_data).items():
                setattr(meal, attr, value)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if is_meal_completed_criteria_satisfied(instance.days_range, meal_data.get('meal_type')):
                instance.total_completed += 1
            if instance.time_logs:
                instance.time_logs.append(timezone.now().time())
            else:
                instance.time_logs = [timezone.now().time()]
            check_required_weight_completion(meal, instance)
            meal.save()
            instance.save()
        return instance


class WeightWeeklyAssessmentLogsSerializer(CustomModelSerializer):

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        validated_data = Validations.validate_weekly_log(
            instance, validated_data
        )
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = WeightWeeklyAssessmentLogs
        exclude = ['user']


class WeightDailyAssessmentOverviewSerializer(CustomModelSerializer):

    class Meta:
        model = WeightDailyAssessment
        fields = [
            "id",
            "day",
            "status"
        ]


class WeightOverviewSerializer(CustomSerializer):
    status = serializers.IntegerField()
    challenges = serializers.ListField()
    installation_progress = WeightDailyAssessmentOverviewSerializer(many=True)


class WeightReopenAssessmentSerializer(CustomSerializer):
    def create(self, validated_data):
        if not generic_validations.validate_reopen(self.context.get('request').user, badges_enum.WEIGHT):
            return Utils.error_response(
                "Your need to complete the assessment before you reopen."
            )
        try:
            with transaction.atomic():
                new_weight_assessment_object = reopen_daily_assessment(
                    self.context.get('request').user,
                    self.context.get('request').user.weight_assessment,
                    WeightDailyAssessment,
                    WeightDaysRange
                )
                new_weight_assessment_object.meal_plan = self.context.get(
                    'request'
                ).user.weight_assessment.meal_plan
                new_weight_assessment_object.save()
                create_weight_daily_assessment_meal(
                    self.context.get(
                        'request'
                    ).user.weight_assessment.first_meal_of_day,
                    new_weight_assessment_object
                )
                return Utils.success_response()
        except Exception as e:
            return Utils.error_response(str(e))
