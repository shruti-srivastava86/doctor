"""user urls."""
from django.conf.urls import url

from doctor.alerts.api import (
    DeviceRegister,
    DeviceUnregister,
    TestNotification
)
from doctor.user.api import (
    UserSignupView,
    UserLoginView,
    UserProfileRetrieveUpdateDeleteView,
    UserLogoutView,
    UserForgotPasswordView,
    UserChangePasswordView,
    UserDashboardView,
    UserResultsView,
    ChooseNextMacroView,
    NotificationSettingsView
)
from doctor.user.views import (
    ForgotPasswordTemplateView,
    ForgotPasswordSuccessTemplateView
)

AUTH_URLPATTERNS = [
    url(
        r'^sign_up/$',
        UserSignupView.as_view(),
        name='sign_up'
    ),
    url(
        r'^login/$',
        UserLoginView.as_view(),
        name='login'
    ),
    url(
        r'^logout/$',
        UserLogoutView.as_view(),
        name='logout'
    )
]


PROFILE_URLPATTERNS = [
    url(
        r'^profile/$',
        UserProfileRetrieveUpdateDeleteView.as_view(),
        name='profile'
    ),
    url(
        r'^change_password/$',
        UserChangePasswordView.as_view(),
        name='change_password'
    ),
    url(
        r'^forgot_password/$',
        UserForgotPasswordView.as_view(),
        name='forgot_password_email'
    ),
    url(
        r'^forgot_password/(?P<token>.+)/$',
        ForgotPasswordTemplateView.as_view(),
        name='forgot_password'
    ),
    url(
        r'^forgot_password_success/$',
        ForgotPasswordSuccessTemplateView.as_view(),
        name='forgot_password_success'
    ),
    url(
        r'^notification_settings/$',
        NotificationSettingsView.as_view(),
        name='notification_settings'
    )
]


DASHBOARD_URLPATTERNS = [
    url(
        r'^dashboard/$',
        UserDashboardView.as_view(),
        name='dashboard'
    ),
    url(
        r'^next_macro/$',
        ChooseNextMacroView.as_view(),
        name='next_macro'
    ),
]


RESULTS_URLPATTERNS = [
    url(
        r'^results/$',
        UserResultsView.as_view(),
        name='results'
    )
]


NOTIFICATION_URLPATTERNS = [
    url(
        r'^device_register/$',
        DeviceRegister.as_view(),
        name="register_device"
    ),
    url(
        r'^device_unregister/$',
        DeviceUnregister.as_view(),
        name="unregister_device"
    ),
    url(
        r'^test_notification/$',
        TestNotification.as_view(),
        name="test_notification"
    )
]


urlpatterns = AUTH_URLPATTERNS + \
              PROFILE_URLPATTERNS + \
              DASHBOARD_URLPATTERNS + \
              RESULTS_URLPATTERNS + \
              NOTIFICATION_URLPATTERNS
