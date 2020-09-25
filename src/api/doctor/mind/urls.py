"""mind urls."""
from django.conf.urls import url

from doctor.mind.api import (
    MindAssessmentRetrieveView,
    MindDailyAssessmentLogView,
    MindOverviewView,
    MindAssessmentReopen
)


urlpatterns = [
    url(
        r'^assessment/$',
        MindAssessmentRetrieveView.as_view(),
        name='assessment'
    ),
    url(
        r'^daily_assessment/(?P<pk>[0-9]+)/$',
        MindDailyAssessmentLogView.as_view(),
        name='daily_assessment'
    ),
    url(
        r'^overview/$',
        MindOverviewView.as_view(),
        name='overview'
    ),
    url(
        r'^reopen/$',
        MindAssessmentReopen.as_view(),
        name='reopen'
    ),
]
