"""badges urls."""
from django.conf.urls import url

from doctor.badges.api import BadgesListView

urlpatterns = [
    url(
        r'^$',
        BadgesListView.as_view(),
        name='list'
    )
]
