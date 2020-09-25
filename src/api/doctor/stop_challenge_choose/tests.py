from rest_framework import status

from doctor.user.tests import UserSetup
from django.urls import reverse


class StopChallengeChooseTestUtils(object):

    @staticmethod
    def get_stop_challenge_choose_view_retrieve_url():
        return reverse('doctor.stop_challenge_choose:view')

    @staticmethod
    def get_stop_challenge_choose_assessment_list_create_url():
        return reverse('doctor.stop_challenge_choose:assessment')


class StopChallengeChooseViewTest(UserSetup):

    def test_stop_challenge_choose_retrieve_view(self):
        response = self.user_client.get(
            StopChallengeChooseTestUtils.get_stop_challenge_choose_view_retrieve_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StopChallengeChooseAssessmentListCreateViewTest(UserSetup):
    data = {
        "stop": "I would like the bugs to shop",
        "choose": "I would like to choose test cases for it",
        "challenge": "I would like to challenge myself by writing test cases for each api"
    }

    def test_stop_challenge_choose_create_view(self):
        response = self.user_client.post(
            StopChallengeChooseTestUtils.get_stop_challenge_choose_assessment_list_create_url(),
            data=self.data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
