"""user serializers."""
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.generics.generics import (
    DualSerializerCreateAPIView,
    CustomRetrieveAPIView,
    DualSerializerUpdateDeleteAPIView,
    DualSerializerDeleteAPIView,
    DualSerializerUpdateAPIView,
    SuccessResponseSerializer,
    CustomRetrieveUpdateAPIView
)
from api.generics.utils import Utils
from doctor.badges import enums
from doctor.user.models import (
    User,
    ForgotPassword
)
from doctor.user.serializers import (
    UserSignUpSerializer,
    UserTokenSerializer,
    UserSignInSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    ForgotPasswordSerializer,
    ChangePasswordSerializer,
    UserDashboardSerializer,
    UserResultSerializer,
    ChooseNextMacroSerializer,
    NotificationSettingsSerializer
)
from doctor.user.token import get_token, regenerate_token
from doctor.user.utils import send_forgot_password_email


class UserSignupView(DualSerializerCreateAPIView):
    """
        User Signup view.
    """
    permission_classes = [AllowAny]
    request_serializer_class = UserSignUpSerializer
    response_serializer_class = UserTokenSerializer

    def perform_create(self, serializer):
        """
            Validate and create a new User.
            Return the User with their newly created token.
        """
        user = super(UserSignupView, self).perform_create(serializer)
        token = get_token(user)
        return {
            'user': user,
            'token': token.key
        }


class UserLoginView(DualSerializerCreateAPIView):
    """
        View for logging a User into the system.
    """
    permission_classes = [AllowAny]
    request_serializer_class = UserSignInSerializer
    response_serializer_class = UserTokenSerializer

    def perform_create(self, serializer):
        """
            Validate the credentials passed in and retrieve the related User.
            Return the User with their token
        """
        user = serializer.validated_data['user']
        token = regenerate_token(user)
        return {
            'user': user,
            'token': token.key
        }


class UserProfileRetrieveUpdateDeleteView(CustomRetrieveAPIView, DualSerializerUpdateDeleteAPIView):
    """
        View for retrieve and update User profile.
    """
    serializer_class = UserProfileSerializer
    request_serializer_class = UserProfileUpdateSerializer
    response_serializer_class = serializer_class

    def get_object(self):
        return self.request.user


class UserLogoutView(DualSerializerDeleteAPIView):
    """
        View for logging out a User from the system.
    """
    def get_object(self):
        """
            Delete a User's token.
        """
        return get_token(self.request.user)


class UserChangePasswordView(DualSerializerUpdateAPIView):
    """
        View for changing a User's password.
    """
    request_serializer_class = ChangePasswordSerializer
    response_serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserForgotPasswordView(DualSerializerCreateAPIView):
    """
        View for sending User's forgot password link.
    """
    request_serializer_class = ForgotPasswordSerializer
    response_serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user = User.filter.with_email(
            self.request.data.get('email')
        ).first()
        if not user:
            return Utils.error_response_400(
                "No user with this email exists"
            )
        try:
            forgot_password_object = ForgotPassword.objects.get_or_create(
                user=user
            )[0]
            send_forgot_password_email(
                forgot_password_object.user,
                forgot_password_object.token
            )
        except Exception:
            return Utils.exception_error("Couldn't send forgot password email. "
                                         "Please contact Admin.")
        return Utils.message_response_200("successful")


class UserDashboardView(CustomRetrieveAPIView):
    """
        View for retrieving User's dashboard.
    """
    serializer_class = UserDashboardSerializer

    def get_object(self):
        return self.request.user

    def get_recently_completed(self, instance, assessments_progress):
        recently_completed = []
        if len(assessments_progress) < 2:
            completed_alerts = instance.alerts.type_completed()
            if completed_alerts:
                latest_completed_alerts = completed_alerts.latest(
                    'created_at'
                )
                recently_completed.append(
                    latest_completed_alerts.macro_type
                )

                second_completed_alerts = instance.alerts.type_completed().exclude(
                    id=latest_completed_alerts.id
                )
                if second_completed_alerts:
                    second_latest_completed_alert = second_completed_alerts.latest(
                        'created_at'
                    )
                    recently_completed.append(
                        second_latest_completed_alert.macro_type
                    )
        elif len(assessments_progress) < 3:
            completed_alerts = instance.alerts.type_completed()
            if completed_alerts:
                latest_completed_alerts = completed_alerts.latest(
                    'created_at'
                )
                recently_completed.append(
                    latest_completed_alerts.macro_type
                )
        return recently_completed

    def get_choose_next_macro(self, instance, assessments_progress, recently_completed):
        return list(
            set(
                enums.MACRO_BADGES_TYPE
            ) - set(
                instance.badges.type_macro().values_list(
                    "type",
                    flat=True
                )
            ) - set(
                assessments_progress
            )
        ) if recently_completed else []

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        weight_assessment = instance.weight_daily_assessments.today_assessment().first()
        assessments_progress = [enums.SURROUNDINGS]
        if weight_assessment:
            assessments_progress.append(enums.WEIGHT)

        food_and_hydration_assessment = instance.food_and_hydration_daily_assessments.today_assessment().first()
        if food_and_hydration_assessment:
            assessments_progress.append(enums.FOOD_AND_HYDRATION)

        motion_assessment = instance.motion_daily_assessments.today_assessment().first()
        if motion_assessment:
            assessments_progress.append(enums.MOTION)

        sleep_assessment = instance.sleep_daily_assessments.today_assessment().first()
        if sleep_assessment:
            assessments_progress.append(enums.SLEEP)

        mind_assessment = instance.mind_daily_assessments.today_assessment().first()
        if mind_assessment:
            assessments_progress.append(enums.MIND)

        data = {
            "weight":  weight_assessment,
            "food_hydration": food_and_hydration_assessment,
            "motion": motion_assessment,
            "sleep": sleep_assessment,
            "mind": mind_assessment,
            "surrounding": instance.surrounding_daily_assessments.today_assessment().in_progress_or_complete()
        }
        data[
            "recently_completed"
        ] = self.get_recently_completed(
            instance,
            assessments_progress
        )
        data[
            "choose_next_macro"
        ] = self.get_choose_next_macro(
            instance,
            assessments_progress,
            data["recently_completed"]
        )
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class UserResultsView(CustomRetrieveAPIView):
    """
        View for retrieving User's tasks results.
    """
    serializer_class = UserResultSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(UserResultsView, self).get_serializer_context()
        context["earned_assessment_badges"] = context['request'].user.earned_assessment_badges()
        return context


class ChooseNextMacroView(DualSerializerCreateAPIView):
    """
        View for choosing next macro for a User.
    """
    request_serializer_class = ChooseNextMacroSerializer
    response_serializer_class = SuccessResponseSerializer


class NotificationSettingsView(CustomRetrieveUpdateAPIView):
    """
        View for retrieving user notification settings.
    """
    serializer_class = NotificationSettingsSerializer

    def get_object(self):
        return self.request.user.notification_settings
