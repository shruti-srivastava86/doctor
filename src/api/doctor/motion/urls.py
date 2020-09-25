from django.conf.urls import url

from doctor.motion.api import (
    MotionAssessmentRetrieveView,
    MotionDailyAssessmentLogView,
    MotionOverviewView,
    MotionAssessmentReopen
)


urlpatterns = [
    url(
        r'^assessment/$',
        MotionAssessmentRetrieveView.as_view(),
        name='assessment'
    ),
    url(
        r'^daily_assessment/(?P<pk>[0-9]+)/$',
        MotionDailyAssessmentLogView.as_view(),
        name='daily_assessment'
    ),
    url(
        r'^overview/$',
        MotionOverviewView.as_view(),
        name='overview'
    ),
    url(
        r'^reopen/$',
        MotionAssessmentReopen.as_view(),
        name='reopen'
    ),
]
