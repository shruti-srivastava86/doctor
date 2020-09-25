"""weight urls."""
from django.conf.urls import url

from doctor.weight.api import (
    WeightAssessmentRetrieveUpdateView,
    WeightDailyAssessmentLogView,
    WeightWeeklyAssessmentListView,
    WeightWeeklyAssessmentUpdateView,
    WeightOverviewView,
    WeightAssessmentReopen
)


urlpatterns = [
    url(
        r'^assessment/$',
        WeightAssessmentRetrieveUpdateView.as_view(),
        name='assessment'
    ),
    url(
        r'^daily_assessment/(?P<pk>[0-9]+)/$',
        WeightDailyAssessmentLogView.as_view(),
        name='daily_assessment'
    ),
    url(
        r'^weekly_checkup/$',
        WeightWeeklyAssessmentListView.as_view(),
        name='daily_assessment'
    ),
    url(
        r'^weekly_checkup/(?P<pk>[0-9]+)/$',
        WeightWeeklyAssessmentUpdateView.as_view(),
        name='update_daily_assessment'
    ),
    url(
        r'^overview/$',
        WeightOverviewView.as_view(),
        name='overview'
    ),
    url(
        r'^reopen/$',
        WeightAssessmentReopen.as_view(),
        name='reopen'
    ),
]
