from django.conf.urls import url

from doctor.video.api import (
    WelcomeView,
    StopChallengeChooseView
)


urlpatterns = [
    url(
        r'^welcome/$',
        WelcomeView.as_view(),
        name='welcome'
    ),
    url(
        r'^stop_challenge_choose/$',
        StopChallengeChooseView.as_view(),
        name='stop_challenge_choose'
    )
]
