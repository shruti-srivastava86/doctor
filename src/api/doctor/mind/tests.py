from django.urls import reverse
from rest_framework import status

from doctor.mind.factory import MindAssessmentFactory
from doctor.user.tests import UserSetup, UserTestUtils


class MindTestUtils(object):

    @staticmethod
    def get_mind_daily_assessment_retrieve_url():
        return reverse('doctor.mind:assessment')

    @staticmethod
    def get_mind_daily_assessment_log_url(id):
        return reverse('doctor.mind:daily_assessment', kwargs={"pk": id})

    @staticmethod
    def get_mind_overview_url():
        return reverse('doctor.mind:overview')


class MindAssessmentRetrieveViewTest(UserSetup):

    def test_mind_daily_assessment_retrieve_view(self):
        response = self.user_client.get(
            MindTestUtils.get_mind_daily_assessment_retrieve_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('average_stress_level'),
            MindAssessmentFactory.average_stress_level
        )


class MindDailyAssessmentLogViewTest(UserSetup):
    data = {
        "total_completed": 2
    }

    def test_mind_daily_assessment_log_retrieve_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        mind_assessment = response.data.get('mind')
        if mind_assessment:
            response = self.user_client.get(
                MindTestUtils.get_mind_daily_assessment_log_url(
                    response.data.get('mind').get('id')
                )
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class MindOverviewViewTest(UserSetup):

    def test_mind_overview(self):
        response = self.user_client.get(
            MindTestUtils.get_mind_overview_url()
        )
        self.assertContains(response, "status")
