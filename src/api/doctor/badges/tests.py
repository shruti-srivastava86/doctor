from django.urls import reverse
from rest_framework import status

from doctor.user.tests import UserSetup


class BadgesTestUtils(object):

    @staticmethod
    def get_badges_list_url():
        return reverse('doctor.badges:list')


class BadgesViewTest(UserSetup):

    def test_badges_list_view(self):
        response = self.user_client.get(
            BadgesTestUtils.get_badges_list_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
