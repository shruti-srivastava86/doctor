"""feedback urls."""
from django.conf.urls import url

from doctor.feedback.api import (
    FeedbackListCreateView
)


urlpatterns = [
    url(
        r'^$',
        FeedbackListCreateView.as_view(),
        name='list_create'
    )
]
