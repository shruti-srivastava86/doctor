from django.urls import reverse
from rest_framework import status

from doctor.user.tests import UserSetup


class FeedbackTestUtils(object):

    @staticmethod
    def get_feedback_list_create_url():
        return reverse('doctor.feedback:list_create')


class FeedbackListCreateViewTest(UserSetup):
    data = {
        "message": "this is a test feedback message"
    }

    def test_feedback_list_create_view(self):
        create_response = self.user_client.post(
            FeedbackTestUtils.get_feedback_list_create_url(),
            self.data
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        response = self.user_client.get(
            FeedbackTestUtils.get_feedback_list_create_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
