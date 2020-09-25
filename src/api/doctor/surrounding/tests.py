from django.urls import reverse
from rest_framework import status

from doctor import enums
from doctor.user.tests import (
    UserSetup,
    UserTestUtils
)
from doctor.surrounding import enums as surrounding_enums


class SurroundingTestUtils(object):

    @staticmethod
    def get_surrounding_daily_assessment_retrieve_url():
        return reverse('doctor.surrounding:assessment')

    @staticmethod
    def get_surrounding_daily_assessment_log_url(id):
        return reverse('doctor.surrounding:daily_assessment', kwargs={"pk": id})

    @staticmethod
    def get_surrounding_overview_url():
        return reverse('doctor.surrounding:overview')


class SurroundingAssessmentRetrieveViewTest(UserSetup):

    def test_surrounding_daily_assessment_retrieve_view(self):
        response = self.user_client.get(
            SurroundingTestUtils.get_surrounding_daily_assessment_retrieve_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SurroundingDailyAssessmentLogViewTest(UserSetup):

    def test_complete_surrounding_daily_assessment_log_retrieve_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        surrounding_assessment = response.data.get('surrounding')
        if surrounding_assessment:
            response = self.user_client.patch(
                SurroundingTestUtils.get_surrounding_daily_assessment_log_url(
                    response.data.get('sleep').get('id')
                ),
                data={
                    "status": enums.COMPLETE
                }
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('status'), enums.COMPLETE)

    def test_remind_me_surrounding_daily_assessment_log_retrieve_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        surrounding_assessment = response.data.get('surrounding')
        if surrounding_assessment:
            response = self.user_client.patch(
                SurroundingTestUtils.get_surrounding_daily_assessment_log_url(
                    response.data.get('sleep').get('id')
                ),
                data={
                    "status": surrounding_enums.REMIND_ME_LATER
                }
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('status'), surrounding_enums.REMIND_ME_LATER)


class SurroundingOverviewViewTest(UserSetup):

    def test_surrounding_overview(self):
        response = self.user_client.get(
            SurroundingTestUtils.get_surrounding_overview_url()
        )
        self.assertContains(response, "status")
