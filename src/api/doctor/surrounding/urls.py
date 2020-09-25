"""surrounding urls."""
from django.conf.urls import url

from doctor.surrounding.api import (
    SurroundingRetrieveUpdateView,
    SurroundingDailyAssessmentLogView,
    SurroundingOverviewView
)


urlpatterns = [
    url(
        r'^assessment/$',
        SurroundingRetrieveUpdateView.as_view(),
        name='assessment'
    ),
    url(
        r'^daily_assessment/(?P<pk>[0-9]+)/$',
        SurroundingDailyAssessmentLogView.as_view(),
        name='daily_assessment'
    ),
    url(
        r'^overview/$',
        SurroundingOverviewView.as_view(),
        name='overview'
    ),
]
