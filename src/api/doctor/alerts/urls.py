"""alerts urls."""
from django.conf.urls import url

from doctor.alerts.api import (
    AlertsView,
    AlertUpdateView,
    NewAlertsCountView
)

urlpatterns = [
    url(
        r'^$',
        AlertsView.as_view(),
        name='list'
    ),
    url(
        r'^(?P<pk>[0-9]+)/read/',
        AlertUpdateView.as_view(),
        name='update'
    ),
    url(
        r'^new/',
        NewAlertsCountView.as_view(),
        name='new'
    )
]
