from django.urls import reverse
from rest_framework import status

from doctor.alerts.factory import AlertsFactory
from doctor.user.tests import UserSetup


class AlertTestUtils(object):

    @staticmethod
    def get_alerts_list_url():
        return reverse('doctor.alerts:list')

    @staticmethod
    def get_alert_update_url(id):
        return reverse('doctor.alerts:update', kwargs={"pk": id})


class AlertsViewTest(UserSetup):

    def test_alerts_list_view(self):
        AlertsFactory(
            user=self.user,
            content_object=self.user
        )
        response = self.user_client.get(
            AlertTestUtils.get_alerts_list_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_response = self.user_client.patch(
            AlertTestUtils.get_alert_update_url(
                response.data.get('results')[0].get('id')
            )
        )
        self.assertEqual(update_response.data.get('read'), True)
