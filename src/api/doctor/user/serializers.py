"""user serializer."""
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from api.generics.generics import (
    CustomModelSerializer,
    CustomSerializer
)
from doctor.badges.models import Badges
from doctor.badges.serializers import BadgesSerializer
from doctor.utils import (
    get_assessment_by_type,
    create_daily_assessment,
    get_days_range_by_assessment
)
from doctor.weight.serializers import (
    WeightDashboardSerializer,
    WeightAssessmentSerializer
)
from doctor.food_hydration.serializers import (
    FoodAndHydrationDashboardSerializer,
    FoodAndHydrationAssessmentSerializer
)
from doctor.mind.serializers import (
    MindDashboardSerializer,
    MindAssessmentSerializer
)
from doctor.motion.serializers import (
    MotionDashboardSerializer,
    MotionAssessmentSerializer
)
from doctor.sleep.serializers import (
    SleepDashboardSerializer,
    SleepAssessmentSerializer
)
from doctor.surrounding.serializers import (
    SurroundingDashboardSerializer,
    SurroundingAssessmentSerializer
)
from doctor.user.models import User, NotificationSettings
from doctor.user.utils import (
    create_assessments,
    create_user_daily_assessment
)
from doctor.user.validators import Validations
from doctor.weight.utils import (
    calculate_bmi,
    create_weight_weekly_assessment_log
)


class UserProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for user with the User model for the current user.
    """
    bmi = serializers.SerializerMethodField()
    badges = BadgesSerializer(
        many=True,
        read_only=True
    )
    habits_installed = serializers.SerializerMethodField()

    def get_bmi(self, obj):
        """
            calculate bmi for a User.
        """
        return calculate_bmi(obj.weight, obj.height)

    def get_habits_installed(self, obj):
        """
            check total habits installed by a User.
        """
        return obj.earned_assessment_badges().count()

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'gender',
            'dob',
            'photo',
            'bmi',
            'height',
            'is_active',
            'one_last_thing',
            'best_day_streak',
            'badges',
            'habits_installed',
            'time_offset'
        ]
        read_only_fields = [
            'id',
            'gender',
            'is_active',
            'bmi',
            'best_day_streak'
        ]


class UserSignUpSerializer(CustomModelSerializer):
    """
        User Signup serializer
    """
    glasses_of_water_per_day = serializers.IntegerField(
        required=True
    )
    steps_each_day = serializers.IntegerField(
        required=True
    )
    sleep_hours_each_night = serializers.IntegerField(
        required=True
    )
    average_stress_level = serializers.IntegerField(
        required=True
    )
    bmi = serializers.IntegerField(
        required=True
    )

    def validate_email(self, obj):
        """
            Validate user email.
        """
        return Validations.validate_email(
            obj
        )

    def validate_password(self, obj):
        """
            Validate user password.
        """
        return Validations.validate_password(
            obj
        )

    def create(self, validated_data):
        """
            Over ride create method to create an user.
        """
        assessment_data = {
            'bmi': validated_data.pop(
                'bmi'
            ),
            'glasses_of_water_per_day': validated_data.pop(
                'glasses_of_water_per_day'
            ),
            'steps_each_day': validated_data.pop(
                'steps_each_day'
            ),
            'sleep_hours_each_night': validated_data.pop(
                'sleep_hours_each_night'
            ),
            'average_stress_level': validated_data.pop(
                'average_stress_level'
            )
        }
        with transaction.atomic():
            user = User.objects.create_user(
                **validated_data
            )
            create_assessments(
                user,
                assessment_data
            )
            create_user_daily_assessment(
                user
            )
            create_weight_weekly_assessment_log(
                user=user,
                bmi=assessment_data.get('bmi'),
                waist=validated_data.get('waist')
            )
            NotificationSettings.objects.get_or_create(
                user=user
            )
        return user

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password',
            'dob',
            'photo',
            'one_last_thing',
            'gender',
            'height',
            'weight',
            'waist',
            'bmi',
            'glasses_of_water_per_day',
            'steps_each_day',
            'sleep_hours_each_night',
            'average_stress_level',
            'time_offset'
        ]


class UserSignInSerializer(CustomSerializer):
    """
        Serializer for dealing with a Login post request.
    """
    email = serializers.CharField(
        required=True
    )
    password = serializers.CharField(
        required=True
    )

    def validate_email(self, obj):
        """
            Validate user email.
        """
        return Validations.validate_valid_email(
            obj
        )

    def validate(self, attrs):
        """
            Validate user login
        """
        return Validations.validate_login(
            attrs
        )


class UserTokenSerializer(serializers.Serializer):
    """
        Serializer for a User and a Token.
    """
    user = UserProfileSerializer()
    token = serializers.CharField()


class UserProfileUpdateSerializer(UserProfileSerializer):
    """
        Serializer for updating User profile.
    """
    badges = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Badges.objects.all()
    )

    def validate_email(self, obj):
        """
            Validate user email
        """
        if not self.instance.email == obj.lower():
            return Validations.validate_email(
                obj
            )
        return obj.lower()

    def validate_badges(self, obj):
        """
            Validate badges if type sharing and influencer
        """
        return Validations.validate_badges(
            obj
        )

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        badges = validated_data.pop('badges', None)
        if badges:
            for badge in badges:
                if badge not in instance.badges.all():
                    instance.badges.add(badge)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(CustomSerializer):
    """
        Serializer for changing a User's password.
    """
    old_password = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    password = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    def validate_password(self, obj):
        """
            Validate user password
        """
        return Validations.validate_password(obj)

    def validate(self, attrs):
        return Validations.validate_change_password(
            self.instance,
            attrs
        )

    def update(self, instance, validated_data):
        instance.set_password(
            validated_data.get(
                "password"
            )
        )
        instance.save()
        return instance


class ForgotPasswordSerializer(CustomSerializer):
    """
        Serializer for forgot User's password.
    """
    email = serializers.CharField(
        required=True
    )


class UserDashboardSerializer(CustomSerializer):
    """
        Serializer for User's dashboard view.
    """
    weight = WeightDashboardSerializer()
    food_hydration = FoodAndHydrationDashboardSerializer()
    motion = MotionDashboardSerializer()
    sleep = SleepDashboardSerializer()
    mind = MindDashboardSerializer()
    surrounding = SurroundingDashboardSerializer(many=True)
    recently_completed = serializers.ListField()
    choose_next_macro = serializers.ListField()


class UserResultSerializer(CustomModelSerializer):
    """
        Serializer for User's results view.
    """
    weight_assessment = WeightAssessmentSerializer()
    food_and_hydration_assessment = FoodAndHydrationAssessmentSerializer()
    motion_assessment = MotionAssessmentSerializer()
    sleep_assessment = SleepAssessmentSerializer()
    mind_assessment = MindAssessmentSerializer()
    surrounding_assessment = SurroundingAssessmentSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "weight_assessment",
            "food_and_hydration_assessment",
            "motion_assessment",
            "sleep_assessment",
            "mind_assessment",
            "surrounding_assessment"
        ]


class ChooseNextMacroSerializer(CustomSerializer):
    next_macro = serializers.IntegerField(required=True)

    def create(self, validated_data):
        user = self.context['request'].user
        assessment = get_assessment_by_type(
            validated_data.get('next_macro')
        )
        stage = 1
        existing_user_assessments = assessment.objects.for_user(user)
        if existing_user_assessments:
            if existing_user_assessments.in_progress():
                raise Exception("Invalid macro type selected")
            completed_user_assessments = existing_user_assessments.complete()
            if completed_user_assessments:
                latest_completed_user_assessments = completed_user_assessments.latest('created_at')
                stage = latest_completed_user_assessments.days_range.stage + 1
        days_range = get_days_range_by_assessment(
            validated_data.get('next_macro')
        ).objects.for_stage(stage).for_day(1).first()
        if days_range:
            create_daily_assessment(
                assessment,
                days_range,
                user=user,
                day=1,
                assessment_date=(timezone.now() + timedelta(seconds=user.time_offset)).date()
            )
            return {"success": True}
        raise Exception("No days rage data available")


class NotificationSettingsSerializer(CustomModelSerializer):

    class Meta:
        model = NotificationSettings
        exclude = [
            "user",
            "created_at",
            "updated_at"
        ]
