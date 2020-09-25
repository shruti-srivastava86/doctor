from django.conf.urls import url

from doctor.stop_challenge_choose.api import (
    StopChallengeChooseView,
    StopChallengeChooseAssessmentListCreateView
)


urlpatterns = [
    url(
        r'^$',
        StopChallengeChooseView.as_view(),
        name='view'
    ),
    url(
        r'^assessment/$',
        StopChallengeChooseAssessmentListCreateView.as_view(),
        name='assessment'
    )
]
