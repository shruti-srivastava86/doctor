import factory
from doctor.alerts.models import Alerts
from doctor.user.factory import UserFactory
from doctor.alerts import enums


class AlertsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Alerts

    user = factory.SubFactory(UserFactory)
    content_object = factory.SubFactory(UserFactory)
    text = "This is a test text"
    message = "This is a test message"
    type = enums.GENERAL
