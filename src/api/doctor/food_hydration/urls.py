"""food and hydration urls."""
from django.conf.urls import url

from doctor.food_hydration.api import (
    FoodAndHydrationAssessmentRetrieveView,
    FoodAndHydrationDailyAssessmentLogView,
    FoodAndHydrationOverviewView,
    FoodAndHydrationAssessmentReopen
)


urlpatterns = [
    url(
        r'^assessment/$',
        FoodAndHydrationAssessmentRetrieveView.as_view(),
        name='assessment'
    ),
    url(
        r'^daily_assessment/(?P<pk>[0-9]+)/$',
        FoodAndHydrationDailyAssessmentLogView.as_view(),
        name='daily_assessment'
    ),
    url(
        r'^overview/$',
        FoodAndHydrationOverviewView.as_view(),
        name='overview'
    ),
    url(
        r'^reopen/$',
        FoodAndHydrationAssessmentReopen.as_view(),
        name='reopen'
    ),
]
