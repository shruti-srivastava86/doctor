"""sleep urls."""
from django.conf.urls import url

from doctor.sleep.api import (
    SleepAssessmentRetrieveUpdateView,
    SleepDailyAssessmentLogView,
    SleepOverviewView,
    SleepAssessmentReopen
)


urlpatterns = [
    url(
        r'^assessment/$',
        SleepAssessmentRetrieveUpdateView.as_view(),
        name='assessment'
    ),
    url(
        r'^daily_assessment/(?P<pk>[0-9]+)/$',
        SleepDailyAssessmentLogView.as_view(),
        name='daily_assessment'
    ),
    url(
        r'^overview/$',
        SleepOverviewView.as_view(),
        name='overview'
    ),
    url(
        r'^reopen/$',
        SleepAssessmentReopen.as_view(),
        name='reopen'
    ),
]
